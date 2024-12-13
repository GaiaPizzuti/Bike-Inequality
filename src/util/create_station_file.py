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

def create_csv(data, location, path):
    """
    Function to create a csv file with the data.
    
    Input:
        - data: list with the data to be saved
    """
    
    # check if the file already exists
    if not os.path.exists(path):
        with open(path, 'w') as f:
            header = 'zipcode,age,household,family,nonfamily,married,race\n'
            f.write(header)
            for item in data.values():
                line = '' + location + ','
                for item in data.values():
                    line += str(item) + ','
                line = line[:-1] + '\n'
            f.write(line)
    else:
        with open(path, 'a') as f:
            line = '' + location + ','
            for item in data.values():
                line += str(item) + ','
            line = line[:-1] + '\n'
            f.write(line)

if __name__ == '__main__':
    
    city = sys.argv[1]
    
    data_path = f'data\\bikes\\{city}\\2022'
    print("Creating stations file for city: ", city)
    
    create_stations(path, city)