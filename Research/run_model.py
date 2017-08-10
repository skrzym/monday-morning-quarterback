import nfl_model
from sklearn.externals import joblib

X_train, X_test, y_train, y_test = nfl_model.gather_and_process_data("data/playbyplaydata/*")

random_forest = nfl_model.build_random_forest_model(X_train,y_train)
print(random_forest.predict([[4, 4, 1, 20, -3]]))

joblib.dump(random_forest, 'Data/models/random_forest_classifier.pkl')

rfc = joblib.load('Data/models/random_forest_classifier.pkl')
print(rfc.predict([[4, 4, 1, 20, -3]]))
