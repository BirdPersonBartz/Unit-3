from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3 as lite
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"

r = requests.get(url)

soup = BeautifulSoup(r.content, "lxml")


con = lite.connect('educationVSgdp.db')
cur = con.cursor()



trlist = soup.findAll('tr')#, attrs=('class', 'tcont'))


with con:
	cur.execute('DROP TABLE IF EXISTS school_years')
	cur.execute('CREATE TABLE school_years ( Country TEXT, Year DATE, Total INT, Men INT, Women INT);')

for val in trlist[18:]:
#	print(type(val.contents[1].text))
#	print(val.contents[1].text)
	with con:
		if val.contents[1].string == 'Zimbabwe':
			cur.execute('INSERT INTO school_years (Country) VALUES ("' + val.contents[1].text + '");')
			break
		else:
			cur.execute('INSERT INTO school_years (Country) VALUES ("' + val.contents[1].text + '");')

# df = pd.read_sql_query('SELECT * from school_years', con)
# print(df)	

for val in trlist[18:]:
	if val.contents[1].string == "Zimbabwe":
		with con:
			cur.execute('UPDATE school_years SET Year=' + val.contents[3].string +
				 ', Total=' + val.contents[9].string +
				 ', Men=' + val.contents[15].string +
				 ', Women=' + val.contents[21].string +
				 ' WHERE Country = "' + val.contents[1].text + '";')
		break
	else:
		with con:
			cur.execute('UPDATE school_years SET Year=' + val.contents[3].string +
			 ', Total=' + val.contents[9].string +
			 ', Men=' + val.contents[15].string +
			 ', Women=' + val.contents[21].string +
			 ' WHERE Country = "' + val.contents[1].text + '";')



df = pd.read_sql_query('SELECT * from school_years', con)



print(df.mean())
print(df.median())
print(df.var())

df2 = pd.read_csv('API_NY.GDP.MKTP.CD_DS2_en_v2.csv', header = 2, usecols=['Country Name','1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010'])




df2.to_sql('GDPtable', con, if_exists = "replace")





df = pd.read_sql_query('SELECT Country, Year, Total, Men, Women, [Country Name], [1999], [2000], [2001], [2002], [2003], [2004], [2005], [2006], [2007], [2008], [2009], [2010] FROM school_years LEFT JOIN GDPtable ON school_years.[Country] = GDPtable.[Country Name]', con)#, index_col = "Country Name")





df['GDP'] = 0

def update_gdp (yearneeded):
	if df.ix[index, 'Year'] == yearneeded:
		if df.ix[index, '2004'] > 1: SHOULD DO STR(YEARNEEDED) HERE
			gdp_value = df.ix[index, str(yearneeded)] 	
			#print(gdp_value)
			df.set_value(index, 'GDP', gdp_value)#gdp_value)
		else:
			df.set_value(index, 'GDP', 0)

for index, row in df.iterrows():
	# if df['GDP'] = '1999'
	# if df.ix[index, 'Year'] == 1999:
	# 	if df.ix[index, '2004'] > 1:
	# 		gdp_value = df.ix[index, '2004']
	# 		print(gdp_value)
	# 		df.set_value(index, 'GDP', gdp_value)#gdp_value)
	# 	else:
	# 		continue
	update_gdp(1999)
	update_gdp(2000)
	update_gdp(2002)
	update_gdp(2003)
	update_gdp(2004)
	update_gdp(2005)
	update_gdp(2006)
	update_gdp(2007)
	update_gdp(2008)
	update_gdp(2009)
	update_gdp(2010)


df = df[df['GDP'] != 0]

print(df.head())


df.reset_index



gdpreg = df['GDP'].map(lambda x: np.log(float(x)))
school_yearsreg = df['Total'].map(lambda x: int(x))
male_reg = df['Men'].map(lambda x: int(x))
female_reg = df['Women'].map(lambda x: int(x))




plt.scatter(school_yearsreg, gdpreg)
plt.title('Total')
plt.show()
plt.scatter(male_reg, gdpreg)
plt.title('Men')
plt.show()
plt.scatter(female_reg, gdpreg)
plt.title('woment')
plt.show()



Y = df['GDP'][:-1]
X = df[['Total', 'Men', 'Women']][:-1]
X = sm.add_constant(X)

results = sm.OLS(Y,X).fit()
print(results.params)
print(results.summary())