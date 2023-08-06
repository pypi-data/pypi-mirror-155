# load.py

import pandas as pd
import importlib.resources
# import pathlib

def load_word():
	# return pd.read_csv('wordjc/data/web4.csv')
	return importlib.resources.read_text("wordjc.data", "web4.csv")
	# return pathlib.Path(__file__).parent.joinpath("data/web4.csv").read_text()
