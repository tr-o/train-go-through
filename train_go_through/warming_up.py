import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
import networkx as nx

# csvファイルからpandsa形式のテーブルを作成
station = pd.read_csv("station20200316free.csv")
join = pd.read_csv("join20200306.csv")
# pref = pd.read_csv("pref.csv")
line = pd.read_csv("line20200306free.csv")
company = ("company20200309.csv")