import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import networkx as nx

# csvファイルからpandsa形式のテーブルを作成
station = pd.read_csv(r"ekidata\station20250529free.csv")
join = pd.read_csv(r"ekidata\join20250430.csv")
line = pd.read_csv(r"ekidata\line20250529free.csv")
company = (r"ekidata\company20250529.csv")

zen_join = join
zen = station[["station_cd", "station_name", "line_cd", "lon", "lat"]]
zen = pd.merge(zen, line, on='line_cd')
zen = zen[["station_cd", "station_name", "line_cd", "lon_x", "lat_x", "line_name"]]
lon = zen["lon_x"]
lat = zen["lat_x"]
zen["lon"] = lon
zen["lat"] = lat
zen = zen[["station_cd", "station_name", "line_cd", "lon", "lat", "line_name"]]
cd1_lat = []
cd1_lon = []
cd2_lat = []
cd2_lon = []
dist = []
not_exist = []
for i, j in zip(zen_join["station_cd1"], zen_join["station_cd2"]):
  flag = True
  for k, l, m in zip(zen["station_cd"], zen["lat"], zen["lon"]):
    if i == k:
      cd1_x = l
      cd1_y = m
      cd1_lat.append(l)
      cd1_lon.append(m)
      flag = False
    if j == k:
      cd2_x = l
      cd2_y = m
      cd2_lat.append(l)
      cd2_lon.append(m)
  if flag:
    not_exist.append([i, j])
    #print(i, j)
  else:
    dist.append(((cd1_x-cd2_x)**2 + (cd1_y-cd2_y)**2)**0.5)
# stationテーブルに存在しておらず、joinテーブルから不要なので削除
for i in range(len(not_exist)):
  zen_join = zen_join[zen_join["station_cd1"] != not_exist[i][0]]# & zen_join["station_cd2"] != not_exist[i][1]]
zen_join["cd1_lat"] = cd1_lat
zen_join["cd1_lon"] = cd1_lon
zen_join["cd2_lat"] = cd2_lat
zen_join["cd2_lon"] = cd2_lon
zen_join["distance"] = dist

# nodes is station_cd
G = nx.Graph()
G.add_nodes_from(zen["station_cd"])
pos={}
for i, j, k in zip(zen["station_cd"], zen["lon"], zen["lat"]):
  pos[i] = (j, k)
for i, j, m in zip(zen_join["station_cd1"], zen_join["station_cd2"], zen_join["distance"]):
  G.add_edge(i, j, weight=m)
for i, j, m in zip(zen["station_name"], zen["station_cd"], zen["lat"]):
  for k, l, n in zip(zen["station_name"], zen["station_cd"], zen["lat"]):
    if i == k and j != l and m == n:
      #print(i, j, k, l)
      G.add_edge(j, l, weight=0)
plt.figure(figsize=(10,10),dpi=200)
plt.title('全日本', fontsize=20)
plt.axes().set_aspect('equal', 'datalim')
nx.draw_networkx(G, pos, alpha=0.0, with_labels=False)
nx.draw_networkx_edges(G, pos)
plt.show()
