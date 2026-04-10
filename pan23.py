# statistical summary of dataframe using describe() function
# std(), min(), max() - function on dataframe

from pandas import DataFrame
   
states = { 'State' : ['Gujarat', 'Tamil Nadu', 'Andhra', 'Karnataka', 'Kerala','Punjab'],\
           'Population' : [36, 44, 67, 89, 30, 34],\
           'Language' : ['Gujarati', 'Tamil', 'Telugu', 'Kannada', 'Malayalam','Punjabi'],\
           'Food' : ['Dhokla', 'Idli', 'Biryani', 'Bisi Bele Bath', 'Appam', 'Sarson da Saag'],\
           'Literacy' : [86.6, 80.3, 67.4, 75.4, 93.9, 76.2],\
           'Capital' : ['Gandhinagar', 'Chennai', 'Amaravati', 'Bengaluru', 'Thiruvananthapuram', 'Chandigarh']
         } 

df = DataFrame(states)
print('--- complete DF ---')
print(df)
print('--- std Function ---') # include only numeric column
print(df['population'].std())
print(df['literacy'].std())
print('--- min Function ---') # include only numeric column
print(df['population'].min())
print(df['literacy'].min())
print('--- max Function ---') # include only numeric column
print(df['population'].max())
print(df['literacy'].max())
print('--- median function ---') # include only numeric column
print(df['population'].median) # 44.0
print(df['literacy'].median)  # 76.2
print('--- Mode Function ---') # includes only numeric columns - most frequently occuring value
print(df['population'].mode())
print(df['literacy'].mode())



