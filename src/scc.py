import esda
import pandas as pd
import geopandas as gpd
import libpysal as lps
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
import sys
import os
import seaborn as sns
from copy import deepcopy

sys.path.append('src')
from starter import zipcode_file, data_indexes, data_osm, data_destinations

# read only the zipcodes in the index dataframe
zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")

osm_types = {
    'building': ['building'],
    'commercial': ['shop', 'tourism', 'office'],
    'emergency': ['emergency'],
    'government': ['government', 'military'],
    'healthcare': ['healthcare'],
    'landuse': ['landuse'],
    'natural': ['natural'],
    'power': ['power', 'backup_generator'],
    'public': ['historic'],
    'sport': ['sport'],
    'transportation': ['aeroway', 'highway', 'railway', 'waterway'],
}

amenities = {
    'commercial': ['marketplace', 'restaurant', 'fast_food', 'cafe', 'bar', 'pub'],
    'education': ['kindergarten', 'school', 'college', 'university', 'language_school'],
    'emergency': ['police', 'fire_station'],
    'financial': ['atm', 'bank', 'bureau_de_change', 'microfinance', 'mobile_money_agent', 'money_transfer'],
    'governement': ['court_house', 'townhall', 'embassy', 'post_office'],
    'healthcare': ['doctors', 'dentist', 'clinic', 'toilets', 'hospital', 'pharmacy'],
    'power': ['fuel'],
    'public': ['place_of_worship', 'community_centre', 'library', 'toilets'],
    'transportation': ['ferry_terminal', 'bus_station']
}

leisures = {
    'sport': ['stadium', 'swimming pool', 'pitch', 'sport_centre'],
    'landuse': ['park'],
}

def scc(city, type = None):

    # read only the zipcodes in the index dataframe
    zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")
    
    print('reading the indexes data')
    path = os.path.join(data_indexes, city + '.csv')
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})

    path_indexes = os.path.join(data_destinations, city + '.csv')
    df_index = pd.read_csv(path_indexes, encoding='cp1252', dtype={'zipcode': str})

    # get only the zipcodes that are in the index map
    zicodes = df["zipcode"].unique()
    df_index =  df_index[df_index["zipcode"].isin(zicodes)]

    # remove station column
    df_index = df_index.drop(columns=["station"])

    # in the DataFrame there are multiple lines for the same zipcode, so we need to group them
    df_index = df_index.groupby("zipcode").mean().reset_index()
    
    df_osm = get_pois(city, type)

    print('adding the zipcodes to the dataframe')

    # add the zipcodes to the dataframe using sjoin -> zipcode and ZCTA5CE10 columns
    pois_by_zip = gpd.sjoin(df_osm, zipcode_gdf, how="inner", predicate="within")

    # rename the columns
    pois_by_zip.rename(columns={"ZCTA5CE10": "zipcode"}, inplace=True)
    zipcode_gdf.rename(columns={"ZCTA5CE10": "zipcode"}, inplace=True)

    print('grouping the data by zipcode')

    # group the data by zipcode (count the number of points in each zipcode)
    poi_counts = pois_by_zip.groupby("zipcode").size().reset_index(name="poi_count")

    print('merging the dataframes')

    zipcode_gdf = zipcode_gdf.merge(df_index, on="zipcode", how="left")
    zipcode_gdf = zipcode_gdf.merge(poi_counts, on="zipcode", how="left")
    zipcode_gdf["poi_count"].fillna(0, inplace=True)  # Fill ZIP codes with no POIs

    print('calculating the density of POIs')

    zipcode_gdf["poi_density"] = zipcode_gdf["poi_count"] / zipcode_gdf["geometry"].area

    print('plotting the data')

    # select only zipcodes with at least one POI
    zipcode_gdf = zipcode_gdf[zipcode_gdf["poi_count"] > 0]
    
    # select only zipcodes in the index dataframe
    zipcode_gdf = zipcode_gdf[zipcode_gdf["zipcode"].isin(df_index["zipcode"])]

    print('calculating the Moran\'s I')

    weights = lps.weights.Queen.from_dataframe(zipcode_gdf)

    y = zipcode_gdf["race"]
    x = zipcode_gdf["poi_density"]

    moran = esda.Moran(x, weights)
    print(f"Moran's I: {moran.I}, p-value: {moran.p_sim}")

    # plot the data
    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    zipcode_gdf.plot(column="poi_density", ax=axes[0], legend=True, cmap="plasma")
    axes[0].set_title("POI Density")

    print(zipcode_gdf.poi_density)

    zipcode_gdf.plot(column="race", ax=axes[1], legend=True, cmap="viridis")
    axes[1].set_title("Mixing Index")
    
    plt.suptitle(city)

    plt.show()

    sns.scatterplot(data=zipcode_gdf, x="poi_density", y="race")
    plt.title("Correlation Between POI Density and Mixing Index for " + city)
    plt.show()

def get_pois(city, type = None):
    """
    Function to get the category of the POIs in the city
    """
    print('reading the zipcodes data')

    print('reading the POIs data')
    path_osm = os.path.join(data_osm, city + '.geojson')
    df_osm = gpd.read_file(path_osm).to_crs(zipcode_gdf.crs)

    # filter the POIs by type and the leisure dictionary
    new_df = deepcopy(df_osm)

    # clear the dataframe
    new_df.drop(new_df.index, inplace=True)
    if type:
        if type in osm_types:
            for key in osm_types[type]:
                df = df_osm.loc[df_osm[key].notnull()]
                new_df = pd.concat([new_df, df])
        
        if type in amenities:
            for key in amenities[type]:
                df = df_osm.loc[df_osm['amenity'] == key]
                new_df = pd.concat([new_df, df])
        
        if type in leisures:
            for key in leisures[type]:
                df = df_osm.loc[df_osm['leisure'] == key]
                new_df = pd.concat([new_df, df])

        return new_df
    
    return df_osm

city = sys.argv[1]
for type in ['building', 'commercial', 'education', 'public', 'healthcare', 'transportation']:
    scc(city, type)