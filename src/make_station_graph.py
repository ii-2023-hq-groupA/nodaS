import matplotlib.pyplot as plt
from geopy.distance import geodesic
import argparse
import pandas as pd
from count_taste import TASTE
from make_ratio_graph import TASTES_EN
from write_map import get_taste
from write_layermap import COLORS

TASTE_COUNT = {TASTE[i]: i for i in range(len(TASTE))}

# [latitude, longitude]
STATION = {
    "東京": [35.681382,	139.76608399999998],
    "有楽町": [35.675069, 139.763328],
    "新橋": [35.665498, 139.75964],
    "浜松町": [35.655646, 139.756749],
    "田町": [35.645736, 139.74757499999998],
    "品川": [35.630152, 139.74044000000004],
    "大崎": [35.61971, 39.72855300000003],
    "五反田": [35.626446, 139.72344399999997],
    "目黒": [35.633998, 139.715828],
    "恵比寿": [35.64669, 139.710106],
    "渋谷": [35.658517, 139.70133399999997],
    "原宿": [35.670168, 139.70268699999997],
    "代々木": [35.683061, 139.702042],
    "新宿": [35.690921, 139.70025799999996],
    "新大久保": [35.701306, 139.70004399999993],
    "高田馬場": [35.712285, 139.70378200000005],
    "目白": [35.721204, 139.706587],
    "池袋": [35.728926, 139.71038],
    "大塚": [35.731401, 139.72866199999999],
    "巣鴨": [35.733492, 139.73934499999996],
    "駒込": [35.736489, 139.74687500000005],
    "田端": [35.738062, 139.76085999999998],
    "西日暮里": [35.732135, 139.76678700000002],
    "日暮里": [35.727772, 139.770987],
    "鶯谷": [35.720495, 139.77883700000007],
    "上野": [35.713768, 139.77725399999997],
    "御徒町": [35.707438, 139.774632],
    "秋葉原": [35.698683, 139.77421900000002],
    "神田": [35.69169, 139.77088300000003],
}

STATION_EN = {
    "東京": "Tokyo",
    "有楽町": "Yurakucho",
    "新橋": "Shinbashi",
    "浜松町": "Hamamatsucho",
    "田町": "Tamachi",
    "品川": "Shinagawa",
    "大崎": "Osaki",
    "五反田": "Gotanda",
    "目黒": "Meguro",
    "恵比寿": "Ebisu",
    "渋谷": "Shibuya",
    "原宿": "Harajuku",
    "代々木": "Yoyogi",
    "新宿": "Shinjuku",
    "新大久保": "Shinokubo",
    "高田馬場": "Takadanobaba",
    "目白": "Meziro",
    "池袋": "Ikebukuro",
    "大塚": "Otsuka",
    "巣鴨": "Sugamo",
    "駒込": "Komagome",
    "田端": "Tabata",
    "西日暮里": "Nishi-Nippori",
    "日暮里": "Nippori",
    "鶯谷": "Uguisudani",
    "上野": "Ueno",
    "御徒町": "Okachimachi",
    "秋葉原": "Akihabara",
    "神田": "Kanda",
}
R = 1  # km


def judge_neighbor(station: str, location: list[int]) -> bool:
    distance_km = geodesic(STATION[station], location).km
    if distance_km <= R:
        return True
    return False


def make_graph(station: str, filepath: str):
    df = pd.read_csv(filepath)
    taste_count = {TASTE[i]: 0 for i in range(len(TASTE))}
    for _, data in df.iterrows():
        location = [data["latitude"], data["longitude"]]
        if not judge_neighbor(station, location):
            continue
        taste = get_taste(data)
        taste_count[taste] += 1
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x = [TASTES_EN[taste] for taste in taste_count.keys()]
    y = list(taste_count.values())
    print(y)
    # rect = ax.barh(x, y)
    try:
        ax.pie(y, colors=COLORS[:len(y)])
    except ValueError:
        print(f"can't write {station} station graph")
        return
    # ax.set_title(f"{STATION_EN[station]} Sta.")
    fig.tight_layout()
    fig.savefig(f"analysis_data/graph_{station}.png")


def main(args):
    print(f"read file: {args.file}")
    for sta in STATION.keys():
        print(f"station: {sta}")
        make_graph(sta, args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    main(args)
