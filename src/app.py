import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 

import os

pwd=os.getcwd()

# Read data for maps
case_map =pd.read_excel(pwd+"\\..\\data\\casemapdata.xlsx")
death_map =pd.read_excel(pwd+"\\..\\data\\deathmapdata.xlsx")


# Read line plot data
df1=pd.read_excel(pwd+"\\..\\data\\cases.xlsx")
df2=pd.read_excel(pwd+"\\..\\data\\cases_plot.xlsx")

df6=pd.read_excel(pwd+"\\..\\data\\deaths.xlsx")
df7=pd.read_excel(pwd+"\\..\\data\\deaths_plot.xlsx")

app = dash.Dash(__name__)
fig = go.Figure()
fig2=go.Figure()
fig3=go.Figure()

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    ])

index_page = html.Div([
    #dcc.Link('Home', href='/page-1'),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/page-1'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    
    html.Br(),
    
     dcc.Dropdown(
        id='dropdown3',
        value = 'Cases',
        options=[
            {'label': 'See Global Cases', 'value': 'Cases'},
            {'label': 'See Global Mortality', 'value': 'Deaths'}]),
     
    html.Br(),
    
    dcc.Graph(id="choropleth", figure=fig3),
    
    html.Br(),
    
    
])

page_1_layout = html.Div([
    html.H1('Cases and Deaths by Country'),
    html.Br(),
    
    dcc.Link('Home', href='/index_page'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    
    html.Br(),
    html.Br(),
    
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
    dcc.Link('Home', href='/'),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/page-1'),
    html.Br(),
    dcc.Link('Predict', href='/page-3')
    
])




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
    [Output("graph", "figure"),Output("graph2","figure")],
    [Input('dropdown', 'value'),
     Input('dropdown2', 'value')
     ])


def display_graph(dropdown,dropdown2):
    
    # Prepare cases graphing data
    dffd=df1.loc[df1['Country/Region'] == dropdown]
    dffd=dffd.reset_index()
    dffd=dffd.rename_axis(None, axis=1)
    dffd=dffd.drop(['index','Country/Region'],axis=1)
    
    # Plot cases graph
    fig = px.line(df2,x=df2["Date"], y=dffd.loc[0],
                  hover_data={"Date"},
                  title='Cases By Country',
                  labels={"y": "No. of Cases"}
                  )
    
    # Prepare deaths graphing data
    dff=df6.loc[df6['Country/Region'] == dropdown2]
    dff=dff.reset_index()
    dff=dff.rename_axis(None, axis=1)
    dff=dff.drop(['index','Country/Region'],axis=1)
    
    # Plot deaths graph
    fig2 = px.line(df7,x=df7["Date"], y=dff.loc[0],
                  hover_data={"Date"},
                  title='Deaths By Country',
                  labels={"y": "No. of Deaths"}
                  )
    
    return fig,fig2

@app.callback(
    Output("choropleth", "figure"),
    [Input('dropdown3', 'value'),
     ])

def display_map(dropdown3):
    
    if dropdown3=='Cases':
        fig3 = go.Figure(data=go.Choropleth(
            locations = case_map['CODE'],
            z = case_map['Total Cases'],
            text = case_map['Country/Region'],
            colorscale = 'Blues',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_title = 'Total Cases',
            ))

        fig3.update_layout(
            title_text='Cumulative Cases per Country',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations = [dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
                    JHU CSSE COVID-19 Data</a>',
                showarrow = False
                    )]
                )
    else:
            fig3 = go.Figure(data=go.Choropleth(
                locations = death_map['CODE'],
                z = death_map['Total Deaths'],
                text = death_map['Country/Region'],
                colorscale = 'Reds',
                autocolorscale=False,
                reversescale=False,
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_title = 'Total Cases',
                    ))

            fig3.update_layout(
                title_text='Cumulative Deaths per Country',
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
                annotations = [dict(
                    x=0.55,
                    y=0.1,
                    xref='paper',
                    yref='paper',
                    text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
                        JHU CSSE COVID-19 Data</a>',
                    showarrow = False
                    )]
                    )
        
    return fig3
    
    


    
app.run_server(debug=True)

