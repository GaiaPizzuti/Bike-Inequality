from station_analysis import *
from social_mixing import *
from comparison_stations import *
from starter import data_indexes, data_destinations, data_normalized_destinations, _types
import pandas as pd
import numpy as np

is_zipcode = False
is_mean = True
is_type = True

# UPPERBOUNDS
# age: 18 classes -> ln(18) = 2.89
# income: 10 classes -> ln(10) = 2.30
# race: 9 classes -> ln(9) = 2.20

_upperbound = [2.89, 2.30, 2.30, 2.30, 2.30, 2.20]

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

def get_data(data):
    """
    Function to plot the map of the indexes of each zipcode based on the normalized values
    """
    path = os.path.join(data, city) + '.csv'
    df = pd.read_csv(path, encoding='cp1252', dtype={'zipcode': str})
    
    return df

def get_index_map():
    """
    Function to plot the map of the indexes of each zipcode
    """
    
    df = get_data(data_indexes)
    df_destination = get_data(data_destinations)
    
    # get only the zipcodes that are in the destination map
    zipcodes = get_zipcodes(data_destinations)
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

def get_zipcodes(data):
    """
    Function to get the zipcodes of the city in the destination map
    """

    df = get_data(data)
    return df['zipcode'].unique()

def get_normalized_data(type):
    """
    Function to plot the map of the indexes of each zipcode based on the normalized values

    Args:
        type (str): the type of index to plot
    """
    df = get_data(data_normalized_destinations)

    # standardize the values
    mean = np.mean(df[type])
    std = np.std(df[type])

    print(f'Mean of {type} for the city of {city}:\t', mean)
    print(f"Standard deviation of {type} for the city of {city}:\t", std)

    print(df.head())

    df[type] = (df[type] - mean) / std

    print(df.head())
    plot_heatmap_on_map(df, type, city)

city = sys.argv[1]
#type = sys.argv[2]

for type in _types:
    get_normalized_data(type)
    print('-' * 50)

# index / upperbound
# (index / total_population) / (upperbound / total_population)
# index / upperbound