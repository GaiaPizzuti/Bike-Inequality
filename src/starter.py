import pathlib
import urllib.request
import geopandas as gpd

states_filename = "tl_2017_us_state.zip"
states_url = f"https://www2.census.gov/geo/tiger/TIGER2017/STATE/{states_filename}"
states_file = pathlib.Path(states_filename)

zipcode_filename = "tl_2017_us_zcta510.zip"
zipcode_url = f"https://www2.census.gov/geo/tiger/TIGER2017/ZCTA5/{zipcode_filename}"
zipcode_file = pathlib.Path(zipcode_filename)

for data_file, url in zip([states_file, zipcode_file], [states_url, zipcode_url]):
    if not data_file.is_file():
        with urllib.request.urlopen(url) as response, open(data_file, 'wb') as f:
            f.write(response.read())

zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")
states_gdf = gpd.read_file(f"zip://{states_file}")


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

# parth for the difference data
data_differences = 'data\\differences'

# list of the types of data
_types = ['age', 'household', 'family', 'nonfamily', 'married', 'race']

# list of the incomes types
_incomes = ['household', 'married', 'nonfamily', 'family']