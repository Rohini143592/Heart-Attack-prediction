# Reading data from data file into the DataFrame .csv


import pandas as pd

df = pd.read_csv('student.csv')
print('--- complete DF ---')
print(df)
print('--- shape ---')
print(df.shape) # no of row and column
print('--- columns ---')
print(df.columns)
print('--- Data Types ---')
print(df.dtypes)
print('--- Head ---')
print(df.head(2))
print('--- Tail ---')
print(df.tail(2))
print('--- statistical summary ---')
print(df.describe()) # works on numeric columns