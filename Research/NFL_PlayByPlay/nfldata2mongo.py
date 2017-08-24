import nfldatatools as tools
import pandas as pd
import pymongo


def convert(playtype):
    valid_play_types = {
        'Field Goal':'fg',
        'Pass':'pass',
        'Run':'run',
        'QB Kneel':'kneel',
        'Punt':'punt',
    }
    if playtype in valid_play_types.keys():
        return valid_play_types[playtype]

def match(playtype):
    valid_play_types = [
        'Field Goal',
        'Pass',
        'Run',
        'QB Kneel',
        'Punt'
    ]
    return playtype in valid_play_types


def condense_pbp_data(df):
    new_df = df[[
            'Date',
            'GameID',
            'Drive',
            'qtr',
            'down',
            'time',
            'TimeUnder',
            'TimeSecs',
            'yrdline100',
            'ydstogo',
            'PlayType',
            'ScoreDiff',
            'HomeTeam',
            'AwayTeam',
            'Season',
            'Playoffs'
    ]]
    new_df = new_df[new_df.PlayType.map(match)]
    new_df.PlayType = new_df.PlayType.apply(convert)
    new_df = new_df[new_df['down'].isnull()==False]
    new_df.columns=[
            'Date',
            'GameID',
            'Drive',
            'quarter',
            'down',
            'time',
            'clock',
            'TimeSecs',
            'field',
            'yards',
            'PlayType',
            'score',
            'HomeTeam',
            'AwayTeam',
            'Season',
            'Playoffs'
    ]
    return new_df


def transform():
    playoffs_df = tools.gather_data(playoffs=True)
    regular_df = tools.gather_data(playoffs=False)
    playoffs_df['Playoffs'] = True
    regular_df['Playoffs'] = False
    play_by_play = pd.concat([regular_df, playoffs_df], ignore_index=True)
    play_by_play = play_by_play[play_by_play.columns[1:]]
    play_by_play = condense_pbp_data(play_by_play)
    return play_by_play


def transform_and_insert():
    mongo = pymongo.MongoClient()
    print(mongo.database_names())
    db = mongo.get_database('mmq')
    print(db.collection_names())
    nfldata = db.nfldata
    cleaned_nfldata = transform()
    # help found here:
    # http://stackoverflow.com/questions/33979983/insert-rows-from-pandas-dataframe-into-mongodb-collection-as-individual-document
    cleaned_nfldata_data_records = cleaned_nfldata.to_dict('records')
    nfldata.insert_many(cleaned_nfldata_data_records)
    print(mongo.database_names())
    print(db.collection_names())
