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
from util.create_station_file import create_csv


path = 'data\\social'
_year = '2022'

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