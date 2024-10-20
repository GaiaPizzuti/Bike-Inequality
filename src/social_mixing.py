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

path = 'data\\social'
csv_path = 'data\\social_mixing.csv'
complete_csv_path = 'data\\social_mixing_complete.csv'

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


def create_csv(data, location, path = csv_path):
    """
    Function to create a csv file with the data.
    
    Input:
        - data: list with the data to be saved
    """
    
    # check if the file already exists
    if not os.path.exists(path):
        with open(path, 'w') as f:
            header = 'location,age,household,family,nonfamily,married,race\n'
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

def get_indexes():
    """
    Function to get the social mixing index of a specific location and for each type of data.
    
    Output:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    indexes = {
        'age': list(),
        'household': list(),
        'family': list(),
        'nonfamily': list(),
        'married': list(),
        'race': list()
    }
    
    with open(csv_path, 'r') as f:
        lines = f.readlines()
        
        for line in lines:
            if 'location' in line:
                continue
            data = line.split(',')
            for index, key in enumerate(indexes.keys()):
                indexes[key].append(float(data[index + 1]))
    
    return indexes

# ------------------------------------------ type indexes ------------------------------------------

def analyse_type_indexes(type, year):
    """
    Function to create a dictionary with the indexes of a specific type of data from each city.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type of data
        - type: string with the type of data
    
    Output:
        - final_index: dictionary with the indexes of a specific type of data from each city
    """
    
    # remove the file if it already exists
    if os.path.exists(complete_csv_path):
        os.remove(complete_csv_path)
    
    for city in os.listdir(path):
        city_path = os.path.join(path, city)
        
        full_path = os.path.join(city_path, year)
        
        for location in os.listdir(full_path):
            if not os.path.isdir(os.path.join(full_path, location)):
                continue
            location_path = os.path.join(full_path, location)
            indexes = get_social_mixing_index(location_path)
            create_csv(indexes, city, complete_csv_path)
    
    final_index = get_type_indexes(type)
    mean_type_indexes = get_mean_index(final_index)
    
    return final_index, mean_type_indexes

def get_type_indexes(type):
    """
    Function to get the indexes of a specific type of data from each city.
    
    Input:
        - type: string with the type of data
        
    Output:
        - indexes: dictionary with the indexes of a specific type of data from each city
    """            
    
    df = pd.read_csv(complete_csv_path)
    
    indexes = dict()
    
    order = ['age', 'household', 'family', 'nonfamily', 'married', 'race']
    
    with open(complete_csv_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            
            if 'location' in line:
                continue
            
            data = line.split(',')
            if data[0] not in indexes:
                indexes[data[0]] = list()
            
            indexes[data[0]].append(float(data[order.index(type) + 1]))
    
    return indexes

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

# ------------------------------------------ plot indexes ------------------------------------------

def plot_multiple_indexes(indexes):
    """
    Function to plot the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    X = np.random.randn(1000, 6)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    
    fig, ax = plt.subplots(2, 3, sharex=True, sharey=True)
    # make a hist plot to represent how the data is distributed
    for index, (key, values) in enumerate(indexes.items()):
        ax[index // 3, index % 3].hist(values, bins=10, histtype='bar', color=colors[index % 6])
        ax[index // 3, index % 3].set_title(key)
    
    # add the title to the plot
    fig.suptitle('SMI Distribution')
    # add x and y labels
    fig.supxlabel('Social Mixing Index')
    fig.supylabel('Frequency')
    plt.show()

def plot_multiple_types_indexes(indexes, type=None):
    """
    Function to plot the social mixing index of a specific location and for each type of data.

    Args:
        indexes (dict): dictionary with the indexes of a specific type of data from each city
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    X = np.random.randn(1000, 8)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    
    fig, ax = plt.subplots(2, 4, sharex=True, sharey=True)
    # make a hist plot to represent how the data is distributed
    for index, (key, values) in enumerate(indexes.items()):
        ax[index // 4, index % 4].hist(values, bins=10, histtype='bar', color=colors[index % 8])
        ax[index // 4, index % 4].set_title(key)
    
    # add the title to the plot
    if type:
        fig.suptitle('SMI Distribution for ' + type)
    else:
        fig.suptitle('SMI Distribution')
    # add x and y labels
    fig.supxlabel('Social Mixing Index')
    fig.supylabel('Frequency')
    plt.show()

def plot_indexes(indexes, type=None):
    """
    Function to plot the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.displot(indexes, kind='kde')
    
    if type:
        plt.title('SMI Density Plot for ' + type)
    else:
        plt.title('SMI Density Plot')
    plt.xlabel('Social Mixing Index')
    plt.ylabel('Density')
    
    plt.show()

if __name__ == '__main__':
    
    city = sys.argv[1]
    year = sys.argv[2]
    
    city_path = os.path.join(path, city)
    full_path = os.path.join(city_path, year)
    
    # remove the file if it already exists
    if os.path.exists(csv_path):
        os.remove(csv_path)
    
    print('\tCalculating social mixing index for each location...')
    print('-' * 50)
    
    for location in os.listdir(full_path):
        # check if the location is a directory
        check = os.path.join(full_path, location)
        if not os.path.isdir(check):
            type = location.split('.')[0]
            if type == 'gender':
                print('\tCalculating social mixing index for the general data...')
                print('-' * 50)
            get_general_social_mixing_index(check, type)
        else:
            location_path = os.path.join(full_path, location)
            indexes = get_social_mixing_index(location_path)
            create_csv(indexes, location)
    
    print('-' * 50)
    print('\tSocial mixing index calculated and saved in the csv file.')
    print('-' * 50)
    
    extract_indexes = get_indexes()
    final_index = get_mean_index(extract_indexes)
    
    print_indexes(final_index)
    
    #plot_indexes(extract_indexes)
    #plot_multiple_indexes(extract_indexes)
    
    types = ['age', 'household', 'family', 'nonfamily', 'married', 'race']
    
    for type in types:
        full_indexes, types_indexes = analyse_type_indexes(type, year)
        print_indexes(types_indexes, type)
        plot_indexes(full_indexes, type)
        plot_multiple_types_indexes(full_indexes, type)