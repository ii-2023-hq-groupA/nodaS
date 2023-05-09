from typing import Any
import folium
import argparse
import pandas as pd
from count_taste import TASTE

TASTE_COUNT = {TASTE[i]: i for i in range(len(TASTE))}

COLORS = ["red", "blue", "green", "purple", "orange", "darkred", "lightred", "beige",
          "darkblue", "darkgreen", "cadetblue", "darkpurple", "white", "pink",
          "lightblue", "lightgreen", "gray", "black", "lightgray"]


def get_taste_color(data: Any):
    taste_count = [[data[taste], taste] for taste in TASTE]
    taste_count.sort(reverse=True)
    taste = taste_count[0][1]
    color = COLORS[TASTE_COUNT[taste]]
    return taste, color


def main(args):
    print(f"read file: {args.file}")
    folium_map = folium.Map(location=[35.690921, 139.700258], zoom_start=15,
                            tiles="cartodbpositron")
    df = pd.read_csv(args.file)
    for _, data in df.iterrows():
        location = [data["latitude"], data["longitude"]]
        shop_name = data["name"]
        taste, color = get_taste_color(data)
        folium.CircleMarker(
            location=location,
            radius=5,
            popup=f"{shop_name}\n taste: {taste}",
            color=color,
            fill_color=color,
        ).add_to(folium_map)
    folium_map.save('../map/map.html')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    main(args)
