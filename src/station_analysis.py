import pandas as pd
import sys
import os
import numpy as np

from util.plots import *
from social_mixing import get_indexes, get_mean_index
from starter import _types, data_indexes, data_stations
from util.create_station_file import create_csv

path = 'data\\social'
_year = '2022'

def get_stations_zipcodes(city):
    
    stations_zipcodes = dict()
    
    path = data_stations + city + '.csv'
    # path example -> 'data\\stations\\Chicago.csv'
    
    df = pd.read_csv(path, encoding="ISO-8859-1", dtype={'zipcode': str})
    
    for index, row in df.iterrows():
        station = row['station']
        zipcode = str(row['zipcode'])
        
        if zipcode not in stations_zipcodes:
            stations_zipcodes[zipcode] = 0
        
        stations_zipcodes[zipcode] += 1
    
    return stations_zipcodes

def get_station_indexes(station, city):
    """
    Function to get the indexes of each station in a city. Each station has a zipcode and each zipcode has an index for each type.
    The function will return a dictionary with the indexes of each type.

    Args:
        - station: station name
        - city: city name
    """
    
    station_path = data_stations + city + '.csv'
    index_path = data_indexes + city + '.csv'
    
    # get the zipcode of the station in the station file
    station_df = pd.read_csv(station_path, encoding='cp1252', dtype={'zipcode': str})
    station_info = station_df[station_df['station'] == station]
    
    if station_info.isnull().values.any():
        return None
    
    zipcode = station_info['zipcode'].values[0]
    
    # get the indexes of the zipcode in the index file
    index_df = pd.read_csv(index_path, encoding='cp1252', dtype={'location': str})
    index_info = index_df[index_df['location'] == zipcode]
    
    if index_info.empty:
        return None
    
    indexes = dict()
    
    for type in _types:
        indexes[type] = index_info[type].values[0]
    
    return indexes

def get_zipcode_indexes(zipcode):
    """
    Function to get the indexes of a specific zipcode. Each zipcode has an index for each type.

    Args:
        zipcode (string): zipcode
    """
    index_path = data_indexes + city + '.csv'
    
    # get the indexes of the zipcode in the index file
    index_df = pd.read_csv(index_path, encoding='cp1252', dtype={'location': str})
    index_info = index_df[index_df['location'] == zipcode]
    
    indexes = dict()
    
    for type in _types:
        indexes[type] = index_info[type].values[0]
        
    print(indexes)
    
    return indexes


def get_bikes_indexes(indexes, city, data=None):
    """
    Function to get the distribution of social mixing index for each bike station.
    
    Input:
        - indexes: dict with the social mixing index for each zipcode
    
    Output:
        - bikes_indexes: dict indicating the number of stations with a specific social mixing index
    """
    
    bikes_indexes = {
        'gender': dict(),
        'household': dict(),
        'family': dict(),
        'nonfamily': dict(),
        'married': dict(),
        'race': dict()
    }
    
    stations = get_stations_zipcodes(city)
    
    for zipcode, count in stations.items():
        if zipcode not in indexes:
            continue
        index = indexes[zipcode]
        for key, value in index.items():
            if key not in bikes_indexes:
                bikes_indexes[key] = dict()
            if value not in bikes_indexes[key]:
                bikes_indexes[key][value] = 0
            bikes_indexes[key][value] += count
    
    if data:
        return bikes_indexes[data]
    
    return bikes_indexes

# ------------------------------------------ print indexes ------------------------------------------

def print_indexes(indexes, type=None):
    """
    Function to print the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    print('-' * 50)
    if type:
        print('\tSocial Mixing Index for ' + type)
    for key, values in indexes.items():
        print(key, values)
    print('-' * 50)

def get_city_data(data, type=None):
    
    city_path = os.path.join(path, data)
    # city_path example -> 'data\\social\\Chicago'
    
    full_path = os.path.join(city_path, _year)
    # full_path example -> 'data\\social\\Chicago\\2022'
    
    csv_path = data_indexes + data + '.csv'
    
    zipcodes = dict()
    
    # remove the file if it already exists
    if not os.path.exists(csv_path):
    
        for location in os.listdir(full_path):
            # check if the location is a directory
            check = os.path.join(full_path, location)
            # check example -> 'data\\social\\Chicago\\2022\\60601'
            
            if os.path.isdir(check):
                location_path = os.path.join(full_path, location)
                
                # get the social mixing index for the location
                indexes = get_zipcode_indexes(location)
                
                # save the indexes in a csv file
                create_csv(indexes, location, csv_path)
                
                zipcodes[location] = indexes
    else:
        
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                
                if 'location' in line:
                    continue
                
                datas = line.split(',')
                indexes = dict()
                
                for index, key in enumerate(_types):
                    indexes[key] = float(datas[index + 1])
            
                zipcodes[datas[0]] = indexes

    bikes_indexes = get_bikes_indexes(zipcodes, data, type)
    return bikes_indexes

def get_type_data(data):
    
    full_data = dict()
    
    for city in os.listdir(path):
        
        if city == "Austin":
            continue
        
        print(f"\tCalculating the indexes for {city}")
        
        type_data = get_city_data(city, data)
        full_data[city] = type_data
    
    return full_data

def get_station_analysis(data, data_to_analyse='city'):
    if data_to_analyse == 'city':
    
        bikes_data = get_city_data(data)
        plot_stations_indexes(bikes_data)
        
        print('-' * 50)
        print('\tSocial mixing index calculated and saved in the csv file.')
        
        path = 'data\\indexes\\' + data + '.csv'
        extract_indexes = get_indexes(path)
        final_index = get_mean_index(extract_indexes)

        print_indexes(final_index)

    else:
        
        type_data = get_type_data(data)
        subplot_indexes_per_types(type_data, data)