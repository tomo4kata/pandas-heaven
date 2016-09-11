database.py

import sqlite3 as lite
import pandas as pd
import sys

# Connect to the database
con = lite.connect('/home/sroy/ThinkfulTest1.db')
c = con.cursor()



populate_cities = """
INSERT INTO cities (name, state) VALUES
    ('New York City', 'NY'),
    ('Boston', 'MA'),
    ('Chicago', 'IL'),
    ('Miami', 'FL'),
    ('Dallas', 'TX'),
    ('Seattle', 'WA'),
    ('Portland', 'OR'),
    ('San Francisco', 'CA'),
    ('Los Angeles', 'CA');
"""

populate_weather = """
INSERT INTO weather (city,year,warm_month,cold_month,average_high) VALUES
    ('New York City',2013,'July','January',62),
    ('Boston',2013,'July','January',59),
    ('Chicago',2013,'July','January',59),
    ('Miami',2013,'August','January',84),
    ('Dallas',2013,'July','January',77),
    ('Seattle',2013,'July','January',61),
    ('Portland',2013,'July','December',63),
    ('San Francisco',2013,'September','December',64),
    ('Los Angeles',2013,'September','December',75);
"""

# Create the cities and weather tables (HINT: first pass the statement DROP TABLE IF EXISTS <table_name>; to remove the table before you execute the CREATE TABLE ... statement)
c.execute("DROP TABLE IF EXISTS cities")
c.execute("CREATE TABLE cities (name text, state text)")
c.execute("DROP TABLE IF EXISTS weather")
c.execute("CREATE TABLE weather (city text,year integer,warm_month text,cold_month text,average_high integer)")

c.execute(populate_weather)
c.execute(populate_cities)

# Insert data into the two tables

cities = pd.read_sql("select * from cities",con)

weather = pd.read_sql("select * from weather",con)
weather["name"] = weather["city"]
weather.drop('city', axis=1, inplace=True)

# Join the data together
city_weather = pd.DataFrame.merge(cities,weather, how='inner', left_on = 'name', right_on = 'name')
city_weather

# Pick the records where July is the warmest month
city_weather_july = city_weather[city_weather['warm_month'] == 'July']

# Print out the resulting city and state in a full sentence. For example The cities that are warmest in July are: Las Vegas, NV, Atlanta, GA
together = city_weather_july.apply(lambda x:'%s, %s' % (x['name'],x['state']),axis=1)
print "The cities that are warmest in July are:", ', '.join(together.tolist())
