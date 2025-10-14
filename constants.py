# ------------------------------------------------------------------------------------------------ #
#                                             CONSTANTS                                            #
# ------------------------------------------------------------------------------------------------ #

DATA_FILE_PATH = "./data/ValeursFoncieres-2024.txt"
DATA_SEP_CHAR = "|"
DATA_CHUNK_SIZE = 10_000

DATA_VALEUR_FONCIERE_COLUMN = "Valeur fonciere"
DATA_CODE_COMMUNE_COLUMN = "Code commune"
DATA_CODE_POSTAL_COLUMN = "Code postal"
DATA_NATURE_MUTATION_COLUMN = "Nature mutation"
DATA_TYPE_LOCAL_COLUMN = "Type local"
DATA_SURFACE_TERRAIN_COLUMN = "Surface terrain"
DATA_SURFACE_REELLE_COLUMN = "Surface reelle bati"
DATA_NB_PIECES_COLUMN = "Nombre pieces principales"
DATA_DATE_COLUMN = "Date mutation"
DATA_TIME_COLUMN = "Jours_depuis"
DATA_COLUMNS = [
	DATA_CODE_POSTAL_COLUMN, DATA_CODE_COMMUNE_COLUMN, DATA_NATURE_MUTATION_COLUMN,
	DATA_TYPE_LOCAL_COLUMN, DATA_SURFACE_TERRAIN_COLUMN, DATA_SURFACE_REELLE_COLUMN,
	DATA_NB_PIECES_COLUMN, DATA_DATE_COLUMN, DATA_VALEUR_FONCIERE_COLUMN
]
DATA_NATURE_MUTATION_VENTE_VALUE = "Vente"
DATA_TYPE_LOCAL_VALUE = [
	"Appartement", "Maison"
]
DATA_SIZE = 100_000

GEO_DATA_FILE_PATH = "./data/20230823-communes-departement-region.csv"
GEO_DATA_SEP_CHAR = ","
GEO_DATA_CODE_COMMUNE_COLUMN = "code_commune"
GEO_DATA_LATITUDE_COLUMN = "latitude"
GEO_DATA_LONGITUDE_COLUMN = "longitude"
GEO_DATA_COLUMNS = [
	GEO_DATA_CODE_COMMUNE_COLUMN, GEO_DATA_LATITUDE_COLUMN, GEO_DATA_LONGITUDE_COLUMN
]

XGB_MODEl_PATH = "./models/xgb"
XGB_TEST_SET_PATH = "./models/xgb_test"

DATA_COLUMNS_STR = {column: column for column in DATA_COLUMNS}
DATA_COLUMNS_STR[DATA_SURFACE_REELLE_COLUMN] = "Surface réelle"
DATA_COLUMNS_STR.pop(DATA_NATURE_MUTATION_COLUMN)
DATA_COLUMNS_STR.pop(DATA_VALEUR_FONCIERE_COLUMN)

# ------------------------------------------------------------------------------------------------ #