# Credit Card Fraud Detection Project

## 📝 Introduction 
A fictional credit card company, Company ABC, is struggling with their current fraud detection system. In this project, I am working as a financial analyst, whom the company hired to spot and flag suspicious transactions for further review. I will follow various data analysis process like:<ins> data cleaning, data preprocessing, handling imbalanced data and model training and evaluation</ins>.

## 💬 Background
Company ABC, a fictional company credit cards, is struggling with their current fraud detection system. It faces challenges with their existing fraud detection system and is slow to catch new fraud patterns, which has been costing them a lot of money. To fix this, they've hired us to create an algorithm that can quickly spot and flag suspicious transactions for further review. They've given us two datasets to work with: cc_info, which has general info about credit cards and their users, and transactions, which includes details of all credit card transactions made between August 1st and October 30th.

## ⚙ Approach/Steps
**Business Task -**
The goal of this project is to create a smart fraud detection system using neural networks to spot unusual or suspicious transactions. We’ll use object-oriented programming (OOP) to build a solution that's scalable, easy to manage, and capable of handling large amounts of data while giving useful insights to Company ABC.

**Data Sets -**
We have two files in our datasets , **cc_info.csv** and **transactions.csv**, which are described below:-

Here is the column description for *cc_info.csv*<br>
|  **Variable**       |  **Description**                                                             |
|------------------   | -----------------------------------------------------------------------------|
| credit_cad          | Unique identifier for each transaction.                                      |
| city                | The city where the transaction occurred                                      |
| state               | The state or region where the transaction occurred                           |
| zipcode             | The postal code of the transaction location                                  |
| credit_card_limit   | The credit limit associated with the credit card used in the transaction     |

Here is the column description for *transactions.csv*<br>
|  **Variable**             |  **Description**                                                             |
|-----------------------    | -----------------------------------------------------------------------------|
| credit_cad                | Unique identifier for each transaction.                                      |
| date                      | The date of the transaction (between August 1st and October 30th)            |
| transaction_dollar_amount | The dollar amount of the transaction                                         |
| Long                      | The longitude coordinate of the transaction location                         |
| Lat                       | The latitude coordinate of the transaction location                          |

**Data Pre-processing**<br>
- Data Wrangling : all the modifications were done to the *transaction.csv* file, later which was used in developing the detection algorithm.
    - added a new column, **card_limit**, using vlookup function in excel.
    - removed two columns, **Long** and **Lat**, as they were not required for our detection model.
    - new columns such as, **year**,**month**, **day** and **day_of_week**, are created from the **date** column on Python.
    - several other columns, such as, **total_transaction, avg_transaction,	max_transaction,	min_transaction,	transaction_count,	total_over_limit,	avg_transaction_to_limit_ratio and total_transaction_to_limit_ratio**, are created on Python.   

## 🛠️ Plan of the Fraud Detection System
The system will:
- Ingest large volumes of transaction data.
- Train a neural network for fraud detection.
- Provide predictions and insights efficiently.

## ✏️ Design of the System Using OOP Concepts
OOP principles such as encapsulation, abstraction, inheritance, and polymorphism will make the solution modular and scalable.

**Classes that are Included:**
- *DataHandler*: For data ingestion, and cleaning.
- *FeatureEngineer*: For creating new features and aggregating existing ones.
- *FraudDetectionModel*: For building, training, and evaluating the neural network.
- *InsightsGenerator*: For analyzing results and generating insights.
- *Pipeline*: A class to orchestrate the workflow.

## 🖥️ Implementation
Since, fraud detection is a supervised learning problem, we need labels to train a model effectively. But the dataset we used doesn't have any labels indicating fraud status (e.g., is_fraud). So, we used **Unsupervised anomaly detection techniques** to identify anomalies.

We used **Isolation Forest** to identify unusual patterns that may indicate fraud.
- The model has flagged data points with -1 as anomalies (potential fraud).

Fraud detection model :  [CODE](https://github.com/sangeetbanik/CreditCard_Fraud_Detection/blob/main/Detection_model.py)

## 🔮 Conclusion
The model depicts that the dataset contains **14730 potential fraud cases.**

- Insights from Histogram plot
    - High transaction amounts (closer to 1000) are more likely to indicate fraud due to the observed peak in fraudulent transactions in that range.
  
![output](https://github.com/user-attachments/assets/0ee3a5c6-eef7-46ca-ac8e-3468e828e7d7)

- Insights from Box plot
    - The median transaction amount for fraudulent predictions is roughly 200.
    - The median transaction amount for normal predictions is much lower (closer to 50).
![output1](https://github.com/user-attachments/assets/b43423ce-1aeb-445e-9877-a175db7840c2)

- Insights from Scatter plot
    - The presence of overlap between fraudulent and normal points suggests that the model might need additional feature engineering or refinement to better distinguish between these categories.
    - The sparsely distributed fraudulent transactions and the compact normal transactions imply that fraud cases are less frequent but more varied in nature.

  ![output2](https://github.com/user-attachments/assets/a180f36c-7234-4a44-90b2-4e2600b1647c)


  

