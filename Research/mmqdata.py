import numpy as np
import pandas as pd
import glob as gl

def csv_to_df(path, combine=True):
    # gather all csv files, convert them to Pandas DataFrames and store them in a list
    seasons = [pd.read_csv(f) for f in gl.glob(path)]
    
    # If the 'combine' argument is True then concatenate together all the dataframes.
    if combine:
        seasons = pd.concat(seasons, ignore_index=True)
    
    return seasons
