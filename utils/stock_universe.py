import pandas as pd
import os
from utils.build_stock_universe import build_stock_universe


def load_stock_universe():

    path = "data/stock_universe.csv"

    if not os.path.exists(path):

        print("Stock universe not found. Building dataset...")

        build_stock_universe()

    df = pd.read_csv(path)

    return df