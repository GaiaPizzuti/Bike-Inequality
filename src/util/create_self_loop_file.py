import pandas as pd
import sys
import os

sys.path.append('src')
from starter import data_trips, data_filtered_trips, data_self_loops, data_filtered_self_loops

def create_self_loop_file(city, year, filtered=False):
    """
    Function to create the file with the number of rides that start and end at the same zipcode.
    """

    if filtered:
        path = os.path.join(data_filtered_self_loops, year, city) + '.csv'
    else:
        path = os.path.join(data_self_loops, year, city) + '.csv'

    if filtered:
        trips_path = os.path.join(data_filtered_trips, year, city) + '.csv'
    else:
        trips_path = os.path.join(data_trips, year, city) + '.csv'

    self_loops = dict()
    trips_df = pd.read_csv(trips_path, dtype={'departure': str, 'arrival': str})
    for _, row in trips_df.iterrows():
        
        departure = row['departure']
        arrival = row['arrival']
        trips = row['trips']
        
        # non ha molto senso fare da arrival -> nel centro arrivano milioni di persone
        # self loop -> pensato per chi vive nel nodo e rimane nel nodo
        if arrival not in self_loops:
            self_loops[arrival] = {'loop': 0, 'total': 0}
        #if departure not in self_loops:
        #    self_loops[departure] = {'loop': 0, 'total': 0}
        
        if departure == arrival:
            self_loops[arrival]['loop'] += trips
        
        self_loops[arrival]['total'] += trips
        
    with open(path, 'w') as f:
        f.write('zipcode,self_loops,total_trips\n')
        for zipcode in self_loops:
            f.write(f"{zipcode},{self_loops[zipcode]['loop']},{self_loops[zipcode]['total']}\n")

if __name__ == "__main__":
    
    city = sys.argv[1]
    year = sys.argv[2]
    
    create_self_loop_file(city, year, filtered=False)
