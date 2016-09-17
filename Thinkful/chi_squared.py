chi_squared.py

from scipy import stats
import collections

# Load the reduced version of the Lending Club Dataset
loansData = pd.read_csv('https://github.com/Thinkful-Ed/curric-data-001-data-sets/raw/master/loans/loansData.csv')
# Drop null rows
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])


# Distribution of data
plt.figure()
plt.bar(freq.keys(), freq.values(), width=1)
plt.show()

# Chi-Squared test
chi, p = stats.chisquare(freq.values())
# chi = 2408.433146517214
# p = 0.0