from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd 

def predict(data: str,data_type: str,x: str, y: str,value: str):

    ERROR_LIST = {
        'null_value': "'value' Input can't be null"
    }
    if data_type == "xlsx":
        if len(value) != 0:
            data = pd.read_excel(data)

            train_x = data[[x]].values
            y_output = data[[y]].values

            vectorizer = CountVectorizer(binary=True)
            vectors = vectorizer.fit_transform(train_x.ravel())

            model = svm.SVC(kernel='linear')
            model.fit(vectors,y_output.ravel())
            input = vectorizer.transform([value])
            print(model.predict(input))
        else:
            print(ERROR_LIST['null_value'])

    if data_type == 'csv':
        if len(value) != 0:
            data = pd.read_csv(data)

            train_x = data[[x]].values
            y_output = data[[y]].values

            vectorizer = CountVectorizer(binary=True)
            vectors = vectorizer.fit_transform(train_x.ravel())

            model = svm.SVC(kernel='linear')
            model.fit(vectors,y_output.ravel())
            input = vectorizer.transform([value])
            print(model.predict(input))
        else:
            print(ERROR_LIST['null_value'])