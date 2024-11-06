import os
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import sys

sys.path.append('src')

# load the zipcode data
from block_analysis import zipcode_gdf

def get_station_zipcode(point):
    '''
    function to get the zipcode of each station given its latitude and longitude
    
    Inputs:
        - point: point object with the latitude and longitude of the station
    
    Outputs:
        - zipcode: zipcode of the station
    '''
    
    for index, row in zipcode_gdf.iterrows():
        if row['geometry'].contains(point):
            return row.ZCTA5CE10
    
    return None

def create_stations(path, city):
    """
    Function to analyse the data and create a file with the stations and their most important information
    
    Parameters:
        - path: path to the data file
    """
    
    stations = []
    
    newfile = 'data\\stations\\' + city + '.csv'
    
    # check if the file already exists
    if os.path.exists(newfile):
        os.remove(newfile)
    
    with open(newfile, 'w') as f:
        f.write('station,latitude,longitude,zipcode\n')
    
    for file in os.listdir(path):
        
        # example file = 'Divvy_Trips_2013.csv'
        
        print("\t - Analyzing file: ", file)
        
        full_path = os.path.join(path, file)
        
        # example full_path = 'data\\bikes\\Chicago\\Divvy_Trips_2022.csv'
        df = pd.read_csv(full_path)
        
        for index, row in df.iterrows():
            
            for type in ['start', 'end']:
                station = row['station_' + type]
                lat = row['latitude_' + type]
                lon = row['longitude_' + type]
                
                if station is not None and lat is not None and lon is not None:
                    if station not in stations:
                        stations.append(station)
                        
                        point = Point(lon, lat)
                        zipcode = get_station_zipcode(point)
                        
                        with open(newfile, 'a') as f:
                            f.write(str(station) + ',' + str(lat) + ',' + str(lon) + ',' + str(zipcode) + '\n')

if __name__ == '__main__':
    
    data_path = 'data\\bikes'
    
    can_be_created = False
    for city in os.listdir(data_path):

        if city == 'Chicago':
            can_be_created = True
        
        if can_be_created:
            print("Creating stations file for city: ", city)
            city_path = os.path.join(data_path, city)
            # example city_path = 'data\\bikes\\Chicago'
            
            path = os.path.join(city_path, '2022')
            
            create_stations(path, city)