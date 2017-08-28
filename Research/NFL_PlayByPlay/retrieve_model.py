from sklearn.externals import joblib
import json

rfc = joblib.load('../Data/models/random_forest_classifier.pkl')

def predict(qtr, down, timeunder, yrdline100, scorediff):
    return rfc.predict_proba([[qtr, down, timeunder, yrdline100, scorediff]])

def predict_proba(qtr, down, yards, timeunder, yrdline100, scorediff, return_json=True):
    rfcp = rfc.predict_proba([[qtr, down, yards, timeunder, yrdline100, scorediff]])[0]*100
    rfcp = [str(round(x,2)) for x in rfcp]
    classes = rfc.classes_
    prediction_dict = {class_:result for class_,result in zip(classes,rfcp)}
    if return_json:
        return json.dumps(prediction_dict)
    else:
        return prediction_dict

def predict_group_proba(qtr, down, yards, timeunder, yrdline100, scorediff, group_stat):
    if group_stat == 'quarter':
        qtr_list = [1, 2, 3, 4]
        return [{str(x):predict_proba(x, down, yards, timeunder, yrdline100, scorediff, False)} for x in qtr_list]
    elif group_stat == 'down':
        down_list = [1, 2, 3, 4]
        return [predict_proba(qtr, x, yards, timeunder, yrdline100, scorediff, False) for x in down_list]
    elif group_stat == 'yards':
        yards_list = [item for item in range(26)]
        return [predict_proba(qtr, down, x, timeunder, yrdline100, scorediff, False) for x in yards_list]
    elif group_stat == 'timeunder':
        time_list = [item for item in range(1,16)]
        return [predict_proba(qtr, down, yards, x, yrdline100, scorediff, False) for x in time_list]
    elif group_stat == 'yrdline100':
        field_list = [item for item in range(101)]
        return [predict_proba(qtr, down, yards, timeunder, x, scorediff, False) for x in field_list]
    elif group_stat == 'scorediff':
        score_list = [item for item in range(-60,61)]
        return [predict_proba(qtr, down, yards, timeunder, yrdline100, x, False) for x in score_list]
    else:
        return -1
