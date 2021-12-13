# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:49:53 2021

@author: ianmo
"""

import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import seaborn as sns
from fpdf import FPDF
from datetime import date
import smtplib
from smtplib import *
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

pwd=os.getcwd()

# Read data for maps
case_map =pd.read_excel(pwd+"\\..\\data\\casemapdata.xlsx")
death_map =pd.read_excel(pwd+"\\..\\data\\deathmapdata.xlsx")

# Read data for global trends
global_plot_data_cases=pd.read_excel(pwd+"\\..\\data\\cases_plot.xlsx")
global_plot_data_deaths=pd.read_excel(pwd+"\\..\\data\\deaths_plot.xlsx")

# Create data for plotting last 14 days cases globally
trend_c=global_plot_data_cases[['Date','Global Cases']].tail(15)
trend_c=trend_c.reset_index()
trend_c=trend_c.drop(columns=['index'])
base_no=trend_c.iloc[0]['Global Cases']

y=trend_c['Global Cases']

n=[]
c=base_no
d=base_no
for i in y:
    c=i-d
    d=i
    n.append(c)

list_dataframe = pd.DataFrame(n)
trend_c['Global Cases']=list_dataframe
trend_c=trend_c.tail(14)


# Create data for plotting last 14 days deaths globally
trend_d=global_plot_data_deaths[['Date','Global Deaths']].tail(15)
trend_d=trend_d.reset_index()
trend_d=trend_d.drop(columns=['index'])
base_no=trend_d.iloc[0]['Global Deaths']
w=trend_d['Global Deaths']

m=[]
s=base_no
b=base_no
for i in w:
    s=i-b
    b=i
    m.append(s)

list_dataframe1 = pd.DataFrame(m)
trend_d['Global Deaths']=list_dataframe1
trend_d=trend_d.tail(14)

# Create figures for use in PDF report
def create_figures(trend_c,trend_d,grouped_cases,grouped_deaths):
    fig1 = go.Figure(data=go.Choropleth(
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

    fig1.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
            ),
        )
    
        
    fig2= go.Figure(data=go.Choropleth(
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

    fig2.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
                
                )
  
    plt.figure(figsize=(9,6))
    # Time series plot with Seaborn lineplot()
    fig3= sns.lineplot(x=trend_c["Date"], y=trend_c['Global Cases'],data=trend_c,
                ci=None)
    # axis labels
    plt.xlabel("Date", size=14)
    plt.ylabel("Daily New Cases", size=14)
    plt.grid()
    # save image as PNG file
    plt.savefig(pwd+"\\..\\data\\fig3.png",
                        format='png',
                        dpi=150)
    
    plt.figure(figsize=(9,6))
    fig4 = sns.lineplot(x=trend_d["Date"], y=trend_d['Global Deaths'],data=trend_d,
                ci=None)
    # axis labels
    plt.xlabel("Date", size=14)
    plt.ylabel("Global Deaths", size=14)
    plt.grid()
    # save image as PNG file
    plt.savefig(pwd+"\\..\\data\\fig4.png",
                format='png',
                dpi=150)
    
    # Pie chart for total global cases by region
    grouped_cases=grouped_cases.reset_index()
    labels_c=grouped_cases['Region']
    values_c = grouped_cases['Total Cases']
    # Using `hole` to create a donut-like pie chart
    fig5 = go.Figure(data=[go.Pie(labels=labels_c, values=values_c, hole=.3)])
        
    # Pie chart for total global deaths by region
    grouped_deaths=grouped_deaths.reset_index()
    labels_d=grouped_deaths['Region']
    values_d = grouped_cases['Total Cases']
    # Using `hole` to create a donut-like pie chart
    fig6 = go.Figure(data=[go.Pie(labels=labels_d, values=values_d, hole=.3)])

    fig1.write_image(pwd+"\\..\\data\\fig1.png")
    fig2.write_image(pwd+"\\..\\data\\fig2.png")
    fig5.write_image(pwd+"\\..\\data\\fig5.png")
    fig6.write_image(pwd+"\\..\\data\\fig6.png")

# Function to group data by region
def regions_group(case_map,death_map):
    # Group total cases by region
    regions= [['Afghanistan', 'Asia'], ['Albania', 'Europe'], ['Algeria', 'Africa'], ['Andorra', 'Europe'], ['Angola', 'Africa'], ['Antigua and Barbuda', 'North America'], ['Argentina', 'South America'], ['Armenia', 'Europe'], ['Australia', 'Australia and Oceania'], ['Austria', 'Europe'], ['Azerbaijan', 'Europe'], ['Bahamas', 'North America'], ['Bahrain', 'Asia'], ['Bangladesh', 'Asia'], ['Barbados', 'North America'], ['Belarus', 'Europe'], ['Belgium', 'Europe'], ['Belize', 'North America'], ['Benin', 'Africa'], ['Bhutan', 'Asia'], ['Bolivia', 'South America'], ['Bosnia and Herzegovina', 'Europe'], ['Botswana', 'Africa'], ['Brazil', 'South America'], ['Brunei', 'Asia'], ['Bulgaria', 'Europe'], ['Burkina Faso', 'Africa'], ['Burma', 'Asia'], ['Burundi', 'Africa'], ['Cabo Verde', 'Africa'], ['Cambodia', 'Asia'], ['Cameroon', 'Africa'], ['Canada', 'North America'], ['Central African Republic', 'Africa'], ['Chad', 'Africa'], ['Chile', 'South America'], ['China', 'Asia'], ['Colombia', 'South America'], ['Comoros', 'Africa'], ['Congo (Brazzaville)', 'Africa'], ['Congo (Kinshasa)', 'Africa'], ['Costa Rica', 'North America'], ["Cote d'Ivoire", 'Africa'], ['Croatia', 'Europe'], ['Cuba', 'South America'], ['Cyprus', 'Europe'], ['Czechia', 'Europe'], ['Denmark', 'Europe'], ['Djibouti', 'Africa'], ['Dominica', 'North America'], ['Dominican Republic', 'North America'], ['Ecuador', 'South America'], ['Egypt', 'Africa'], ['El Salvador', 'South America'], ['Equatorial Guinea', 'Africa'], ['Eritrea', 'Africa'], ['Estonia', 'Europe'], ['Eswatini', 'Africa'], ['Ethiopia', 'Africa'], ['Fiji', 'Australia and Oceania'], ['Finland', 'Europe'], ['France', 'Europe'], ['Gabon', 'Africa'], ['Gambia', 'Africa'], ['Georgia', 'Europe'], ['Germany', 'Europe'], ['Ghana', 'Africa'], ['Greece', 'Europe'], ['Grenada', 'North America'], ['Guatemala', 'South America'], ['Guinea', 'Africa'], ['Guinea-Bissau', 'Africa'], ['Guyana', 'South America'], ['Haiti', 'North America'], ['Honduras', 'South America'], ['Hungary', 'Europe'], ['Iceland', 'Europe'], ['India', 'Asia'], ['Indonesia', 'Asia'], ['Iran', 'Asia'], ['Iraq', 'Asia'], ['Ireland', 'Europe'], ['Israel', 'Asia'], ['Italy', 'Europe'], ['Jamaica', 'North America'], ['Japan', 'Asia'], ['Jordan', 'Asia'], ['Kazakhstan', 'Asia'], ['Kenya', 'Africa'], ['Kiribati', 'Australia and Oceania'], ['Korea, South', 'Asia'], ['Kosovo', 'Europe'], ['Kuwait', 'Asia'], ['Kyrgyzstan', 'Asia'], ['Laos', 'Asia'], ['Latvia', 'Europe'], ['Lebanon', 'Asia'], ['Lesotho', 'Africa'], ['Liberia', 'Africa'], ['Libya', 'Africa'], ['Liechtenstein', 'Europe'], ['Lithuania', 'Europe'], ['Luxembourg', 'Europe'], ['Madagascar', 'Africa'], ['Malawi', 'Africa'], ['Malaysia', 'Asia'], ['Maldives', 'Asia'], ['Mali', 'Africa'], ['Malta', 'Europe'], ['Marshall Islands', 'Australia and Oceania'], ['Mauritania', 'Africa'], ['Mauritius', 'Africa'], ['Mexico', 'North America'], ['Moldova', 'Europe'], ['Monaco', 'Europe'], ['Mongolia', 'Asia'], ['Montenegro', 'Europe'], ['Morocco', 'Africa'], ['Mozambique', 'Africa'], ['Namibia', 'Africa'], ['Nepal', 'Asia'], ['Netherlands', 'Europe'], ['New Zealand', 'Australia and Oceania'], ['Nicaragua', 'North America'], ['Niger', 'Africa'], ['Nigeria', 'Africa'], ['Norway', 'Europe'], ['Oman', 'Asia'], ['Pakistan', 'Asia'], ['Palau', 'Australia and Oceania'], ['Panama', 'North America'], ['Papua New Guinea', 'Australia and Oceania'], ['Paraguay', 'South America'], ['Peru', 'South America'], ['Philippines', 'Asia'], ['Poland', 'Europe'], ['Portugal', 'Europe'], ['Qatar', 'Asia'], ['Romania', 'Europe'], ['Russia', 'Europe'], ['Rwanda', 'Africa'], ['Saint Kitts and Nevis', 'North America'], ['Saint Lucia', 'North America'], ['Saint Vincent and the Grenadines', 'North America'], ['Samoa', 'Australia and Oceania'], ['San Marino', 'Europe'], ['Sao Tome and Principe', 'Africa'], ['Saudi Arabia', 'Asia'], ['Senegal', 'Africa'], ['Serbia', 'Europe'], ['Seychelles', 'Africa'], ['Sierra Leone', 'Africa'], ['Singapore', 'Asia'], ['Slovakia', 'Europe'], ['Slovenia', 'Europe'], ['Solomon Islands', 'Australia and Oceania'], ['Somalia', 'Africa'], ['South Africa', 'Africa'], ['South Sudan', 'Africa'], ['Spain', 'Europe'], ['Sri Lanka', 'Asia'], ['Sudan', 'Africa'], ['Suriname', 'South America'], ['Sweden', 'Europe'], ['Switzerland', 'Europe'], ['Syria', 'Asia'], ['Taiwan*', 'Asia'], ['Tajikistan', 'Asia'], ['Tanzania', 'Africa'], ['Thailand', 'Asia'], ['Timor-Leste', 'Asia'], ['Togo', 'Africa'],['Tonga','Australia and Oceania'],['Trinidad and Tobago', 'North America'], ['Tunisia', 'Africa'], ['Turkey', 'Europe'], ['US', 'North America'], ['Uganda', 'Africa'], ['Ukraine', 'Europe'], ['United Arab Emirates', 'Asia'], ['United Kingdom', 'Europe'], ['Uruguay', 'South America'], ['Uzbekistan', 'Asia'], ['Vanuatu', 'Australia and Oceania'], ['Venezuela', 'South America'], ['Vietnam', 'Asia'], ['West Bank and Gaza', 'Asia'], ['Yemen', 'Asia'], ['Zambia', 'Africa'], ['Zimbabwe', 'Africa']]
    regions=pd.DataFrame(regions)
    regions=regions.rename(columns={"Country": "Country/Region",1:"Region",0:"Country/Region"})
    case_by_region_df = pd.merge(case_map,regions, how="left",on=case_map['Country/Region'])
    grouped_cases=pd.DataFrame(case_by_region_df.groupby(['Region']).sum())
    
    # Group total deaths by region
    death_by_region_df = pd.merge(death_map,regions, how="left", on="Country/Region")
    grouped_deaths=pd.DataFrame(death_by_region_df.groupby('Region').sum())

    #return grouped_deaths,grouped_cases
    return grouped_cases,grouped_deaths

# Call regions_group()
grouped_cases,grouped_deaths=regions_group(case_map,death_map)

# Create variables for report paragraphs

def paragraph_vars(global_plot_data_cases, global_plot_data_deaths, grouped_cases, grouped_deaths):
    global pg2_cases, pg2_deaths, pg3_africa_case, pg3_africa_death, pg3_europe_case,pg3_europe_death, pg3_asia_case, pg3_asia_death, pg3_na_case, pg3_na_death,pg3_sa_case, pg3_sa_death,  pg3_au_case, pg3_au_death, pg4_cases1, pg4_cases2, pg4_cases_per, pg4_deaths1,pg4_deaths2, pg4_deaths_per
    pg2_cases=global_plot_data_cases['Global Cases'].sum()
    pg2_deaths=global_plot_data_deaths['Global Deaths'].sum()

    pg3_africa_case=grouped_cases.loc['Africa'].at['Total Cases']
    pg3_africa_death=grouped_deaths.loc['Africa'].at['Total Deaths']
    
    pg3_europe_case=grouped_cases.loc['Europe'].at['Total Cases']
    pg3_europe_death=grouped_deaths.loc['Europe'].at['Total Deaths']

    pg3_asia_case=grouped_cases.loc['Asia'].at['Total Cases']
    pg3_asia_death=grouped_deaths.loc['Asia'].at['Total Deaths']

    pg3_na_case=grouped_cases.loc['North America'].at['Total Cases']
    pg3_na_death=grouped_deaths.loc['North America'].at['Total Deaths']

    pg3_sa_case=grouped_cases.loc['South America'].at['Total Cases']
    pg3_sa_death=grouped_deaths.loc['South America'].at['Total Deaths']

    pg3_au_case=grouped_cases.loc['Australia and Oceania'].at['Total Cases']
    pg3_au_death=grouped_deaths.loc['Australia and Oceania'].at['Total Deaths']

    pg4_cases=global_plot_data_cases['Global Cases'].tail(14).reset_index().drop(columns=['index'])
    pg4_cases1=pg4_cases.loc[0].at['Global Cases']
    pg4_cases2=pg4_cases.iloc[-1].at['Global Cases']
    pg4_cases_per=((pg4_cases2 - pg4_cases1)/pg4_cases1)*100
    pg4_cases_per=str(round(pg4_cases_per, 2))

    pg4_deaths=global_plot_data_deaths['Global Deaths'].tail(14).reset_index().drop(columns=['index'])
    pg4_deaths1=pg4_deaths.loc[0].at['Global Deaths']
    pg4_deaths2=pg4_deaths.iloc[-1].at['Global Deaths']
    pg4_deaths_per=((pg4_deaths2 - pg4_deaths1)/pg4_deaths1)*100
    pg4_deaths_per=str(round(pg4_deaths_per, 2))

# Call create_vars()
paragraph_vars(global_plot_data_cases, global_plot_data_deaths, grouped_cases, grouped_deaths)

# Call create_figures()
create_figures(trend_c,trend_d,grouped_cases,grouped_deaths)



WIDTH = 210
HEIGHT = 297
today = date.today()
#Textual month, day and year	
today= today.strftime("%B %d, %Y")
pdf = FPDF('P', 'mm', (210,296))

emptyline=''

heading11='Total Cases By Country Globally'
figure11=pwd+"\\..\\data\\fig1.png"
line11=f'Total cases recorded globally have now reached {pg2_cases}'
heading12='Total By Country Deaths Globally'
figure12=pwd+"\\..\\data\\fig2.png"
line12=f'Total deaths recorded globally have now reached {pg2_deaths}'

heading31='Composition of Cases by Region'
figure31=pwd+"\\..\\data\\fig5.png"
line31=f'Deaths in Africa are {pg3_africa_case}, Europe {pg3_europe_case}, Asia {pg3_asia_case}, Australia and Oceania {pg3_au_case}'
line33=f'North America {pg3_na_case} and South America {pg3_sa_case} '
heading32='Composition of Deaths by Region'
figure32=pwd+"\\..\\data\\fig6.png"
line32=f'Deaths in Africa are {pg3_africa_death}, Europe {pg3_europe_death}, Asia {pg3_asia_death}, Australia and Oceania {pg3_au_death}'
line34=f'North America {pg3_na_death} and South America {pg3_sa_death} '

heading21='Total New Cases For Last 2 Weeks Globally'
figure21=pwd+"\\..\\data\\fig3.png"
line21=f'Total Global Cases have increased {pg4_cases_per}% from {pg4_cases1} to {pg4_cases2} in the last two weeks'
heading22='Total New Deaths For Last 2 Weeks Globally'
figure22=pwd+"\\..\\data\\fig4.png"
line22=f'Total Global Deaths have increased {pg4_deaths_per}% from {pg4_deaths1} to {pg4_deaths2} in the last two weeks'


pdf.add_page()
pdf.set_font('Arial', '', 24)  
pdf.ln(60)
pdf.write(10, f"Covid Analytics Report")
pdf.ln(10)
pdf.set_font('Arial', '', 16)
pdf.write(4, f'{today}')
pdf.ln(5)

def generate_reports(heading1,figure1,line1,heading2,figure2,line2,line3,line4):
    pdf.add_page()
    pdf.set_font('Arial', '', 15)  
    pdf.cell(10,5,heading1)
    pdf.ln()
    pdf.image(figure1,x=30,y=15,h=90,w=120)
    pdf.ln(95)
    pdf.set_font('Arial', '', 10)
    pdf.cell(10,10,line1)
    pdf.ln()
    pdf.cell(1,1,line3)
    pdf.ln(10)
    pdf.set_font('Arial','',15)
    pdf.cell(10,10,heading2)
    pdf.ln()
    pdf.image(figure2,y=153,x=30,h=90,w=120)
    pdf.ln(100)
    pdf.set_font('Arial', '', 10)
    pdf.cell(10,10,line2)
    pdf.ln()
    pdf.cell(1,1,line4)

def send_mail():
    email_list=pd.read_csv(pwd+'\\..\\data\\emaillist.csv')
    EMAIL_ADDRESS = "iannjari@gmail.com"
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    for address in email_list['Address']:
        
        sender_address = EMAIL_ADDRESS
        receiver_address = address
        mail_content = '''Hello,
                
This is a test mail.
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



generate_reports(heading11,figure11,line11,heading12,figure12,line12,emptyline,emptyline)
generate_reports(heading21,figure21,line21,heading22,figure22,line22,emptyline,emptyline)
generate_reports(heading31,figure31,line31,heading32,figure32,line32,line33,line34)

pdf.output(pwd+'\\..\\data\\report.pdf', 'F')

send_mail()


