import pandas as pd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from prophet import Prophet
import os

pwd=os.getcwd()

cases = pd.read_excel(pwd+'/../data/cases_plot.xlsx')
deaths = pd.read_excel(pwd+'/../data/deaths_plot.xlsx')


# Predict for deaths
predict_data_cases=cases.diff()
predict_data_cases['Date']=cases['Date']
predict_data_cases=predict_data_cases.rename(columns={'Date':'ds'})

predicted_cases=pd.DataFrame(cases['Date'])
for col in predict_data_cases.iloc[:,1:]:
    m = Prophet(interval_width=0.95, daily_seasonality=True)
    temp_df=pd.DataFrame()
    temp_df['ds']=cases['Date']
    temp_df['y']=predict_data_cases[col]
    m.fit(temp_df)
    future = m.make_future_dataframe(periods=14,freq='D')
    forecast = m.predict(future)
    predicted_cases[col]=forecast['yhat']
    predicted_cases.rename(columns={'yhat':col})

# Save predicted dataset
predicted_cases.tail(14).to_csv(pwd+'/../data/casepredictions.csv')


# Predict for deaths
predict_data_deaths=deaths.diff()
predict_data_deaths['Date']=deaths['Date']
predict_data_deaths=predict_data_deaths.rename(columns={'Date':'ds'})

predicted_deaths=pd.DataFrame(deaths['Date'])
for col in predict_data_deaths.iloc[:,1:]:
    m = Prophet(interval_width=0.95, daily_seasonality=True)
    temp_df=pd.DataFrame()
    temp_df['ds']=deaths['Date']
    temp_df['y']=predict_data_deaths[col]
    m.fit(temp_df)
    future = m.make_future_dataframe(periods=14,freq='D')
    forecast = m.predict(future)
    predicted_deaths[col]=forecast['yhat']
    predicted_deaths.rename(columns={'yhat':col})

# Save predicted dataset
predicted_deaths.tail(14).to_csv(pwd+'/../data/deathpredictions.csv')


