import requests
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import sqlite3 as lite
import time
from dateutil.parser import parse
import collections
import datetime


r = requests.get('http://www.citibikenyc.com/stations/json')

key_list = []

for station in r.json()['stationBeanList']:
	for k in station.keys():
		if k not in key_list:
			key_list.append(k)


df = json_normalize(r.json()['stationBeanList'])

#print(df['totalDocks'].mean())

#condition = (df['statusValue'] == 'In Service')

#print(df[condition]['totalDocks'].mean())


#print(df['totalDocks'].median())
#print(df[df['statusValue'] == 'In Service']['totalDocks'].median())


con = lite.connect('citi_bike.db')
cur = con.cursor()



with con:
	cur.execute('DROP TABLE IF EXISTS citibike_reference')
	cur.execute('DROP TABLE IF EXISTS available_bikes')
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')

sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"



with con:
	for station in r.json()['stationBeanList']:
		cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))


station_ids = df['id'].tolist()

station_ids = ['_' + str(x) + ' INT' for x in station_ids]

with con:
	cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

exec_time = parse(r.json()['executionTime'])

#exec_time = (exec_time - datetime.datetime(1970,1,1)).total_seconds()

with con:
	cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%Y-%m-%dT%H:%M:%S'),))

id_bikes = collections.defaultdict(int)

for station in r.json()['stationBeanList']:
	id_bikes[station['id']] = station['availableBikes']

with con:
	for k, v in id_bikes.items():
		cur.execute("UPDATE available_bikes SET _" + str(k) + "=" + str(v) + " WHERE execution_time = " + exec_time.strftime('%S') + ";")
	

