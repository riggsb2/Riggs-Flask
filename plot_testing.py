#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 08:11:55 2017

@author: riggs
"""

from bokeh.plotting import figure,show
from bokeh.models import DatetimeTickFormatter,Plot
from math import pi

import pandas as pd
import requests
import simplejson as json


Quandl = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=Pmcp5Sx6Juhs4MyAyhUU'
Quandl_csv = 'WIKI-PRICES-sample.csv'

df = pd.DataFrame.from_csv(Quandl_csv)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date'])

ticker ='A'

subset = df.loc[ticker]

#Plots selected company ID
x = subset['date']
y = subset['close']
y2 = subset['high']

print(subset.head())
p = figure(plot_width = 300, plot_height = 300)
p.multi_line(xs = [x,x], ys=[y,y2])
p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
p.xaxis.major_label_orientation = pi/4
show(p)