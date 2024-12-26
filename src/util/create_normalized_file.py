"""
This script is used to create a file in which each line represent the movement from a neighborhood to another.
In particular, each movement is represented by the size of the starting population and how many trips end in that second neighborhood.
"""

import pandas as pd
import sys
import os

sys.path.append('src')
from starter import data_bikes, data_stations, data_destinations, _types, data_normalized

def get_station_zipcode(station, city):
    """
    Function to get the zipcode of a station

    Args:
        station (str): The station name
        city (str): The city name
        
    Returns:
        str: The zipcode of the station
    """
    
    path = os.path.join(data_stations, city) + '.csv'
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
    
    # check if the station is in the dataframe
    if station not in df['station'].values:
        return None
    
    return df[df['station'] == station]['zipcode'].values[0]

def get_trips_informations(city):
    """
    Function to get the informations about the trips
    
    Parameters:
        city (str): the city to analyze
    """
    
    path = os.path.join(data_bikes, city, '2022')
    
    datas = dict()
    
    zipcodes = dict()
    
    for file in os.listdir(path):
        
        print('Processing file: ', file)
        
        full_path = os.path.join(path, file)
        df = pd.read_csv(full_path, encoding='cp1252')
        
        for index, row in df.iterrows():
            
            departure = row['station_start']
            arrival = row['station_end']
            
            if departure in zipcodes:
                departure_zipcode = zipcodes[departure]
            else:
                departure_zipcode = get_station_zipcode(departure, city)
                zipcodes[departure] = departure_zipcode
                
            if arrival in zipcodes:
                arrival_zipcode = zipcodes[arrival]
            else:
                arrival_zipcode = get_station_zipcode(arrival, city)
                zipcodes[arrival] = arrival_zipcode
            
            if departure_zipcode is None or arrival_zipcode is None:
                continue
            
            if departure_zipcode not in datas:
                datas[departure_zipcode] = dict()
                
            if arrival_zipcode not in datas[departure_zipcode]:
                datas[departure_zipcode][arrival_zipcode] = 0
            
            datas[departure_zipcode][arrival_zipcode] += 1
        
    return datas

def create_normalized_file(city):
    """
    Function to create the normalized file
    
    Parameters:
        city (str): the city to analyze
    """
    
    path = os.path.join(data_normalized, city) + '.csv'
    datas = get_trips_informations(city)
    
    with open(path, 'w') as f:
        f.write('departure,arrival,trips,percent\n')
        
        for departure, arrivals in datas.items():
            total = sum(arrivals.values())
            
            for arrival, size in arrivals.items():
                f.write(str(departure) + ',' + str(arrival) + ',' + size + ',' + str(size / total) + '\n')

if __name__ == '__main__':
    
    city = sys.argv[1]
    create_normalized_file(city)