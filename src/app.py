import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go 
import os
import smtplib
from smtplib import *
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import DNS
from validate_email import validate_email
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

# Read Vaccinations data
vaccines=pd.read_csv(pwd+'\\..\\data\\vaccinations.csv')

# GLOBAL VARIABLES DECLARATION

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

fig3=go.Figure()


app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    ])

index_page = html.Div([
    html.H1('Global Caseload and Mortality by Country',
            style={'textAlign':'center'}),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/compare'),
    html.Br(),
    html.Br(),
    dcc.Link('Download Report', href='/report'),
    html.Br(),
    html.Br(),
    dcc.Link('Predictions', href='/predict'),
    html.Br(),
    html.Br(),
    dcc.Link('Kenya Vaccinations by County/Region', href='/vaccines'),
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
            },
            clearable=False
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
    
    dcc.Link('Global Caseload and Mortality by Country', href='/index_page'),
    html.Br(),
    html.Br(),
    dcc.Link('Download Report', href='/report'),
    html.Br(),
    html.Br(),
    dcc.Link('Predictions', href='/predict'),
    html.Br(),
    html.Br(),
    dcc.Link('Kenya Vaccinations by County/Region', href='/vaccines'),
    html.Br(),
    html.Br(),
    
    html.Div([
    dcc.Dropdown(
        id='dropdown1',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in cases.columns[1:]],
        style={'width': '40%',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'bottom': '2px'},
        clearable=False),

    dcc.Dropdown(
        id='dropdown6',
        value = 'Kenya',
        options=[{'label': i, 'value': i} for i in cases.columns[1:]],
        style={'width': '40%',
                'margin-left': 'auto',
                'margin-right': 'auto'},
        clearable=False),
    
    dcc.Graph(id='graph1'),
     html.Div(id='dd-output-container1'),],
     style={'width': '50%','display': 'inline-block'}),
    html.Div([
    dcc.Dropdown(
        id='dropdown2',
        value = 'Afghanistan',
        options=[{'label': i, 'value': i} for i in deaths.columns[1:]],
        style={'width': '40%',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'bottom': '2px'},
        clearable=False),
    dcc.Dropdown(
        id='dropdown7',
        value = 'Kenya',
        options=[{'label': i, 'value': i} for i in deaths.columns[1:]],
        style={'width': '40%',
                'margin-left': 'auto',
                'margin-right': 'auto'},
        clearable=False),
    
    dcc.Graph(id='graph2'),
    
    html.Div(id='dd-output-container')],
    style={'width': '50%', 'display': 'inline-block'})
])


page_2_layout = html.Div([
    html.Br(),
    html.Br(),
    html.H1('Download or Mail Report',style={'textAlign':'center'}),
    dcc.Link('Global Caseload and Mortality', href='/'),
    html.Br(),
    html.Br(),
    dcc.Link('Cases and Deaths By Country', href='/compare'),
    html.Br(),
    html.Br(),
    dcc.Link('Predictions', href='/predict'),
    html.Br(),
    html.Br(),
    dcc.Link('Kenya Vaccinations by County/Region', href='/vaccines'),
    html.Br(),
    html.P('Download the latest COVID-19  report by clicking the button below;',style={'textAlign':'center'}),
    html.Br(),
    html.Div(
    [html.Button("Download Report", id="btn_doc"),
    dcc.Download(id="download-doc")],style={'textAlign':'center'}),
    html.Br(),
    html.P('To have the report automatically sent to you via email, enter your email address below then click Submit Email.',style={'textAlign':'center'}),
    html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='email',value=""),style={'textAlign':'center'}),
    html.Br(),
    html.Div(
    html.Button('Submit Email', id='submit-val', n_clicks=0),style={'textAlign':'center'}),
    html.Br(),
    html.Div(id='email-string',style={'textAlign':'center'})
    ])
])

# Page 3, for predictions
page_3_layout = html.Div([
    html.H1('Predict Cases and Deaths by Country',
        style={'textAlign':'center'}),
    html.Br(),
    
    dcc.Link('Global Caseload and Mortality by Country', href='/index_page'),
    html.Br(),
    html.Br(),
    dcc.Link('Compare Cases and Deaths by Country', href='/compare'),
    html.Br(),
    html.Br(),
    dcc.Link('Download Report', href='/report'),
    html.Br(),
    html.Br(),
    dcc.Link('Kenya Vaccinations by County/Region', href='/vaccines'),
    html.Br(),
    html.Br(),
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

page_4_layout=html.Div(
    [html.Br(),
    html.H1('Kenya Vaccinations by County and Region',style={'textAlign':'center'}),
    html.Br(),
    html.Br(),
    dcc.Link('Global Caseload and Mortality by Country', href='/index_page'),
    html.Br(),
    html.Br(),
    dcc.Link('Compare Cases and Deaths by Country', href='/compare'),
    html.Br(),
    html.Br(),
    dcc.Link('Download Report', href='/report'),
    html.Br(),
    html.Br(),
    dcc.Link('Predictions', href='/predict'),
    html.Br(),
    html.Br(),
    dcc.RadioItems(id='radio-button',options=[{'label': 'Region', 'value': 'r'},
                                              {'label': 'County', 'value': 'c'}
                                        ],
                                        value='r'),
    html.Br(),
    html.Br(),
    dcc.Graph(id='vaccines-graph')
    ])


# Update the pages index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/compare':
        return page_1_layout
    elif pathname == '/report':
        return page_2_layout
    elif pathname == '/predict':
        return page_3_layout
    elif pathname=='/vaccines':
        return page_4_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

@app.callback(
    Output("graph1", "figure"),
    Input('dropdown6', 'value'),
    Input('dropdown1','value')
        )


def display_graph1(dropdown1,dropdown6):
    
    # Plot cases graph
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cases['Date'],y=cases[dropdown1],name=dropdown1))
    fig.add_trace(go.Scatter(x=cases['Date'],y=cases[dropdown6],name=dropdown6))
    fig.update_layout( title="Caseload", xaxis_title="Dates", yaxis_title="Cases")
    
    return fig

@app.callback(
    Output("graph2","figure"),
    [Input('dropdown2', 'value'),
    Input('dropdown7', 'value')])

def display_graph2(dropdown2,dropdown7): 
    # Plot deaths graph
    fig2=go.Figure()
    fig2.add_trace(go.Scatter(x=deaths['Date'],y=deaths[dropdown2],mode='lines',name=dropdown2,line=dict(color='#00ff7f')))
    fig2.add_trace(go.Scatter(x=deaths['Date'],y=deaths[dropdown7],mode='lines',name=dropdown7,line=dict(color='#800080')))
    fig2.update_layout( title="Mortality", xaxis_title="Dates", yaxis_title="Deaths")
    
    return fig2

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
    return dcc.send_file(pwd+"\\..\\data\\report.pdf")


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


# Email callback
@app.callback(
    Output('email-string', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)


def email(n_clicks,value):
    email_string=""
    if value !="":
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
        # pass the regular expression and the string into the fullmatch() method
        # check whether the email exists
        if(re.fullmatch(regex, value)) and validate_email(value,verify=True):
 
            if n_clicks>0:
                try:
                    # Validate  and save email address
                    EMAIL_ADDRESS = "iannjari@gmail.com"
                    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

                    sender_address = EMAIL_ADDRESS
                    receiver_address = value
                    mail_content = '''Hello,

Here is today's Covid report.
If you did not request this mail, kindly ignore it!
                        
Thank you!
                    '''

                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = "COVID-19 REPORT"
                        

                    message.attach(MIMEText(mail_content, 'plain'))
                    attach_file_name = pwd+"\\..\\data\\report.pdf"
                    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
                    payload = MIMEBase('application', 'octate-stream')
                    payload.set_payload((attach_file).read())
                    encoders.encode_base64(payload) #encode the attachment
                    #add payload header with filename
                    payload.add_header('Content-Disposition', 'attachment', filename='report.pdf')
                    message.attach(payload)

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                        smtp.send_message(message)

                    email_string="An email with the report has been sent and your email address saved to our list."
                    email_list=pd.read_csv(pwd+'\\..\\data\\emaillist.csv')
                    email_list=email_list['Address']
                    if value not in email_list:
                        value=pd.Series(value)
                        email_list=email_list.append(value, ignore_index = True)
                        email_list=pd.DataFrame(email_list)
                        email_list=email_list.rename(columns={0:'Address'})
                        email_list.to_csv(pwd+'\\..\\data\\emaillist.csv')


                except SMTPRecipientsRefused:
                    email_string= str("The email address you entered may not exist! Please check it again and retry.")
                except SMTPServerDisconnected:
                    email_string=str('The server unexpectedly disconnected, or an attempt \n'
                    'was made to use the SMTP instance before connecting it to a server. Try again later')
                except SMTPSenderRefused:
                    email_string='Sender address refused.'
                except SMTPConnectError:
                    email_string='An error occurred during establishment of a connection with the server.'
                except SMTPAuthenticationError:
                    email_string='An Authentication Error occured'
            else:
                email_string=""
        else:
            email_string="Invalid Email. Check whether you have typed the address correctly."
        
    else:
        if n_clicks>0:
            email_string="Please enter an address!"
    return email_string  

# Vaccinations callback
@app.callback(
    Output('vaccines-graph','figure'),
    Input('radio-button','value')
)

def vaccinations(value):
    if value =='c':
        fig9 = go.Figure(go.Bar(
            y=vaccines['County'].values[::-1],
            x=vaccines['Vaccinations'].values[::-1],
            orientation='h'))

    else:
        df=vaccines.groupby(['Region']).sum()
        df=df.reset_index()
        fig9=go.Figure(go.Bar(
            y=df['Region'].values[::-1],
            x=vaccines['Vaccinations'].values[::-1],
            orientation='h'))
        
    return fig9
app.run_server(debug=True)

