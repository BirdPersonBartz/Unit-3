
import requests
import sqlite3 as lite
import datetime
import pandas as pd
import collections

cities = {"Boston": '42.331960,-71.020173',
		"Seattle": '47.620499,-122.350876',
		"Denver": '39.761850,-104.881105',
		"Minneapolis": '44.963324,-93.268320',
		"NYC": '40.663619,-73.938589',
		}

key = '2f4ef2844027ca42aaa3406c3894b53a'
baseurl = 'https://api.forecast.io/forecast/'+ key + '/'
end_date = datetime.datetime.now()
query_date = end_date - datetime.timedelta(days=30)

con = lite.connect('weather.db')
cur = con.cursor()

with con:
    cur.execute('DROP TABLE IF EXISTS daily_temp')
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, Boston REAL, Seattle REAL, Denver REAL, Minneapolis REAL, NYC REAL);')

with  con:
  while query_date < end_date:
    cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%d')),))
    query_date += datetime.timedelta(days=1)

for k,v in cities.items():
    query_date = end_date - datetime.timedelta(days=30) 
    while query_date < end_date:
        r = requests.get(baseurl + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))
        with con:
          cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%d'))
        query_date += datetime.timedelta(days=1) 

df = pd.read_sql_query("SELECT * FROM daily_temp ORDER BY day_of_reading",con,index_col='day_of_reading')

changedict = (df.max()-df.min())


print("The city with the greatest temp change was %s with a %s degree change" % (changedict.idxmax(), changedict.max()))
