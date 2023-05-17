import matplotlib.pyplot as plt
from geopy.distance import geodesic
import argparse
import pandas as pd
from count_taste import TASTE
from write_map import get_taste
from googletrans import Translator
from make_station_graph import STATION

translator = Translator()
STATION_EN = {station: translator.translate(station).text for station in STATION.keys()}
print("{")
for station, en in STATION_EN.items():
    print(f"\"{station}\": \"{en}\",")
print("}")
