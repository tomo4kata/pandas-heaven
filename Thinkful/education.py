education.py

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import sqlite3 as lite
import csv

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)
soup = BeautifulSoup(r.content, "lxml")

for row in soup('table'):
    print(row)

soup('table')[6]

A = soup('table')[6].findAll('tr', {'class': 'tcont'})
B = [x for x in A if len(x)== 25] # removing records without value

records = []
for rows in B:
    col = rows.findAll('td')
    country = col[0].string
    year = col[1].string
    total = col[4].string
    men = col[7].string
    women = col[10].string
    record = (country, year, total, men, women)
    records.append(record)
column_name = ['country', 'year', 'total_schoollife', 'men_schoollife', 'women_schoollife']
table_schoollife = pd.DataFrame(records, columns = column_name )
table_schoollife=table_schoollife.dropna(axis=1,how='all')

con = lite.connect('/Users/Tomo/thinkful/education.db')
cur = con.cursor()

with con:
    cur.execute("DROP TABLE IF EXISTS gdp")
    cur.execute('CREATE TABLE gdp (country REAL, GDP_1999 INT, GDP_2000 INT, GDP_2001 INT, GDP_2002 INT, GDP_2003 INT, GDP_2004 INT, GDP_2005 INT, GDP_2006 INT, GDP_2007 INT, GDP_2008 INT, GDP_2009 INT, GDP_2010 INT);')

with open('/Users/Tomo/thinkful/world_bank_data/Metadata_Indicator_v2.csv','rU') as inputFile:
    next(inputFile) # skip the first two lines
    next(inputFile)
    header = next(inputFile)
    inputReader = csv.reader(inputFile)
    for line in inputReader:
        with con:
            cur.execute('INSERT INTO gdp (country_name, _1999, _2000, _2001, _2002, _2003, _2004, _2005, _2006, _2007, _2008, _2009, _2010) VALUES ("' + line[0] + '","' + '","'.join(line[42:-5]) + '");')

# /Users/Tomo/anaconda/envs/py35/bin/ipython:1: DeprecationWarning: 'U' mode is deprecated
  #!/bin/bash /Users/Tomo/anaconda/envs/py35/bin/python.app
#---------------------------------------------------------------------------
#StopIteration                             Traceback (most recent call last)
#<ipython-input-20-559db1e4427b> in <module>()
#      2     next(inputFile) # skip the first two lines
#      3     next(inputFile)
#----> 4     header = next(inputFile)
#      5     inputReader = csv.reader(inputFile)
#      6     for line in inputReader:

#StopIteration: 














