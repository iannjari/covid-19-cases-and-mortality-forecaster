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

df6=pd.read_excel(pwd+"\\deaths.xlsx")
df7=pd.read_excel(pwd+"\\deaths_plot.xlsx")

app = dash.Dash(__name__)
fig = go.Figure()
fig2=go.Figure()

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    
    
    
    
])

index_page = html.Div([
    #dcc.Link('Home', href='/page-1'),
    html.Br(),
    dcc.Link('Cases and Deaths Board', href='/page-1'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3')
])

page_1_layout = html.Div([
    html.H1('Cases and Deaths by Country'),
    html.Br(),
    
    dcc.Link('Home', href='/index_page'),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/page-1'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    dcc.Dropdown(
        id='dropdown',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in df2.columns[1:]]),
    
    dcc.Graph(id='graph'),
     html.Div(id='dd-output-container1'),
    
    dcc.Dropdown(
        id='dropdown2',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in df7.columns[1:]]),
    
    dcc.Graph(id='graph2'),
    
    html.Div(id='dd-output-container')
])




page_2_layout = html.Div([
    html.H1('Reports'),
    html.Br(),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

@app.callback(
    [Output("graph", "figure"),Output("graph2","figure"),],
    [Input('dropdown', 'value'),
     Input('dropdown2', 'value')
     ])


def display_graph(dropdown,dropdown2):
    
    dffd=df1.loc[df1['Country/Region'] == dropdown]
    dffd=dffd.reset_index()
    dffd=dffd.rename_axis(None, axis=1)
    dffd=dffd.drop(['index','Country/Region'],axis=1)
    
    
    fig = px.line(df2,x=df2["Date"], y=dffd.loc[0],
                  hover_data={"Date"},
                  title='Cases By Country',
                  labels={"y": "No. of Cases"}
                  )
    
    dff=df6.loc[df6['Country/Region'] == dropdown2]
    dff=dff.reset_index()
    dff=dff.rename_axis(None, axis=1)
    dff=dff.drop(['index','Country/Region'],axis=1)
    
    
    fig2 = px.line(df7,x=df7["Date"], y=dff.loc[0],
                  hover_data={"Date"},
                  title='Deaths By Country',
                  labels={"y": "No. of Deaths"}
                  )
    
    return fig,fig2



    
app.run_server(debug=True) 
