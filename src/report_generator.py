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
                showarrow = False
                        )]
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
  
    plt.figure(figsize=(9,6))
    # Time series plot with Seaborn lineplot()
    fig3= sns.lineplot(x=trend_c["Date"], y=trend_c['Global Cases'],data=trend_c,
                ci=None)
    # axis labels
    plt.xlabel("Date", size=14)
    plt.ylabel("Daily New Cases", size=14)
    plt.grid()
    # save image as PNG file
    plt.savefig("fig3.png",
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
    plt.savefig("fig4.png",
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

    fig1.write_image("fig1.png")
    fig2.write_image("fig2.png")
    fig5.write_image("fig5.png")
    fig6.write_image("fig6.png")

# Function to group data by region
def regions_group(case_map,death_map):
    # Group total cases by region
    regions= [['Afghanistan', 'Asia'], ['Albania', 'Europe'], ['Algeria', 'Africa'], ['Andorra', 'Europe'], ['Angola', 'Africa'], ['Antigua and Barbuda', 'North America'], ['Argentina', 'South America'], ['Armenia', 'Europe'], ['Australia', 'Australia and Oceania'], ['Austria', 'Europe'], ['Azerbaijan', 'Europe'], ['Bahamas', 'North America'], ['Bahrain', 'Asia'], ['Bangladesh', 'Asia'], ['Barbados', 'North America'], ['Belarus', 'Europe'], ['Belgium', 'Europe'], ['Belize', 'North America'], ['Benin', 'Africa'], ['Bhutan', 'Asia'], ['Bolivia', 'South America'], ['Bosnia and Herzegovina', 'Europe'], ['Botswana', 'Africa'], ['Brazil', 'South America'], ['Brunei', 'Asia'], ['Bulgaria', 'Europe'], ['Burkina Faso', 'Africa'], ['Burma', 'Asia'], ['Burundi', 'Africa'], ['Cabo Verde', 'Africa'], ['Cambodia', 'Asia'], ['Cameroon', 'Africa'], ['Canada', 'North America'], ['Central African Republic', 'Africa'], ['Chad', 'Africa'], ['Chile', 'South America'], ['China', 'Asia'], ['Colombia', 'South America'], ['Comoros', 'Africa'], ['Congo (Brazzaville)', 'Africa'], ['Congo (Kinshasa)', 'Africa'], ['Costa Rica', 'North America'], ["Cote d'Ivoire", 'Africa'], ['Croatia', 'Europe'], ['Cuba', 'South America'], ['Cyprus', 'Europe'], ['Czechia', 'Europe'], ['Denmark', 'Europe'], ['Djibouti', 'Africa'], ['Dominica', 'North America'], ['Dominican Republic', 'North America'], ['Ecuador', 'South America'], ['Egypt', 'Africa'], ['El Salvador', 'South America'], ['Equatorial Guinea', 'Africa'], ['Eritrea', 'Africa'], ['Estonia', 'Europe'], ['Eswatini', 'Africa'], ['Ethiopia', 'Africa'], ['Fiji', 'Australia and Oceania'], ['Finland', 'Europe'], ['France', 'Europe'], ['Gabon', 'Africa'], ['Gambia', 'Africa'], ['Georgia', 'Europe'], ['Germany', 'Europe'], ['Ghana', 'Africa'], ['Greece', 'Europe'], ['Grenada', 'North America'], ['Guatemala', 'South America'], ['Guinea', 'Africa'], ['Guinea-Bissau', 'Africa'], ['Guyana', 'South America'], ['Haiti', 'North America'], ['Honduras', 'South America'], ['Hungary', 'Europe'], ['Iceland', 'Europe'], ['India', 'Asia'], ['Indonesia', 'Asia'], ['Iran', 'Asia'], ['Iraq', 'Asia'], ['Ireland', 'Europe'], ['Israel', 'Asia'], ['Italy', 'Europe'], ['Jamaica', 'North America'], ['Japan', 'Asia'], ['Jordan', 'Asia'], ['Kazakhstan', 'Asia'], ['Kenya', 'Africa'], ['Kiribati', 'Australia and Oceania'], ['Korea, South', 'Asia'], ['Kosovo', 'Europe'], ['Kuwait', 'Asia'], ['Kyrgyzstan', 'Asia'], ['Laos', 'Asia'], ['Latvia', 'Europe'], ['Lebanon', 'Asia'], ['Lesotho', 'Africa'], ['Liberia', 'Africa'], ['Libya', 'Africa'], ['Liechtenstein', 'Europe'], ['Lithuania', 'Europe'], ['Luxembourg', 'Europe'], ['Madagascar', 'Africa'], ['Malawi', 'Africa'], ['Malaysia', 'Asia'], ['Maldives', 'Asia'], ['Mali', 'Africa'], ['Malta', 'Europe'], ['Marshall Islands', 'Australia and Oceania'], ['Mauritania', 'Africa'], ['Mauritius', 'Africa'], ['Mexico', 'North America'], ['Moldova', 'Europe'], ['Monaco', 'Europe'], ['Mongolia', 'Asia'], ['Montenegro', 'Europe'], ['Morocco', 'Africa'], ['Mozambique', 'Africa'], ['Namibia', 'Africa'], ['Nepal', 'Asia'], ['Netherlands', 'Europe'], ['New Zealand', 'Australia and Oceania'], ['Nicaragua', 'North America'], ['Niger', 'Africa'], ['Nigeria', 'Africa'], ['Norway', 'Europe'], ['Oman', 'Asia'], ['Pakistan', 'Asia'], ['Palau', 'Australia and Oceania'], ['Panama', 'North America'], ['Papua New Guinea', 'Australia and Oceania'], ['Paraguay', 'South America'], ['Peru', 'South America'], ['Philippines', 'Asia'], ['Poland', 'Europe'], ['Portugal', 'Europe'], ['Qatar', 'Asia'], ['Romania', 'Europe'], ['Russia', 'Europe'], ['Rwanda', 'Africa'], ['Saint Kitts and Nevis', 'North America'], ['Saint Lucia', 'North America'], ['Saint Vincent and the Grenadines', 'North America'], ['Samoa', 'Australia and Oceania'], ['San Marino', 'Europe'], ['Sao Tome and Principe', 'Africa'], ['Saudi Arabia', 'Asia'], ['Senegal', 'Africa'], ['Serbia', 'Europe'], ['Seychelles', 'Africa'], ['Sierra Leone', 'Africa'], ['Singapore', 'Asia'], ['Slovakia', 'Europe'], ['Slovenia', 'Europe'], ['Solomon Islands', 'Australia and Oceania'], ['Somalia', 'Africa'], ['South Africa', 'Africa'], ['South Sudan', 'Africa'], ['Spain', 'Europe'], ['Sri Lanka', 'Asia'], ['Sudan', 'Africa'], ['Suriname', 'South America'], ['Sweden', 'Europe'], ['Switzerland', 'Europe'], ['Syria', 'Asia'], ['Taiwan*', 'Asia'], ['Tajikistan', 'Asia'], ['Tanzania', 'Africa'], ['Thailand', 'Asia'], ['Timor-Leste', 'Asia'], ['Togo', 'Africa'], ['Trinidad and Tobago', 'North America'], ['Tunisia', 'Africa'], ['Turkey', 'Europe'], ['US', 'North America'], ['Uganda', 'Africa'], ['Ukraine', 'Europe'], ['United Arab Emirates', 'Asia'], ['United Kingdom', 'Europe'], ['Uruguay', 'South America'], ['Uzbekistan', 'Asia'], ['Vanuatu', 'Australia and Oceania'], ['Venezuela', 'South America'], ['Vietnam', 'Asia'], ['West Bank and Gaza', 'Asia'], ['Yemen', 'Asia'], ['Zambia', 'Africa'], ['Zimbabwe', 'Africa']]
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
    pg2_cases=global_plot_data_cases['Global Cases'].sum()
    pg2_deaths=global_plot_data_deaths['Global Deaths'].sum()

    pg3_africa_case=grouped_cases.loc['Africa']
    pg3_africa_death=grouped_deaths.loc['Africa']
    
    pg3_europe_case=grouped_cases.loc['Europe']
    pg3_europe_death=grouped_deaths.loc['Europe']

    pg3_asia_case=grouped_cases.loc['Asia']
    pg3_asia_death=grouped_deaths.loc['Asia']

    pg3_na_case=grouped_cases.loc['North America']
    pg3_na_death=grouped_deaths.loc['North America']

    pg3_sa_case=grouped_cases.loc['South America']
    pg3_sa_death=grouped_deaths.loc['South America']

    pg3_au_case=grouped_cases.loc['Australia and Oceania']
    pg3_au_death=grouped_deaths.loc['Australia and Oceania']

    pg4_cases=global_plot_data_cases['Global Cases'].tail(14).reset_index().drop(columns=['index'])
    pg4_cases1=pg4_cases.loc[0]
    pg4_cases2=pg4_cases.iloc[-1]
    pg4_cases_per=((pg4_cases2 - pg4_cases1)/pg4_cases1)*100

    pg4_deaths=global_plot_data_deaths['Global Deaths'].tail(14).reset_index().drop(columns=['index'])
    pg4_deaths1=pg4_deaths.loc[0]
    pg4_deaths2=pg4_deaths.iloc[-1]
    pg4_deaths_per=((pg4_deaths2 - pg4_deaths1)/pg4_deaths1)*100

    return pg2_cases, pg2_deaths, pg3_africa_case, pg3_africa_death, pg3_europe_case,pg3_europe_death, pg3_asia_case, pg3_asia_death, pg3_na_case, pg3_na_death,pg3_sa_case, pg3_sa_death,  pg3_au_case, pg3_au_death, pg4_cases1, pg4_cases2, pg4_cases_per, pg4_deaths1,pg4_deaths2, pg4_deaths_per

# Call create_vars()
paragraph_vars(global_plot_data_cases, global_plot_data_deaths, grouped_cases, grouped_deaths)

# Call create_figures()
create_figures(trend_c,trend_d,grouped_cases,grouped_deaths)



WIDTH = 210
HEIGHT = 297

pdf = FPDF() # A4 (210 by 297 mm)

pdf.add_page()
pdf.image("fig1.png")
pdf.image("fig2.png")

pdf.add_page()
pdf.image("fig3.png", 0, 0, WIDTH)
pdf.image("fig4.png", 0, 0, WIDTH)

pdf.output('testpdf.pdf', 'F')