import pathlib
import urllib.request
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
from copy import deepcopy
import matplotlib.lines as mlines
import numpy as np

from trips_analysis import get_number_trips

debug = False
categorical = False
show = True

data_bikes = 'data\\bikes'

states_filename = "tl_2017_us_state.zip"
states_url = f"https://www2.census.gov/geo/tiger/TIGER2017/STATE/{states_filename}"
states_file = pathlib.Path(states_filename)

zipcode_filename = "tl_2017_us_zcta510.zip"
zipcode_url = f"https://www2.census.gov/geo/tiger/TIGER2017/ZCTA5/{zipcode_filename}"
zipcode_file = pathlib.Path(zipcode_filename)

for data_file, url in zip([states_file, zipcode_file], [states_url, zipcode_url]):
    if not data_file.is_file():
        with urllib.request.urlopen(url) as response, open(data_file, 'wb') as f:
            f.write(response.read())

zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")
states_gdf = gpd.read_file(f"zip://{states_file}")


def plot_bikes(city):
    
    path = os.path.join(data_bikes, city, year)
    stations = get_number_trips(path)
    
    latitudes = list()
    longitudes = list()
    sizes = list()
    colors = list()
    
    for name, station in stations.items():
        start = station['start']
        end = station['end']
        size = max(start, end)
        sizes.append(size / 1000)
        if size == start:
            colors.append('red')
        else:
            colors.append('blue')

        latitudes.append(station['lat'])
        longitudes.append(station['lon'])
    
    bikes = pd.DataFrame({
        'lat': latitudes,
        'lon': longitudes,
        'size': sizes,
        'color': colors
    })
    
    return bikes

def plot_map(city_name, function, path, year):
    
    city = deepcopy(zipcode_gdf)
    
    results = list()
    
    for zip in os.listdir(path):
        
        if not zip.endswith('.csv'):
        
            zip_path = os.path.join(path, zip)
            
            for file in os.listdir(zip_path):
                
                file_path = os.path.join(zip_path, file)
                df = pd.read_csv(file_path)
            
        
                if function == 'income' and file == 'income.csv':
                    household, married, nonfamily, family = get_income(df)
                    if household is not None:
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'household'] = household
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'married'] = married
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'nonfamily'] = nonfamily
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'family'] = family
                elif function == 'gender' and file == 'gender.csv':
                    maximum = get_gender(df)
                    if maximum is not None:
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'result'] = maximum
                elif function == 'race' and file == 'race.csv':
                    maximum = get_race(df)
                    if maximum is not None:
                        city.loc[city.ZCTA5CE10.str.startswith(zip), 'result'] = maximum
    
    if function == 'gender':
        
        city = city[city['result'].notna()]
        
        bikes = plot_bikes(city_name)
        
        if categorical:
            order = ['<5', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                    '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
            
            base = city.plot(column='result', cmap='viridis', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_ancor': (1, 0.5) }, categories = order)
            
            if show:
                counters = {age: 0 for age in order}
                for age in city['result']:
                    counters[age] += 1
                print(counters)
                
        else:
            base = city.plot(column='result', cmap='viridis', legend = True)
            
            if show:
                counter = 0
                for age in city['result']:
                    counter += age
                counter /= len(city['result'])
                print(counter)
        
        plt.xticks([], [])
        plt.yticks([], [])
        plt.title(f'Gender in {city_name} in 2022')
        
        geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
        points = geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
        
    elif function == 'income':
        
        city = city[city['household'].notna()]
        
        bikes = plot_bikes(city_name)
        
        if categorical:
            
            order = ['<10,000', '10,000-14,999', '15,000-24,999', '25,000-34,999', '35,000-49,999',
                    '50,000-74,999', '75,000-99,999', '100,000-149,999', '150,000-199,999', '200,000+']
            
            types = ['household', 'married', 'nonfamily', 'family']
            for type in types:
                base = city.plot(column=type, cmap='viridis', categorical = True, categories = order, legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}, edgecolor='black')
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title(type + ' income in ' + city_name + ' in 2022')
                if results:
                    for type in types:
                        counters = {income: 0 for income in order}
                        for income in city[type]:
                            counters[income] += 1
                        print(counters)
                        
                geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
                points = geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
                
        else:
                
            fig, ax = plt.subplots(2, 2, figsize=(7, 7))
            
            types = ['household', 'married', 'nonfamily', 'family']
            for x in [0, 1]:
                for y in [0, 1]:
                    type = types[x + y * 2]
                    base = city.plot(column=type, cmap='viridis', ax=ax[x, y])
                    ax[x, y].set_xticks([], [])
                    ax[x, y].set_yticks([], [])
                    plt.suptitle('Income in ' + city_name + ' in 2022')
                    ax[x, y].set_title(type)        
                
                    geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
                    geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
                    
            axs = ax.ravel()
            fig.colorbar(ax[0, 0].collections[0], ax=axs, shrink= 0.5)
                    
            if show:
                counter = {
                    'household': 0,
                    'married': 0,
                    'nonfamily': 0,
                    'family': 0
                }
                for type in types:
                    for income in city[type]:
                        counter[type] += income
                    counter[type] /= len(city[type])
                print(counter)
            
    
    elif function == 'race':
        
        city = city[city['result'].notna()]
        
        order = ['White', 'Black or \n African American', 'Indian and \n Alaska Native',
            'Asian', 'Native Hawaiian', 'Some Other Race', 'Two or More Races']
        
        base = city.plot(column='result', cmap='viridis', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}, categories = order)
        
        bikes = plot_bikes(city_name)
        
        if debug:
            # insert the zip code on the map
            for idx, row in city.iterrows():
                plt.annotate(text=row['ZCTA5CE10'], xy=(row['geometry'].centroid.x, row['geometry'].centroid.y), horizontalalignment='center')
        
        plt.title(f'Races in {city_name} in {year}')
        plt.xticks([], [])
        plt.yticks([], [])
        
        if debug:
            counter = {race: 0 for race in order}
            for race in city['result']:
                counter[race] += 1
            print(counter)
        
        geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
        points = geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
    
    plt.show()

def get_gender(df):
    '''
    function to get the gender from the social data and plot it
    
    Inputs:
        - df: pandas dataframe
    
    Outputs:
        - the most common age or the mean age
    '''
    
    if categorical:
        estimates = list()
        margins = list()
        is_age = False
        for i in range(30):
            if df['label'][i].endswith('Under 5 years'):
                is_age = True
            if is_age:
                estimate = df['total_estimates'][i]
                if type(estimate) == float:
                    estimate = str(estimate)
                estimate = int(estimate.replace(',', ''))
                estimates.append(estimate)
            if df['label'][i].endswith('85 years and over'):
                break
        # return the maximum value
        ages = ['<5', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
        max_total = estimates.index(max(estimates))
        return ages[max_total]
    else:
        for i in range(40):
            if df['label'][i].endswith('Median age (years)'):
                estimate = df['total_estimates'][i]
                if estimate != '-':
                    return float(df['total_estimates'][i])
        return None

def get_income(df):
    '''
    function to get the income from the social data and plot it
    
    Inputs:
        - df: pandas dataframe
    
    Outputs:
        - the most common income or the median income
    '''
    estimates = {
        'household': list(),
        'family': list(),
        'married': list(),
        'nonfamily': list()
    }
    if categorical:
        is_income = False
        for i in range(16):
            if df['label'][i].endswith('Less than $10,000'):
                is_income = True
            if is_income:
                for type in ['household', 'married', 'nonfamily', 'family']:
                    if df[type + '_estimates'][i] == '-':
                        return None, None, None, None
                    estimate = float(df[type + '_estimates'][i][:-1])
                    estimates[type].append(estimate)
            if df['label'][i].endswith('$200,000 or more'):
                is_income = False
        
        # return the maximum value
        incomes = ['<10,000', '10,000-14,999', '15,000-24,999', '25,000-34,999', '35,000-49,999',
                '50,000-74,999', '75,000-99,999', '100,000-149,999', '150,000-199,999', '200,000+']
        return incomes[estimates['household'].index(max(estimates['household']))], incomes[estimates['married'].index(max(estimates['married']))], incomes[estimates['nonfamily'].index(max(estimates['nonfamily']))], incomes[estimates['family'].index(max(estimates['family']))]
    else:
        for i in range(16):
            if df['label'][i].endswith('Median income (dollars)'):
                for type in ['household', 'married', 'nonfamily', 'family']:
                    estimate = df[type + '_estimates'][i]
                    if estimate == '-':
                        return None, None, None, None
                    else:
                        if estimate.endswith('+'):
                            estimate = estimate[:-1]
                        estimate = int(estimate.replace(',', ''))
                        estimates[type].append(estimate)
        return estimates['household'][0], estimates['married'][0], estimates['nonfamily'][0], estimates['family'][0]
    
def get_race(df):
    '''
    the function to get the race from the social data and plot it
    
    Input:
        - df: pandas dataframe
    
    Output:
        - the most common race
    '''
    
    estimates = list()
    
    is_race = False
    for i in range(10):
        if df['label'][i].endswith('White alone'):
            is_race = True
        if is_race:
            estimate = df['total_estimates'][i]
            if type(estimate) != str:
                estimate = str(estimate)
            estimate = int(estimate.replace(',', ''))
            estimates.append(estimate)
        if df['label'][i].endswith('Two or More Races'):
            is_race = False
    
    # return the maximum value
    races = ['White', 'Black or \n African American', 'Indian and \n Alaska Native',
        'Asian', 'Native Hawaiian', 'Some Other Race', 'Two or More Races']
    return races[estimates.index(max(estimates))]
        
if __name__ == '__main__':
    
    # load date
    data = 'data\\social'
    
    function = sys.argv[1]
    city = sys.argv[2]
    year = sys.argv[3]
    
    city_path = os.path.join(data, city)
        
    year_path = os.path.join(city_path, '2022')
    plot_map(city, function, year_path, year)