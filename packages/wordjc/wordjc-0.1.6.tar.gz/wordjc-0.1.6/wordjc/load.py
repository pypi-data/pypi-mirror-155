# load.py

import pandas as pd
import importlib.resources

def load_word():
	#return pd.read_csv('wordjc/data/web4.csv')
	return importlib.resources.read_text("wordjc", "data/web4.csv")