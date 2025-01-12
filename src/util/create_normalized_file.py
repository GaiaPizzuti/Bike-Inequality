"""
This script is used to create a file in which each line represent the movement from a neighborhood to another.
In particular, each movement is represented by the size of the starting population and how many trips end in that second neighborhood.
"""

import pandas as pd
import sys
import os

sys.path.append('src')
from starter import data_indexes, data_normalized, _types, data_social
from social_mixing import get_normalized_index

city = sys.argv[1]

def get_city_normalized_index():
    """
    Function to get the normalized index of the city
    """
    city_path = os.path.join(data_indexes, city) + '.csv'
    city_df = pd.read_csv(city_path, encoding='cp1252', dtype={'zipcode': str})

    social_path = os.path.join(data_social, city)
    social_path = os.path.join(social_path, "2022")

    # normalized file
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

if __name__ == '__main__':
    get_city_normalized_index()