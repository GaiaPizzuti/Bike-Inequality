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

sys.path.append('src')
from starter import zipcode_file, data_destinations, data_indexes, data_osm

def scc(city):
    
    print('reading the indexes data')
    path_indexes = os.path.join(data_indexes, city + '.csv')
    df_index = pd.read_csv(path_indexes, encoding='cp1252', dtype={'zipcode': str})
    
    print('reading the zipcodes data')
    # read only the zipcodes in the index dataframe
    zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")

    print('reading the POIs data')
    path_osm = os.path.join(data_osm, city + '.geojson')
    df_osm = gpd.read_file(path_osm).to_crs(zipcode_gdf.crs)

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


city = 'NYC'
scc(city)