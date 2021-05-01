import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 

import os

pwd=os.getcwd()
df1=pd.read_excel(pwd+"\\cases.xlsx")
df2=pd.read_excel(pwd+"\\cases_plot.xlsx")

df1=pd.read_excel(pwd+"\\cases.xlsx")
df2=pd.read_excel(pwd+"\\cases_plot.xlsx")

app = dash.Dash(__name__)
fig = go.Figure()

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in df2.columns[1:]]),
    
    dcc.Graph(id='graph'),
    
    html.Div(id='dd-output-container')
])

@app.callback(
    Output("graph", "figure"), 
    [Input('dropdown', 'value')])


def display_graph(dropdown):
    
    dffd=df1.loc[df1['Country/Region'] == dropdown]
    dffd=dffd.reset_index()
    dffd=dffd.rename_axis(None, axis=1)
    dffd=dffd.drop(['index','Country/Region'],axis=1)
    
    
    fig = px.line(df2,x=df2["Date"], y=dffd.loc[0],
                  hover_data={"Date"},
                  title='Cases By Country',
                  labels={"y": "No. of Cases"}
                  )
    return fig

 

    
    
app.run_server(debug=True) 
