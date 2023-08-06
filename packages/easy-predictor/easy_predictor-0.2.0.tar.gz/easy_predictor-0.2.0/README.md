# Easy Predictor 

Perform regression/classification prediction on small Excel dataset in one line!

# Side Note

Currently only two columns are allowed be use on the prediction (Independent & Dependent variable).

## Instruction

1. Linear Regression Prediction

```python
from easy_predictor import linear 

dataset = "path_to_excel_file"
linear.predict(dataset,dataset_type: 'xlsx','csv',column_x,column_y,value: int)
```
2. Text Classification Prediction

```python
from easy_predictor import classification

dataset = "path_to_excel_file"
classification.predict(dataset,dataset_type: 'xlsx','csv',column_x,column_y,value: str)
```
## Latest Update 0.0.2

```
CSV (Comma Seperated Values) File supported
```
