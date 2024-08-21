# -*- coding: utf-8 -*-
"""stock_price_predict.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l2T5Aslq-3TxB1UJI9l_e-NUO-ioevqs
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel('./Top_performer_NL.xlsx')
df.columns = df.iloc[0]
df = df[1:]
df.head()

def convert_string_to_float(s):
    try:
        # Remove any commas from the string
        s = str(s)  # Convert to string if it's not already
        s = s.replace(",", "")
        # Convert the string to a float
        return float(s)
    except ValueError:
        return None

# Apply the function to the entire column
df['%'] = df['%'].apply(convert_string_to_float)
df['Last'] = df['Last'].apply(convert_string_to_float)
df['Turnover'] = df['Turnover'].apply(convert_string_to_float)
df['Volume'] = df['Volume'].apply(convert_string_to_float)

plt.figure(figsize=(15,5))
plt.plot(df['Last'])
plt.title('Market Close price.', fontsize=15)
plt.ylabel('Price in euro.')
plt.show()

# check whether data in the ‘Close’ column and that available in the ‘Adj Close’ column is the same with each row or not
#df[df['Close'] == df['Adj Close']].shape
#df = df.drop(['Adj Close'], axis=1)

# check for null values
df.isnull().sum()

df.dropna(inplace=True)

# visualise features
features = ['Turnover', 'Last', 'Volume', '%']

plt.subplots(figsize=(20,10))

for i, col in enumerate(features):
  plt.subplot(2,3,i+1)
  sb.distplot(df[col])
plt.show()

# from these boxplots we can see if there are any outliers
plt.subplots(figsize=(20,10))
for i, col in enumerate(features):
  plt.subplot(2,3,i+1)
  sb.boxplot(df[col])
plt.show()

# feature Engineering
# quarterly results affect the stock prices heavily
# splitted = df['Date'].str.split('/', expand=True)

# df['day'] = splitted[1].astype('int')
# df['month'] = splitted[0].astype('int')
# df['year'] = splitted[2].astype('int')

# df['is_quarter_end'] = np.where(df['month']%3==0,1,0)

# df['open-close'] = df['Open'] - df['Close']
# df['low-high'] = df['Low'] - df['High']
# target feature is a signal whether to buy or not
df['target'] = np.where(df['Last'].shift(-1) > df['Last'], 1, 0)

df.head()

# data_grouped = df.groupby('year').mean()
# plt.subplots(figsize=(20,10))

# for i, col in enumerate(['Last', 'Volume', '%', 'Turnover']):
#   plt.subplot(2,2,i+1)
#   data_grouped[col].plot.bar()
# plt.show()

# Check whether Prices are higher in the months which are quarter end as compared to that of the non-quarter end months.
# Check the volume of trades in the months which are quarter end.
#df.groupby('is_quarter_end').mean()

plt.pie(df['target'].value_counts().values,
		labels=[0, 1], autopct='%1.1f%%')
plt.show()

df_feat = df[['%', 'Volume','Turnover','Last']]
plt.figure(figsize=(10, 10))

# As our concern is with the highly correlated features only so, we will visualize our heatmap as per that criteria only.
sb.heatmap(df_feat.corr() > 0.9, annot=True, cbar=False)
plt.show()

# Data splitting and Normalization
features = df[['Volume', 'Turnover', '%']]
target = df['target']

scaler = StandardScaler()
features = scaler.fit_transform(features)

X_train, X_valid, Y_train, Y_valid = train_test_split(
	features, target, test_size=0.1, random_state=2022)
print(X_train.shape, X_valid.shape)

# Model development and Evaluation
#  instead of predicting the hard probability that is 0 or 1 we would like it to predict soft probabilities that are continuous values between 0 to 1.
# And with soft probabilities, the ROC-AUC curve is generally used
models = [LogisticRegression(), SVC(
kernel='poly', probability=True), XGBClassifier()]

for i in range(3):
  models[i].fit(X_train, Y_train)

print(f'{models[i]} : ')
print('Training Accuracy : ', metrics.roc_auc_score(
	Y_train, models[i].predict_proba(X_train)[:,1]))
print('Validation Accuracy : ', metrics.roc_auc_score(
	Y_valid, models[i].predict_proba(X_valid)[:,1]))
print()

ConfusionMatrixDisplay.from_estimator(models[0], X_valid, Y_valid)
plt.show()