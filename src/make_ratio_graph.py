import matplotlib.pyplot as plt
import argparse
import pandas as pd
from count_taste import TASTE
from write_map import get_taste
from googletrans import Translator

TASTE_COUNT = {TASTE[i]: i for i in range(len(TASTE))}
# matplotlib用 color
COLORS = ["red", "blue", "green", "purple", "orange", "darkred", "pink", "beige",
          "lightblue", "lightgreen", "cadetblue", "darkviolet", "lightgray", "lightcoral",
          "darkblue", "darkgreen", "gray", "black", "white"]
translator = Translator()
TASTES_EN = {
    "醤油": "soy sauce",
    "豚骨": "pig bones",
    "味噌": "miso",
    "塩": "salt",
    "つけ麺": "tsukemen",
    "家系": "Family line",
    "二郎系": "Erlang",
    "担々麺": "Dandan noodles",
    "魚介": "seafood",
    "油そば": "Oil soba",
    "まぜそば": "Maze soba",
    "ちゃんぽん": "Champon",
    "鶏白湯": "Chicken hot water",
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
    fig.savefig("analysis_data/graph_all.pdf")


def main(args):
    print(f"read file: {args.file}")
    make_graph(args.file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()
    main(args)
