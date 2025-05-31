import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import networkx as nx

# csvファイルからpandsa形式のテーブルを作成
station = pd.read_csv("ekidata\station20250529free.csv")
join = pd.read_csv("ekidata\join20250430.csv")
line = pd.read_csv("ekidata\line20250529free.csv")
company = ("ekidata\company20250529.csv")

# 全国の駅から東京メトロの駅のみ抽出する 東京メトロ...company_cd == 18
metro = station[["station_cd", "station_name", "line_cd", "lon", "lat"]]
metro = pd.merge(metro, line, on = 'line_cd')
metro = metro[metro["company_cd"] == 18]
metro = metro[["station_cd", "station_name", "line_cd", "lon_x", "lat_x", "line_name", "line_color_c", "line_color_t"]]
lon = metro["lon_x"]
lat = metro["lat_x"]
metro["lon"] = lon
metro["lat"] = lat
metro = metro[["station_cd", "station_name", "line_cd", "lon", "lat", "line_name"]]

# 東京メトロの接続辺を抽出する 路線...line_cd == 28001---28010
metro_join = join[(join["line_cd"]==28001)|(join["line_cd"]==28002)|(join["line_cd"]==28003)|(join["line_cd"]==28004)|(join["line_cd"]==28005)|(join["line_cd"]==28006)|(join["line_cd"]==28007)|(join["line_cd"]==28008)|(join["line_cd"]==28009)|(join["line_cd"]==28010)]
metro_join = metro_join[["station_cd1", "station_cd2"]]

# グラフの宣言
G = nx.Graph()
# 頂点を駅名にする
G.add_nodes_from(metro["station_name"])
# plotの座標を設定
pos={}
for i, j, k in zip(metro["station_name"], metro["lon"], metro["lat"]):
  pos[i] = (j, k)
# リストeにstation_nameとstation_cdを格納し、リンクさせる
e = []
for i, j in zip(metro["station_name"], metro["station_cd"]):
  e.append([i, j])
# グラフに辺情報を加える
for i, j in zip(metro_join["station_cd1"], metro_join["station_cd2"]):
    for k in e:
      if k[1] == i:
        for l in e:
          if l[1] == j:
            G.add_edge(k[0], l[0])
# グラフの出力の設定
plt.figure(figsize=(10,10),dpi=200)
plt.title('東京メトロ', fontsize=20)
plt.axes().set_aspect('equal', 'datalim')
nx.draw_networkx(G, pos, node_color='b', alpha=0.8, node_size=10, font_size=5, font_family='IPAexGothic')
plt.show()
