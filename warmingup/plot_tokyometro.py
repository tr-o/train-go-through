import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import networkx as nx

def create_train_network(station_file, join_file, line_file, company_cd):
    """
    指定した鉄道会社の駅データを抽出し、鉄道ネットワークを可視化する関数

    :param station_file: 駅データのCSVファイル
    :param join_file: 接続データのCSVファイル
    :param line_file: 路線データのCSVファイル
    :param company_cd: 抽出する会社コード (例: 東京メトロは 18)
    """

    # CSV データの読み込み
    station = pd.read_csv(station_file)
    join = pd.read_csv(join_file)
    line = pd.read_csv(line_file)

    # 指定した鉄道会社の駅のみ抽出
    selected_stations = station[["station_cd", "station_name", "line_cd", "lon", "lat"]]
    selected_stations = pd.merge(selected_stations, line, on="line_cd")
    selected_stations = selected_stations[selected_stations["company_cd"] == company_cd]
    selected_stations = selected_stations[["station_cd", "station_name", "line_cd", "lon_x", "lat_x", "line_name"]]

    # 経度・緯度を整理
    selected_stations["lon"] = selected_stations["lon_x"]
    selected_stations["lat"] = selected_stations["lat_x"]
    selected_stations = selected_stations[["station_cd", "station_name", "line_cd", "lon", "lat", "line_name"]]

    # 路線に関係する接続データを抽出
    selected_joins = join[join["line_cd"].isin(selected_stations["line_cd"])]
    selected_joins = selected_joins[["station_cd1", "station_cd2"]]

    # グラフの宣言
    G = nx.Graph()
    G.add_nodes_from(selected_stations["station_name"])

    # 座標設定
    pos = {name: (lon, lat) for name, lon, lat in zip(selected_stations["station_name"], selected_stations["lon"], selected_stations["lat"])}

    # 駅コードと駅名のリンク
    station_map = {cd: name for name, cd in zip(selected_stations["station_name"], selected_stations["station_cd"])}

    # グラフに接続情報を追加
    for i, j in zip(selected_joins["station_cd1"], selected_joins["station_cd2"]):
        if i in station_map and j in station_map:
            G.add_edge(station_map[i], station_map[j])

    # グラフの出力設定
    plt.figure(figsize=(10, 10), dpi=200)
    plt.title(f'鉄道ネットワーク ({company_cd})', fontsize=20)
    plt.axes().set_aspect('equal', 'datalim')
    nx.draw_networkx(G, pos, node_color='b', alpha=0.8, node_size=10, font_size=5, font_family='IPAexGothic')
    plt.show()

# 使い方：東京メトロ (company_cd = 18) を表示
create_train_network("ekidata/station20250529free.csv", "ekidata/join20250430.csv", "ekidata/line20250529free.csv", 18)