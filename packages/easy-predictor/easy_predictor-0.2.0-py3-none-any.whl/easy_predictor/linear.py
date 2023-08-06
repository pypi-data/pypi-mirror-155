from sklearn.linear_model import LinearRegression
import pandas as pd 

def predict(data: str,data_type: str,x: str, y: str,value: int):

    ERROR_LIST = {
        'null_value': "'value' Input can't be null"
    }
    if data_type == 'xlsx':
        if value != None:
            data = pd.read_excel(data)

            train = data[[x]].values
            predict_value = data[[y]].values
            
            lr = LinearRegression()
            lr.fit(train,predict_value) 
            print(lr.predict([[value]]))
        else:
            print(ERROR_LIST['null_value'])

    if data_type == 'csv':   
        if value != None:
            data = pd.read_csv(data)

            train = data[[x]].values
            predict_value = data[[y]].values
            
            lr = LinearRegression()
            lr.fit(train,predict_value) 
            print(lr.predict([[value]]))
        else:
            print(ERROR_LIST['null_value'])