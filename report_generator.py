# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:49:53 2021

@author: ianmo
"""

import os
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

pwd=os.getcwd()

# Read data for maps
case_map =pd.read_excel(pwd+"\\casemapdata.xlsx")
death_map =pd.read_excel(pwd+"\\deathmapdata.xlsx")

# Read data for global trends
global_plot_data_cases=pd.read_excel(pwd+"\\cases_plot.xlsx")
global_plot_data_deaths=pd.read_excel(pwd+"\\deaths_plot.xlsx")

trend_c=global_plot_data_cases[['Date','Global Cases']]
trend_d=global_plot_data_deaths[['Date','Global Deaths']]

fig1=go.Figure()
fig2=go.Figure()

def create_figures():
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
    
        
    return fig1,fig2,fig3,fig4




    