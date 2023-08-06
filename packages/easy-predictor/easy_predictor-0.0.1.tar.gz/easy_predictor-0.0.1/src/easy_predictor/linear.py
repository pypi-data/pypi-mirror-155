from sklearn.linear_model import LinearRegression
import pandas as pd 

def predict(data: str,x: str, y: str,value: int):

    data = pd.read_excel(data)
    
    train = data[[x]].values
    predict_value = data[[y]].values
    
    lr = LinearRegression()
    lr.fit(train,predict_value) 
    print(lr.predict([[value]]))