naive_bayes.py

import pandas as pd
from os.path import join
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB

saved_data_path = '/Users/Tomo/thinkful/'
df  = pd.read_csv(join(saved_data_path,'ideal_weight.csv'), names=['id', 'sex', 'actual', 'ideal', 'diff'], header=0)
df['sex'] = df['sex'].map(lambda x: x.replace("'",""))


plt.figure()
plt.hist([df['actual'], df['ideal']], histtype='bar', stacked=False)
plt.show()

# Convert into categorical variable
df['gender'] = df['sex'].astype('category')


gnb = GaussianNB()
data = df[['actual','ideal','diff']]
target = df['gender']
model = gnb.fit(data, target)
y_pred = model.predict(data)
print("Number of mislabeled points out of a total %d points: %d" %(data.shape[0], (target != y_pred).sum()))

# Number of mislabeled points out of a total 182 points: 14

# Predict the sex for an actual weight of 145, an ideal weight of 160, and a diff of -15." 

d1 = {'actual': 145, 'ideal': 160, 'diff': -15}
df = pd.DataFrame(data=d1, index=[1])
df = df[['actual','ideal', 'diff']]
pred = model.predict(df)
print(pred) # Male


# Predict the sex for an actual weight of 160, an ideal weight of 145, and a diff of 15.
d2 = {'actual': 160, 'ideal': 145, 'diff': 15}
df = pd.DataFrame(data=d2, index=[1])
df = df[['actual','ideal', 'diff']]
pred = model.predict(df)
print(pred) # Female












