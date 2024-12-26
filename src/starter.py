import pathlib
import urllib.request
import geopandas as gpd

states_filename = "tl_2017_us_state.zip"
states_url = f"https://www2.census.gov/geo/tiger/TIGER2017/STATE/{states_filename}"
states_file = pathlib.Path(states_filename)

zipcode_filename = "tl_2017_us_zcta510.zip"
zipcode_url = f"https://www2.census.gov/geo/tiger/TIGER2017/ZCTA5/{zipcode_filename}"
zipcode_file = pathlib.Path(zipcode_filename)



# boolean to enable/disable debug mode -> print results
debug = False

# boolean to enable/disable the use of the categorical data
categorical = False

# path to the trips data
data_bikes = 'data\\bikes'

# path to the U.S. social data
data_social = 'data\\social'

# path to the indexes data
data_indexes = 'data\\indexes'

# path to the stations data
data_stations = 'data\\stations'

# path to the destinations data
data_destinations = 'data\\destinations'

# path for the difference data
data_differences = 'data\\differences'

# path for the normalized data
data_normalized = 'data\\normalized'

# path for the OpenStreetMap data
data_osm = 'data\\osm'

# list of the types of data
_types = ['age', 'household', 'family', 'nonfamily', 'married', 'race']

# list of the incomes types
_incomes = ['household', 'married', 'nonfamily', 'family']