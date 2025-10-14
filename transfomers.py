# ------------------------------------------------------------------------------------------------ #
#                                           TRANSFORMERS                                           #
# ------------------------------------------------------------------------------------------------ #

# ------------------------------------------ LIBRAIRIES ------------------------------------------ #

from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

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

		X_[DATA_DATE_COLUMN] = pd.to_datetime(X_[DATA_DATE_COLUMN], dayfirst=True)

		for column in self.str_features:
			X_[column] = X_[column].values.astype(str)

		for column in self.num_features:
			X_[column] = X_[column].values.astype(float)
		
		return X_

# ------------------------------------------------------------------------------------------------ #

class DateTransformer(BaseEstimator, TransformerMixin):
	def __init__(self, date_column=DATA_DATE_COLUMN):
		self.date_column = date_column
		self.scaler = StandardScaler()
	
	def fit(self, X, y=None):
		X_ = X.copy()

		# Tendance temporelle
		self.min_date = X_[self.date_column].min()
		X_[DATA_TIME_COLUMN] = (X_[self.date_column] - self.min_date).dt.days

		# Scaler
		self.scaler.fit(X_[[DATA_TIME_COLUMN]].values.astype(float))
		
		return self
	
	def transform(self, X, y = None):
		X_ = X.copy()

		# Tendance temporelle
		X_[DATA_TIME_COLUMN] = (X_[self.date_column] - self.min_date).dt.days
		X_[DATA_TIME_COLUMN] = self.scaler.transform(X_[[DATA_TIME_COLUMN]].values.astype(float))

		# Suppression des colonnes redondantes
		X_ = X_.drop(columns=[self.date_column], axis=1)

		return X_

# ------------------------------------------------------------------------------------------------ #