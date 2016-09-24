linear_regression.py

import pandas as pd
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

loansData['Interest.Rate'][0:5]
loansData['Loan.Length'][0:5]
loansData['FICO.Range'][0:5]


#cleaning up the columns
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))
#loansData[‘FICO.Score’] = [str(x) for x in loansData[‘FICO.Range’]] # another way


loansData['FICO.Score'] = loansData['FICO.Range']
print loansData['FICO.Score'][0:5]

loansData['FICO.Score'] = loansData['FICO.Range'].map(lambda x: (x.split('-')))
loansData['FICO.Score'] = loansData['FICO.Score'].map(lambda x: int(x[0]))

type(FICO.Score[0:5].values[0])
# > list
type(FICO.Score[0:5].values[0][0])
# > int

loansData['FICO.Score'] = FICO

#######
A =loansData['FICO.Score'].tolist()
for j in range(len(A)):   
		#for j in between 0 to len(A)
  B = A[j].split("-")
        #split each sub-array on - and save it to B
  C = float(B[0])           
  		#convert the string to int, using only the first value
  FICO.append(C)          
  		#append each C to the empty array, using first value
loansData['FICO.Score']=FICO
#######


import matplotlib.pyplot as plt
# Create a scatterplot matrix
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10))
plt.show()

# Plots on the diagonal showing histogram for each variable
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()


import numpy as np
import pandas as pd
import statsmodels.api as sm

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

# The dependent variable
y = np.matrix(intrate).transpose()
# The independent variables shaped as columns
x1 = np.matrix(fico).transpose()
x2 = np.matrix(loanamt).transpose()
# Put the two columns together to create an input matrix 
x = np.column_stack([x1,x2])

# Create a linear model
X = sm.add_constant(x)
model = sm.OLS(y,X)
f = model.fit()

f.summary()




