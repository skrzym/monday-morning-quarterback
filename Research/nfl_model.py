import pandas as pd
import numpy as np
import glob
import time
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

def gather_and_process_data(path):
    # TODO Error raised if passed path is invalid
    files = glob.glob(path)
    seasons = pd.read_csv(files[0])
    for x in files[1:-1]:
        data = pd.read_csv(x)
        seasons = seasons.append(data)

    # Pull specific columns for the model here
    # 'time' column has the specific 'XX:XX' game clock that can be used if converted to a usable number
    cdata = seasons[['qtr', 'down', 'TimeUnder', 'yrdline100', 'ScoreDiff', 'PlayType']]


    def match(playtype):
        valid_play_types = [
        'Field Goal',
        'Pass',
        'Run',
        'QB Kneel',
        'Punt'
        ]
        return playtype in valid_play_types

    cdata = cdata[cdata.PlayType.map(match)]
    cdata = cdata[cdata['down'].isnull()==False]

    X = [list(rec) for rec in cdata[['qtr', 'down', 'TimeUnder', 'yrdline100', 'ScoreDiff']].to_records(index=False)]
    y = cdata['PlayType'].tolist()

    X = np.array(X)
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(0.33), random_state=42)

    return X_train, X_test, y_train, y_test


def build_bagging_model(x,y):
    clf = OneVsRestClassifier(
        BaggingClassifier(
            SVC(kernel='linear', \
                probability=True, \
                class_weight='balanced'\
                ), \
            max_samples=1.0 / 1000, \
            n_estimators=10 \
        ) \
    )
    clf.fit(x,y)
    # print(clf.predict_proba(x))
    return clf


def build_random_forest_model(x,y):
    clf = RandomForestClassifier(min_samples_leaf=20)
    clf.fit(x,y)
    # print(clf.score(x,y))
    # print(clf.predict_proba(x[5]))
    return clf
