import pandas as pd
import sys
import os
import numpy as np

sys.path.append('src')
from station_analysis import get_zipcode_indexes, get_station_indexes, get_stations_zipcodes

_types  = ['gender', 'household', 'family', 'nonfamily', 'married', 'race']

def get_mean_indexes_file(city):
    
    path = f'data\\destinations\\{city}.csv'
    bike_path = f'data\\bikes\\{city}\\2022'
    zipcode_path = f'data\\stations\\{city}.csv'
    zipcode_df = pd.read_csv(zipcode_path, encoding='cp1252', dtype={'zipcode': str})
    
    arrival_averages = dict()
    stations_indexes = dict()
    
    if os.path.exists(path):
        return
    
    for month in os.listdir(bike_path):
    
        file = os.path.join(bike_path, month)
        df = pd.read_csv(file)
        df = df.dropna()
        
        print('Processing month: ', month)
        
        for index, row in df.iterrows():
            
            departure = row['station_start']
            arrival = row['station_end']
            
            if arrival not in arrival_averages:
                arrival_averages[arrival] = {type: list() for type in _types}
            
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
                arrival_averages[arrival][type].append(indexes[type])
    
    with open(path, 'w') as f:
        f.write('station,zipcode,gender,household,family,nonfamily,married,race\n')
        
        # get the mean for each type for each arrival station
        for station, types in arrival_averages.items():
            
            zipcode = zipcode_df[zipcode_df['station'] == station]['zipcode'].values[0]
            
            line = str(station) + ',' + str(zipcode)
            for type, values in types.items():
                mean = np.mean(values)

                line += ',' + str(mean)
            
            line += '\n'
            f.write(line)

if __name__ == '__main__':
    
    city = sys.argv[1]
    get_mean_indexes_file(city)