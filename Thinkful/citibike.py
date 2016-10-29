citibike.py

# Goal is to record the number of bikes available every minute for an hour across all of New York City in order to see which station or set of stations is the most active in New York City for that hour. 
# Activity is defined as the total number of bicycles taken out or returned in an hour. So if 2 bikes are brought in and 4 bikes are taken out, that station has an activity level of 6.



import time
import requests
from dateutil.parser import parse
import collections
import sqlite3 as lite
import pandas as pd
import matplotlib.pyplot as plt
import collections
from pandas.io.json import json_normalize

r = requests.get('http://www.citibikenyc.com/stations/json')

r.json().keys()
# [u'executionTime', u'stationBeanList']

len(r.json()['stationBeanList'])
# 664

key_list = [] #unique list of keys for each station listing
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)

# Getting data into a dataframe

df = json_normalize(r.json()['stationBeanList'])


# Checking the range of values
df['availableBikes'].hist()
plt.show()


df['totalDocks'].hist()
plt.show()


# Explore the other data variables. 
# Are there any test stations? 
sum(df['testStation'])
# 0

# How many stations are "In Service"? 
sum(df['statusValue'] == "In Service")
# 638

# How many are "Not In Service"? 
sum(df['statusValue'] == "Not In Service")
# 26

# mean and median number of bikes in a station
df['totalDocks'].mean()
# 30.634036144578314
df['totalDocks'].median()
# 30.0

# How does this change if we remove the stations that aren't in service
condition = (df['statusValue'] == 'In Service')
df[condition]['totalDocks'].mean()
# 31.605015673981192
df[condition]['totalDocks'].median()
# 31.0

# Storing Data in SQLiteexi=
con = lite.connect('citi_bike.db')
cur = con.cursor()

with con:
    cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

#for loop to populate values in the database
with con:
    for station in r.json()['stationBeanList']:
        #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))

#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ['_' + str(x) + ' INT' for x in station_ids]

#create the table
#in this case, we're concatenating the string and joining all the station ids (now with '_' and 'INT' added)
with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")

# a package with datetime objects
import time

# a package for parsing a string into a Python datetime object
from dateutil.parser import parse 
import collections

#take the string and parse it into a Python datetime object
exec_time = parse(r.json()['executionTime'])


# create an entry for the execution time by inserting it into the database
with con:
    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))


id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

#loop through the stations in the station list
for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']

#iterate through the defaultdict to update the values in the database
with con:
    for k, v in id_bikes.items():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")


### let the code sleep for a minute and then perform the same task
for i in range(10):
    r = requests.get('http://www.citibikenyc.com/stations/json')
    exec_time = parse(r.json()['executionTime'])

    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%c'),))
    con.commit()
    
    id_bikes = collections.defaultdict(int)
    for station in r.json()['stationBeanList']:
        id_bikes[station['id']] = station['availableBikes']

    for k, v in id_bikes.items():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = '" + exec_time.strftime('%s') + "';")
    con.commit()

    time.sleep(60)
con.close()


import pandas as pd
import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')


hour_change = collections.defaultdict(int)
for col in df.columns:
    station_vals = df[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer

def keywithmaxval(d):
    """Find the key with the greatest value"""
    return max(d, key=lambda k: d[k])

# assign the max key to max_station
max_station = keywithmaxval(hour_change)

#query sqlite for reference information
cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)

# The most active station is station id 3072 at Leonard St & Boerum St latitude: 40.70583339 longitude: -73.94644578 

print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
    ))

import matplotlib.pyplot as plt
plt.bar(hour_change.keys(), hour_change.values())
plt.show()


