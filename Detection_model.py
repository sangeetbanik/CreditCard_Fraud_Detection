#Import all necessary libraries

import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.preprocessing import StandardScaler
import seaborn as sns 
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from urllib.request import DataHandler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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

# Merging the new features to main dataset
df = pd.merge(df,transaction_history, how='outer', on='credit_card')

# Defining DataHandler class
class DataHandler:
    def __init__(self, file_path):
        self.file_path = file_path
   
    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        print("Data loaded successfully.")
        return self.data

# Defining FeatureEngineer Class
class FeatureEngineer:
    def __init__(self, data):
        self.data = data

    def create_features(self):
        # Create derived features
        self.data['deviation_from_avg'] = self.data['transaction_dollar_amount'] - \
        self.data.groupby('credit_card')['transaction_dollar_amount'].transform('mean')
        self.data['transaction_frequency'] = self.data.groupby('credit_card')['transaction_count'].transform('sum')
        print("Feature engineering complete.")
        return self.data

# Defining FraudDetectionModel Class
class FraudDetectionModel:
    def __init__(self, data):
        self.data = data
        self.model = None

    def train_model(self, X):
        # Training Isolation Forest for anomaly detection
        self.model = IsolationForest(contamination=0.05)  # Assuming 5% fraud cases
        self.model.fit(X)
        print("Model trained successfully.")

    def predict(self, X):
        # Predicting anomalies (fraudulent transactions are labeled as -1)
        return self.model.predict(X)

# Defining InsightsGenerator Class
class InsightsGenerator:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def generate_insights(self):
        self.data['fraud_prediction'] = (self.model.predict(self.data.drop(['credit_card'], axis=1)) > 0.5).astype(int)
        fraud_cases = self.data[self.data['fraud_prediction'] == 1]
        print(f"Detected {len(fraud_cases)} potential fraud cases.")
        return fraud_cases

# Defining Pipeline Class
class Pipeline:
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self):
        # Step 1: Load data
        data_handler = DataHandler(self.file_path)
        data = data_handler.load_data()
        #data = data_handler.preprocess_data()

        # Step 2: Feature Engineering
        feature_engineer = FeatureEngineer(data)
        data = feature_engineer.create_features()

        # Step 3: Train Neural Network
        model_trainer = FraudDetectionModel(data)
        features = data.drop(['credit_card','date','time'], axis=1).columns
        #model_trainer.build_model(len(features))
        model_trainer.train_model(data[features])

        # Step 4: Predict anomalies
        data['fraud_prediction'] = model_trainer.predict(data[features])  # Use model to predict fraud
        fraud_cases = data[data['fraud_prediction'] == -1]
        print(f"Detected {len(fraud_cases)} potential fraud cases.")

        return fraud_cases,data

# Checking the model
pipeline  = Pipeline(file_path= "working_dataset.csv")
fraud_cases,data = pipeline.run()

## Visualising the predicted data
# Applying PCA to reduce the dimensions of the features to 2D
pca = PCA(n_components=2)
pca_features = pca.fit_transform(data.drop(['fraud_prediction', 'credit_card','date','time'], axis=1))

# Visualize the results in 2D
plt.figure(figsize=(10, 6))
plt.scatter(pca_features[:, 0], pca_features[:, 1], c=data['fraud_prediction'], cmap='coolwarm', alpha=0.7)
plt.title('Fraud Detection in PCA-Reduced Feature Space')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Fraud Prediction (-1: Fraud, 1: Normal)')
plt.show()

# Visualize the results in Histogram plot
fraud_cases = data[data['fraud_prediction'] == -1]
normal_cases = data[data['fraud_prediction'] == 1]


plt.figure(figsize=(10, 6))
sns.histplot(fraud_cases['transaction_dollar_amount'], color='red', label='Fraud', kde=True)
sns.histplot(normal_cases['transaction_dollar_amount'], color='blue', label='Normal', kde=True)
plt.title('Transaction Amount Distribution')
plt.xlabel('Transaction Amount')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Visualize the results in Box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x=data['fraud_prediction'], y=data['transaction_dollar_amount'], palette="coolwarm", hue=data['fraud_prediction'])
plt.title('Box Plot of Transaction Amounts by Fraud Detection')
plt.xlabel('Fraud Prediction (-1: Fraud, 1: Normal)')
plt.ylabel('Transaction Amount')
plt.show()


accuracy = accuracy_score(true_labels, data['fraud_prediction'])
precision = precision_score(true_labels, data['fraud_prediction'], pos_label=-1)  # Assuming -1 is the fraud label
recall = recall_score(true_labels, data['fraud_prediction'], pos_label=-1)
f1 = f1_score(true_labels, data['fraud_prediction'], pos_label=-1)

# Print the results
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

