# ------------------------------------------------------------------------------------------------ #
#                                           TRANSFORMERS                                           #
# ------------------------------------------------------------------------------------------------ #

# ------------------------------------------ LIBRAIRIES ------------------------------------------ #

from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from sys import stderr

from utilities import local_trend, local_mean

# ------------------------------------------- CONSTANTS ------------------------------------------ #

from constants import *

# -------------------------------------------- CLASSES ------------------------------------------- #

class TypeTransformer(BaseEstimator, TransformerMixin):
	def __init__(self, str_features = None, num_features = None):
		if not str_features:
			self.str_features = [DATA_CODE_POSTAL_COLUMN, DATA_TYPE_LOCAL_COLUMN]
		else:
			self.str_features = str_features

		if not num_features:
			self.num_features = [DATA_SURFACE_REELLE_COLUMN, DATA_SURFACE_TERRAIN_COLUMN, DATA_NB_PIECES_COLUMN]
		else:
			self.num_features = num_features
	
	def fit(self, X, y = None):
		return self

	def transform(self, X, y = None):
		X_ = X.copy()

		X_[DATA_DATE_COLUMN] = pd.to_datetime(X_[DATA_DATE_COLUMN], yearfirst=True)

		for column in self.str_features:
			X_[column] = X_[column].values.astype(str)

		for column in self.num_features:
			X_[column] = X_[column].values.astype(float)
		
		return X_

# ------------------------------------------------------------------------------------------------ #
class FeaturesExtractor(BaseEstimator, TransformerMixin):
	def __init__(self):
		super().__init__()
	
	def fit(self, X, y = None):
		X_ = X.copy()

		# Initialisation
		X_[DATA_VALEUR_FONCIERE_COLUMN] = y
		X_[DATA_TIME_COLUMN] = X_[DATA_DATE_COLUMN].astype('int64') // 10**9

		X_ = X_.groupby(DATA_CODE_POSTAL_COLUMN).apply(local_trend).reset_index(drop=True)
		X_ = X_.groupby(DATA_CODE_POSTAL_COLUMN).apply(local_mean).reset_index(drop=True)

		self.history = X_[[
			DATA_DATE_COLUMN, DATA_CODE_POSTAL_COLUMN, DATA_CODE_POSTAL_TREND_6M_COLUMN,
			DATA_CODE_POSTAL_MEAN_6M_COLUMN
		]]

		return self
	
	def transform(self, X, y = None):
		X_ = X.copy()

		# Initialisation
		X_[DATA_TIME_COLUMN] = X_[DATA_DATE_COLUMN].astype('int64') // 10**9
		X_[DATA_CODE_POSTAL_MEAN_6M_COLUMN] = np.nan
		X_[DATA_CODE_POSTAL_TREND_6M_COLUMN] = np.nan

		for i, row in X_.iterrows():
			code_postal = row[DATA_CODE_POSTAL_COLUMN]
			date = row[DATA_DATE_COLUMN]

			hist = self.history[(self.history[DATA_CODE_POSTAL_COLUMN] == code_postal) &
					   			(self.history[DATA_DATE_COLUMN] < date)]
			
			if not hist.empty:
				last_row = hist.sort_values(DATA_DATE_COLUMN).iloc[-1]
				X_.at[i, DATA_CODE_POSTAL_MEAN_6M_COLUMN] = last_row[DATA_CODE_POSTAL_MEAN_6M_COLUMN]
				X_.at[i, DATA_CODE_POSTAL_TREND_6M_COLUMN] = last_row[DATA_CODE_POSTAL_TREND_6M_COLUMN]
			else:
				X_.at[i, DATA_CODE_POSTAL_MEAN_6M_COLUMN] = self.history[DATA_CODE_POSTAL_MEAN_6M_COLUMN].mean()
				X_.at[i, DATA_CODE_POSTAL_TREND_6M_COLUMN] = 0
		
		X_[DATA_CODE_POSTAL_TREND_6M_COLUMN] = X_[DATA_CODE_POSTAL_TREND_6M_COLUMN].fillna(0.)
		X_ = X_.drop([DATA_CODE_POSTAL_COLUMN, DATA_DATE_COLUMN], axis=1)

		return X_
		

# ------------------------------------------------------------------------------------------------ #	