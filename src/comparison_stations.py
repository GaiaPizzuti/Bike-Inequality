from station_analysis import get_zipcode_indexes, get_station_indexes
from util.plots import plot_stations_differences, plot_heatmap, plot_zipcode_heatmap

import pandas as pd
import os
import sys
import numpy as np

_types = ['age', 'household', 'family', 'nonfamily', 'married', 'race']

def get_difference_stations(departure, arrival, city):
    """
    Function to get the difference between two stations
    
    Input:
        - departure: string with the departure station
        - arrival: string with the arrival station
        - city: string with the city name
    """
    
    departure_indexes = get_station_indexes(departure, city)
    arrival_indexes = get_station_indexes(arrival, city)
    
    if departure_indexes is None or arrival_indexes is None:
        return None
    
    difference = dict()
    
    for type in _types:
        difference[type] = departure_indexes[type] - arrival_indexes[type]
    
    return difference

def get_difference_zipcodes(departure, arrival, city):
    """
    Function to get the difference between two zipcodes
    
    Input:
        - departure: string with the departure zipcode
        - arrival: string with the arrival zipcdoe
        - city: string with the city name
    """
    
    departure_indexes = get_zipcode_indexes(departure, city)
    arrival_indexes = get_zipcode_indexes(arrival, city)
    
    difference = dict()
    
    for type in _types:
        difference[type] = departure_indexes[type] - arrival_indexes[type]
    
    return difference

def get_differences(city):
    
    path = 'data\\differences\\' + city + '.csv'
    
    df = pd.read_csv(path, encoding='cp1252')
    
    df = df.dropna()
    
    # count how many times a certain index appears
    difference_indexes = {type : {} for type in _types}
    
    for index, row in df.iterrows():
        
        for type in _types:
            if row[type] not in difference_indexes[type]:
                difference_indexes[type][row[type]] = 0
            difference_indexes[type][row[type]] += row['counter']
            
    return difference_indexes

def get_mean_zipcode(city, zipcode):
    """
    Function to get the mean indexes for a certain zipcode

    Args:
        city (str): the city name
        zipcode (str): the zipcode to get the indexes
    """
    
    path = 'data\\destinations\\' + city + '.csv'
    
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
    
    df = df.dropna()
    df = df[df['zipcode'] == zipcode]
    
    return df

def get_mean_all_zipcodes(city):
    
    zipcodes = get_zipcodes(city)
    indexes = list()
    
    for zipcode in zipcodes:
        
        # get the stations of the zipcode
        df = get_mean_zipcode(city, zipcode)
        
        # choose a random station (the first one)
        if df.empty:
            continue
        line = df.iloc[0]
        
        # insert the indexes in the list
        indexes.append(line)
        
    new_df = pd.DataFrame(indexes)
    return new_df

def get_zipcode_mean(city):
    
    zipcodes = get_zipcodes(city)
    indexes = list()
    
    for zipcode in zipcodes:
        
        # get the stations of the zipcode
        df = get_mean_zipcode(city, zipcode)
        
        # choose a random station (the first one)
        if df.empty:
            continue
        
        zipcode_means = {type: list() for type in _types}
        for index, row in df.iterrows():
            for type in _types:
                zipcode_means[type].append(row[type])
        
        # get the mean for each type
        mean = {type: np.mean(values) for type, values in zipcode_means.items()}
        
        line = {'zipcode': zipcode}
        for type, value in mean.items():
            line[type] = value
            
        # insert the indexes in the list
        indexes.append(line)
        
    new_df = pd.DataFrame(indexes)
    print(new_df)
    return new_df

def get_zipcodes(city):
    
    path = f'data\\social\\{city}\\2022'
    zipcodes = []
    
    for zipcode in os.listdir(path):
        zipcodes.append(zipcode)
    
    return zipcodes

if __name__ == '__main__':
    
    city = sys.argv[1]
    is_zipcode = False
    is_mean = True
    
    if len(sys.argv) > 2:
        zipcode = str(sys.argv[2])
        is_zipcode = True
    
    if not is_mean:
        df = get_mean_zipcode(city, zipcode)
        df = get_mean_all_zipcodes(city)
    
        plot_heatmap(df, city, zipcode=is_zipcode)
    
    else:
        df = get_zipcode_mean(city)
        plot_zipcode_heatmap(df, city)