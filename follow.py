import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('csv_files/Full Team Data.csv', encoding='utf-8')


X = df.iloc[:, :]
y = df.iloc[:, 12]

check = X.head()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=17, test_size=0.2)
dtc = DecisionTreeClassifier()
par = dtc.get_params()
dtc.fit(X_train, y_train)

print(par)

# print(check)