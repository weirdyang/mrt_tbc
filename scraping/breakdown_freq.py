import pandas as pd
import re
import csv
from collections import Counter

df = pd.read_csv('disrupt_v2.csv', sep=',',encoding='utf-8', header='infer' )
print(df)
total_list = list(zip(df['Station1_Index'].tolist(), df['Station2_Index'].tolist()))
stations_list = []
station_numbers = []
for item in total_list:
    code = re.match(r'[A-Z]+', item[0]).group(0)
    num_1 = int(re.findall(r'\d+', item[0] )[0])
    try:
        num_2 = int(re.findall(r'\d+', item[1] )[0])
    except TypeError as e:
        num_2 = num_1
    print(num_1)
    print(num_2)
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
    entry = {'code': code, 'station_1': item[0], 'station_2': item[1], 'stations': stations}
    stations_list.append(entry)
    station_numbers.extend(stations)

keys = stations_list[0].keys()
with open('stations_list.csv', 'w+') as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(stations_list)
df = pd.DataFrame(station_numbers, columns=['station'])
data = dict(Counter(station_numbers))
headers = ['station', 'count']
with open('station_count.csv', 'w+') as f:
    dict_writer = csv.DictWriter(f, headers)
    dict_writer.writeheader()
    data = [dict(zip(headers, [k, v])) for k, v in data.items()]
    dict_writer.writerows(data)
