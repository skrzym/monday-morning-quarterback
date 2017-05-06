import pandas as pd
import numpy as np
import re
import pymongo
from pprint import pprint

mongo = pymongo.MongoClient()
print(mongo.database_names())

cf_data = pd.read_csv('Data/Football-Scenarios-DFE-832307.csv')
cf_data = cf_data[cf_data['_golden'] == False]

split_scenarios = cf_data.orig_antecedent.str.split('.').tolist()
split_scenarios = [scenario[0:-1] for scenario in split_scenarios]


def convert_ordinal(value):
    if value == 'first':
        return 1
    elif value == 'second':
        return 2
    elif value == 'third':
        return 3
    elif value == 'fourth':
        return 4
    else:
        return value


def convert_clock(value):
    min = re.search('(.+?) minute', value)
    sec = re.search('(.+?) second', value)
    if min:
        return int(min.group(1)) * 60
    elif sec:
        return int(sec.group(1))
    else:
        return value


def convert_scoredelta(value):
        down_by = re.search('down by (.+?)', value)
        up_by = re.search('up by (.+?)', value)

        if down_by:
            return int(down_by.group(1)) * -1
        elif up_by:
            return int(up_by.group(1))
        else:
            return value


def convert_fieldpos(value):
    _list = value.split(' ')
    if len(_list) > 1:
        return int(_list[1])
    elif len(_list) == 1:
        return 100 - int(_list[0])
    else:
        return value


def extract(line):
    down = re.search('It is (.+?) down', line)
    ytg = re.search('down and (.+?). ', line)
    fieldpos = re.search("your (.+?) yardline", line)
    quarter = re.search('the (.+?) quarter', line)
    clock = re.search('There is (.+?) left', line)
    scoredelta = re.search('You are (.+?) points', line)

    extraction = (
        line,
        convert_ordinal(down.group(1)) if down else np.NaN,
        int(ytg.group(1).replace('inches', '0')) if ytg else np.NaN,
        convert_fieldpos(fieldpos.group(1)) if fieldpos else np.NaN,
        convert_ordinal(quarter.group(1)) if quarter else np.NaN,
        convert_clock(clock.group(1)) if clock else np.NaN,
        convert_scoredelta(scoredelta.group(1)) if scoredelta else np.NaN
    )
    return extraction


data = [
    extract(scenario)
    for scenario in cf_data.orig_antecedent
]

data_df = pd.DataFrame.from_records(data, columns=['scenario', 'down', 'yards', 'field',
                                                   'quarter', 'clock', 'score'])


def parse_antecedent(antecedent):
    if antecedent in ['pass', 'run', 'punt']:
        return antecedent
    elif antecedent == 'kneel down':
        return 'kneel'
    elif antecedent == 'kick a field goal':
        return 'fg'
    elif antecedent == "Don't know / it depends":
        return 'idk'


guesses = [parse_antecedent(antecedent) for antecedent in cf_data.loc[:, 'antecedent']]


data_df.loc[:, 'guess'] = guesses

#help found here http://stackoverflow.com/questions/33979983/insert-rows-from-pandas-dataframe-into-mongodb-collection-as-individual-document

cleaned_cf_data = data_df.copy()
cleaned_cf_data_records = cleaned_cf_data.to_dict('records')

db = mongo.get_database('mmq')
db.collection_names()
scenarios = db.scenarios
# Uncomment next line to actually run the insert command
#scenarios.insert_many(cleaned_cf_data_records)
pprint([s for s in scenarios.find()])
