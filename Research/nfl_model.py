import pandas as pd
import numpy as np
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

seasons = pd.read_csv("Data/RegularSeasonData/pbp2009.csv")
for i in range(7):
    data = pd.read_csv("Data/RegularSeasonData/pbp201"+str(i)+".csv")
    seasons = seasons.append(data)

cdata = seasons[['qtr', 'down', 'TimeUnder', 'yrdline100', 'ScoreDiff', 'PlayType']]

valid_play_types = [
    'Field Goal',
    'Pass',
    'Run',
    'QB Kneel',
    'Punt'
]


def match(playtype):
    return playtype in valid_play_types

cdata = cdata[cdata.PlayType.map(match)]
cdata = cdata[cdata['down'].isnull() == False]

X = [list(rec) for rec in cdata[['qtr', 'down', 'TimeUnder', 'yrdline100', 'ScoreDiff']].to_records(index=False)]
Y = cdata['PlayType'].tolist()

X = np.array(X)
Y = np.array(Y)


def build_bagging_model():
    clf = OneVsRestClassifier(BaggingClassifier(SVC(kernel='linear', probability=True, class_weight='balanced'),
                                                max_samples=1.0 / 1000, n_estimators=10))
    clf.fit(X, Y)
    return clf


def build_random_forest_model():
    clf = RandomForestClassifier(min_samples_leaf=20)
    clf.fit(X, Y)
    return clf


