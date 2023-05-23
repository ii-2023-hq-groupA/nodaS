import matplotlib.pyplot as plt
import argparse
import pandas as pd
from count_taste import TASTE
from write_map import get_taste
from googletrans import Translator
from write_layermap import COLORS

TASTE_COUNT = {TASTE[i]: i for i in range(len(TASTE))}
# # matplotlib用 color
# COLORS = ["red", "blue", "green", "purple", "orange", "darkred", "pink", "beige",
#           "lightblue", "lightgreen", "cadetblue", "darkviolet", "lightgray", "lightcoral",
#           "darkblue", "darkgreen", "gray", "black", "white"]
translator = Translator()
TASTES_EN = {
    "醤油": "Soy sauce",
    "豚骨": "Tonkotsu",
    "味噌": "Miso",
    "塩": "Salt",
    "つけ麺": "Tsukemen",
    "家系": "Ie-kei",
    "二郎系": "\n\nJiro-kei",  # 文字被り　　防止
    "担々麺": "Tantanmen",
    "魚介": "Seafood",
    "油そば": "Oil soba",
    "まぜそば": "Oiled Ramen Noodles",
    "ちゃんぽん": "Chanpon",
    "鶏白湯": "Slow-cooked chicken broth",
}



def make_graph(filepath: str):
    df = pd.read_csv(filepath)
    taste_count = {TASTE[i]: 0 for i in range(len(TASTE))}
    for _, data in df.iterrows():
        taste = get_taste(data)
        taste_count[taste] += 1
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    x = [TASTES_EN[taste] for taste in taste_count.keys()]
    y = list(taste_count.values())
    print(y)
    ax.pie(y, labels=x, colors=COLORS[:len(y)])
    fig.tight_layout()
    fig.savefig("analysis_data/graph_all.png")


def main(args):
    print(f"read file: {args.file}")
    make_graph(args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    main(args)
