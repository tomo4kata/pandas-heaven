stats.py

import pandas as pd
from scipy import stats

data = '''Region,Alcohol,Tobacco
North,6.47,4.03
Yorkshire,6.13,3.76
Northeast,6.19,3.77
East Midlands,4.89,3.34
West Midlands,5.63,3.47
East Anglia,4.52,2.92
Southeast,5.89,3.20
Southwest,4.79,2.71
Wales,5.27,3.53
Scotland,6.08,4.51
Northern Ireland,4.02,4.56''' 

# split the string on the (hidden characters that indicate) newlines
data = data.splitlines()

# split each item in this list on the commas
data = [i.split(',') for i in data]

# create pandas dataframe
column_names = list(data[0]) #first row
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns = column_names)

# Now, convert create a pandas dataframe
column_names = data[0]
data_rows = data[1::]
df = pd.DataFrame(data_rows, columns=column_names)

# convert columns to float
df['Alcohol'] = df['Alcohol'].astype(float)
df['Tobacco'] = df['Tobacco'].astype(float)

# calculate mean
alcohol_mean = df['Alcohol'].mean()
tobacco_mean = df['Tobacco'].mean()
print "The mean of the alcohol and tobacco is %.2f %.2f" %(alcohol_mean, tobacco_mean)

#calculate median
alcohol_median = df['Alcohol'].median()
tobacco_median = df['Tobacco'].median()
print "The median of the alcohol and tobacco is %.2f %.2f" %(alcohol_median, tobacco_median)

# calculate mode
alcohol_mode = stats.mode(df['Alcohol'])
tobacco_mode = stats.mode(df['Tobacco'])
print "The mode of the alcohol and tobacco is %.2f %.2f" %(float(alcohol_mode[0]), float(tobacco_mode[0]))

# calculate variance
alcohol_var = df['Alcohol'].var()
tobacco_var = df['Tobacco'].var()
print "The variance of the alcohol and tobacco is %.2f %.2f" %(alcohol_var, tobacco_var)

# calculate standard deviation
alcohol_std = df['Alcohol'].std() 
tobacco_std = df['Tobacco'].std() 
print "The standard deviation of the alcohol and tobacco is %.2f %.2f" %(alcohol_std, tobacco_std)






