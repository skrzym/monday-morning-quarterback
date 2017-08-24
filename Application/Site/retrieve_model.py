from sklearn.externals import joblib
import json

rfc = joblib.load('mmq\main\data\models\\random_forest_classifier.pkl')

def predict(qtr, down, timeunder, yrdline100, scorediff):
    return rfc.predict_proba([[qtr, down, timeunder, yrdline100, scorediff]])

def predict_proba(qtr, down, yards, timeunder, yrdline100, scorediff):
    rfcp = rfc.predict_proba([[qtr, down, yards, timeunder, yrdline100, scorediff]])[0]*100
    rfcp = [str(round(x,2)) for x in rfcp]
    classes = rfc.classes_
    prediction_dict = {class_:result for class_,result in zip(classes,rfcp)}
    return json.dumps(prediction_dict)
