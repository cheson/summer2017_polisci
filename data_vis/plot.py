#!/usr/bin/python

# AUTHOR: JASON CHEN (cheson@stanford.edu)
# DATE: August 15, 2017
# This function is responsible for using the plotly 
# library and the data csv provided through src_csv to
# generate a line plot of the frequency analysis done 
# in the keyword_count_all or percentage_keyword_speech functions.

# References:
# https://plot.ly/python/time-series/
# https://plot.ly/python/reference/#scatter

import plotly
import plotly.graph_objs as go
import pandas as pd
import colorlover as cl # sudo pip install colorlover

############### INPUTS ###############
# src csv to generate graph
src_csv = '../frequency_analysis/outputs/demo.csv'
# chart title
title = "demo"
# date range on chart x-axis in YYYY-MM-DD format
date_min = '2010-01-01'
date_max = '2018-01-01'
# output filename
output_filename = "./plots/demo.html"
# 'colorful' or 'party' palette
palette = 'colorful'
# graphing percentage keyword (alternative is keyword_count_all)
graphing_percentage_keyword = True
################# END #################

df = pd.read_csv(src_csv)
names = df.columns[2:] # 1 is index column and 2 is Date

# 11 color palette : print cl.scales['11']['qual']['Paired']
colorful_palette = ['rgb(166,206,227)', 'rgb(31,120,180)', 'rgb(178,223,138)', 'rgb(51,160,44)', 'rgb(251,154,153)', 'rgb(227,26,28)', 'rgb(253,191,111)', 'rgb(255,127,0)', 'rgb(202,178,214)', 'rgb(106,61,154)', 'rgb(255,255,153)']
# party affiliated palette : blue, red, and green
party_palette = {'democrat': 'rgb(31,120,180)', 'republican':'rgb(227,26,28)', 'other': 'rgb(51,160,44)'}
party_mapping = {'name':'democrat', 'name':'republican'}
# again, hardcoded for the 50 governors dataset. will need to generalize this data for all datasets.
date_mapping = {"kay ivey" : '2017-04-10', "bill walker" : '2014-12-01', "doug ducey" : '2015-01-05', "asa hutchinson" : '2015-01-13', "jerry brown" : '2011-01-03', "john hickenlooper" : '2011-01-11', "dannel malloy" : '2011-01-05', "john carney" : '2017-01-17', "rick scott" : '2011-01-04', "nathan deal" : '2011-01-10', "david ige" : '2014-12-01', "butch otter" : '2007-01-01', "bruce rauner" : '2015-01-12', "eric holcomb" : '2017-01-09', "kim reynolds" : '2017-05-24', "sam brownback" : '2011-01-10', "matt bevin" : '2015-12-08', "john bel edwards" : '2016-01-11', "paul lepage" : '2011-01-05', "larry hogan" : '2015-01-21', "charlie baker" : '2015-01-08', "rick snyder" : '2011-01-01', "mark dayton" : '2011-01-03', "phil bryant" : '2012-01-10', "eric greitens" : '2017-01-09', "steve bullock" : '2013-01-07', "pete ricketts" : '2015-01-08', "brian sandoval" : '2011-01-03', "chris sununu" : '2017-01-05', "chris christie" : '2010-01-19', "susana martinez" : '2011-01-01', "andrew cuomo" : '2011-01-01', "roy cooper" : '2017-01-01', "doug burgum" : '2016-12-15', "john kasich" : '2011-01-10', "mary fallin" : '2011-01-10', "kate brown" : '2015-02-18', "tom wolf" : '2015-01-20', "gina raimondo" : '2015-01-06', "henry mcmaster" : '2017-01-24', "dennis daugaard" : '2011-01-08', "bill haslam" : '2011-01-15', "greg abbott" : '2015-01-20', "gary herbert" : '2009-08-11', "phil scott" : '2017-01-05', "terry mcauliffe" : '2014-01-11', "jay inslee" : '2013-01-16', "jim justice" : '2017-01-16', "scott walker" : '2011-01-03', "matt mead" : '2011-01-03'}

data = []
counter = 0
ones = [1] * len(df.Date)
for name in names:
    if "raw_" in name:
        continue
    if palette == 'colorful':
        color = colorful_palette[counter % len(colorful_palette)]
    if palette == 'party':
        color = party_mapping[name]
    hovertext = ""
    visible = True
    if graphing_percentage_keyword == True:
        raw_counts = df["raw_" + name]
        hovertext = raw_counts
        visible = "legendonly"
    trace = go.Scatter(
        x=df.Date,
        y=df[name],
        hovertext=hovertext,
        name = name,
        line = dict(color = color),
        opacity = 0.8,
        visible = visible)
    data.append(trace)
    if "_trend" not in name and graphing_percentage_keyword == True:
        dates = [date_mapping.get(name)] * len(df.Date)
        # dates = [date_mapping.get(name)] * (len(df.Date) / 2)
        # dates += ['2017-04-10'] * (len(df.Date) / 2)
        print dates
        tokens = name.split()
        last_name = tokens[len(tokens)-1]
        trace = go.Scatter(
            x=dates,
            y=1,
            name = last_name + " election date",
            line = dict(color = color, width = 1, dash = "dot"),
            opacity = 0.8,
            hoverinfo = "name",
            hoverlabel = dict(namelength = 100),
            visible = "legendonly")
        data.append(trace)
    counter += 1

y_range = []
if graphing_percentage_keyword:
    y_range = [0, 0.8]

layout = dict(
    title = title,
    xaxis = dict(
        range = [date_min, date_max],
        title = "date range"),
    yaxis = dict (
        range = y_range,
        title = "proportion w/ keywords")
)

fig = dict(data=data, layout=layout)
plotly.offline.plot(fig, filename = output_filename)
