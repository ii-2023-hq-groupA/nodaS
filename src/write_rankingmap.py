from typing import Any
import pandas as pd
import argparse
import folium
from folium import FeatureGroup, LayerControl
from count_taste import TASTE

#参考 https://chayarokurokuro.hatenablog.com/entry/2021/08/03/065148

# TASTE = ["醤油", "豚骨", "味噌", "塩", "つけ麺", "家系", "二郎系",
#          "担々麺", "魚介", "油そば", "まぜそば", "ちゃんぽん", "鶏白湯"]
TASTE_COUNT = {TASTE[i]: i for i in range(len(TASTE))}
GROUP = [FeatureGroup(name=TASTE[i]) for i in range(len(TASTE))]
COLORS = ["#000000", "#f5deb3", "#c18a39", "#ffa500", "#8b4513", "#ff0000", "#ffd700", #[黒、ベージュ、黄土色、オレンジ、茶色、赤、黄色、
          "#660066", "#0000ff", "#006400", "#adff2f", "#ff00ff", "#ffffff"] #　紫、青、緑、黄緑、マゼンタ、白]
MAP_COLORS = ["#ff0000", "#ffa700", "#afff00", "#08ff00", "#00b7ff", "#0010ff"] # 赤、オレンジ、黄緑、緑、水色、青

def get_taste(data: Any) -> str:
    taste_count = [[data[taste], taste] for taste in TASTE]
    taste_count.sort(reverse=True)
    taste = taste_count[0][1]
    return taste

def find_group(taste: str) -> FeatureGroup:
    return GROUP[TASTE.index(taste)]

def main():
    # print(f"read file: {args.file}")
    center_lat=35.6858375
    center_lon=139.729528
    folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=12,
                            tiles="cartodbpositron")
    for rank in range(6):
        df = pd.read_csv("../analysis_data/" + f"ramen_count_taste_{rank}.csv")

        for _, data in df.iterrows():
            # print(data["latitude"])
            location = [float(data["latitude"]), float(data["longitude"])]
            shop_name = data["name"]
            taste = get_taste(data)

            folium.CircleMarker(
                location=location,
                radius=5,
                popup=f"{shop_name}\n taste: {taste}\n ranking: {rank}",
                # color=COLORS[TASTE_COUNT[taste]],
                color=MAP_COLORS[rank],
                fill_color=MAP_COLORS[rank],
            ).add_to(find_group(taste))

    for group in GROUP:
        group.add_to(folium_map)

    LayerControl().add_to(folium_map)

    folium_map.save('../map/map_ranking.html')


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-f', '--file', type=str, required=True)
    # args = parser.parse_args()
    main()