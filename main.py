# ------------------------------------------------------------------------------------------------ #
#                                    HOUSING PRICE PREDICTOR UI                                    #
# ------------------------------------------------------------------------------------------------ #

# ------------------------------------------ LIBRAIRIES ------------------------------------------ #

import streamlit as st
import joblib
import numpy as np
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from transfomers import *

# ------------------------------------------- CONSTANTS ------------------------------------------ #

from constants import *

MODEL_TEST_SUBMIT = "model_test_submit"
MODEL_TEST_INPUTS = "model_test_inputs"
DATAFRAME_INPUT = "dataframe_input"

# --------------------------------------------- MODEL -------------------------------------------- #

model = joblib.load(CAT_MODEl_PATH)
test_data = joblib.load(CAT_TEST_SET_PATH)

# ------------------------------------------- FUNCTIONS ------------------------------------------ #

def inputs_str(inputs):
	inputs = inputs.iloc[0]

	return (
		f"À la date du ```{inputs[DATA_DATE_COLUMN]}```, pour un bien de type "
		f"```{inputs[DATA_TYPE_LOCAL_COLUMN]}``` situé au ```{inputs[DATA_CODE_POSTAL_COLUMN]}``` "
		f"avec une surface terrain de ```{inputs[DATA_SURFACE_TERRAIN_COLUMN]}``` m2, une surface réelle de "
		f"```{inputs[DATA_SURFACE_REELLE_COLUMN]}``` m2 et ```{inputs[DATA_NB_PIECES_COLUMN]}``` pièces principales."
	)

# ---------------------------------------------- UI ---------------------------------------------- #

def dataframe_data_selector():
	with st.expander(label="Jeu de test", expanded=False):
		# Options
		gb = GridOptionsBuilder.from_dataframe(test_data)
		gb.configure_selection(suppressRowDeselection=True)
		gb.configure_default_column(editable=False)
		grid_options = gb.build()

		# Grille
		grid_input = AgGrid(
			test_data,
			gridOptions=grid_options,
			theme="streamlit"
		)

		selected = grid_input.get("selected_rows", [])

		if selected is not None:
			st.session_state[DATAFRAME_INPUT] = selected

# ------------------------------------------------------------------------------------------------ #

def model_test_form():
	columns = DATA_COLUMNS_STR
	columns_keys = list(columns.keys())
	mid = len(columns) // 2 + 1

	with st.expander(label="Entrée", expanded=True):
		with st.form("model_test_form", border=False):

			selected = st.session_state[DATAFRAME_INPUT].iloc[0]
			inputs = {}

			col1, col2 = st.columns(2)

			with col1:	
				for column in columns_keys[:mid]:
					inputs[column] = st.text_input(columns[column], selected.get(column, ""))
			with col2:	
				for column in columns_keys[mid:]:
					inputs[column] = st.text_input(columns[column], selected.get(column, ""))

			submit_button = st.form_submit_button("Soumettre")

			if submit_button:
				st.session_state[MODEL_TEST_SUBMIT] = True
				st.session_state[MODEL_TEST_INPUTS] = pd.DataFrame(inputs, index=[0])

# ------------------------------------------------------------------------------------------------ #

def model_test_view(inputs, selected):
	with st.expander(label="Estimation du prix", expanded=True):
		st.markdown(inputs_str(inputs))

		with st.spinner("Predicting..."):
			result = model.predict(inputs)

			st.success(f"Prix estimé : **{f"{int(result[0]):,}".replace(",", " ")} €**")

			sel_row = selected[inputs.columns].iloc[0].astype(str).str.strip()
			inp_row = inputs.iloc[0].astype(str).str.strip()

			if (sel_row == inp_row).all():
				st.error(f"Prix réel : **{f"{int(selected[DATA_VALEUR_FONCIERE_COLUMN].iloc[0]):,}".replace(",", " ")} €**")

# --------------------------------------------- MAIN --------------------------------------------- #

def main():
	# State
	if MODEL_TEST_SUBMIT not in st.session_state:
		st.session_state[MODEL_TEST_SUBMIT] = False
		st.session_state[MODEL_TEST_INPUTS] = None
		st.session_state[DATAFRAME_INPUT] = test_data.head(1)

	# UI
	st.header("Prédicteur du prix immobilier")

	dataframe_data_selector()

	model_test_form()

	if st.session_state[MODEL_TEST_SUBMIT]:
		inputs = st.session_state[MODEL_TEST_INPUTS]
		selected = st.session_state[DATAFRAME_INPUT]

		model_test_view(inputs, selected)

# --------------------------------------------- EXEC --------------------------------------------- #

main()

# ------------------------------------------------------------------------------------------------ #