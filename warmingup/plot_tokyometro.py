import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import networkx as nx
import random

def create_multi_train_network(station_file, join_file, line_file, company_cd_list):
    """
    指定した複数の鉄道会社の駅データを抽出し、鉄道ネットワークを可視化し、凡例を追加する関数
    
    :param station_file: 駅データのCSVファイル
    :param join_file: 接続データのCSVファイル
    :param line_file: 路線データのCSVファイル
    :param company_cd_list: 抽出する会社コードのリスト
    """

    # CSV データの読み込み
    station = pd.read_csv(station_file)
    join = pd.read_csv(join_file)
    line = pd.read_csv(line_file)

    # 指定した鉄道会社の駅のみ抽出
    selected_stations = station[["station_cd", "station_name", "line_cd", "lon", "lat"]]
    selected_stations = pd.merge(selected_stations, line, on="line_cd")
    selected_stations = selected_stations[selected_stations["company_cd"].isin(company_cd_list)]
    selected_stations = selected_stations[["station_cd", "station_name", "line_cd", "lon_x", "lat_x", "line_name"]]

    # 経度・緯度を整理
    selected_stations["lon"] = selected_stations["lon_x"]
    selected_stations["lat"] = selected_stations["lat_x"]
    selected_stations = selected_stations[["station_cd", "station_name", "line_cd", "lon", "lat", "line_name"]]

    # 路線に関係する接続データを抽出
    selected_joins = join[join["line_cd"].isin(selected_stations["line_cd"])]
    selected_joins = selected_joins[["station_cd1", "station_cd2", "line_cd"]]

    # グラフの宣言
    G = nx.Graph()

    # 路線ごとの色を設定 (ランダムなカラー)
    line_colors = {line_name: "#{:06x}".format(random.randint(0, 0xFFFFFF)) for line_name in selected_stations["line_name"].unique()}
    
    # 駅コードと駅名のリンク
    station_map = {cd: name for name, cd in zip(selected_stations["station_name"], selected_stations["station_cd"])}

    # プロット座標設定
    pos = {name: (lon, lat) for name, lon, lat in zip(selected_stations["station_name"], selected_stations["lon"], selected_stations["lat"])}

    # 路線ごとに異なる色でグラフの辺を追加
    edge_colors = []
    edge_labels = []
    for i, j, line_cd in zip(selected_joins["station_cd1"], selected_joins["station_cd2"], selected_joins["line_cd"]):
        if i in station_map and j in station_map:
            line_name = selected_stations[selected_stations["line_cd"] == line_cd]["line_name"].iloc[0]
            G.add_edge(station_map[i], station_map[j])
            edge_colors.append(line_colors[line_name])
            edge_labels.append(line_name)

    # グラフの出力設定
    plt.figure(figsize=(10, 10), dpi=200)
    plt.title(f'鉄道ネットワーク ({", ".join(map(str, company_cd_list))})', fontsize=20)
    plt.axes().set_aspect('equal', 'datalim')

    # グラフの描画
    nx.draw_networkx(G, pos, node_color='black', alpha=0.8, node_size=10, font_size=5, font_family='IPAexGothic', edge_color=edge_colors)

    # 凡例の追加
    handles = [plt.Line2D([0], [0], color=color, lw=2) for color in line_colors.values()]
    plt.legend(handles, line_colors.keys(), loc="upper right", fontsize=10)

    # グラフ表示
    plt.show()

# **使い方：東京メトロ (18) と 都営地下鉄 (13) の路線を表示**
create_multi_train_network("ekidata/station20250529free.csv", "ekidata/join20250430.csv", "ekidata/line20250529free.csv", [13])