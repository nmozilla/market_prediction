# -*- coding: utf-8 -*-
"""prediction_RFRegressor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PL4PKDqp0qQ_MnmrXBo96OOgIz4jnkqw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression

df = pd.read_csv('/content/STOCK_NVDA.csv')
sorted_data = df.sort_values(by='Date', ascending=True)
sorted_data

sorted_data.plot(x='Date', y='Close')
plt.xticks(rotation=95)
plt.title('Close Price history')
plt.ylabel('Price')
plt.show()

def convert_string_to_float(s):
    try:
        # Remove any commas from the string
        s = str(s)  # Convert to string if it's not already
        s = s.replace(",", "")
        # Convert the string to a float
        return float(s)
    except ValueError:
        return None
for col in df.columns:
  df[col] = df[col].apply(convert_string_to_float)

model = RandomForestRegressor()

X = df[["Open",'High','Low','Volume']]
# Keep the last rows for test
X = X[:int(len(df)-2)]

# Target would be the close price of tomorrow ( next day data)
y = df['Close'].shift(-1)
y = y[:int(len(df)-2)]

model.fit(X,y)

print('model score',model.score(X,y))

# test data, unseen data, the last two rows of data ( second two last rows).
new_data = df[["Open",'High','Low','Volume']].tail(2)[0:1]
prediction = model.predict(new_data)
print('model predicted close price ', prediction)
print('Actual close Price', df[['Close']].tail(1).values[0][0])

