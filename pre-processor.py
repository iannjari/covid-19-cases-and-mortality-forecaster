# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:17:27 2021

@author: iannjari
"""

import pandas as pd
import os
import plotly.express as px
#import plotly.graph_objects as go

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

# Prepare deaths data for the map

df6=deaths.drop('Province/State',axis=1)
df6["Country/Region"].nunique(dropna = True)
df6=df6.drop(['Lat','Long'],axis=1)
cols2=df6[df6.columns[1:-1]]
df7=df6.drop(cols2,axis=1)
#df7 will be the new sliced dataframe 

df8=pd.merge(df7,df4,how='inner',left_on=['Country/Region'],right_on=['COUNTRY'])
df8=df8.drop('COUNTRY',axis=1)
deathmapdata = df8.rename(columns={df8.columns[1]: 'Total Deaths'})
deathmapdata.to_excel ("deathmapdata.xlsx", index = False, header=True)

# Prepare Line Graph data

# Transpose the data and re-allocate the column headers
df1=df1.transpose()
new_header = df1.iloc[0] #grab the first row for the header
df1 = df1[1:] #take the data less the header row
df1.columns = new_header #set the header row as the df header

df1=df1.reset_index()

df2=df1.rename(columns = {'index':'Date'})

# Convert datatypes into dates and integers
df2[df2.columns[1:]]=df2[df2.columns[1:]].astype('int64')
df2[df2.columns[1:]]

date_convert=df2[df2.columns[0]]
date_converted= pd.to_datetime(date_convert)

df2['Date']=date_converted

plot_df=df2.rename_axis(None, axis=1)
plot_df.to_excel ("cases_plot.xlsx", index = False, header=True)










