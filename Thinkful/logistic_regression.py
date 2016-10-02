logistic_regression.py

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

##### Same as before we did for linear regression

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

#print the first 5 rows of each of the column to see what needs to be cleaned
print loansData['Interest.Rate'][0:5]
print loansData['Loan.Length'][0:5]
print loansData['FICO.Range'][0:5]

#cleaning up the columns
loansData['Interest.Rate'] = loansData['Interest.Rate'].map(lambda x: x.rstrip('%'))
loansData['Interest.Rate'] = loansData['Interest.Rate'].astype(float)
loansData['Loan.Length'] = loansData['Loan.Length'].map(lambda x: x.rstrip('months'))

'''convert the data in FICO.Range into string and split the string and take the lowest value'''
loansData['FICO.Score'] = loansData['FICO.Range']
print loansData['FICO.Score'][0:5]
A =loansData['FICO.Score'].tolist()
FICO=[] #declare an empty array
for j in range(len(A)):   
  B = A[j].split("-")    
  C = float(B[0])           
  FICO.append(C)        
loansData['FICO.Score']=FICO


### logistical part

ir = loansData['Interest.Rate']
ir = [1 if x < 12 else 0 for x in ir]
loansData['IR_TF'] = ir

df[df['Interest.Rate'] == 10].head() # should all be True
df[df['Interest.Rate'] == 13].head() # should all be False


# constant intercept of 1.0
intercept = [1] * len(loansData)
loansData['Intercept'] = intercept

# independant variables
ind_vars = ['Intercept', 'Amount.Requested', 'FICO.Score']

# define logistic model
X = loansData[ind_vars]
y = loansData['IR_TF']
logit = sm.Logit(y,X)

# fit the model
result = logit.fit() #to be asked

# Get the fitted coefficients from the results
coeff = result.params
print(coeff)

import math
from math import * 

# take a FICO Score and a Loan Amount of this linear predictor, and return p
def logistic_function(FicoScore, LoanAmount,coeff):
    """ p(x) = 1/(1 + e^(intercept + 0.087423(FicoScore) − 0.000174(LoanAmount)) """
    prob = 1/(1+exp(coeff[0]+coeff[2]*FicoScore+coeff[1]*LoanAmount))
    if prob > 0.7:
        p = 1
    else:
        p = 0
    return prob, p



# Determine the probability that we can obtain a loan at ≤12% Interest for $10,000 with a FICO score of 720
prob = logistic_function(720, 10000,coeff)[0]
print(prob)
# >> 0.25362141104848657
# predict we won't obtain the loan.


## plotting: lets test different FICO score for 10,000 USD loan
Fico = range(550, 950, 10)
p_plus = []
p_minus = []
p = []
for j in Fico:
    p_plus.append(1/(1+exp(coeff[0]+coeff[2]*j+coeff[1]*10000)))
    p_minus.append(1/(1+exp(-coeff[0]-coeff[2]*j-coeff[1]*10000)))
    p.append(logistic_function(j, 10000,coeff)[1])




plt.plot(Fico, p_plus, label = 'p(x) = 1/(1+exp(b+mx))', color = 'blue')
plt.hold(True)
plt.plot(Fico, p_minus, label = 'p(x) = 1/(1+exp(-b-mx))', color = 'green')    
plt.hold(True)
plt.plot(Fico, p, 'ro', label = 'Decision for 10000 USD')
plt.legend(loc='upper right')
plt.xlabel('Fico Score')
plt.ylabel('Probability and decision, yes = 1, no = 0')







