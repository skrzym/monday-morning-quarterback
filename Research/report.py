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
#sns.set_context({"figure.figsize": (10, 7)})
sns.set_context('talk')

################################################
# PART 1
################################################
# Part 1 Figure 1 - HeatMap
def p1f1_patriots_passing_heat(filename=None, figsize=(15,10)):
    filtered_data = rs_pbp.mask('posteam', 'NE')
    outcomes = ['Complete', 'Touchdown', 'Incomplete', 'Fumble', 'Interception']
    cmaps = ['Greens', 'Oranges', 'Greys', 'Purples', 'Reds']
    annot=True
    yard_grouping = 10
    
    fig,axes = plt.subplots(1,5,figsize=figsize, sharey=True)
    
    for index in range(5):
        nfltools.plotPassingHeatMap(filtered_data, filters=[['PassOutcome', outcomes[index]]], ax=axes[index], yard_grouping=yard_grouping, annot=annot, cmap=cmaps[index], cbar=False)
        axes[index].set_title(outcomes[index])
        if index > 0:
            axes[index].set_ylabel('')
    
    # Filter out 0 value annotations on the heatmaps
    for col in range(5):
        for text in axes[col].texts:
            if text.get_text() == '0':
                text.set_text('')
    
    fig.suptitle('Patriots Passing Game Since 2009')
    if filename:
        plt.savefig(filename)

        
################################################
#Part 1 Figure 1 Auxilary - HeatMap
def p1f1_patriots_rushing_heat(filename=None, figsize=(15,10)):
    sns.set_context('notebook')
    filtered_data = rs_pbp.mask('posteam', 'NE')
    outcomes = ['Run', 'Touchdown', 'Fumble']
    cmaps = ['Greens', 'Oranges', 'Purples']
    annot=True
    yard_grouping = 10
    
    fig,axes = plt.subplots(1,3,figsize=figsize, sharey=True)
    
    for index in range(3):
        nfltools.plotRushingHeatMap(filtered_data, filters=[['RunOutcome', outcomes[index]]], ax=axes[index], yard_grouping=yard_grouping, annot=annot, cmap=cmaps[index], cbar=False)
        axes[index].set_title(outcomes[index])
        if index > 0:
            axes[index].set_ylabel('')
    
    # Filter out 0 value annotations on the heatmaps
    for col in range(3):
        for text in axes[col].texts:
            if text.get_text() == '0':
                text.set_text('')
    
    fig.suptitle('Patriots Rushing Game Since 2009')
    if filename:
        plt.savefig(filename)


################################################
#Part 1 Figure 2 - SwarmPlot
def p1f2_patriots_passing_swarm(filename=None, figsize=(10,8)):
    sns.set_style('darkgrid')
    sns.set_context('talk')
    ylim=(-15,80)
    figsize=None
    filters = [['posteam', 'NE'], ['PassOutcome', 'Complete', '!='], ['PassOutcome', 'Incomplete', '!=']]

    fig, axes = plt.subplots(1,1, figsize=figsize)
    nfltools.plotPassingSwarm(rs_pbp, filters, ylim=ylim, axes=axes, title='Regular Season Fumbles, Touchdowns, and Interceptions')
    #nfltools.plotPassingSwarm(po_pbp, filters, ylim=ylim, axes=axes[1], title='Postseason Passing')
    fig.suptitle('Patriots Passing Data Since 2009')
    #return fig
    if filename:
        plt.savefig(filename)


################################################
#Part 1 Figure 3 - HeatMap
def p1f3_superbowl_li_heat(filename=None, figsize=(10,12)):
    sns.set_context('talk')
    title = 'SuperBowl LI Passing, Rushing, and Field Goals'
    gen_filters =  None
    pass_filters = [['PassOutcome', 'Complete']]
    run_filters =  [['Fumble',0]]
    fg_filters =   [['FieldGoalResult', 'Good']]
    nfltools.PlotGamesHeatMaps([2017020500], title, gen_filters=gen_filters, pass_filters=pass_filters, run_filters=run_filters, fg_filters=fg_filters, figsize=figsize)
    plt.subplots_adjust(hspace=0.35)
    if filename:
        plt.savefig(filename)
    plt.show()


################################################
# Part 1 Figure 4 - hist
def p1f4_plays_over_time(filename=None, figsize=(10,12)):
    sns.set_style('dark')
    fig, ax = plt.subplots(3,1,figsize=figsize)

    plots = ['Pass', 'Run', 'Field Goal']
    colors = ['Green', 'Blue', 'Red']

    loc = plticker.MultipleLocator(base=300.0) # this locator puts ticks at regular intervals

    for i in range(len(plots)):
        ax[i].hist(regular.loc[regular.PlayType == plots[i]].TimeSecs, bins=60, normed=False, label=plots[i], color=colors[i])
        ax[i].legend()
        ylim = ax[i].get_ylim()
        ax[i].plot([15*60,15*60],[ylim[0],ylim[1]], c='white', linewidth=2, alpha=0.6)
        ax[i].plot([30*60,30*60],[ylim[0],ylim[1]], c='white', linewidth=2, alpha=0.6)
        ax[i].plot([45*60,45*60],[ylim[0],ylim[1]], c='white', linewidth=2, alpha=0.6)
        ax[i].set_ylim(ylim)
        ax[i].grid(True,'major','y')
        ax[i].grid(False,'major','x')
        ax[i].set_xlim(0,3600)
        ax[i].xaxis.set_major_locator(loc)
        ax[i].set_xticklabels([0,0,5,10,15,20,25,30,35,40,45,50,55,60])
        ax[i].set_xlabel('Mintues Remaining in Game')
        ax[i].set_ylabel('Number of Plays')
        ax[i].set_title('{} Plays per Game Minute'.format(plots[i]))
    plt.suptitle('09-16 Regular Season NFL Plays per Game Minute') 
    plt.subplots_adjust(hspace=0.5)
    if filename:
        plt.savefig(filename)
    plt.show()

    
################################################
# Part 1 Figure 5 - Swarm
def p1f5_postseason_fieldgoals_swarm(filename=None, figsize=(10,12)):
    seasons = po_pbp.Season.unique().tolist()
    ylim=(15,70)
    figsize=None

    fig, axes = plt.subplots(2,4, figsize=figsize, sharey=True)
    row = 0
    col = 0
    for season in seasons:
        filters=[['Season', season, '==']]
        nfltools.plotFieldGoalSwarm(po_pbp, filters=filters, ylim=ylim, title='{}'.format(season), figsize=figsize, axes=axes[row][col])
        if col > 0:
            axes[row][col].set_ylabel('')
        if season in seasons[1:]:
            axes[row][col].legend().set_visible(False)
        col += 1
        if col > 3:
            row += 1
            col = 0
    
    fig.tight_layout()
    fig.suptitle('Postseason Field Goals by Distance Since 2009')
    fig.subplots_adjust(top=0.94)
    if filename:
        plt.savefig(filename)

################################################
# PART 2
################################################
# Part 2 Figure 1 - Counting Plays
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


def p2f1_counting_plays(include_playoffs=False, filename=None, figsize=(10,8)):
    fig, ax1 = plt.subplots(1,1,figsize=figsize)
    
    rdf = regular
    rdf = rdf.groupby('PlayType').agg({'qtr':len}).reset_index()
    rdf.columns = ['PlayType', 'Count']
    rdf['Percent Total'] = rdf.Count/rdf.Count.sum()*100
    rdf['ID'] = 'Regular'
    
    if include_playoffs:
        pdf = playoffs
        pdf = pdf.groupby('PlayType').agg({'qtr':len}).reset_index()
        pdf.columns = ['PlayType', 'Count']
        pdf['Percent Total'] = pdf.Count/pdf.Count.sum()*100
        pdf['ID'] = 'Playoffs'

        x = rdf.append(pdf, ignore_index=True)
        plt.title('Regular and Playoff Play Types Since 2009')
    else:
        x = rdf.copy()
        plt.title('Regular Seasons Play Types Since 2009')
    
    sns.barplot(ax=ax1, data=x, y='PlayType', x='Percent Total',hue='ID', order=['Pass', 'Run', 'Punt', 'Field Goal', 'QB Kneel'])
    ax1.set_xlabel('Percent of All Plays')
    ax1.set_xlim(0,60)
    if filename:
        plt.savefig(filename)
