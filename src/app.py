import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 
import os
from prophet import Prophet

pwd=os.getcwd()


# DATA PREPERATION
# Read data for maps
case_map =pd.read_excel(pwd+"\\..\\data\\casemapdata.xlsx")
death_map =pd.read_excel(pwd+"\\..\\data\\deathmapdata.xlsx")


# Read cases line plot and predicted data
case_preds=pd.read_csv(pwd+"\\..\\data\\casepredictions.csv")
cases=pd.read_excel(pwd+"\\..\\data\\cases_plot.xlsx")

# Read deaths line plot and predicted data
death_preds=pd.read_csv(pwd+"\\..\\data\\deathpredictions.csv")
deaths=pd.read_excel(pwd+"\\..\\data\\deaths_plot.xlsx")


# GLOBAL VARIABLES DECLARATION

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

fig = go.Figure()
fig2=go.Figure()
fig3=go.Figure()

m = Prophet(interval_width=0.95, daily_seasonality=True)
n = Prophet(interval_width=0.95, daily_seasonality=True)

app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    ])

index_page = html.Div([
    #dcc.Link('Home', href='/page-1'),
    html.H1('Global Caseload and Mortality by Country',
            style={'textAlign':'center'}),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/page-1'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    html.Br(),
    html.Br(),
    
     dcc.Dropdown(
        id='dropdown3',
        value = 'Cases',
        options=[
            {'label': 'See Global Cases', 'value': 'Cases'},
            {'label': 'See Global Mortality', 'value': 'Deaths'}],
            style={'textAlign': 'center',
            'width':'50%',
            'margin-left': 'auto',
            'margin-right': 'auto'
            }
            ),
     
    html.Br(),
    html.Br(),
    html.Br(),
    
    dcc.Graph(id="choropleth", figure=fig3,
                style={'width':'75%',
               'margin-left': 'auto',
               'margin-right': 'auto' }),
    
    html.Br(),
    
    
])

page_1_layout = html.Div([
    html.H1('Cases and Deaths by Country',
        style={'textAlign':'center'}),
    html.Br(),
    
    dcc.Link('Home', href='/index_page'),
    html.Br(),
    dcc.Link('Generate Report', href='/page-2'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    
    html.Br(),
    html.Br(),
    
    html.Div([
    dcc.Dropdown(
        id='dropdown1',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in cases.columns[1:]],
        style={'width': '50%',
                'margin-left': 'auto',
                'margin-right': 'auto'}),
    
    dcc.Graph(id='graph1'),
     html.Div(id='dd-output-container1'),],
     style={'width': '50%','display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='dropdown2',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in deaths.columns[1:]],
        style={'width': '50%',
                'margin-left': 'auto',
                'margin-right': 'auto'}),
    
    dcc.Graph(id='graph2'),
    
    html.Div(id='dd-output-container')],
    style={'width': '50%', 'display': 'inline-block'})
])



page_2_layout = html.Div([
    html.Br(),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Home', href='/'),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/page-1'),
    html.Br(),
    dcc.Link('Predict', href='/page-3'),
    html.Br(),
    html.H1('Reports'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Button("Download Report", id="btn_doc"),
    dcc.Download(id="download-doc")
    
])

# Page 3, for predictions
page_3_layout = html.Div([
    html.H1('Predict Cases and Deaths by Country',
        style={'textAlign':'center'}),
    html.Br(),
    
    dcc.Link('Home', href='/index_page'),
    html.Br(),
    dcc.Link('Download Report', href='/page-2'),
    html.Br(),
    dcc.Link('Cases and Deaths by Country', href='/page-3'),
    
    html.Br(),
    html.Br(),
    
    html.Div([
    dcc.Dropdown(
        id='dropdown4',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in cases.columns[1:]],
        style={'width': '50%',
                'margin-left': 'auto',
                'margin-right': 'auto'}),
    
    dcc.Graph(id='graph4'),
     html.Div(id='dd-output-container1'),],
     style={'width': '50%','display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='dropdown5',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in deaths.columns[1:]],
        style={'width': '50%',
                'margin-left': 'auto',
                'margin-right': 'auto'}),
    
    dcc.Graph(id='graph5'),
    
    html.Div(id='dd-output-container')],
    style={'width': '50%', 'display': 'inline-block'})
])



# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

@app.callback(
    [Output("graph1", "figure"),Output("graph2","figure")],
    [Input('dropdown1', 'value'),
     Input('dropdown2', 'value')
     ])


def display_graph(dropdown1,dropdown2):
    
    # Prepare cases graphing data
    plot_data_cases=cases[['Date',dropdown1]]

    # Plot cases graph
    fig = px.line(plot_data_cases,x=plot_data_cases["Date"], y=plot_data_cases[dropdown1],
                  hover_data={"Date"},
                  title='Cases By Country',
                  labels={"y": "No. of Cases"}
                  )
    
    # Prepare deaths graphing data
    plot_data_deaths=deaths[['Date',dropdown2]]
    
    # Plot deaths graph
    fig2 = px.line(plot_data_deaths,x=plot_data_deaths["Date"], y=plot_data_deaths[dropdown2],
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
    

@app.callback(
    Output("download-doc", "data"),
    Input("btn_doc", "n_clicks"),
    prevent_initial_call=True,
)
def download_doc(n_clicks):
    return dcc.send_file(
        "testpdf.pdf"
    )


# Callback for predictions
@app.callback(
    [Output("graph4", "figure"),Output("graph5","figure")],
    [Input('dropdown4', 'value'),
    Input('dropdown5', 'value')
     ])

def prediction_cases(dropdown4,dropdown5):
    
    # Filter cases prediction data
    predict_data_cases=case_preds[['Date',dropdown4]]

    # Plot Cases predictions
    fig7 = go.Figure(data=[go.Table(
            header=dict(values=list(['Date','Cases']),
                fill_color='paleturquoise',
                align='left'),
            cells=dict(values=[predict_data_cases['Date'], predict_data_cases[dropdown4].astype(int)],
               fill_color='lavender',
               align='left'))
            ])
    
    # Filter deaths prediction data
    predict_data_deaths=death_preds[['Date',dropdown5]]

    # Plot Deaths predictions
    fig8 = go.Figure(data=[go.Table(
            header=dict(values=list(['Date','Deaths']),
                fill_color='paleturquoise',
                align='left'),
            cells=dict(values=[predict_data_deaths['Date'], predict_data_deaths[dropdown5].astype(int)],
               fill_color='lavender',
               align='left'))
            ])

    return fig7, fig8
    

    
app.run_server(debug=True)

