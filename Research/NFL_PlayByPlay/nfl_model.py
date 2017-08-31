import pandas as pd
import numpy as np
import glob
import time
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import warnings
from sklearn.externals import joblib

def gather_and_process_data(path, test_season=None):
    # TODO Error raised if passed path is invalid
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        files = glob.glob(path)
        seasons = pd.read_csv(files[0])
        for x in files[1:]:
            data = pd.read_csv(x)
            seasons = seasons.append(data)
    
    # Pull specific columns for the model here
    # 'time' column has the specific 'XX:XX' game clock that can be used if converted to a usable number
    cdata = seasons[['qtr', 'down', 'ydstogo', 'TimeUnder', 'yrdline100', 'ScoreDiff', 'PlayType', 'Season']]


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

    if test_season is None:
        X = [list(rec) for rec in cdata[
                ['qtr',
                 'down',
                 'ydstogo',
                 'TimeUnder',
                 'yrdline100',
                 'ScoreDiff']
            ].to_records(index=False)]
        y = cdata['PlayType'].tolist()

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=(0.33), random_state=42)
    else:
        train_data = cdata[cdata.Season != test_season]
        X_train = [list(rec) for rec in train_data[
            ['qtr',
             'down',
             'ydstogo',
             'TimeUnder',
             'yrdline100',
             'ScoreDiff']
        ].to_records(index=False)]
        y_train = train_data.PlayType.tolist()
        
        test_data = cdata[cdata.Season == test_season]
        X_test = [list(rec) for rec in test_data[
            ['qtr',
             'down',
             'ydstogo',
             'TimeUnder',
             'yrdline100',
             'ScoreDiff']
        ].to_records(index=False)]
        y_test = test_data.PlayType.tolist()
        
    return X_train, X_test, y_train, y_test


def build_bagging_model(X_train, y_train):
    clf = OneVsRestClassifier(
        BaggingClassifier(
            SVC(kernel='linear',
                probability=True,
                class_weight='balanced'
            ),
            max_samples=1.0 / 1000,
            n_estimators=10
        )
    )
    clf.fit(X_train, y_train)
    return clf


def build_random_forest_model(X_train, y_train, n_estimators=10,
    max_depth=None, min_samples_split=2, min_samples_leaf=1,
    max_features='auto', bootstrap=True, oob_score=False, n_jobs=1,
    random_state=None
    ):
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        bootstrap=bootstrap,
        oob_score=oob_score,
        n_jobs=n_jobs,
        random_state=random_state
    )
    clf.fit(X_train, y_train)
    return clf

def build_extra_trees_model(X_train, y_train,n_estimators=10,
    max_depth=None, min_samples_split=2, min_samples_leaf=1,
    max_features='auto', bootstrap=True, oob_score=False, n_jobs=1,
    random_state=None
    ):
    clf = ExtraTreesClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        bootstrap=bootstrap,
        oob_score=oob_score,
        n_jobs=n_jobs,
        random_state=random_state
    )
    clf.fit(X_train, y_train)
    return clf


def build_gradient_boosted_regression_trees(X_train, y_train, n_estimators=100,
    learning_rate=1.0, max_depth=1, random_state=0):
    clf = GradientBoostingClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        random_state=random_state
    ).fit(X_train, y_train)
    return clf


def store_model(model, file_name, protocol=3):
    joblib.dump(model, '../Data/models/{}.pkl'.format(file_name),protocol=protocol)
