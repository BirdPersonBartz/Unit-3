import requests
import sqlite3 as lite
import datetime
import pandas as pd



cities = {"Boston": '42.331960,-71.020173'}#,
		#"Seattle": '47.620499,-122.350876',
		#"Denver": '39.761850,-104.881105',
		#"Minneapolis": '44.963324,-93.268320',
		#"NYC": '40.663619,-73.938589'
		
		#}

citynames = list(cities.keys())


key = '2f4ef2844027ca42aaa3406c3894b53a'
baseurl = 'https://api.forecast.io/forecast/'+ key + '/'
end_date = datetime.datetime.now()
query_date = end_date - datetime.timedelta(days=30)
query_date_range = pd.date_range(end_date - datetime.timedelta(days = 30), periods = 30)

df = pd.DataFrame()
df['daily_temp'] = query_date_range.strftime('%Y-%m-%dT12:00:00')
df['bscol'] = 1
df.set_index('daily_temp')




for k,v in cities.items():
	query_date = end_date - datetime.timedelta(days=30)
	tempsdict = {}
	cityname = k
	while query_date < end_date:
		r = requests.get(baseurl + v + ',' + query_date.strftime('%Y-%m-%dT12:00:00'))
		temp = str(r.json()['daily']['data'][0]['temperatureMax'])
		time = query_date.strftime('%Y-%m-%dT12:00:00')
		tempsdict.update({time:temp})
		query_date += datetime.timedelta(days=1)
	#tempseries = pd.Series(tempsdict)
	df2 = pd.DataFrame.from_dict(tempsdict, orient = 'index')
	df2.columns = [cityname]
	print(df2)
	df.join(df2)


print(df)




