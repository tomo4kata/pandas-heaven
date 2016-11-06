temperature.py


import requests
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 as lite
import datetime
import time
import json

api_key = "0c30be27a18558751980de6dc45f8c1a"

cities  = { "Atlanta": '33.762909,-84.422675',
            "Chicago": '41.837551,-87.681844',
            "Boston": '42.331960,-71.020173',
            "Seattle": '47.620499,-122.350876',
            "Washington": '38.904103,-77.017229'
        }

tgtURL =  "https://api.forecast.io/forecast/" + "0c30be27a18558751980de6dc45f8c1a" + "/"

def init_db():
	con = lite.connect('weather.db')
	cur = con.cursor()
	tgtCreateTableQuery = '''CREATE TABLE IF NOT EXISTS hourly (
		ozone REAL,
        cloudCover REAL, 
        apparentTemperature REAL, 
        precipAccumulation REAL,
        pressure REAL, 
        precipProbability REAL, 
        visibility REAL,
        precipType TEXT,
        summary TEXT, 
        icon TEXT, 
        temperature REAL, 
        dewPoint REAL, 
        humidity REAL, 
        windSpeed REAL, 
        time INT,
        precipIntensity REAL,
        windBearing INT,
        latitude REAL,
        longitude REAL,
        UNIQUE(latitude,longitude,time) ON CONFLICT REPLACE )'''
	with con:
		cur.execute(tgtCreateTableQuery)
	con.commit()
	con.close()

def init_city_table():
	con = lite.connect('weather.db')
	cur = con.cursor()
	tgtCreateTableQuery = '''CREATE TABLE IF NOT EXISTS cities ( 
		name TEXT,
        latitude REAL, 
        longitude REAL,UNIQUE(name,latitude,longitude) ON CONFLICT REPLACE )'''
	cur.execute(tgtCreateTableQuery)
	for key in cities:
		tgtInsertQuery = "INSERT into cities(name,latitude,longitude) VALUES (?,?,?)"
		cur.execute(tgtInsertQuery,(key,cities[key].split(",")[0],cities[key].split(",")[1]))

	con.commit()
	con.close()

def get_max_depth_level(tgtJson):
	# if not list or dict, return one
	if not isinstance(tgtJson, dict) and not isinstance(tgtJson,list):
		return 0
	curDepth = []
	if isinstance(tgtJson, dict):
		for key in tgtJson:
			curDepth.append(get_max_depth_level(tgtJson[key])+1)
	elif isinstance(tgtJson,list):
		for curElement in tgtJson:
			curDepth.append(get_max_depth_level(curElement)+1)
	return max(curDepth)

def update_hourly():
	con = lite.connect('weather.db')
	cur = con.cursor()
	for key in cities:
		if key != 'NewYork':
			continue
		for i in range(0,30):
			curDate = datetime.datetime.now() - datetime.timedelta(days=i)
			curTime = curDate.strftime("%Y-%m-%dT%H:%M:%S")
			curURL = tgtURL + cities[key] + "," + curTime
			r = requests.get(curURL)
			curJSON = r.json()
			for curHourly in curJSON["hourly"]["data"]:
				curHourly["latitude"] = cities[key].split(",")[0]
				curHourly["longitude"] = cities[key].split(",")[1]
				print(getInsertFromDict(curHourly))
				cur.execute(getInsertFromDict(curHourly))
		break
	con.commit()
	con.close()

def getInsertFromDict(tgtJson):
	tgtKeyList = []
	tgtValueList = []
	for key in tgtJson:
		tgtKeyList.append(key)
		if isinstance(tgtJson[key],str):
			tgtValueList.append("'" + str(tgtJson[key]) + "'")
		else:
			tgtValueList.append(str(tgtJson[key]))
	tgtInsertQuery = "INSERT INTO hourly(" + ",".join(tgtKeyList) + ")"
	tgtInsertQuery += " VALUES (" + ",".join(tgtValueList) + ")"
	return  tgtInsertQuery

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

init_db()
init_city_table()
update_hourly()


# Write a script that takes each city and queries every day for the past 30 days 
# (Hint: You can use the datetime.timedelta(days=1) to increment the value by day) 
# update_hourly()
# Save the max temperature values to the table, keyed on the date. 
# You can leave the date in Unix time or convert to a string. 


tgtQuery = "select distinct latitude,longitude, max(temperature) as temperature ,time  from hourly group by latitude,longitude"

con = lite.connect('weather.db')

df = pd.read_sql(tgtQuery,con) # can't we use this reading the query
print("Maximum temperature in last 30 days "+str(df['temperature'].tolist()[0]))

# check the database and plot temp variation over time
hrlyQuery =  "select * from hourly order by time"
df_hrly = pd.read_sql(hrlyQuery, con)
plt.figure()
plt.plot(df_hrly['time'], df_hrly['temperature'], color = 'green')
plt.xlabel('Time')
plt.ylabel('Temperature')
plt.title('Temperature variation in NewYork city for last 30 days')
plt.savefig('/Users/shubhabrataroy/Desktop/Thinkful/Data/NYTemp30days.jpg')

# What's the range of temperatures? -> New York 38~83
# What is the mean temperature for each city? -> 57.73550000000001
# What's the variance? Are there any patterns in the data? -> Variance is 45.

url = 'https://api.forecast.io/forecast/' + api_key + "/"

end_date = datetime.datetime.now()

#creating the database
con = lite.connect('/Users/Tomo/thinkful/weather.db')
cur = con.cursor()
cities.keys()
with con:
    cur.execute("DROP TABLE IF EXISTS daily_temp")
    cur.execute('CREATE TABLE daily_temp(day_of_reading INT, Washington REAL, Chicago REAL, Atlanta REAL, Boston REAL, Seattle REAL);')

query_date = end_date - datetime.timedelta(days=30) #the current value being processed
with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)


#loop through the cities and query the api
for k,v in cities.items():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime("%Y-%m-%dT%H:%M:%S"))

        with con: #inrsert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))
        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day

con.close()


