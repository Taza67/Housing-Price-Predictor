# ------------------------------------------------------------------------------------------------ #
#                                             UTILITIES                                            #
# ------------------------------------------------------------------------------------------------ #

# ------------------------------------------ LIBRAIRIES ------------------------------------------ #

import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from sys import stderr

# ------------------------------------------- CONSTANTS ------------------------------------------ #

from constants import *

# ------------------------------------------- FUNCTIONS ------------------------------------------ #

def analyse(data):
	nas = data.isna().sum()
	nuniques = data.nunique()
	types = data.dtypes
	
	return pd.DataFrame({
		"NA": nas,
		"Uniques": nuniques,
		"types": types
	})

# ------------------------------------------------------------------------------------------------ #

def local_trend(group: pd.DataFrame, window_days: int = 180):
	g = group.sort_values(DATA_DATE_COLUMN)

	trends = []
	for i, row in g.iterrows():
		cutoff = row[DATA_DATE_COLUMN] - pd.Timedelta(days=window_days)
		window = g[(g[DATA_DATE_COLUMN] >= cutoff) & (g[DATA_DATE_COLUMN] < row[DATA_DATE_COLUMN])]

		if len(window) >= 5:
			x = (window[DATA_TIME_COLUMN] - window[DATA_TIME_COLUMN].min()).values.reshape(-1, 1)
			y = np.log(window[DATA_VALEUR_FONCIERE_COLUMN])

			lr = LinearRegression().fit(x, y)
			trends.append(lr.coef_[0])
		else:
			trends.append(np.nan)
	
	g[DATA_CODE_POSTAL_TREND_6M_COLUMN] = trends

	return g

def local_mean(group: pd.DataFrame, window_days: int = 180):
    group[DATA_DATE_COLUMN] = pd.to_datetime(group[DATA_DATE_COLUMN])  # Assurez le bon type
    g = group.sort_values(DATA_DATE_COLUMN).set_index(DATA_DATE_COLUMN)
    
    rolling_mean = g[DATA_VALEUR_FONCIERE_COLUMN].rolling(f"{window_days}D", closed="left").mean()
    g[DATA_CODE_POSTAL_MEAN_6M_COLUMN] = rolling_mean

    g.reset_index(inplace=True)
    return g

# ------------------------------------------------------------------------------------------------ #