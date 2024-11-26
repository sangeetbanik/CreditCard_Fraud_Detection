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

-- Importing dataset for wrangling
df = pd.read_csv(r"C:\Users\Pratik Banik\Downloads\UM_Projects\Project_4_CreditCardFraud\transactions.csv")

df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date
df['date'] = pd.to_datetime(df['date']) 
df['year'] = df['date'].dt.year         # Extract year
df['month'] = df['date'].dt.month       # Extract month
df['day'] = df['date'].dt.day           # Extract day
df['day_of_week'] = df['date'].dt.dayofweek  # Extract day of the week

