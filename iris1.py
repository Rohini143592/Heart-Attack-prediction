# Case Study 1 : Supervised Machine Learning
# Iris Flower Prediction of Class - Setosa, Virginica, Versicolor

import pandas as pd
import matplotlib.pyplot as plt

cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

# 1. Read the dataset
df = pd.read_csv("iris.csv",names=cols) # when the dataset is without header or headless dataset

# 2. Understanding Dataset
print('--- No of Rows and Columns ---')
print(df.shape) # no or rows and columns (600,5)
print('--- Column Names ---')
print(df.columns) # columns of dataframe
print('--- Data Types ---')
print(df.dtypes) # data types of each column
print('--- All Information ---')
print(df.info()) # all information about the dataframe

# 3. Display some rows or records from the dataset
print('--- First 5 Rows ---')
print(df.head())
print('--- Last 5 Rows ---')
print(df.tail())

# 4. Statistical Summary
print('--- Statistical Summary ---')
print(df.describe()) # statistical summary of numerical columns

# 5. Find Missing Values
print('--- Find Missing Values ---')
print(df.isnull().sum()) # find missing values in each column

# 6. Data Visualization - Univariable - single variable
print('--- Count of each class ---')
print(df['class'].value_counts()) # counts total in each class
data = df['class'].value_counts().tolist()

# Distribution of each class - Distribulation Analsys
label = ['Setosa', 'Versicolor', 'Virginica']
colors = ['red', 'green', 'blue']
print(data) # [200,200,200]
plt.title('Distribution of Iris Classes')
plt.xlabel('Class')
plt.ylabel('Count')
plt.grid(True)
plt.bar(label,data,color=colors)
plt.show()

