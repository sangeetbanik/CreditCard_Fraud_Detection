#Import all necessary libraries

import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.preprocessing import StandardScaler
import seaborn as sns 
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Dropout # type: ignore
from sklearn.metrics import classification_report
from urllib.request import DataHandler

print('Import successful')

#Importing dataset for wrangling
df = pd.read_csv("transactions.csv")

#creating a new feature : year, month, day, day_of_week and transaction_history
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date
df['date'] = pd.to_datetime(df['date']) 
df['year'] = df['date'].dt.year         # Extract year
df['month'] = df['date'].dt.month       # Extract month
df['day'] = df['date'].dt.day           # Extract day
df['day_of_week'] = df['date'].dt.dayofweek  # Extract day of the week


transaction_history = df.groupby('credit_card').agg(
    total_transaction = ('transaction_dollar_amount', 'sum'),
    avg_transaction = ('transaction_dollar_amount', 'mean'),
    max_transaction = ('transaction_dollar_amount','max'),
    min_transaction = ('transaction_dollar_amount','min'),
    transaction_count = ('transaction_dollar_amount', 'count'),
    total_over_limit=('transaction_dollar_amount', lambda x: (x > df.loc[x.index, 'card_limit']).sum())).reset_index()

# Calculate Transaction Amount-to-Limit Ratio for each user
transaction_history['avg_transaction_to_limit_ratio'] = transaction_history['avg_transaction'] / df['card_limit'].mean()
transaction_history['total_transaction_to_limit_ratio'] = transaction_history['total_transaction'] / df['card_limit'].mean()

#Merging the new features to main dataset
df = pd.merge(df,transaction_history, how='outer', on='credit_card')

#





