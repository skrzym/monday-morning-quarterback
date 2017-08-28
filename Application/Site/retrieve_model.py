from sklearn.externals import joblib
import json

rfc = joblib.load('mmq\main\data\models\\random_forest_classifier.pkl')


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
    classes = rfc.classes_
    if group_stat == 'quarter':
        qtr_list = [1, 2, 3, 4]
        rfcp = rfc.predict_proba([[q,down,yards,timeunder,yrdline100,scorediff] for q in qtr_list])
        prediction_dict = {qtr_list[q]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[q])} for q in range(len(qtr_list))}
        return prediction_dict
        #return [{str(x):predict_proba(x, down, yards, timeunder, yrdline100, scorediff, False)} for x in qtr_list]
    elif group_stat == 'down':
        down_list = [1, 2, 3, 4]
        rfcp = rfc.predict_proba([[qtr,d,yards,timeunder,yrdline100,scorediff] for d in down_list])
        prediction_dict = {down_list[d]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[d])} for d in range(len(down_list))}
        return prediction_dict
        #return [{str(x):predict_proba(qtr, x, yards, timeunder, yrdline100, scorediff, False)} for x in down_list]
    elif group_stat == 'yards':
        yards_list = [item for item in range(26)]
        rfcp = rfc.predict_proba([[qtr,down,y,timeunder,yrdline100,scorediff] for y in yards_list])
        prediction_dict = {yards_list[y]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[y])} for y in range(len(yards_list))}
        return prediction_dict
        #return [{str(x):predict_proba(qtr, down, x, timeunder, yrdline100, scorediff, False)} for x in yards_list]
    elif group_stat == 'timeunder':
        time_list = [item for item in range(1,16)]
        rfcp = rfc.predict_proba([[qtr,down,yards,t,yrdline100,scorediff] for t in time_list])
        prediction_dict = {time_list[t]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[t])} for t in range(len(time_list))}
        return prediction_dict
        #return [{str(x):predict_proba(qtr, down, yards, x, yrdline100, scorediff, False)} for x in time_list]
    elif group_stat == 'yrdline100':
        field_list = [item for item in range(101)]
        rfcp = rfc.predict_proba([[qtr,down,yards,timeunder,f,scorediff] for f in field_list])
        prediction_dict = {field_list[f]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[f])} for f in range(len(field_list))}
        return prediction_dict
        #return [{str(x):predict_proba(qtr, down, yards, timeunder, x, scorediff, False)} for x in field_list]
    elif group_stat == 'scorediff':
        score_list = [item for item in range(-60,61)]
        rfcp = rfc.predict_proba([[qtr,down,yards,timeunder,yrdline100,s] for s in score_list])
        prediction_dict = {score_list[s]:{class_:str(round(result,2)) for class_,result in zip(classes,rfcp[s])} for s in range(len(score_list))}
        return prediction_dict
        #return [{str(x):predict_proba(qtr, down, yards, timeunder, yrdline100, x, False)} for x in score_list]
    else:
        return -1
