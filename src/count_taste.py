import json
import glob
import csv
from typing import Any
from scrap_tabelog import Restaurant

TASTE = ["醤油", "豚骨", "味噌", "塩", "つけ麺", "家系", "二郎系",
         "担々麺", "魚介", "油そば", "まぜそば", "ちゃんぽん", "鶏白湯"]


def count_taste(reviews: list[str]) -> dict[str, int]:
    count_result = {taste: 0 for taste in TASTE}
    for taste in TASTE:
        for review in reviews:
            count_result[taste] += review.count(taste)
    return count_result


def read_json_data(json_filename: str) -> list[dict[str, Any]]:
    count_data = []
    with open(json_filename, "r") as f:
        data = json.load(f)
        for restaurant_data in data:
            restaurant = Restaurant(**restaurant_data)
            taste_count_result = count_taste(restaurant.review)
            restaurant_dict = {"name": restaurant.name,
                               "latitude": restaurant.latitude,
                               "longitude": restaurant.longitude}
            for taste, count in taste_count_result.items():
                restaurant_dict[taste] = count
            count_data.append(restaurant_dict)
    return count_data


def read_data(output_csv_filename: str) -> None:
    json_file_list = glob.glob("../data/*.json")
    for i, json_filename in enumerate(json_file_list):
        count_data = read_json_data(json_filename)
        with open(f"../analysis_data/{output_csv_filename}", "a", encoding="utf_8_sig") as f:
            filed_name = list(count_data[0].keys())
            writer = csv.DictWriter(f, fieldnames=filed_name)
            if i == 0:
                writer.writeheader()
            writer.writerows(count_data)
        print(f"write data: {json_filename}")


def main():
    csv_filename = "ramen_count_taste.csv"
    read_data(csv_filename)


if __name__ == "__main__":
    main()
