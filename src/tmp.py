import matplotlib.pyplot as plt
from geopy.distance import geodesic
import argparse
import pandas as pd
from count_taste import TASTE
from write_map import get_taste
from googletrans import Translator

translator = Translator()
TASTES_EN = {taste: translator.translate(taste).text for taste in TASTE}
print("{")
for taste, en in TASTES_EN.items():
    print(f"\"{taste}\": \"{en}\",")
print("}")
