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

def gather_data(playoffs=False):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        if playoffs:
            return csv_to_df('data\playbyplaydata\[po]*')
        else:
            return csv_to_df('data\playbyplaydata\[rs]*')
    

def make_run_df(dataframe):
     # Create rushing data DataFrame
    df = dataframe.copy()
    run_df = df[df.PlayType == 'Run'][\
    ['Season',
     'GameID',
     'posteam',
     'TimeSecs',
     'Rusher',
     'RunLocation',
     'yrdline100',
     'Yards.Gained',
     'Touchdown']
    ].reset_index(drop=True)

    return run_df


def pass_completion_mapper(row):
    if row.PassOutcome == 'Incomplete Pass':
        if row.InterceptionThrown == 1:
            return 'Interception'
        else:
            return 'Incomplete'
    else:
        return 'Complete'


def make_pass_df(dataframe):
    # Create passing data DataFrame
    df = dataframe.copy()

    pass_df = df[df.PlayType == 'Pass'][\
    ['Season',
     'GameID',
     'posteam',
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
     'Touchdown']
    ].reset_index(drop=True)

    pass_df.PassOutcome = pass_df.apply(pass_completion_mapper,axis=1)
    pass_df['ReceiveYrdLine100'] = pass_df.yrdline100 - pass_df.AirYards

    return pass_df


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
    pass_results_df = pass_df.groupby([throw_or_catch_string,'PassLocation']).agg({'GameID':len}).reset_index()

    # Build numpy array representing the football field to structure the heatmap and populate the counts
    field = np.empty((300,3),dtype='object')
    yardline = 0
    pass_location = ['left','middle','right']
    for row in range(0,300):
        field[row][0] = yardline
        field[row][1] = pass_location[row%3]
        temp = pass_results_df.mask(throw_or_catch_string, yardline).mask('PassLocation', field[row][1]).values
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
                columns=[y_label, 'Pass Location', 'Count']
                ).pivot(y_label, 'Pass Location','Count')

    #with sns.axes_style("ticks"):
    #fig,ax1 = plt.subplots(1,1,figsize=figsize)
    ax = sns.heatmap(data=heat_map_df, cmap=cmap, square=False, linewidths=1, linecolor='white', annot=annot, fmt="d", vmin=vmin, vmax=vmax, cbar=True, cbar_ax=None, ax=ax)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks([x for x in range(0,int(100 / yard_grouping) + 1)])

    return ax
