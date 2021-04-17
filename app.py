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

app = dash.Dash(__name__)
fig = go.Figure()

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df1['Country/Region'].unique()],
        value='Kenya'),
    
    dcc.Graph(figure=fig),
    
    html.Div(id='dd-output-container')
])

@app.callback(
    Output("graph", "fig"), 
    [Input("dropdown", "value")])


def get_dff1(df1):
    dff1 = df1.loc[df1['Country/Region']== 'value']
    return dff1

def get_y(dff1):
    
    dff1.columns = range(dff1.shape[1])
    dff2=pd.Index(dff1.iloc[0])
    yval=dff2[1:]
    return yval

def display_graph(value,dff1,yval):
   
    
    fig = px.line(dff1, x=dff1.columns[1:], y=yval)    
    return fig


    
    
app.run_server(debug=True) 
