import geopandas as gpd
import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
from copy import deepcopy

from trips_analysis import get_number_trips
from starter import zipcode_file, debug, categorical, data_bikes, data_social

_incomes = ['household', 'family', 'married', 'nonfamily']

def plot_bikes(city):
    
    path = os.path.join(data_bikes, city, year)
    stations = get_number_trips(path)
    
    latitudes = list()
    longitudes = list()
    sizes = list()
    colors = list()
    names = list()
    
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
        names.append(name)
    
    bikes = pd.DataFrame({
        'name': names,
        'lat': latitudes,
        'lon': longitudes,
        'size': sizes,
        'color': colors
    })
    
    return bikes

def plot_map(city_name, function, path, year):
    
    zipcode_gdf = gpd.read_file(f"zip://{zipcode_file}")
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

    bikes = plot_bikes(city_name)
    
    if function == 'gender':
        
        city = city[city['result'].notna()]
        
        if debug:
            print("\t Start plotting gender")
            
        if categorical:
            order = ['<5', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44',
                    '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
            
            base = city.plot(column='result', cmap='viridis', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}, categories = order)
            
            if debug:
                counters = {age: 0 for age in order}
                for age in city['result']:
                    counters[age] += 1
                print(counters)
                
        else:
            base = city.plot(column='result', cmap='viridis', legend = True)
            
            if debug:
                counter = 0
                for age in city['result']:
                    counter += age
                counter /= len(city['result'])
                print(counter)
        
        plt.xticks([], [])
        plt.yticks([], [])
        plt.title(f'Gender in {city_name} in 2022')
        
        # insert the points on the map
        
        if debug:
            print('-' * 50)
            print("\t Inserting points on the map")
        
        geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
        geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
        
    elif function == 'income':
        
        city = city[city['household'].notna()]
        
        if debug:
            print("\t Start plotting gender")
        
        if categorical:
            
            order = ['<10,000', '10,000-14,999', '15,000-24,999', '25,000-34,999', '35,000-49,999',
                    '50,000-74,999', '75,000-99,999', '100,000-149,999', '150,000-199,999', '200,000+']
            
            for type in _incomes:
                base = city.plot(column=type, cmap='viridis', categorical = True, categories = order, legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}, edgecolor='black')
                plt.xticks([], [])
                plt.yticks([], [])
                plt.title(type + ' income in ' + city_name + ' in 2022')
                if results:
                    for type in _incomes:
                        counters = {income: 0 for income in order}
                        for income in city[type]:
                            counters[income] += 1
                        print(counters)
                
                if debug:
                    print('-' * 50)
                    print("\t Inserting points on the map")
                
                geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
                geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
                
                if debug:
                    print('-' * 50)
                    print("\t Inserting lines on the map")
                
        else:
                
            fig, ax = plt.subplots(2, 2, figsize=(7, 7))
            
            for x in [0, 1]:
                for y in [0, 1]:
                    type = _incomes[x + y * 2]
                    base = city.plot(column=type, cmap='viridis', ax=ax[x, y])
                    ax[x, y].set_xticks([], [])
                    ax[x, y].set_yticks([], [])
                    plt.suptitle('Income in ' + city_name + ' in 2022')
                    ax[x, y].set_title(type)      
                    
                    if debug:
                        print('-' * 50)
                        print("\t Inserting points on the map")
                
                    geopuffer = gpd.GeoDataFrame(bikes, geometry = gpd.points_from_xy(bikes.lon, bikes.lat))
                    geopuffer.plot(ax=base, color=geopuffer['color'], markersize=geopuffer['size'], legend=True)
                    
                    if debug:
                        print('-' * 50)
                        print("\t Inserting lines on the map")
                    
                    geom = list()
                    sizes = list()
                    for start, ends in trips.items():
                        for end, size in ends.items():
                            plt.plot([start.y, end.y], [start.x, end.x], color='black', linewidth=size / 1000)
                    
            axs = ax.ravel()
            fig.colorbar(ax[0, 0].collections[0], ax=axs, shrink= 0.5)
                    
            if debug:
                counter = {
                    'household': 0,
                    'married': 0,
                    'nonfamily': 0,
                    'family': 0
                }
                for type in _incomes:
                    for income in city[type]:
                        counter[type] += income
                    counter[type] /= len(city[type])
                print(counter)
            
    
    elif function == 'race':
        
        city = city[city['result'].notna()]
        
        order = ['White', 'Black or \n African American', 'Indian and \n Alaska Native',
            'Asian', 'Native Hawaiian', 'Some Other Race', 'Two or More Races']
        
        base = city.plot(column='result', cmap='viridis', legend=True, legend_kwds={'loc': 'center left', 'bbox_to_anchor': (1, 0.5)}, categories = order)
        
        if debug:
            print("\t Start plotting gender")
        
        plt.title(f'Races in {city_name} in {year}')
        plt.xticks([], [])
        plt.yticks([], [])
        
        if debug:
            counter = {race: 0 for race in order}
            for race in city['result']:
                counter[race] += 1
            print(counter)
        
        if debug:
            print('-' * 50)
            print("\t Inserting points on the map")
        
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
    
    function = sys.argv[1]
    city = sys.argv[2]
    year = sys.argv[3]
    
    city_path = os.path.join(data_social, city)
        
    year_path = os.path.join(city_path, '2022')
    plot_map(city, function, year_path, year)