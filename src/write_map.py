import folium
import argparse
import pandas as pd


def main(args):
    print(f"read file: {args.file}")
    folium_map = folium.Map(location=[35.690921, 139.700258], zoom_start=15)
    df = pd.read_csv(args.file)
    for _, data in df.iterrows():
        location = [data["latitude"], data["longitude"]]
        folium.Marker(
            location=location,
            popup=data["name"],
            icon=folium.Icon(color='red', icon='home')
        ).add_to(folium_map)
    folium_map.save('../map/map.html')
    






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    main(args)
