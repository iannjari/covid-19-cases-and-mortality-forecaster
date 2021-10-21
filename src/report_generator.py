# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:49:53 2021

@author: ianmo
"""

import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from fpdf import FPDF
import matplotlib as plt

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


# Create data for plotting last 7 days deaths globally
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

def create_figures(trend_c,trend_d):
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
            text='Source: <a href="https://github.com/CSSEGISandData/COVID-19">\
                JHU CSSE COVID-19 Data</a>',
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
    
    fig3 = px.line(trend_c,x=trend_c["Date"], y=trend_c['Global Cases'],
                  
                  title='Global Cases Trend',
                  labels={"y": "No. of Cases"}
                  ) 
    
    fig4 = px.line(trend_d,x=trend_d["Date"], y=trend_d['Global Deaths'],
                  
                  title='Global Deaths Trend',
                  labels={"y": "No. of Deaths"}
                  )
    
        
    fig1.write_image("fig1.png")
    fig2.write_image("fig2.png")
    fig3.write_image("fig3.png")
    fig4.write_image("fig4.png")


create_figures(trend_c,trend_d)



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