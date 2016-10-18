citibike.py

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
for i in range(60):
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




