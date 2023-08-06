# pivot.py

import pandas as pd
from importlib_resources import files

def load_word():
	scfile = files('wordjc.data').joinpath('web4.csv')
	return pd.read_csv(scfile)

def bible_stat(df):
	stat_df = pd.pivot_table(df, index=['book_no', 'book', 'category', 'cat_no'],
                          values=['chapter', 'verse', 'text'],
                          aggfunc={'chapter': lambda ch: len(ch.unique()),
                                   'verse': 'count',
                                   'text': lambda ts: sum([len(t.split()) for t in ts])})
	stat_df = stat_df[['chapter', 'verse', 'text']].sort_index()

	stat_df2 = stat_df.groupby('cat_no').apply(lambda sub: sub.pivot_table(
                        index=['category', 'book_no', 'book'],
                        values=['chapter', 'verse', 'text'],
                        aggfunc={'chapter': 'sum',
                                 'verse': 'sum',
                                 'text': 'sum'},
                        margins=True,
                        margins_name='Sub-Total'))

	stat_df2.loc[('', '', 'Total', '')] = stat_df2.sum() // 2
	stat_df2.index = stat_df2.index.droplevel(0)
	stat_df2.fillna('', inplace=True)
	stat_df2 = stat_df2[['chapter', 'verse', 'text']]
	return stat_df2
