prob_lending_club.py

import matplotlib.pyplot as plt
import pandas as pd

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

# remove rows with null values
loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Funded.By.Investors')
plt.show()

loansData.hist(column='Amount.Funded.By.Investors')
plt.show()


import scipy.stats as stats

plt.figure()
graph = stats.probplot(loansData['Amount.Funded.By.Investors'], dist="norm", plot=plt)
plt.show()



# Generate and save a boxplot, histogram, and QQ-plot for the values in the "Amount.Requested" column

import matplotlib.pyplot as plt
import pandas as pd

loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')

# remove rows with null values
loansData.dropna(inplace=True)

loansData.boxplot(column='Amount.Requested')
plt.show()

loansData.hist(column='Amount.Requested')
plt.show()


import scipy.stats as stats

plt.figure()
graph = stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.show()



# The histogram of Amount.Requested is slightly more right skewed compared to the one of Amount.Invested.By.Investors.

# The QQ-plots of both column indeed show right skew. R^2 is smaller in the QQ plot of Amount.Requested, which means it's more deviated from normal distribution than the one of Amount.Invested.By.Investors.






