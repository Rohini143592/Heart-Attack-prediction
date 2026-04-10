# Case Study 1 : Supervised Machine Learning
# Iris Flower Prediction of Class - Setosa, Virginica, Versicolor

from tkinter.font import names
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

class IrisProject:
    def __init__(self):
        print("Iris Project Initialized")
        # 1. Read the dataset
        self.df = pd.read_csv("iris.csv", names=cols)  # when the dataset is without header or headless dataset

    def understandDataset(self):
        # 2. Understanding Dataset
        print('--- No of Rows and Columns ---')
        print(self.df.shape)  # no or rows and columns (600,5) shape is a property
        print('--- Column Names ---')
        print(self.df.columns)  # columns of dataframe
        print('--- Data Types ---')
        print(self.df.dtypes)  # data types of each column
        print('--- All Information of Iris Dataset ---')
        print(self.df.info())  # all information about the dataframe - info is a function

    def displayRows(self):
        # 3. Display some rows or records from the dataset
        print('--- First 5 Rows ---')
        print(self.df.head())  # first 5 rows
        print('--- Last 5 Rows ---')
        print(self.df.tail())  # last 5 rows
        print('--- Random 5 Rows ---')
        print(self.df.sample(5))  # random 5 rows - sample function is used to get random rows

    def statisticalSummary(self):
        # 4. Statistical Summary
        print('--- Statistical Summary ---')
        print(self.df.describe())  # statistical summary of numerical columns

    def findMissingValues(self):
        # 5. Find Missing Values
        print('--- Find Missing Values ---')
        print(self.df.isnull().sum())  # find missing values in each column

    def dataVisualization(self):
        # 6. Data Visualization - Univariable - single variable
        print('--- Count of each class ---')
        print(self.df['class'].value_counts())  # counts total in each class
        data = self.df['class'].value_counts().tolist()

        # Distribution of each class - Distribulation Analsys
        label = ['Setosa', 'Versicolor', 'Virginica']
        colors = ['red', 'green', 'blue']
        print(data)  # [200,200,200]
        plt.title('Distribution of Iris Classes')
        plt.xlabel('Class')
        plt.ylabel('Count')
        plt.grid(True)
        plt.bar(label, data, color=colors)
        plt.show()

        # Univariate Analysis - Box Plot
        self.df.plot(kind='box', subplots=True, layout=(2, 2), title='Box Plot for each attribute', grid=True)
        plt.show()

        # histogram
        self.df.hist()
        plt.show()

        # Multivariate Analysis - Bivariate Analysis
        sns.pairplot(self.df, hue='class', markers='o') # symbol + * ^ s o
        plt.show()

        plt.figure(figsize=(15,10))    
        plt.title('Box Plot for each attribute')
        plt.subplot(2,2,1)
        sns.boxplot(x='class',y='sepal_length',data=self.df)
        plt.subplot(2,2,2)
        sns.boxplot(x='class',y='sepal_width',data=self.df)
        plt.subplot(2,2,3)
        sns.boxplot(x='class',y='petal_length',data=self.df)
        plt.subplot(2,2,4)
        sns.boxplot(x='class',y='petal_width',data=self.df)
        plt.tight_layout()
        plt.show()

    def splitDataSet(self):
        # Begining of AL with Machine Learning
        # 7. Creating X and y variable and Training Set and Testing set
        array = self.df.values # converting the entire dataset(DataFrame) into numpy array
        X = array[:,0:4]  # 0 1 2 3 input variables sl(0), sw(1), pl(2), pw(3)
        y = array[:,4]    # output variable class
        print(X) # input variables sl, sw, pl, pw
        print(y) # output variable class
        # 0.20 specifies the testing set as 20%
        # random_state is the seed value, it can be any integer but common is 1 or 42
        # Training set is 80% and testing set 20%
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, y, \
                                    test_size=0.20, random_state=1)
        # X_train - 80% training input sl, sw, pl, pw (total record 480)
        # X_test - 20% testing input sl, sw, pl, pw (total record 120)
        # Y_train - 80% training output class (total record 480)
        # Y_test - 20% testing output class (total record 120)  

    def modelTraining(self):
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
        self.results = []  # create an empty list to store results of the algo.
        self.names = []    # create an empty list to stores names of the algo.

        for name, model in models: # the loop runs 5 times for 5 algo.
            model.fit(self.X_train, self.Y_train) # train the model with training data
            pred = model.predict(self.X_test) # predict the output using testing input
            acc = accuracy_score(self.Y_test, pred) # compare the predicted output with actual output
            acc = round(acc * 100,2)
            print(name,' : ', acc, '%') # accuracy in percentage 98.45 %
            self.results.append(acc) # add the accuracy result to results list
            self.names.append(name) # add the name of the algo to names list 

    def compareAlgorithms(self):    
        # 9. Compare the results of all algo.
        plt.figure(figsize=(10,5))
        plt.grid(True)
        sns.set_style('darkgrid')
        # adding values to each bar
        for i in range(len(self.names)):
            plt.text(i,self.results[i],self.results[i], ha = 'center', fontsize=12, color='black')
        plt.title('Algorithm Comparison')
        plt.xlabel('Algorithm')
        plt.ylabel('Accuracy')
        plt.bar(self.names,self.results)
        plt.show()

    def printConfusionMatrix(self):
        models = []
        models.append(('LR', LogisticRegression()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('DT', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))
        # add up to 10 models if needed

        fig, axes = plt.subplots(2, 5, figsize=(25, 10))  # 2 rows × 5 columns
        axes = axes.ravel()  # flatten into 1D array of Axes objects

        for i, (name, model) in enumerate(models):
            model.fit(self.X_train, self.Y_train)
            pred = model.predict(self.X_test)

            acc = accuracy_score(self.Y_test, pred)
            acc = round(acc * 100, 2)

            print('---', name, '---')
            print('Accuracy : ', acc, '%')
            print(confusion_matrix(self.Y_test, pred))
            print(classification_report(self.Y_test, pred))

            # ✅ Pass a single axis object, not the whole array
            sns.heatmap(
                confusion_matrix(self.Y_test, pred),
                annot=True, fmt='d', cmap='Blues', ax=axes[i]
            )
            axes[i].set_title(f'{name}\nAcc: {acc}%')
            axes[i].set_xlabel('Predicted')
            axes[i].set_ylabel('Actual')

        # Hide unused subplots if < 10 models
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()

    def saveModelAndPredictOutput(self):
        # 11. Save the model for future use - Model Persistence
        import joblib # to save the model
        model = LogisticRegression() # create the model 
        model.fit(self.X_train, self.Y_train) # train the model
        # save the model to disk
        joblib.dump(model, 'iris_model.pkl')
        # load the model from disk
        loaded_model = joblib.load('iris_model.pkl')
        # predict the output using testing input
        data = [[7.9,3.8,6.4,2.0]] # single record
        #data = [[5.1,3.5,1.4,0.2]] # single record
        pred = loaded_model.predict(data)
        print('Predicted Value : ', pred) # predicted output

    def runPipeline(self):
        self.understandDataset()
        self.displayRows()
        self.statisticalSummary()
        self.findMissingValues()
        self.dataVisualization()
        self.splitDataSet()
        self.modelTraining()
        self.compareAlgorithms()
        self.printConfusionMatrix()       
        self.saveModelAndPredictOutput()

# End of class
obj = IrisProject()
obj.runPipeline()
