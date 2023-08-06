# load.py

import pandas as pd
# import pathlib
# import importlib.resources
from importlib_resources import files

def load_word():
	# return pd.read_csv('wordjc/data/web4.csv')
	# return pathlib.Path(__file__).parent.joinpath("data/web4.csv").read_text()
	# return importlib.resources.read_text("wordjc.data", "web4.csv")
	scfile = files('wordjc.data').joinpath('web4.csv')
	return pd.read_csv(scfile)
