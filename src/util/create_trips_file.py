import os
import sys
import pandas as pd

sys.path.append("src")
from starter import data_bikes, data_trips, data_stations, data_filtered_trips
from create_station_file import get_station_zipcode

city = sys.argv[1]
year = sys.argv[2]

# check if there is a second argument
filtered = False
if len(sys.argv) > 3:
    if sys.argv[3] == 'filtered':
        filtered = True

def create_trips_file(city, filtered):
    """
    Function to create a file in which each row has a initial zipcode and a final zipcode and the number of trips
    starting from the initial zipcode and ending in the final zipcode
    """

    bikes_data = os.path.join(data_bikes, city, year)
    files = os.listdir(bikes_data)

    df_station = pd.read_csv(os.path.join(data_stations, city) + '.csv', encoding='cp1252', dtype={'zipcode': str})

    stats = {}

    for file in files:
        print(file)
        path = os.path.join(bikes_data, file)
        df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
        
        for _, row in df.iterrows():

            # get station start and end zipcodes from the station file
            departure = df_station[df_station['station'] == row['station_start']]['zipcode']
            arrival = df_station[df_station['station'] == row['station_end']]['zipcode']

            if departure.empty or arrival.empty:
                continue

            if filtered:
                if row.usertype == 'casual' or row.usertype == 'Day Pass' or row.usertype == 'Customer':
                    continue
            
            departure = departure.values[0]
            arrival = arrival.values[0]

            if departure not in stats:
                stats[departure] = {}

            if arrival not in stats[departure]:
                stats[departure][arrival] = 0

            # increment the number of trips from departure to arrival
            stats[departure][arrival] += 1
    
    if filtered:
        output_file = data_filtered_trips
    else:
        output_file = data_trips
    
    output_file = os.path.join(output_file, year)
    
    with open(os.path.join(output_file, city) + '.csv', 'w') as f:
        f.write('departure,arrival,trips\n')
        for departure in stats:
            for arrival in stats[departure]:
                f.write(f'{departure},{arrival},{stats[departure][arrival]}\n')
    
def get_ratio(city):
    """
    Function that takes the trip DataFrame of the city and calculates for each zipcode the ratio between the number
    of trips that ends in a destination and the total number of trips that start in that zipcode

    Args:
        city: str -> the city to analyze
    """
    
    df = pd.read_csv(os.path.join(data_trips, year, city) + '.csv', encoding='cp1252', dtype={'departure': str, 'arrival': str})
    
    # get the list of zipcodes
    zipcodes = df['departure'].unique()

    for _, row in df.iterrows():
        departure = row['departure']
        arrival = row['arrival']
        trips = row['trips']

        # get the total number of trips starting from the departure zipcode
        total = df[df['departure'] == departure]['trips'].sum()

        # calculate the ratio
        # thus the ratio represent the number of trips that ends in a destination
        # divided by the total number of trips that start in that zipcode
        df.loc[(df['departure'] == departure) & (df['arrival'] == arrival), 'ratio'] = trips / total
    
    # remove nan values
    df = df.dropna()
    
    # insert the new column in the DataFrame
    df.to_csv(os.path.join(data_trips, year, city) + '.csv', index=False)

create_trips_file(city, filtered)
get_ratio(city)