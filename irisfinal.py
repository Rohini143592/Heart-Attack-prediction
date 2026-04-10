# Case Study 1 : Supervised Machine Learning
# Iris Flower Prediction of Class - Setosa, Virginica, Versicolor

from matplotlib import cm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# sklearn is machine learning library and contains all function for ML
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression # ML Method
from sklearn.tree import DecisionTreeClassifier # Decision Tree
from sklearn.neighbors import KNeighborsClassifier # K Nearest Neighbors
from sklearn.naive_bayes import GaussianNB # Naive Bayes
from sklearn.svm import SVC # Support Vector Classifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

# 1. Read the dataset
df = pd.read_csv("iris.csv",names=cols) # when the dataset is without header or headless dataset

# 2. Understanding Dataset
print('--- No of Rows and Columns ---')
print(df.shape) # no or rows and columns (600,5) shape is a property
print('--- Column Names ---')
print(df.columns) # columns of dataframe
print('--- Data Types ---')
print(df.dtypes) # data types of each column
print('--- All Information of Iris Dataset ---')
print(df.info()) # all information about the dataframe - info is a function

# 3. Display some rows or records from the dataset
print('--- First 5 Rows ---')
print(df.head()) # first 5 rows
print('--- Last 5 Rows ---')
print(df.tail()) # last 5 rows
print('--- Random 5 Rows ---')
print(df.sample(5)) # random 5 rows - sample function is used to get random rows

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

# Univariate Analysis - Box Plot
df.plot(kind='box',subplots=True,layout=(2,2),title='Box Plot for each attribute',grid=True)
plt.show()

# histogram
df.hist()
plt.show()

# Multivariate Analysis - Bivariate Analysis
sns.pairplot(df, hue='class', markers='o') # symbol + * ^ s o
plt.show()

plt.figure(figsize=(15,10))    
plt.title('Box Plot for each attribute')
plt.subplot(2,2,1)
sns.boxplot(x='class',y='sepal_length',data=df)
plt.subplot(2,2,2)
sns.boxplot(x='class',y='sepal_width',data=df)
plt.subplot(2,2,3)
sns.boxplot(x='class',y='petal_length',data=df)
plt.subplot(2,2,4)
sns.boxplot(x='class',y='petal_width',data=df)
plt.tight_layout()
plt.show()

# Begining of AL with Machine Learning
# 7. Creating X and y variable and Training Set and Testing set
array = df.values # converting the entire dataset(DataFrame) into numpy array
X = array[:,0:4]  # 0 1 2 3 input variables sl(0), sw(1), pl(2), pw(3)
y = array[:,4]    # output variable class
print(X) # input variables sl, sw, pl, pw
print(y) # output variable class
# 0.20 specifies the testing set as 20%
# random_state is the seed value, it can be any integer but common is 1 or 42
# Training set is 80% and testing set 20%
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state=1)
# X_train - 80% training input sl, sw, pl, pw (total record 480)
# X_test - 20% testing input sl, sw, pl, pw (total record 120)
# Y_train - 80% training output class (total record 480)
# Y_test - 20% testing output class (total record 120)  

# 8. Model Training
# Logistic Regression, Decision Tree, SVM, KNN, Naive Bayes
models = [] # create an empty list called models

models.append(('LR', LogisticRegression()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('DT', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))

print(models) # print the models list - list of tuples and each tuple contains name and algo. 
# models list would be created with 5 algorithm functions
results = []  # create an empty list to store results of the algo.
names = []    # create an empty list to stores names of the algo.

for name, model in models: # the loop runs 5 times for 5 algo.
    model.fit(X_train, Y_train) # train the model with training data
    pred = model.predict(X_test) # predict the output using testing input
    acc = accuracy_score(Y_test, pred) # compare the predicted output with actual output
    acc = round(acc * 100,2)
    print(name,' : ', acc, '%') # accuracy in percentage 98.45 %
    results.append(acc) # add the accuracy result to results list
    names.append(name) # add the name of the algo to names list 

# 9. Compare the results of all algo.
plt.figure(figsize=(10,5))
plt.grid(True)
sns.set_style('darkgrid')
# adding values to each bar
for i in range(len(names)):
    plt.text(i,results[i],results[i], ha = 'center', fontsize=12, color='black')
plt.title('Algorithm Comparison')
plt.xlabel('Algorithm')
plt.ylabel('Accuracy')
plt.bar(names,results)
plt.show()   

# 10. Detailed accuracy report of each model including confusion matrix
for name, model in models: # the loop runs 5 times for 5 algo.
    model.fit(X_train, Y_train) # train the model with training data
    pred = model.predict(X_test) # predict the output using testing input
    acc = accuracy_score(Y_test, pred) # compare the predicted output with actual output
    acc = round(acc * 100,2)
    print('---',name,'---')
    print('Accuracy : ', acc, '%') # accuracy in percentage 98.45 %
    print(confusion_matrix(Y_test, pred)) # confusion matrix
    print(classification_report(Y_test, pred)) # precision, recall, f1-score, support
    # print('--- Confusion matrix graphs for each model ---')
    plt.figure(figsize=(10,5))
    sns.heatmap(confusion_matrix(Y_test, pred), annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix - ' + name)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()   

   
# 11. Save the model for future use - Model Persistence
model = LogisticRegression() # create the model 
model.fit(X_train, Y_train) # train the model
# save the model to disk
joblib.dump(model, 'iris_model.pkl')

# 12. Load the model and predict the output
# load the model from disk
loaded_model = joblib.load('iris_model.pkl')
# predict the output using testing input
data = [[7.9,3.8,6.4,2.0]] # single record
pred = loaded_model.predict(data)
print('Predicted Value : ', pred) # predicted output
