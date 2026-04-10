# 9. PairPlot - plot pairwise relationships in a dataset

import seaborn as sns
import matplotlib.pyplot as plt

ds = sns.load_dataset('car_crashes')
plt.figure(figsize=(10,6))
sns.pairplot(ds) 
plt.grid(True)
plt.title('PairPlot on Car Crash Dataset')
plt.tight_layout()
plt.show()
