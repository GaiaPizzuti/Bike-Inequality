"""
This script is used to create a file in which each line represent the movement from a neighborhood to another.
In particular, each movement is represented by the size of the starting population and how many trips end in that second neighborhood.
"""

import pandas as pd
import sys
import os

sys.path.append('src')
from starter import data_indexes, data_normalized, _types, data_social, data_normalized_destinations, data_destinations
from social_mixing import get_normalized_index

is_normalized = True

city = sys.argv[1]

def get_data(data, city):
    """
    Function to get the data of the city
    """
    path = os.path.join(data, city) + '.csv'
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
    
    return df

def get_city_normalized_index():
    """
    Function to get the normalized index of the city
    """

    city_df = get_data(data_indexes, city)

    social_path = os.path.join(data_social, city)
    social_path = os.path.join(social_path, "2022")

    normalized_path = os.path.join(data_normalized, city) + '.csv'

    if os.path.exists(normalized_path):
        return
    
    normalized = dict()
    
    for _, row in city_df.iterrows():
        path = os.path.join(social_path, row["zipcode"])
        normalized[row["zipcode"]] = {type: get_normalized_index(row[type], path) for type in _types}
    
    with open(normalized_path, 'w') as f:
        f.write("zipcode,age,household,family,nonfamily,married,race\n")

        for zipcode, types in normalized.items():
            line = str(zipcode)
            for type, value in types.items():
                line += ',' + str(value)
            line += '\n'
            f.write(line)

def get_normalized_destination():
    """
    Function to get the normalized index for the destinations
    """

    destination_df = get_data(data_destinations, city)
    # get only the station and zipcode columns
    destination_df = destination_df[['zipcode', 'station']]

    normalized_df = get_data(data_normalized, city)

    social_path = os.path.join(data_social, city)
    social_path = os.path.join(social_path, "2022")

    # normalized file
    normalized_path = os.path.join(data_normalized_destinations, city) + '.csv'

    if os.path.exists(normalized_path):
        return
    
    for _, row in destination_df.iterrows():
        zipcode = row['zipcode']

        indexes = normalized_df[normalized_df['zipcode'] == zipcode]
        
        if indexes.empty:
            continue

        destination_df.loc[destination_df['zipcode'] == zipcode, 'age'] = indexes['age'].values[0]
        destination_df.loc[destination_df['zipcode'] == zipcode, 'household'] = indexes['household'].values[0]
        destination_df.loc[destination_df['zipcode'] == zipcode, 'family'] = indexes['family'].values[0]
        destination_df.loc[destination_df['zipcode'] == zipcode, 'nonfamily'] = indexes['nonfamily'].values[0]
        destination_df.loc[destination_df['zipcode'] == zipcode, 'married'] = indexes['married'].values[0]
        destination_df.loc[destination_df['zipcode'] == zipcode, 'race'] = indexes['race'].values[0]

    destination_df.to_csv(normalized_path, index=False)

if __name__ == '__main__':
    get_normalized_destination()