import os
import sys
import pandas as pd

sys.path.append('src')
from station_analysis import get_station_indexes
from starter import _types, data_differences, data_bikes

cities = ['Boston', 'Chicago', 'Columbus', 'NYC', 'Philly', 'SanFrancisco', 'Washington']

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

def get_difference_file(city):
    """
    Function to get the difference between the various stations and zipcodes.
    
    Input:
        - city: string with the city name
    """
    
    path = os.path.join(data_differences, city) + '.csv'
    
    if os.path.exists(path):
        return
    
    bike_path = os.path.join(data_bikes, city, '2022')
    stations_differences = dict()
    
    for month in os.listdir(bike_path):
        
        print("Processing month: ", month)
        
        file = os.path.join(bike_path, month)
        # example file = 'data\\bikes\\Chicago\\2022\\01'
        
        df = pd.read_csv(file)
        
        for index, row in df.iterrows():
            
            departure = row['station_start']
            arrival = row['station_end']
            
            if pd.isna(departure) or pd.isna(arrival):
                continue
            
            if departure not in stations_differences:
                stations_differences[departure] = dict()
                
            if arrival not in stations_differences[departure]:
                stations_differences[departure][arrival] = dict()
                stations_differences[departure][arrival]['counter'] = 0
            
            
                difference = get_difference_stations(departure, arrival, city)
                
                if difference is None:
                    continue
                
                for type in _types:
                    stations_differences[departure][arrival][type] = difference[type]
            else:
                stations_differences[departure][arrival]['counter'] += 1
    
    with open(path, 'w') as f:
        f.write('departure,arrival,counter,gender,household,family,nonfamily,married,race\n')
        
        for departure, trips in stations_differences.items():
            
            for arrival, indexes in trips.items():
                
                line = str(departure) + ',' + str(arrival) + ','
                
                for index in indexes.values():
                    line += str(index) + ','
                
                line = line[:-1] + '\n'
                f.write(line)

if __name__ == '__main__':
    
    city = sys.argv[1]
    get_difference_file(city)