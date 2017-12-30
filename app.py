#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 09:18:30 2017

@author: riggs
"""

import os

from flask import Flask,render_template,request

from bokeh.plotting import figure,show,save
from bokeh.models import DatetimeTickFormatter

from math import pi

import pandas as pd
#import requests
#import simplejson as json

app = Flask(__name__)

Quandl_json = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=Pmcp5Sx6Juhs4MyAyhUU'
#Quandl_csv = 'WIKI-PRICES-sample.csv'
Quandl_csv = "https://www.quandl.com/api/v3/datatables/WIKI/PRICES.csv?api_key=Pmcp5Sx6Juhs4MyAyhUU"

df = pd.DataFrame.from_csv(Quandl_csv)
df['date'] = pd.to_datetime(df['date'])

@app.route('/',methods =['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('Start.html')
    else:
        
        #sets ticker value        
        ticker = request.form['ticker']
        
        #checks to see if ticker is in page else refreshes page
        try:
            subset = df.loc[ticker]
            subset = subset.sort_values(by=['date'])
        except:
            return render_template('Start.html')
        
        #sets up data
        x = subset['date']
        
        xs = []
        ys = []
        colors = []
        labels = []
        
        #checks which boxes are checked and assembled data
        if request.form.get('close'):
            y = subset['close']
            xs.append(x) 
            ys.append(y)
            colors.append('blue')
            labels.append('Closing')
            
        if request.form.get('adj_close'):
            y = subset['adj_close']
            xs.append(x) 
            ys.append(y)
            colors.append('green')
            labels.append('Adjusted Closing')

        if request.form.get('open'):
            y = subset['open']
            xs.append(x) 
            ys.append(y)
            colors.append('red')
            labels.append('Opening')
            
        if request.form.get('adj_open'):
            y = subset['adj_open']
            xs.append(x) 
            ys.append(y)
            colors.append('yellow')
            labels.append('Adjusted Opening')
        
        #plots if data exists else refreshes page          
        if xs and ys:
            title = '%s Prices'%(ticker)
            p = figure(plot_width = 500, plot_height = 500, title = title)
            p.title.text_color = "black"
            p.title.text_font = "times"
            p.title.text_font_style = "italic"
            p.title.align = 'center'
            p.title.text_font_size = '14pt'
      
            for (colr, leg, x, y ) in zip(colors, labels, xs, ys):
                my_plot = p.line(x, y, color= colr, legend= leg)            
            p.legend.location = "top_left"
            p.xaxis.major_label_orientation = pi/4
            p.xaxis.formatter=DatetimeTickFormatter(
                                                    hours=["%d %B %Y"],
                                                    days=["%d %B %Y"],
                                                    months=["%d %B %Y"],
                                                    years=["%d %B %Y"],
                                                )
            p.yaxis.axis_label = "U.S. Dollars"
            p.xaxis.axis_label = "Date"
                    
            #Currently does not update displayed plot when resubmitting
            #Plot.html changes in the file system but isn't displayed
            os.chdir('templates')
            save(p,"Plot.html", title="Ticker Plot")
            os.chdir('..')
            
        else:
            return render_template('Start.html')
        
        return render_template('Plot.html')
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)