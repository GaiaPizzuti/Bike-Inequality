import pandas as pd
import sys
import os
import numpy as np

sys.path.append('src')
from station_analysis import get_station_indexes
from starter import _types, data_bikes, data_stations, data_destinations, data_trips, data_filtered_trips, data_filtered_destinations

year = 2022

def get_specific_trips(trips_df, departure_zipcode, arrival_zipcode):
    '''
    function to get the number of trips that start from a departure zipcode and end in an arrival zipcode

    Args:
        trips_df (dataframe): dataframe with the total number of trips for each zipcode
        departure_zipcode (str): departure zipcode
        arrival_zipcode (str): arrival zipcode

    Returns:
        int: number of trips that start from the departure zipcode and end in the arrival zipcode
    '''
    row = trips_df[(trips_df['departure'] == departure_zipcode) & (trips_df['arrival'] == arrival_zipcode)]
    if not row.empty:
        return row['trips'].values[0]
    else:
        return 0

def get_destinations_indexes_file(city, filtered=False):
    
    if filtered:
        path = os.path.join(data_filtered_destinations, city) + '.csv'
    else:
        path = os.path.join(data_destinations, city) + '.csv'
    
    bike_path = os.path.join(data_bikes, city) + f'/{year}'

    if filtered:
        trips_path = os.path.join(data_filtered_trips, city) + '.csv'
    else:
        trips_path = os.path.join(data_trips, city) + '.csv'
    trips_df = pd.read_csv(trips_path, dtype={'arrival': str, 'departure': str})
    
    zipcode_path = os.path.join(data_stations, city) + '.csv'
    zipcode_df = pd.read_csv(zipcode_path, encoding='cp1252', dtype={'zipcode': str})
    
    arrival_averages = dict()
    stations_indexes = dict()
    
    for month in os.listdir(bike_path):
    
        file = os.path.join(bike_path, month)
        df = pd.read_csv(file)
        df = df.dropna()
        
        print('Processing month: ', month)
        
        for _, row in df.iterrows():
            
            # name of the departure station
            departure = row['station_start']
            # name of the arrival station
            arrival = row['station_end']
            
            # if the arrival station is not in the dict, create a new entry
            if arrival not in arrival_averages:
                arrival_averages[arrival] = {type: dict() for type in _types}
            
            # if the departure station is not in the stations indexes dict, get the indexes
            if departure not in stations_indexes:
                # save the indexes from the departure station for future analysis
                indexes = get_station_indexes(departure, city)
                stations_indexes[departure] = indexes
            else:
                indexes = stations_indexes[departure]
            
            if indexes is None:
                continue
            
            # insert the indexes in the arrival indexes dict
            for type in _types:
                
                if departure not in arrival_averages[arrival][type]:
                    arrival_averages[arrival][type][departure] = indexes[type]

    with open(path, 'w') as f:
        f.write('station,zipcode,gender,household,family,nonfamily,married,race\n')
        
        total_length = len(arrival_averages)
        counter = 0
        # get the mean for each type for each arrival station
        for station, types in arrival_averages.items():

            counter += 1
            perc = round((counter / total_length) * 100, 2)
            print(f"Processing... ({perc}%)")
            
            # get the zipcode of the station
            zipcode = zipcode_df[zipcode_df['station'] == station]['zipcode'].values[0]
            

            line = str(station) + ',' + str(zipcode)
            for type, departures in types.items():
                
                mean = 0
                total_trips = 0
                for departure, value in departures.items():
                    
                    # get the zipcode of the departure station
                    zipcode_departure = zipcode_df[zipcode_df['station'] == departure]['zipcode'].values[0]

                    # get the number of trips that start from that zipcode and go to the arrival zipcode
                    departure_trips = get_specific_trips(trips_df, zipcode_departure, zipcode)
                    mean += value * departure_trips
                    total_trips += departure_trips

                if total_trips == 0:
                    line += ',0'
                    continue
                
                mean /= total_trips
                line += ',' + str(mean)
            
            line += '\n'
            f.write(line)

# 2.8 * 10
# 1.5 * 5
# 28 + 7.5 = 35.5
# 43 / 35.5 = 1.21
if __name__ == '__main__':
    
    city = sys.argv[1]

    # check if there is another argument: filtered
    if len(sys.argv) > 2 and sys.argv[2] == 'filtered':
        get_destinations_indexes_file(city, filtered=True)
    else:
        get_destinations_indexes_file(city)