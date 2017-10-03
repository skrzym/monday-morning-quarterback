import glob as gl
import warnings
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def csv_to_df(path, combine=True):
    # gather all csv files, convert them to Pandas DataFrames and store them in a list
    seasons = [pd.read_csv(f) for f in gl.glob(path)]
    
    # If the 'combine' argument is True then concatenate together all the dataframes.
    if combine:
        seasons = pd.concat(seasons, ignore_index=True)
    
    return seasons

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    playoffs_playbyplay = csv_to_df('data\playbyplaydata\[po]*')
    regular_playbyplay = csv_to_df('data\playbyplaydata\[rs]*')
    po_pbp = playoffs_playbyplay
    rs_pbp = regular_playbyplay


def gather_data(playoffs=False):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if playoffs:
            return csv_to_df('data\playbyplaydata\[po]*')
        else:
            return csv_to_df('data\playbyplaydata\[rs]*')


def run_completion_mapper(row):
    if row.Fumble == 1:
        return 'Fumble'
    elif row.Touchdown == 1:
        return 'Touchdown'
    else:
        return 'Run'


def make_run_df(dataframe):
    if dataframe.empty:
        return dataframe
     # Create rushing data DataFrame
    df = dataframe.copy()
    run_df = df.loc[df.PlayType == 'Run'][\
    ['Season',
     'GameID',
     'posteam',
     'DefensiveTeam',
     'TimeSecs',
     'Rusher',
     'RunLocation',
     'RunGap',
     'yrdline100',
     'Yards.Gained',
     'Touchdown',
     'qtr',
     'Fumble']
    ].reset_index(drop=True)
    
    if run_df.empty == False:
        run_df['FinishYrdLine100'] = run_df.yrdline100 - run_df['Yards.Gained']
        run_df['RunOutcome'] = run_df.apply(run_completion_mapper, axis=1)
    
    return run_df


def pass_completion_mapper(row):
    if row.InterceptionThrown == 1:
        return 'Interception'
    elif row.Fumble == 1:
        return 'Fumble'
    elif row.Touchdown == 1:
        return 'Touchdown'
    else:
        if row.PassOutcome == 'Incomplete Pass':
            return 'Incomplete'
        else:
            return 'Complete'


def make_pass_df(dataframe):
    if dataframe.empty:
        return dataframe
    # Create passing data DataFrame
    df = dataframe.copy()

    pass_df = df.loc[df.PlayType == 'Pass'][\
    ['Season',
     'GameID',
     'posteam',
     'DefensiveTeam',
     'TimeSecs',
     'Passer',
     'Receiver',
     'yrdline100',
     'AirYards',
     'YardsAfterCatch',
     'Yards.Gained',
     'PassLength',
     'PassOutcome',
     'PassLocation',
     'InterceptionThrown',
     'Touchdown',
     'qtr',
     'Fumble']
    ].reset_index(drop=True)
    
    if pass_df.empty == False:
        pass_df.PassOutcome = pass_df.apply(pass_completion_mapper,axis=1)
        pass_df['ReceiveYrdLine100'] = pass_df.yrdline100 - pass_df.AirYards

    return pass_df

def make_fg_df(dataframe):
    if dataframe.empty:
        return dataframe
    # Create a Field Goal data DataFrame
    df = dataframe.copy()
    
    fg_df = df.loc[df.PlayType == 'Field Goal'][\
    ['Season',
     'GameID',
     'posteam',
     'DefensiveTeam',
     'TimeSecs',
     'yrdline100',
     'FieldGoalResult',
     'FieldGoalDistance',
     'qtr',
     'Fumble']
     ].reset_index(drop=True)
    
    if fg_df.empty == False:
        fg_df['kickyrdline100'] = fg_df.FieldGoalDistance - 10
        fg_df['KickLocation'] = 'middle'
    
    return fg_df

# Setup Masking Function
# https://stackoverflow.com/questions/11869910/pandas-filter-rows-of-dataframe-with-operator-chaining
def mask(df, key, value, operator='=='):
    if type(value) is list:
        if operator == 'not':
            return df[df[key].apply(lambda x: x not in value)]
        else:
            return df[df[key].apply(lambda x: x in value)]
    else:
        if operator == '!=':
            return df[df[key] != value]
        elif operator == '>':
            return df[df[key] > value]
        elif operator == '>=':
            return df[df[key] >= value]
        elif operator == '<':
            return df[df[key] < value]
        elif operator == '<=':
            return df[df[key] <= value]
        else:
            return df[df[key] == value]

# Set Pandas DF Mask funciton
pd.DataFrame.mask = mask


def compress_field(field, yards_in_group):
    # Group pass count data into sections of the field vs yard by yard
    items_in_group = yards_in_group * 3
    new_field = np.empty(((100//yards_in_group) * 3 + 3,3),dtype='object')
    current_yardline = yards_in_group
    pass_location = ['left', 'middle', 'right']
    count_summation = [0, 0, 0]
    new_field_index = 3

    for a in range(3):
        new_field[0 + a][0] = 0
        new_field[0 + a][1] = pass_location[a]
        new_field[0 + a][2] = field[0 + a][2]

    for i in range(3,300):
        count_summation[i%3] += field[i][2]
        if ((i - 3) % items_in_group == items_in_group - 1) or (i == 299):
            for j in range(3):
                new_field[new_field_index + j][0] = current_yardline
                new_field[new_field_index + j][1] = pass_location[j]
                new_field[new_field_index + j][2] = count_summation[j]
            new_field_index += 3
            current_yardline += yards_in_group
            count_summation = [0, 0, 0]
    return new_field


def plotPassingHeatMap(dataframe, throw_or_catch_yrdline='catch', filters=[], yard_grouping=5,
                       vmin=0, vmax=None, annot=False, cmap='Greens', cbar=True, cbar_ax=None, ax=None):
    """Generates a seaborn HeatMap of nfl passing related data.
    dataframe: (DataFrame)          - NFL data stored in a Pandas DataFrame
    throw_or_catch_yrdline: (String)- 'throw' shows where the LOS is for the play while 'catch' shows where the ball was caught.
    filters: (list)                 - A list of lists containing DataFrame masks - [key, filter, [operator]]
    yard_grouping: (int)            - Number of yards the heatmaps should group the data into.
    vmin: (int)                     - Min value to start the color gradient.
    vmax: (int)                     - Max value to stop the color gradient.
    annot: (Boolean)                - 'True' will label each box with its value
    cmap: (String)                  - seaborn cmap object
    cbar: (Boolean)                 - 'True' will plot the color scale 
    cbar_ax: (Axes)                 - plot data for where to put the cbar
    ax: (Axes)                      - associate this HeatMap with a specific Axes object
    """
    # Create passing data DataFrame
    pass_df = make_pass_df(dataframe)

    # Run any provided filters
    if len(filters) > 0:
        for f in filters:
            if len(f) == 2:
                pass_df = pass_df.mask(f[0], f[1])
            else:
                pass_df = pass_df.mask(f[0], f[1], f[2])

    #pass_results_df = pass_df.mask('PassOutcome','Interception').mask('ReceiveYrdLine100', 0, '>=')
    
    # Group data by throw or catch location:
    if throw_or_catch_yrdline == 'throw':
        throw_or_catch_string = 'yrdline100'
        y_label = 'QB Throw Yard Line'
    else:
        throw_or_catch_string = 'ReceiveYrdLine100'
        y_label = 'Recieved Yard Line'
    
    # Check if any data exists
    if len(pass_df) == 0:
        # Build numpy array representing the football field to structure the heatmap and populate the counts
        field = np.empty((300,3),dtype='object')
        yardline = 0
        pass_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = pass_location[row % 3]
            field[row][2] = 0
            if row % 3 == 2:
                yardline += 1
                
    else:
        pass_results_df = pass_df.groupby([throw_or_catch_string,'PassLocation']).agg({'GameID':len}).reset_index()

        # Build numpy array representing the football field to structure the heatmap and populate the counts
        field = np.empty((300,3),dtype='object')
        yardline = 0
        pass_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = pass_location[row % 3]
            temp = pass_results_df.mask(throw_or_catch_string, yardline).mask('PassLocation', field[row][1]).values
            if temp.shape[0] > 0:
                field[row][2] = temp[0][2]
            else:
                field[row][2] = 0
            if row % 3 == 2:
                yardline += 1

    # Group the count data based on the 'yard_grouping' parameter
    if yard_grouping > 1:
        field = compress_field(field, yard_grouping)

    # Create a seaborn.heatmap() ready dataframe
    heat_map_df = pd.DataFrame.from_records(field,
        columns=[y_label, 'Pass Location', 'Count']
        ).pivot(y_label, 'Pass Location','Count')

    #with sns.axes_style("ticks"):
    #fig,ax1 = plt.subplots(1,1,figsize=figsize)
    ax = sns.heatmap(data=heat_map_df, cmap=cmap, square=False, linewidths=1, linecolor='white', annot=annot, fmt="d", vmin=vmin, vmax=vmax, cbar=cbar, cbar_ax=cbar_ax, ax=ax)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks([x for x in range(0,int(100 / yard_grouping) + 1)])

    return ax


def plotRushingHeatMap(dataframe, start_or_finish_ydline='finish', filters=[], yard_grouping=5,
                       vmin=0, vmax=None, annot=False, cmap='Greens', cbar=True, cbar_ax=None, ax=None):
    """
    Generates a seaborn HeatMap of nfl rush related data.
    dataframe: (DataFrame)          - NFL data stored in a Pandas DataFrame
    start_or_finish_ydline: (String)- 'start' shows where the LOS is for the play while 'finish' shows where the run ended.
    filters: (list)                 - A list of lists containing DataFrame masks - [key, filter, [operator]]
    yard_grouping: (int)            - Number of yards the heatmaps should group the data into.
    vmin: (int)                     - Min value to start the color gradient.
    vmax: (int)                     - Max value to stop the color gradient.
    annot: (Boolean)                - 'True' will label each box with its value
    cmap: (String)                  - seaborn cmap object
    cbar: (Boolean)                 - 'True' will plot the color scale 
    cbar_ax: (Axes)                 - plot data for where to put the cbar
    ax: (Axes)                      - associate this HeatMap with a specific Axes object
    """
    # Create rushing data DataFrame
    run_df = make_run_df(dataframe)
    # Temp Fix to adjust for NFLscrapR bug when coding the 'RunGap' value. (Description contains the letters 'end' in player names 25x for the middle 'RunLocation')
    run_df.loc[run_df.RunLocation=='middle','RunGap'] = np.NaN

    # Run any provided filters
    if len(filters) > 0:
        for f in filters:
            if len(f) == 2:
                run_df = run_df.mask(f[0], f[1])
            else:
                run_df = run_df.mask(f[0], f[1], f[2])

    #pass_results_df = pass_df.mask('PassOutcome','Interception').mask('ReceiveYrdLine100', 0, '>=')

    # Group data by start or finish location:
    if start_or_finish_ydline == 'start':
        start_or_finish_string = 'yrdline100'
        y_label = 'Run Starts Yard Line'
    else:
        start_or_finish_string = 'FinishYrdLine100'
        y_label = 'Run Ends Yard Line'
    
     # Check if any data exists
    if len(run_df) == 0:
        # Build numpy array representing the football field to structure the heatmap and populate the counts
        field = np.empty((300,3),dtype='object')
        yardline = 0
        run_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = run_location[row % 3]
            field[row][2] = 0
            if row % 3 == 2:
                yardline += 1
                
    else:
        run_results_df = run_df.groupby([start_or_finish_string,'RunLocation']).agg({'GameID':len}).reset_index()
        # Build numpy array representing the football field to structure the heatmap and populate the counts
        field = np.empty((300,3),dtype='object')
        yardline = 0
        run_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = run_location[row%3]
            temp = run_results_df.mask(start_or_finish_string, yardline).mask('RunLocation', field[row][1]).values
            if temp.shape[0] > 0:
                field[row][2] = temp[0][2]
            else:
                field[row][2] = 0
            if row%3 == 2:
                yardline += 1

    # Group the count data based on the 'yard_grouping' parameter
    if yard_grouping > 1:
        field = compress_field(field, yard_grouping)

    # Create a seaborn.heatmap() ready dataframe
    heat_map_df = pd.DataFrame.from_records(field,
                columns=[y_label, 'Run Location', 'Count']
                ).pivot(y_label, 'Run Location','Count')

    #with sns.axes_style("ticks"):
    #fig,ax1 = plt.subplots(1,1,figsize=figsize)
    ax = sns.heatmap(data=heat_map_df, cmap=cmap, square=False, linewidths=1, linecolor='white', annot=annot, fmt="d", vmin=vmin, vmax=vmax, cbar=cbar, cbar_ax=cbar_ax, ax=ax)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks([x for x in range(0,int(100 / yard_grouping) + 1)])

    return ax


def plotFieldGoalHeatMap(dataframe, scrimmage_or_kick_line='kick', filters=[], yard_grouping=5,
                       vmin=0, vmax=None, annot=False, cmap='Greens', cbar=True, cbar_ax=None, ax=None):
    """Generates a seaborn HeatMap of NFL field goal related data.
    dataframe: (DataFrame)          - NFL data stored in a Pandas DataFrame
    scrimmage_or_kick_line: (String)- 'scrimmage' shows where the LOS is for the play while 'kick' shows where the kick actually ocurred.
    filters: (list)                 - A list of lists containing DataFrame masks - [key, filter, [operator]]
    yard_grouping: (int)            - Number of yards the heatmaps should group the data into.
    vmin: (int)                     - Min value to start the color gradient.
    vmax: (int)                     - Max value to stop the color gradient.
    annot: (Boolean)                - 'True' will label each box with its value
    cmap: (String)                  - seaborn cmap object
    cbar: (Boolean)                 - 'True' will plot the color scale 
    cbar_ax: (Axes)                 - plot data for where to put the cbar
    ax: (Axes)                      - associate this HeatMap with a specific Axes object
    """
    # Create rushing data DataFrame
    fg_df = make_fg_df(dataframe)
    
    # Run any provided filters
    if len(filters) > 0:
        for f in filters:
            if len(f) == 2:
                fg_df = fg_df.mask(f[0], f[1])
            else:
                fg_df = fg_df.mask(f[0], f[1], f[2])

    # Group data by official play yardline or the yardline from which the ball was kicked (typically 6-7 yards behind the scrimmage line):
    if scrimmage_or_kick_line == 'kick':
        scrimmage_or_kick_line_string = 'kickyrdline100'
        y_label = 'FG Kicking Yard Line'
    else:
        scrimmage_or_kick_line_string = 'yrdline100'
        y_label = 'FG Scrimmage Line'
    
    # Check if any data exists
    if len(fg_df) == 0:
        # Build numpy array representing the football field to structure the heatmap and populate the counts
        field = np.empty((300,3),dtype='object')
        yardline = 0
        fg_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = fg_location[row % 3]
            field[row][2] = 0
            if row % 3 == 2:
                yardline += 1
                
    else:
        
        fg_results_df = fg_df.groupby([scrimmage_or_kick_line_string,'KickLocation']).agg({'GameID':len}).reset_index()
        field = np.empty((300,3),dtype='object')
        yardline = 0
        fg_location = ['left','middle','right']
        for row in range(0,300):
            field[row][0] = yardline
            field[row][1] = fg_location[row % 3]
            temp = fg_results_df.mask(scrimmage_or_kick_line_string, yardline).mask('KickLocation', field[row][1]).values
            if temp.shape[0] > 0:
                field[row][2] = temp[0][2]
            else:
                field[row][2] = 0
            if row%3 == 2:
                yardline += 1

    # Group the count data based on the 'yard_grouping' parameter
    if yard_grouping > 1:
        field = compress_field(field, yard_grouping)

    # Create a seaborn.heatmap() ready dataframe
    heat_map_df = pd.DataFrame.from_records(field,
                columns=[y_label, 'Kick Location', 'Count']
                ).pivot(y_label, 'Kick Location','Count')

    #with sns.axes_style("ticks"):
    #fig,ax1 = plt.subplots(1,1,figsize=figsize)
    ax = sns.heatmap(data=heat_map_df, cmap=cmap, square=False, linewidths=1, linecolor='white', annot=annot, fmt="d", vmin=vmin, vmax=vmax, cbar=cbar, cbar_ax=cbar_ax, ax=ax)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks([x for x in range(0,int(100 / yard_grouping) + 1)])

    return ax


def two_team_filter(row, team1, team2):
    return (row.posteam == team1 and row.DefensiveTeam == team2) or (row.posteam == team2 and row.DefensiveTeam == team1)


def two_team_gameids(team1, team2, playoffs=False):
    #Ensure teams exist in the data
    if playoffs:
        data = po_pbp
    else:
        data = rs_pbp
    assert team1 in data.posteam.values, '"{}" does not exist in the chosen dataset!'.format(team1)
    assert team2 in data.posteam.values, '"{}" does not exist in the chosen dataset!'.format(team2)
    
    data = data.loc[data.apply(two_team_filter, team1=team1, team2=team2, axis=1)]
    data = data.GameID.unique().tolist()
    return data


def PlotTwoTeamsHeatMaps(team1, team2, playoffs=False, title='Title', gen_filters=None, pass_filters=None, run_filters=None, fg_filters=None):
    """Generates a 2x3 grid of seaborn HeatMaps showcasing how two NFL teams perfomed when playing against eachother in all their games played vs one another with any given filters.
    team1: (String)
    team2: (String)
    playoffs: (Boolean)
    title: (String)
    gen_filters: (list)
    pass_filters: (list)
    run_filters: (list)
    fg_filters: (list)
    """
    
    GameIDs = two_team_gameids(team1, team2, playoffs)
    return PlotGamesHeatMaps(GameIDs, title, gen_filters, pass_filters, run_filters, fg_filters)


def apply_filters(df, filters):
    if filters:
        for f in filters:
            if len(f) == 2:
                df = df.mask(f[0], f[1])
            else:
                df = df.mask(f[0], f[1], f[2])
    return df


def PlotGamesHeatMaps(GameIDs, title, gen_filters=None, pass_filters=None, run_filters=None, fg_filters=None, sharex=False, figsize=(10,8)):
    """Generates a 2x3 grid of seaborn HeatMaps showcasing how the teams in a set of GameIDs perfomred against eachother.
    team1: (String)
    team2: (String)
    playoffs: (Boolean)
    title: (String)
    gen_filters: (list)
    pass_filters: (list)
    run_filters: (list)
    fg_filters: (list)
    """
    # Pull the Home and Away teams from the game
    if GameIDs[0] in rs_pbp.GameID.values:
        data = rs_pbp.loc[rs_pbp.GameID.apply(lambda x: True if x in GameIDs else False)]
    elif GameIDs[0] in po_pbp.GameID.values:
        data = po_pbp.loc[po_pbp.GameID.apply(lambda x: True if x in GameIDs else False)]
    else:
        raise ValueError('The GameID {} does not exist in the regular or postseason datasets!'.format(GameID), GameID)
    
    # Pull the Home and Away teams from the game
    home_team = data.HomeTeam.unique()[0]
    away_team = data.AwayTeam.unique()[0]
    
    # Generate the pass, run, and fg DataFrames needed for each team's heatmaps including any provided filters
    data = apply_filters(data, gen_filters)
    
    home_data = data.mask('posteam', home_team)
    away_data = data.mask('posteam', away_team)
    #return home_data, away_data
    
    # Setup the figure
    yard_grouping = 10
    fig, axes = plt.subplots(2,3,sharey=True,figsize=figsize, sharex=sharex)
    
    # Home - Passing
    plotPassingHeatMap(home_data, filters=pass_filters, ax=axes[0][0], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Reds')
    axes[0][0].set_title('Passing - ' + home_team)

    # Home - Rushing
    plotRushingHeatMap(home_data, filters=run_filters, ax=axes[0][1], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Reds')
    axes[0][1].set_title('Rushing - ' + home_team)

    # Home - FG
    plotFieldGoalHeatMap(home_data, filters=fg_filters, ax=axes[0][2], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Reds')
    axes[0][2].set_title('Field Goals - ' + home_team)
    
    # Away - Passing
    plotPassingHeatMap(away_data, filters=pass_filters, ax=axes[1][0], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Blues')
    axes[1][0].set_title('Passing - ' + away_team)

    # Away - Rushing
    plotRushingHeatMap(away_data, filters=run_filters, ax=axes[1][1], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Blues')
    axes[1][1].set_title('Rushing - ' + away_team)

    # Away - FG
    plotFieldGoalHeatMap(away_data, filters=fg_filters, ax=axes[1][2], yard_grouping=yard_grouping, cbar=False, annot=True, vmax=None, cmap='Blues')
    axes[1][2].set_title('Field Goals - ' + away_team)
    
    # Filter out 0 value annotations on the heatmaps
    for row in range(2):
        for col in range(3):
            for text in axes[row][col].texts:
                if text.get_text() == '0':
                    text.set_text('')
    
    fig.suptitle(title)
    return axes


def plotFieldGoalSwarm(dataset, filters=None, y_value='FieldGoalDistance',ylim=(10,70), size=10, figsize=None, title='Field Goals by Distance', axes=None):
    swarm = make_fg_df(dataset)
    swarm = apply_filters(swarm,filters)
    if swarm.empty:
        plot = sns.swarmplot(ax=axes)
    else:
        palette={'Good': 'green', 'No Good': 'red', 'Blocked': 'yellow'}
        hue_order = ['Good', 'No Good', 'Blocked']
        plot = sns.swarmplot(ax=axes, data=swarm, x='KickLocation', y=y_value, hue='FieldGoalResult', hue_order=hue_order, size=size, split=False, palette=palette)
        plot.legend(frameon = 1).get_frame().set_facecolor('white')
    plot.set_ylim(ylim)
    plot.set_xlabel('Kick Location')
    plot.set_ylabel('Field Goal Distance (yds)')
    plot.set_title(title)
    return plot


def plotPassingSwarm(dataset, filters=None, y_value='AirYards', ylim=(-10,70), size=10, title='Passing Air Yards', axes=None):
    swarm = make_pass_df(dataset)
    swarm = apply_filters(swarm, filters)
    
    if swarm.empty:
        plot = sns.swarmplot(ax=axes)
    else:
        palette = {'Complete': 'green', 'Incomplete': 'grey', 'Interception': 'red', 'Touchdown':'orange', 'Fumble':'purple'}
        hue_order = ['Complete', 'Incomplete', 'Touchdown', 'Fumble', 'Interception']
        plot = sns.swarmplot(ax=axes, data=swarm, x='PassLocation', y=y_value, hue='PassOutcome', order=['left', 'middle', 'right'], hue_order=hue_order, size=size, split=False, palette=palette)
        plot.legend(frameon = 1).get_frame().set_facecolor('white')
    plot.hlines(y=0,xmin=-1,xmax=3,colors='blue', label='Line of Scrimmage')
    plot.set_ylim(ylim)
    plot.set_xlabel('Pass Location')
    plot.set_ylabel('Pass Air Yards (yds)')
    plot.set_title(title)
    return plot


def plotRushingSwarm(dataset, filters=None, y_value='Yards.Gained', ylim=(-10,70), size=10, title='Rushing Yards', axes=None):

    swarm = make_run_df(dataset)
    swarm = apply_filters(swarm, filters)
    
    if swarm.empty:
        plot = sns.swarmplot(ax=axes)
    else:
        palette = {'Run': 'green', 'Fumble': 'purple', 'Touchdown':'orange'}
        plot = sns.swarmplot(ax=axes, data=swarm, x='RunLocation', y=y_value, hue='RunOutcome', order=['left', 'middle', 'right'], size=size, split=False, palette=palette)
        plot.legend(frameon = 1).get_frame().set_facecolor('white')
    plot.hlines(y=0,xmin=-1,xmax=3,colors='blue', label='Line of Scrimmage')
    plot.set_ylim(ylim)
    plot.set_xlabel('Run Location')
    plot.set_ylabel('Total Yards Gained (yds)')
    plot.set_title(title)
    return plot