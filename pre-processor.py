# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:17:27 2021

@author: iannjari
"""

import pandas as pd
import os
cases= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths= pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')


# Start with the cases data for the map

# Drop the Province/State column, then group all rows by country
df1=cases.drop('Province/State',axis=1)
df1=df1.groupby(['Country/Region'],as_index=False).sum()

# Drop un-wanted columns
df1=df1.drop(['Lat','Long'],axis=1)
cols=df1[df1.columns[1:-1]]
df2=df1.drop(cols,axis=1)

# Read COUNTRY CODE data
pwd=os.getcwd()
df4=pd.read_excel(pwd+"\\map_code1.xlsx")

# Perform inner join on the map code and cases(df2)
df5=pd.merge(df2,df4,how='inner',left_on=['Country/Region'],right_on=['COUNTRY'])
df5=df5.drop('COUNTRY',axis=1)

# Rename the Cases column
casemapdata = df5.rename(columns={df5.columns[1]: 'Total Cases'})

# Save data for case map
casemapdata.to_excel ("casemapdata.xlsx", index = False, header=True)




