import re

from flask import Flask, render_template, request

import pandas as pd
from app import app
import math

stations_df = pd.read_csv('static/stations_prob.tsv', sep='\t', encoding='utf-8')


@app.route('/', methods=['GET'])
def line_select():
    """gen dropdown for selection of mrt line"""
    search_term = request.args.get("line")
    print(search_term)
    lines = stations_df.mrt_line_english.unique().tolist()
    if (search_term is None):
        search_term = lines[0]

    results = stations_df[stations_df['mrt_line_english'] == search_term]
    stations_codes = results['stn_code'].tolist()
    station_names = results['mrt_station_english'].tolist()
    stations_list = list(zip(stations_codes, station_names))

    return render_template('line_select.html', lines=lines, selected_line=search_term,
        stations=stations_list)

@app.route('/calculate', methods=["POST"])
def calculate():
    """calculate probability"""
    station_1 = request.form['station_1']
    station_2 = request.form['station_2']
    code = re.match(r'[A-Z]+', station_1).group(0)
    num_1 = int(re.findall(r'\d+', station_1 )[0])
    num_2 = int(re.findall(r'\d+', station_2 )[0])
    stations = []
    if num_1 > num_2:
        for i in range(num_2, num_1 + 1):
            stations.append('{0}{1}'.format(code,i))
    if num_1 == num_2:
       for i in range(num_1, num_1 + 1):
           stations.append('{0}{1}'.format(code,i))
    if num_1 < num_2:
        for i in range(num_1, num_2 + 1):
            stations.append('{0}{1}'.format(code,i))
    product = 1
    results = stations_df[stations_df['stn_code'].isin(stations)]
    for index, item in results.iterrows():
        product *= float(item['p_no_breakdown'])
    p_delay = round((1 - product)*100,2)

    return "<b>Start</b>: {0}</br> <b>End</b>: {1}</br> <b>Probability of Delay</b>: <b><font color = \"red\" size = \"7\">{2}%</font></b>".format(station_1, station_2, p_delay)
