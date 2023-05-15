import folium
import pandas as pd



def make_marker(m, df, rank):
        # データフレームの全ての行のマーカーを作成する。
    for i in range(0,len(df)):
        # 味を振り分けるif文をつける->味による色分け
        # ランキングを振り分けるif文をつける->ランキングによる色分け
        map_color = ["red", "blue", "green", "purple", "orange", "darkred"]

        for j in range(1, 7):
            if (j==rank):
                rank_color = map_color[j]

        # folium.Marker(
        #     location=[df["latitude"][i],df["longitude"][i]],
        #     popup=df["name"],
        #     icon=folium.Icon(icon="bell", color=rank_color)
        # ).add_to(m)

        folium.Circle(
            location=[df["latitude"][i],df["longitude"][i]],
            popup=df["name"],
            radius = 20,
            color = rank_color,
            fill = True
        ).add_to(m)


def visualize_locations(df, rank):

    # 図の大きさを指定
    f = folium.Figure(width=1000, height=500)
    # 初期表示の中心の座標を指定して地図を作成 # 四つ谷駅
    center_lat=35.6858375
    center_lon=139.729528

    m = folium.Map([center_lat,center_lon], zoom_start=12).add_to(f)

    for rank in range(6):
        csv_filename = f"ramen_count_taste_{rank}.csv"
        df = pd.read_csv("../analysis_data/" + csv_filename)
        make_marker(m, df, rank)


    m.save("ramen_rank_map.html")
        
    return m


def main():

    # 図の大きさを指定
    f = folium.Figure(width=1000, height=500)
    # 初期表示の中心の座標を指定して地図を作成 # 四つ谷駅
    center_lat=35.6858375
    center_lon=139.729528

    m = folium.Map([center_lat,center_lon], zoom_start=12).add_to(f)

    for rank in range(6):
        csv_filename = f"ramen_count_taste_{rank}.csv"
        df = pd.read_csv("../analysis_data/" + csv_filename)
        make_marker(m, df, rank)

    m.save("ramen_rank_map.html")


if __name__ == "__main__":
    main()