import pandas as pd
import sys
import os
import numpy as np

sys.path.append('src')
from station_analysis import get_station_indexes
from starter import data_bikes, data_stations, data_destinations, data_trips, data_filtered_trips, data_filtered_destinations

year = 2022
_types = ['age','household','family','nonfamily','married','race']
spring = True

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

def get_destinations_indexes_file(city, year, path, trips_path):
    
    bike_path = os.path.join(data_bikes, city) + f'/{year}'

    trips_df = pd.read_csv(trips_path, dtype={'arrival': str, 'departure': str})
    
    zipcode_path = os.path.join(data_stations, year, city) + '.csv'
    zipcode_df = pd.read_csv(zipcode_path, encoding='cp1252', dtype={'zipcode': str})
    
    arrival_averages = dict()
    stations_indexes = dict()
    
    # iterate over each month file in the bike data
    for month in os.listdir(bike_path):
    
        if spring and month[4:6] not in ['04', '05', '06']:
            print('Skipping month: ', month)
            continue
        
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
                indexes = get_station_indexes(departure, year, city)
                stations_indexes[departure] = indexes
            else:
                indexes = stations_indexes[departure]
            
            if indexes is None:
                continue
            
            # insert the indexes in the arrival indexes dict
            for type in _types:
                
                if departure not in arrival_averages[arrival][type]:
                    arrival_averages[arrival][type][departure] = indexes[type]


    # create the output folder if it does not exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

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
    year = sys.argv[2]
    if len(sys.argv) > 3 and sys.argv[3] == 'filtered':
        filtered = True
    else:
        filtered = False

    if filtered:
        output_city_path = data_filtered_destinations
        trips_city_path = data_filtered_trips
    else:
        output_city_path = data_destinations
        trips_city_path = data_trips

    if spring:
        output_city_path = os.path.join(output_city_path, 'spring')
        trips_city_path = os.path.join(trips_city_path, 'spring')
    output_path = os.path.join(output_city_path, year, city) + '.csv'
    trips_path = os.path.join(trips_city_path, year, city) + '.csv'

    get_destinations_indexes_file(city, year, output_path, trips_path)