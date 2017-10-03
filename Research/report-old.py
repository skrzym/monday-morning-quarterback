from matplotlib import pyplot as plt
import matplotlib.ticker as plticker
import seaborn as sns
import pandas as pd
import numpy as np
import math
import warnings
from collections import Counter
import nfldatatools as nfltools

rs_pbp = nfltools.gather_data(playoffs=False)
po_pbp = nfltools.gather_data(playoffs=True)


sns.set_style("whitegrid")

#Set general plot properties
sns.set_style("white", {"axes.grid": True})
sns.set_context({"figure.figsize": (10, 7)})


################################################
# Figure 1 - HeatMap
def fig1():
    filters=[
        ['Season', 2009, '>=']
    ]
    yard_grouping = 10
    fig,(ax1, ax2) = plt.subplots(1,2,figsize=(15,10))
    nfltools.plotPassingHeatMap(rs_pbp, filters=filters, ax=ax1, yard_grouping=yard_grouping)
    nfltools.plotPassingHeatMap(po_pbp, filters=filters, ax=ax2, yard_grouping=yard_grouping)
    return fig
figure_1 = fig1()

def fig1a():
    filters=[
        ['posteam', 'NE', '==']
    ]
    yard_grouping = 10
    fig,(ax1, ax2) = plt.subplots(1,2,figsize=(15,10))
    nfltools.plotPassingHeatMap(rs_pbp, filters=filters, ax=ax1, yard_grouping=yard_grouping)
    nfltools.plotPassingHeatMap(po_pbp, filters=filters, ax=ax2, yard_grouping=yard_grouping)
    return fig
figure_1a = fig1a()


###############################################################
# Figure 2 - 
def match(playtype):
    valid_play_types = [
        'Field Goal',
        'Pass',
        'Run',
        'QB Kneel',
        'Punt',
        'Extra Point',
        'Sack',
        'Spike',
        'Timeout'
    ]
    return playtype in valid_play_types


def condense_pbp_data(df):
    new_df = df[['qtr', 'down', 'TimeUnder','TimeSecs', 'yrdline100', 'ScoreDiff', 'PlayType','Season']]
    new_df = new_df[new_df.PlayType.map(match)]
    new_df = new_df[new_df['down'].isnull()==False]
    return new_df

playoffs = condense_pbp_data(po_pbp)
regular = condense_pbp_data(rs_pbp)


def makeDF(season=2009):
    rdf = regular#[regular.Season==season]
    rdf = rdf.groupby('PlayType').agg({'qtr':len}).reset_index()
    rdf.columns = ['PlayType', 'Count']
    rdf['Percent Total'] = rdf.Count/rdf.Count.sum()*100
    rdf['ID'] = 'Regular'

    pdf = playoffs#[playoffs.Season==season]
    pdf = pdf.groupby('PlayType').agg({'qtr':len}).reset_index()
    pdf.columns = ['PlayType', 'Count']
    pdf['Percent Total'] = pdf.Count/pdf.Count.sum()*100
    pdf['ID'] = 'Playoffs'

    x = rdf.append(pdf, ignore_index=True)
    fig, ax1 = plt.subplots(1,1,figsize=(12,10))
    sns.barplot(ax=ax1, data=x, y='PlayType', x='Percent Total',hue='ID', order=['Pass', 'Run', 'Punt', 'Field Goal', 'QB Kneel'])
    ax1.set_xlim(0,60)
    return fig

figure_2 = makeDF()



###############################################################
# Figure  - 
def fig3():
    sns.set_style('whitegrid')
    sns.set_palette(['blue', 'green','red'])


    fig, axes = plt.subplots(2, 1, figsize=(15,15))
    shade = True
    bw = '2'

    sns.kdeplot(ax=axes[0],data=rs_pbp[rs_pbp.PlayType == 'Pass'].ScoreDiff.dropna(),label='Pass',shade=shade,bw=bw)
    sns.kdeplot(ax=axes[0],data=rs_pbp[rs_pbp.PlayType == 'Run'].ScoreDiff.dropna(),label='Run',shade=shade,bw=bw)
    sns.kdeplot(ax=axes[0],data=rs_pbp[rs_pbp.PlayType == 'Extra Point'].ScoreDiff.dropna(),label='Extra Point',shade=shade,bw=bw)

    axes[0].set_xlim(-40,40)
    axes[0].set_ylim(0,0.09)

    sns.kdeplot(ax=axes[1],data=po_pbp[po_pbp.PlayType == 'Pass'].ScoreDiff.dropna(),label='Pass',shade=shade,bw=bw)
    sns.kdeplot(ax=axes[1],data=po_pbp[po_pbp.PlayType == 'Run'].ScoreDiff.dropna(),label='Run',shade=shade,bw=bw)
    sns.kdeplot(ax=axes[1],data=po_pbp[po_pbp.PlayType == 'Extra Point'].ScoreDiff.dropna(),label='Extra Point',shade=shade,bw=bw)

    axes[1].set_xlim(-40,40)
    axes[1].set_ylim(0,0.09)
    #SMOOTH IT OUT!
    return fig

figure_3 = fig3()


###############################################################
# Figure  - 
def plot_PlayType(df,stat,playtypelist=['Pass','Run','Field Goal','QB Kneel','Punt'],percent_total=False):
    g = df.groupby([stat,'PlayType']).count().reset_index()
    g = g[g.columns[0:3]]
    last_col_name = g.columns[-1]
    g1 = g.groupby([stat, 'PlayType']).agg({last_col_name: 'sum'})
    if percent_total:
        g1 = g1.groupby(level=1).apply(lambda x: 100 * x / float(x.sum()))
    g1 = g1.reset_index()
    g1 = g1[g1.PlayType.apply(lambda x: x in playtypelist)]
    return sns.barplot(x=stat, y=last_col_name, hue="PlayType", data=g1)


def fig4():
    fig = plt.figure(figsize=(16,32))

    ax3 = fig.add_subplot(513)
    ax3 = plot_PlayType(regular,'qtr',['Run','Pass'],False)

    ax4 = fig.add_subplot(514)
    ax4 = plot_PlayType(regular,'yrdline100',['Run','Pass'],False)
    ax4.xaxis.set_ticks(range(4, 99, 5))
    ax4.xaxis.set_ticklabels(range(5,100,5))
    ax4.grid(True,'major','both')
    return fig


figure_4 = fig4()

###############################################################
# Figure  - 
def fig5():
    fig, axes = plt.subplots(2,1,figsize=(14,7))
    sns.kdeplot(ax=axes[0],data=regular[regular.PlayType == 'Pass'].TimeSecs,bw=20,label='Pass')
    sns.kdeplot(ax=axes[0],data=regular[regular.PlayType == 'Run'].TimeSecs,bw=20,label='Run')
    loc = plticker.MultipleLocator(base=120.0) # this locator puts ticks at regular intervals
    axes[0].xaxis.set_major_locator(loc)
    axes[0].set_xlim(0,3600)
    axes[0].set_ylim(0,0.00085)
    axes[0].vlines([x*60 for x in [15,30,45]],0,0.0009,colors='black')
    axes[0].grid(True,'major','y')
    axes[0].grid(False,'major','x')

    sns.kdeplot(ax=axes[1],data=playoffs[playoffs.PlayType == 'Pass'].TimeSecs,bw=20,label='Pass')
    sns.kdeplot(ax=axes[1],data=playoffs[playoffs.PlayType == 'Run'].TimeSecs,bw=20,label='Run')
    loc = plticker.MultipleLocator(base=120.0) # this locator puts ticks at regular intervals
    axes[1].xaxis.set_major_locator(loc)
    axes[1].set_xlim(0,3600)
    axes[1].set_ylim(0,0.00085)
    axes[1].vlines([x*60 for x in [15,30,45]],0,0.0009,colors='black')
    axes[1].grid(True,'major','y')
    axes[1].grid(False,'major','x')
    return fig

figure_5 = fig5()

#################################################################
# Figure  - 
def fig6():
    rs_fg = rs_pbp[rs_pbp.PlayType =='Field Goal'].groupby('FieldGoalResult').agg({'Date':len}).reset_index()
    rs_fg.columns=['FieldGoalResult', 'Count']
    rs_fg['Percent Total'] = rs_fg.Count.apply(lambda x: 100 * x / float(rs_fg.Count.sum()))

    po_fg = po_pbp[po_pbp.PlayType =='Field Goal'].groupby('FieldGoalResult').agg({'Date':len}).reset_index()
    po_fg.columns=['FieldGoalResult', 'Count']
    po_fg['Percent Total'] = po_fg.Count.apply(lambda x: 100 * x / float(po_fg.Count.sum()))

    sns.set_palette(['green', 'orange', 'red'])


    fig, axes = plt.subplots(2, 2,sharey=True,figsize=(14,7))
    order = ['Good','Blocked','No Good']

    sns.violinplot(ax=axes[0][0], data=rs_pbp[rs_pbp.PlayType=='Field Goal'], x='FieldGoalDistance', y='FieldGoalResult',order=order, scale='width', bw=0.05)
    sns.violinplot(ax=axes[1][0], data=po_pbp[po_pbp.PlayType=='Field Goal'], x='FieldGoalDistance', y='FieldGoalResult',order=order, scale='width', bw=0.05)
    axes[0][0].set_xlim(0,100)
    axes[1][0].set_xlim(0,100)

    sns.barplot(ax=axes[0][1], data=rs_fg,y='FieldGoalResult', x='Percent Total',order=order)
    sns.barplot(ax=axes[1][1], data=po_fg,y='FieldGoalResult', x='Percent Total',order=order)
    axes[0][1].set_xlim(0,100)
    axes[1][1].set_xlim(0,100)

    axes[0][1].set_xticklabels(['0%','20%','40%','60%','80%','100%'])
    axes[1][1].set_xticklabels(['0%','20%','40%','60%','80%','100%'])


    axes[0][0].set_title('Field Goal Results by Distance')
    axes[0][0].set_xlabel('')
    axes[0][0].set_ylabel('Regular Season')

    axes[0][1].set_title('Field Goal Results Distribution')
    axes[0][1].set_xlabel('')
    axes[0][1].set_ylabel('')

    axes[1][0].set_ylabel('Playoffs')
    axes[1][0].set_xlabel('Field Goal Distance (yds)')
    axes[1][0].figure

    axes[1][1].set_ylabel('')
    axes[1][1].set_xlabel('Percent Total')
    return fig


figure_6 = fig6()
#####################################################################
# Figure  - 
teams = [['ARI', 'Arizona', 'Cardinals', 'Arizona Cardinals'],
 ['ATL', 'Atlanta', 'Falcons', 'Atlanta Falcons'],
 ['BAL', 'Baltimore', 'Ravens', 'Baltimore Ravens'],
 ['BUF', 'Buffalo', 'Bills', 'Buffalo Bills'],
 ['CAR', 'Carolina', 'Panthers', 'Carolina Panthers'],
 ['CHI', 'Chicago', 'Bears', 'Chicago Bears'],
 ['CIN', 'Cincinnati', 'Bengals', 'Cincinnati Bengals'],
 ['CLE', 'Cleveland', 'Browns', 'Cleveland Browns'],
 ['DAL', 'Dallas', 'Cowboys', 'Dallas Cowboys'],
 ['DEN', 'Denver', 'Broncos', 'Denver Broncos'],
 ['DET', 'Detroit', 'Lions', 'Detroit Lions'],
 ['GB', 'Green Bay', 'Packers', 'Green Bay Packers', 'G.B.', 'GNB'],
 ['HOU', 'Houston', 'Texans', 'Houston Texans'],
 ['IND', 'Indianapolis', 'Colts', 'Indianapolis Colts'],
 ['JAC', 'Jacksonville', 'Jaguars', 'Jacksonville Jaguars', 'JAX'],
 ['KC', 'Kansas City', 'Chiefs', 'Kansas City Chiefs', 'K.C.', 'KAN'],
 ['LA', 'Los Angeles', 'Rams', 'Los Angeles Rams', 'L.A.'],
 ['MIA', 'Miami', 'Dolphins', 'Miami Dolphins'],
 ['MIN', 'Minnesota', 'Vikings', 'Minnesota Vikings'],
 ['NE', 'New England', 'Patriots', 'New England Patriots', 'N.E.', 'NWE'],
 ['NO', 'New Orleans', 'Saints', 'New Orleans Saints', 'N.O.', 'NOR'],
 ['NYG', 'Giants', 'New York Giants', 'N.Y.G.'],
 ['NYJ', 'Jets', 'New York Jets', 'N.Y.J.'],
 ['OAK', 'Oakland', 'Raiders', 'Oakland Raiders'],
 ['PHI', 'Philadelphia', 'Eagles', 'Philadelphia Eagles'],
 ['PIT', 'Pittsburgh', 'Steelers', 'Pittsburgh Steelers'],
 ['SD', 'San Diego', 'Chargers', 'San Diego Chargers', 'S.D.', 'SDG'],
 ['SEA', 'Seattle', 'Seahawks', 'Seattle Seahawks'],
 ['SF', 'San Francisco', '49ers', 'San Francisco 49ers', 'S.F.', 'SFO'],
 ['STL', 'St. Louis', 'Rams', 'St. Louis Rams', 'S.T.L.'],
 ['TB', 'Tampa Bay', 'Buccaneers', 'Tampa Bay Buccaneers', 'T.B.', 'TAM'],
 ['TEN', 'Tennessee', 'Titans', 'Tennessee Titans'],
 ['WAS', 'Washington', 'Redskins', 'Washington Redskins', 'WSH']]

teams_dict = {x[3]:x[0] for x in teams}
 # Jacksonville Data Fix
rs_pbp.posteam = rs_pbp.posteam.replace('JAX', 'JAC')
rs_pbp.HomeTeam = rs_pbp.HomeTeam.replace('JAX', 'JAC')
rs_pbp.AwayTeam = rs_pbp.AwayTeam.replace('JAX', 'JAC')

pass_rush_attempts_by_team = rs_pbp.groupby(['posteam','Season']).agg(sum)[['PassAttempt','RushAttempt']]
pass_rush_attempts_by_team['PassRushRatio'] = pass_rush_attempts_by_team.apply(lambda x: (x.PassAttempt * 1.0) / x.RushAttempt, axis=1)

sns.set_palette('muted')
plot_df = pass_rush_attempts_by_team
plot_teams = teams_dict


def plotPassRushByTeam(team_focus_1, team_focus_2):
    fig,ax = plt.subplots(1,1,figsize=(15,8))
    for team in plot_teams:
        if (plot_teams[team] != team_focus_1) or (plot_teams[team] != team_focus_1):
            plt.plot(plot_df.loc[plot_teams[team]]['PassRushRatio'], color='0.91')
    plt.plot(plot_df.loc[team_focus_1]['PassRushRatio'], color='Blue', axes=ax)
    plt.plot(plot_df.loc[team_focus_2]['PassRushRatio'], color='Red', axes=ax)
    return fig


def fig7():
    sns.set_style('white')
    return plotPassRushByTeam(team_focus_1 = 'NYG', team_focus_2 = 'NYJ')


figure_7 = fig7()

##########################################################
# Figure  - 

playoff_teams = {year:po_pbp.mask('Season',year).posteam.dropna().unique().tolist() for year in np.arange(2009,2017,1)}

def madeit(row):
    team, season = row.name
    return int(team in playoff_teams[season])

next_df = pass_rush_attempts_by_team.copy()

next_df['PO'] = next_df.apply(madeit, axis=1)

next_df.reset_index().groupby(['posteam','PO']).agg({'PassRushRatio':np.mean}).reset_index().pivot('posteam','PO','PassRushRatio')



def fig8():
    sns.set_context('talk')
    #sns.heatmap(data = pass_rush_attempts_by_team.reset_index().pivot('posteam','PO','PassRushRatio'),
    #            vmin=0,vmax=1,square=False,cmap='rainbow', annot=False)
    fig,ax = plt.subplots(1,1)
    new_df = next_df.reset_index().groupby(['posteam','PO']).agg({'PassRushRatio':np.mean}).reset_index().pivot('posteam','PO','PassRushRatio')
    sns.heatmap(data = new_df, square=False, annot=False, cmap='Greens')
    return fig


figure_8 = fig8()
############################################################
# Figure  - 
def fig9():
    fig,ax = plt.subplots(1,1)
    pass_rush_attempts_by_team.loc['DEN']['PassRushRatio'].plot()
    return fig


figure_9 = fig9()

#############################################################
# Figure  - 
def fig10():
    fig, ax = plt.subplots(1,1,figsize=(3,5))
    sns.boxplot(data=next_df.reset_index(),x='PO', y='PassRushRatio', ax=ax)
    return fig


figure_10 = fig10()
#############################################################
# Figure  - 
avg_prr_by_team = pass_rush_attempts_by_team.reset_index().groupby('posteam').agg({'PassRushRatio':np.mean}).sort_values('PassRushRatio')
avg_prr_by_season = pass_rush_attempts_by_team.reset_index().groupby('Season').agg({'PassRushRatio':np.mean}).sort_values('PassRushRatio')


def fig11():
    with sns.axes_style('ticks'):
        fig,ax = plt.subplots(1,1,figsize=(20,7))
        sns.boxplot(data=next_df.reset_index(),x='posteam', y='PassRushRatio', ax=ax, order=avg_prr_by_team.index.tolist(),hue='PO')
    return fig


figure_11 = fig11()
