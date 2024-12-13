from station_analysis import *
from social_mixing import *
from comparison_stations import *
from starter import data_indexes, _types, data_destinations

import pandas as pd

is_zipcode = False
is_mean = True
is_type = True

# UPPERBOUNDS
# age: 18 classes -> ln(18) = 2.89
# income: 10 classes -> ln(10) = 2.30
# race: 9 classes -> ln(9) = 2.20

def get_destination_map():
    """
    Function to plot the map of the indexes of each zipcode based on the trips that end in that zipcode
    """
    df = get_each_zipcode_mean(city)
    df = get_percentage_values(df)
    
    if is_type:
        type = sys.argv[2]
        zipcodes = plot_heatmap_on_map(df, type, city)
    else:
        plot_zipcode_heatmap(df, city)
    return zipcodes

def get_index_map(zipcodes):
    """
    Function to plot the map of the indexes of each zipcode
    """
    
    path = os.path.join(data_indexes, city) + '.csv'
    path_destination = os.path.join(data_destinations, city) + '.csv'
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
    df_destination = pd.read_csv(path_destination, encoding='cp1252', dtype={'zipcode': str})
    
    # get only the zipcodes that are in the destination map
    df = df[df['zipcode'].isin(zipcodes)]
    
    print(f'Mean of {type} for the city of {city}:\t', df[type].mean())
    print(f'Mean of {type} for the city of {city} based on ending trips:\t', df_destination[type].mean())
    
    print(f'Median of {type} for the city of {city}:\t', df[type].median())
    print(f'Median of {type} for the city of {city} based on ending trips:\t', df_destination[type].median())
    
    print(f'Standard deviation of {type} for the city of {city}:\t', df[type].std())
    print(f'Standard deviation of {type} for the city of {city} based on ending trips:\t', df_destination[type].std())
    
    print(f'Variance of {type} for the city of {city}:\t', df[type].var())
    print(f'Variance of {type} for the city of {city} based on ending trips:\t', df_destination[type].var())
    
    
    # transform the values into percentages
    df = get_percentage_values(df)
    plot_heatmap_on_map(df, type, city)

city = sys.argv[1]
type = sys.argv[2]
zipcodes = get_destination_map()
get_index_map(zipcodes)