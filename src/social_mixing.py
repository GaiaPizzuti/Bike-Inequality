'''
we need to calculate the social mixing index for each location in order to calculate the social mixing index for the entire country.

The maximum is equal to ln(k), where k is the number of species in the location.
The minimum is 0, when all the species are equally distributed.

- gender: 18 classes -> ln(18) = 2.89
- income: 10 classes -> ln(10) = 2.30
- race: 9 classes -> ln(9) = 2.20
    - race general -> ln(7) = 1.95
'''

import pandas as pd
import sys
import os

from util.plots import *


path = 'data\\social'
_year = '2022'
_types = ['gender', 'household', 'family', 'nonfamily', 'married', 'race']

stations_analysis = True

def sdi(data):
    """
    Social Distancing Index (SDI) is a metric that quantifies the extent to which people are practicing social distancing.
    It is calculated as the average distance between people in a given area.
    """
    
    from math import log as ln
    
    def p(n, N):
        
        if n == 0:
            return 0
        else:
            return (float(n) / N) * ln(float(n) / N)
    
    N = sum(data.values())
    
    return -sum(p(n, N) for n in data.values() if n != 0)

def get_total_population(code):
    """
    Function to get the total population of a given location.
    
    Input:
        - code: string with the location code. The string is the path to the csv file with the data.
    
    Output:
        - population: int with the total population of the location
    """
    code = code + '\\gender.csv'
    df = pd.read_csv(code)
    
    return df['total_estimates'][0]

def get_age_distribution(code):
    """
    Function to get the age distribution of a given location.
    
    Input:
        - code: string with the location code. The string is the path to the csv file with the data.
    
    Output:
        - ages: list with the number of people in each age
    """
    
    df = pd.read_csv(code)
    
    ages = dict()
    
    read = False
    
    for index in range(len(df.index)):
        
        label = df['label'][index].replace(u'\xa0', '')
            
        if label == "Under 5 years":
            read = True
        
        if read:
            estimations = int(df['total_estimates'][index].replace(',', ''))
            ages[label] = estimations
        
        if label == "85 years and over":
            break


    return ages

def get_incomes_distribution(code):
    """
    Function to get the income distribution of a given location.
    
    Input:
        - code: string with the location code. The string is the path to the csv file with the data.
    
    Output:
        - households: list with the number of households in each income
        - family: list with the number of families in each income
        - non_family: list with the number of non-families in each income
        - married: list with the number of married couples in each income
    """
    
    df = pd.read_csv(code)
    
    incomes = {
        'household': dict(),
        'family': dict(),
        'nonfamily': dict(),
        'married': dict()
    }
    
    read = False
    
    for index in range(len(df.index)):
        if "Median income (dollars)" in df['label'][index]:
            break
        
        label = df['label'][index].replace(u'\xa0', '')
        
        if label == "Less than $10,000":
            read = True
        
        if read:
            if df['household_estimates'][index][:-1] != '':
                incomes['household'][label] = float(df['household_estimates'][index][:-1])
                incomes['family'][label] = float(df['family_estimates'][index][:-1])
                incomes['nonfamily'][label] = float(df['nonfamily_estimates'][index][:-1])
                incomes['married'][label] = float(df['married_estimates'][index][:-1])
            
    return incomes

def get_race_distribution(code):
    """
    Function to get the race distribution of a given location.
    
    Input:
        - code: string with the location code. The string is the path to the csv file with the data.
    
    Output:
        - races: list with the number of people in each race
    """
    
    df = pd.read_csv(code)
    
    races = dict()
    
    read = False
    
    for index in range(len(df.index)):
        label = df['label'][index].replace(u'\xa0', '')
        
        if label == "White alone":
            read = True
            
        if read:
            # remove the comma from the number
            estimate = str(df['total_estimates'][index])
            if ',' in estimate:
                estimate = estimate.replace(',', '')
            estimate = int(estimate)
            races[label] = estimate
    
    return races

def get_number_species(data):
    """
    Function to get the number of species in a given location.
    
    Input:
        - data: list with the number of people in each species
    
    Output:
        - number_species: int with the number of species in the location
    """
    
    return len(data)

def get_social_mixing_index(path):
    """
    Function to get the social mixing index of a given location.
    
    Input:
        - code: string with the location code. The string is the path to the csv file with the data.
    
    Output:
        - indexes: list containing the Social Distancing Index (SDI) for each type of data
    """
    
    indexes = dict()
    
    # get the total population
    total_population = get_total_population(path)
    
    types = ['gender', 'income', 'race']
    for type in types:
        code = path + '\\' + type + '.csv'
        if type == 'gender':
            data = get_age_distribution(code)
        elif type == 'income':
            data = get_incomes_distribution(code)
        elif type == 'race':
            data = get_race_distribution(code)
        
        if type == 'income':
            for key, values in data.items():
                social_mixing_index = sdi(values)
                indexes[key] = social_mixing_index
        else:
            social_mixing_index = sdi(data)
            indexes[type] = social_mixing_index
    
    return indexes

def get_general_social_mixing_index(path, type):
    if type == 'gender':
        data = get_age_distribution(path)
    elif type == 'income':
        data = get_incomes_distribution(path)
    elif type == 'race':
        data = get_race_distribution(path)
    
    
    if type == 'income':
        for key, values in data.items():
            social_mixing_index = sdi(values)
    else:
        social_mixing_index = sdi(data)

def get_mean_index(indexes):
    """
    Function to get the mean index of a given location.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type of data
    
    Output:
        - mean_index: float with the mean index of the location
    """

    final_index = dict()
    for key, values in indexes.items():
        final_index[key] = sum(values) / len(values)
    
    return final_index


def create_csv(data, location, path):
    """
    Function to create a csv file with the data.
    
    Input:
        - data: list with the data to be saved
    """
    
    # check if the file already exists
    if not os.path.exists(path):
        with open(path, 'w') as f:
            header = 'location,gender,household,family,nonfamily,married,race\n'
            f.write(header)
            for item in data.values():
                line = '' + location + ','
                for item in data.values():
                    line += str(item) + ','
                line = line[:-1] + '\n'
            f.write(line)
    else:
        with open(path, 'a') as f:
            line = '' + location + ','
            for item in data.values():
                line += str(item) + ','
            line = line[:-1] + '\n'
            f.write(line)

def get_indexes(path):
    """
    Function to get the social mixing index of a specific location and for each type of data.
    
    Output:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    indexes = {
        'gender': list(),
        'household': list(),
        'family': list(),
        'nonfamily': list(),
        'married': list(),
        'race': list()
    }
    
    with open(path, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            if 'location' in line:
                continue
            data = line.split(',')
            for index, key in enumerate(indexes.keys()):
                indexes[key].append(float(data[index + 1]))
    
    return indexes

# ------------------------------------------ bikes indexes -----------------------------------------

def get_stations_zipcodes(city):
    
    stations_zipcodes = dict()
    
    path = 'data\\stations\\' + city + '.csv'
    # path example -> 'data\\stations\\Chicago.csv'
    
    df = pd.read_csv(path, encoding="ISO-8859-1", dtype={'zipcode': str})
    
    for index, row in df.iterrows():
        station = row['station']
        zipcode = str(row['zipcode'])
        
        if zipcode not in stations_zipcodes:
            stations_zipcodes[zipcode] = 0
        
        stations_zipcodes[zipcode] += 1
    
    return stations_zipcodes

def get_bikes_indexes(indexes, city, data=None):
    """
    Function to get the distribution of social mixing index for each bike station.
    
    Input:
        - indexes: dict with the social mixing index for each zipcode
    
    Output:
        - bikes_indexes: dict indicating the number of stations with a specific social mixing index
    """
    
    bikes_indexes = {
        'gender': dict(),
        'household': dict(),
        'family': dict(),
        'nonfamily': dict(),
        'married': dict(),
        'race': dict()
    }
    
    stations = get_stations_zipcodes(city)
    
    for zipcode, count in stations.items():
        if zipcode not in indexes:
            continue
        index = indexes[zipcode]
        for key, value in index.items():
            if key not in bikes_indexes:
                bikes_indexes[key] = dict()
            if value not in bikes_indexes[key]:
                bikes_indexes[key][value] = 0
            bikes_indexes[key][value] += count
    
    if data:
        return bikes_indexes[data]
    
    return bikes_indexes

# ------------------------------------------ print indexes ------------------------------------------

def print_indexes(indexes, type=None):
    """
    Function to print the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    print('-' * 50)
    if type:
        print('\tSocial Mixing Index for ' + type)
    for key, values in indexes.items():
        print(key, values)
    print('-' * 50)

# ------------------------------------------ main functions ------------------------------------------

def get_city_data(data, type=None):
    
    city_path = os.path.join(path, data)
    # city_path example -> 'data\\social\\Chicago'
    
    full_path = os.path.join(city_path, _year)
    # full_path example -> 'data\\social\\Chicago\\2022'
    
    csv_path = 'data\\indexes\\' + data + '.csv'
    
    zipcodes = dict()
    
    # remove the file if it already exists
    if not os.path.exists(csv_path):
    
        for location in os.listdir(full_path):
            # check if the location is a directory
            check = os.path.join(full_path, location)
            # check example -> 'data\\social\\Chicago\\2022\\60601'
            
            if os.path.isdir(check):
                location_path = os.path.join(full_path, location)
                indexes = get_social_mixing_index(location_path)
                create_csv(indexes, location, csv_path)
                
                zipcodes[location] = indexes
    else:
        
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                
                if 'location' in line:
                    continue
                
                datas = line.split(',')
                indexes = dict()
                
                for index, key in enumerate(_types):
                    indexes[key] = float(datas[index + 1])
            
                zipcodes[datas[0]] = indexes

    bikes_indexes = get_bikes_indexes(zipcodes, data, type)
    return bikes_indexes

def get_type_data(data):
    
    full_data = dict()
    
    for city in os.listdir(path):
        
        if city == "Austin":
            continue
        
        print(f"\tCalculating the indexes for {city}")
        
        type_data = get_city_data(city, data)
        full_data[city] = type_data
    
    return full_data

if __name__ == '__main__':
    
    data_to_analyse = 'type'
    data = sys.argv[1]
    
    if data_to_analyse == 'city':
        
        bikes_data = get_city_data(data)
        plot_stations_indexes(bikes_data)
        
        print('-' * 50)
        print('\tSocial mixing index calculated and saved in the csv file.')
        
        path = 'data\\indexes\\' + data + '.csv'
        extract_indexes = get_indexes(path)
        final_index = get_mean_index(extract_indexes)
    
        print_indexes(final_index)
    
    else:
        
        type_data = get_type_data(data)
        subplot_indexes_per_types(type_data, data)