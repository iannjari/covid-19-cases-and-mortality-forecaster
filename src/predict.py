import pandas as pd
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from prophet import Prophet
import os

pwd=os.getcwd()

cases = pd.read_excel(pwd+'/../data/cases_plot.xlsx')

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

predicted_cases.tail(14).to_csv(pwd+'/../data/predictions.csv')


