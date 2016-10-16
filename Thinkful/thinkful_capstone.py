# Thinkful Capstone Project 

# Objective 
# The main goal of this project is to predict the financial
# performance of companies, focusing on Earnings per Share (dependent
# variable). To do so, I will apply a multivariate analysis using other
# indexes (independent variable) on the corporate balance sheets.

# All the data that are used for the analysis come from US Fundamentals, who
# provide fundamental data for US stocks based on SEC's XBRL filings. The
# resource link is: usfundamental.com


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('US_Fundamentals.csv', low_memory = False)

df.shape
# (9614, 20)
timeit df.shape 
# 100000 loops, best of 3: 2.1 µs per loop


### Missing values

len(df.index)-df.count() #Count of missing values
# SEC ID                                                0
# Latest Name                                           0
# Latest NAICS Industry Sector Name                     0
# Latest NAICS Industry Sector Code                     0
# Report date                                           0
# Assets                                              311
# AssetsCurrent                                      2395
# CashAndCashEquivalentsAtCarryingValue              1313
# ComprehensiveIncomeNetOfTax                        4452
# EarningsPerShareDiluted                            5049
# Goodwill                                           5616
# Liabilities                                        1776
# LiabilitiesCurrent                                 2369
# NetCashProvidedByUsedInFinancingActivities          582
# NetCashProvidedByUsedInInvestingActivities         1534
# NetCashProvidedByUsedInOperatingActivities          366
# OperatingIncomeLoss                                2734
# PropertyPlantAndEquipmentNet                       2478
# Revenues                                           3522
# WeightedAverageNumberOfDilutedSharesOutstanding    4766

df.dropna(subset=['EarningsPerShareDiluted']) #Delete the rows of companies which are missing values for column EarningsPerShareDiluted

df["EarningsPerShareDiluted"].fillna(df["EarningsPerShareDiluted"].mean(), inplace=True) #Insert mean values for each column's missing values


### Visualization

df.boxplot(column='EarningsPerShareDiluted')
plt.show()

df.hist(column='EarningsPerShareDiluted')
plt.show()



df[(np.abs(stats.zscore(df["EarningsPerShareDiluted"])) < 3).all(axis=0)]














