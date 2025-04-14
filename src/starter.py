import pathlib
import geopandas as gpd

zipcode_filename = "tl_2017_us_zcta510.zip"
zipcode_file = pathlib.Path(zipcode_filename)
zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")


# boolean to enable/disable debug mode -> print results
debug = False

# boolean to enable/disable the use of the categorical data
categorical = False

# path to the trips data
data_bikes = 'data/bikes'

# path to the U.S. social data
data_social = 'data/social'

# path to the indexes data
data_indexes = 'data/indexes'

# path to the stations data
data_stations = 'data/stations'

# path to the destinations data
data_destinations = 'data/destinations'

# path for the difference data
data_differences = 'data/differences'

# path for the normalized data
data_normalized = 'data/normalized'

# path for the OpenStreetMap data
data_osm = 'data/osm'

# path for the normalized destinations data
data_normalized_destinations = 'data/normalized_destinations'

# path for the number of trips data
data_trips = 'data/trips'