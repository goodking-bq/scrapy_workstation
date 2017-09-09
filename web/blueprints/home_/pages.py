# coding:utf-8
from __future__ import absolute_import, unicode_literals
from web.extension import mongo
from flask import jsonify, url_for, render_template
import plotly
import pandas as pd
import plotly.graph_objs as go
import plotly.grid_objs
import random

__author__ = "golden"
__date__ = '2017/6/21'


def index():
    return render_template('base.html')


def proxy():
    """随机获取一个代理"""
    proxys = mongo.db.proxy.find({'checked': 1})
    proxy = random.choice(list(proxys))
    proxy_type = 'http'
    try:
        proxy_type = 'https' if proxy['is_ssl'] else 'http'
    except:
        pass
    return jsonify(
        dict(ip=proxy['ip'], port=proxy['port'], proxy='%s:%s' % (proxy['ip'], proxy['port']), proxy_type=proxy_type))


def day_new():
    sites = ['fang', 'lianjia', 'anjuke']
    traces = []
    for s in sites:
        _data = mongo.db.day_increase.find({"domain": s})
        df = pd.DataFrame([[d['publish_date'], int(d['count'])] for d in _data])
        if not df.empty:
            df = df.rename(columns={0: 'publish_date', 1: 'count'})
            trace = go.Scatter(x=df['publish_date'], y=df['count'], mode='lines+markers', name=s,
                               line=dict(shape='spline'), )
            traces.append(trace)
    layout = go.Layout(
        xaxis=dict(title='日期', calendar='%Y-%m-%d', tickformat='%Y-%m-%d', tickwidth=5, tickcolor='red', ticklen=2,
                   showline=False, showgrid=True, spikethickness=True,
                   autorange=True, ticksuffix=True),
        yaxis=dict(title='条数'),
        title='新发布二手房源',
        showlegend=True, autosize=True
    )
    data = go.Data(traces)
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig, show_link=False, output_type="div", image='png',
                              link_text=False, include_plotlyjs=False)
    return div


def day_average_price():
    sites = ['fang', 'lianjia', 'anjuke']
    traces = []
    for s in sites:
        _data = mongo.db.average_price_day.find({"domain": s})
        df = pd.DataFrame([[d['publish_date'], d['average']] for d in _data])
        if not df.empty:
            df = df.rename(columns={0: 'publish_date', 1: 'average'})
            trace = go.Scatter(x=df['publish_date'], y=df['average'], mode='lines+markers', name=s,
                               line=dict(shape='spline'), )
            traces.append(trace)
    layout = go.Layout(
        xaxis=dict(title='日期', calendar='%Y-%m-%d', tickformat='%Y-%m-%d', tickwidth=5, tickcolor='red', ticklen=2,
                   showline=False, showgrid=True, spikethickness=True,
                   autorange=True, ticksuffix=True),
        yaxis=dict(title='价格(元)'),
        title='新发布二手房源',
        showlegend=True, autosize=True
    )
    data = go.Data(traces)
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig, show_link=False, output_type="div", image='png',
                              link_text=False, include_plotlyjs=False)
    return div
