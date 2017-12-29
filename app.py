#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 09:18:30 2017

@author: riggs
"""

from flask import Flask,render_template,request

from bokeh.plotting import figure,show,output_file
from bokeh.models import DatetimeTickFormatter

from math import pi

import pandas as pd
#import requests
#import simplejson as json

app = Flask(__name__)

Quandl = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=Pmcp5Sx6Juhs4MyAyhUU'
Quandl_csv = 'WIKI-PRICES-sample.csv'

df = pd.DataFrame.from_csv(Quandl_csv)
df['date'] = pd.to_datetime(df['date'])

@app.route('/index',methods =['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('Start.html')
    else:
        ticker = request.form['ticker']
        
        try:
            subset = df.loc[ticker]
            subset = subset.sort_values(by=['date'])
        except:
            return render_template('Start.html')
        
        x = subset['date']
        
        xs = []
        ys = []
        colors = []
        labels = []
        
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
            #p.multi_line(xs, ys)
            p.legend.location = "top_left"
            p.xaxis.major_label_orientation = pi/4
            p.xaxis.formatter=DatetimeTickFormatter(
                                                    hours=["%d %B %Y"],
                                                    days=["%d %B %Y"],
                                                    months=["%d %B %Y"],
                                                    years=["%d %B %Y"],
                                                )
    
            output_file("Plot.html", title="Ticker Plot")
            show(p)
        else:
            return render_template('Start.html')
        
        return render_template('Start.html')
    
if __name__ == '__main__':
    app.run()