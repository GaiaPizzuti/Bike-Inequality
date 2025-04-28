from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

debug = True
data_dir = "data//bikes"

# ----------------- GENERAL ANALYSIS -----------------

def get_colors(data):
    colors = list()
    for value in data:
        if value == min(data):
            colors.append('indianred')
        elif value == max(data):
            colors.append('springgreen')
        else:
            colors.append('lightgrey')
    return colors

def get_date_format(city, year, month):
    year = int(year)
    if city == 'Austin':
        return '%m/%d/%Y %I:%M:%S %p'
    elif city == 'Boston':
        if (year == 2018 and month < 3) or (year == 2023 and month > 2):
            return '%Y-%m-%d %H:%M:%S'
        else:
            return '%Y-%m-%d %H:%M:%S.%f'
    elif city == 'Chicago' or city == 'Columbus' or city == 'Washington':
        return '%Y-%m-%d %H:%M:%S'
    elif city == 'NYC':
        if year <= 2020 or (year == 2021 and month == 0):
            return '%Y-%m-%d %H:%M:%S.%f'
        return '%Y-%m-%d %H:%M:%S'
    elif city == 'Philly':
        if year == 2018 or (year == 2019 and month >= 0 and month <= 5) or (year == 2019 and month >= 9):
            return '%Y-%m-%d %H:%M:%S'
        return '%m/%d/%Y %H:%M'
    elif city == 'SanFrancisco':
        if year < 2020 or (year == 2020 and month < 4):
            return '%Y-%m-%d %H:%M:%S.%f'
        return '%Y-%m-%d %H:%M:%S'

# ----------------- MONTH ANALYSIS -----------------


def compare_trip_for_month(year_path):
    '''
    function to plot the number of trips for every month of a specific year
    '''
    
    months = [0] * 12
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    year_file = os.listdir(year_path)
    
    for file in year_file:
        
        full_path = os.path.join(year_path, file)
        df = pd.read_csv(full_path, dtype=object)
        month = int(file[4:6]) - 1
        months[month] = len(df.index)
    
    colors = get_colors(months)
    plt.barh(months_list, months, color=colors)
    
    for rect in plt.gca().patches:
        width = rect.get_width()
        plt.gca().text(width, rect.get_y() + rect.get_height()/2, str(int(width)), ha='left', va='center')
    
    plt.xlabel('Number of Trips')
    plt.ylabel('Months of the Year')
    title = 'Number of Trips for every month of ' + full_path.split('\\')[1] + ' in ' + full_path.split('\\')[2]
    plt.title(title)
    plt.show()
    
    return months

def plot_specific_year(city_to_analyse, year_to_analyse):
    '''
    function to plot the number of trips for every month of a specific year of a specific city
    
    Inputs:
        - city_to_analyse: the city to analyse
        - year_to_analyse: the year to analyse
    '''
    for city in os.listdir(data_dir):
        if city == city_to_analyse:
            city_path = os.path.join(data_dir, city)
            for year in os.listdir(city_path):
                if year == year_to_analyse:
                    year_path = os.path.join(city_path, year)

# ----------------- HOUR ANALYSIS -----------------

def compare_trip_for_hour(full_path, month_to_check):
    '''
    function to plot the number of trips for every hour of a specific year, month and city
    
    Inputs:
        - df: the dataframe to analyse
        - full_path: the path of the file
        - month_to_check: the month to check
    '''
    
    df = pd.read_csv(full_path, dtype=object)
    hours = [0] * 24
    
    for index in range(len(df.index)):
        city = full_path.split('\\')[1]
        date_format = get_date_format(city, full_path.split('\\')[2], month_to_check)
        if city == 'SanFrancisco':
            if len(df['stop_time'][index]) == 24:
                hour = datetime.strptime(df['stop_time'][index], date_format).hour
            else:
                hour = datetime.strptime(df['stop_time'][index], '%Y-%m-%d %H:%M:%S').hour
        else:
            hour = datetime.strptime(df['stop_time'][index], date_format).hour
        hours[hour] += 1
    
    colors = get_colors(hours)
    plt.barh(range(24), hours, color=colors)
    
    for rect in plt.gca().patches:
        width = rect.get_width()
        plt.gca().text(width, rect.get_y() + rect.get_height()/2, str(int(width)), ha='left', va='center')
    
    plt.xlabel('Number of Trips')
    plt.ylabel('Hours of the Day')
    city = full_path.split('\\')[1]
    year = full_path.split('\\')[2]
    
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    print(months_list[month_to_check])
    title = 'Number of Trips for every hour of ' + city + ' in ' + year + ' for the month of ' + months_list[month_to_check]
    plt.title(title)
    plt.show()

def plot_trip_for_hour(city_to_analyse, year_to_analyse, month_to_analyse):
    '''
    function to plot the number of trips for every hour of a specific month of a specific year of a specific city
    
    Inputs:
        - city_to_analyse: the city to analyse
        - year_to_analyse: the year to analyse
        - month_to_analyse: the month to analyse
    '''
    
    # for each city in the data directory
    for city in os.listdir(data_dir):
        
        # if the city is the one to analyse
        if city == city_to_analyse:
            
            city_path = os.path.join(data_dir, city)
            
            # for each year in the city directory
            for year in os.listdir(city_path):
                
                # if the year is the one to analyse
                if int(year) == year_to_analyse:
                    
                    year_path = os.path.join(city_path, year)
                    
                    # for each month in the year directory
                    for month_file in os.listdir(year_path):
                        
                        full_path = os.path.join(year_path, month_file)
                        df = pd.read_csv(full_path, dtype=object)
                        
                        month = int(month_file[4:6]) - 1
                        # if the month is the one to analyse
                        if month == month_to_analyse:
                            compare_trip_for_hour(full_path, month)

# ---------------- GENDER ANALYSIS ----------------

def compare_gender_per_hour(full_path, month_to_check):
    '''
    function to calculate the number of men and women for every hour of the day
    
    Inputs:
        - df: the dataframe to analyse
        - full_path: the path of the file
        - month_to_check: the month to check
    '''
    
    df = pd.read_csv(full_path, dtype=object)
    months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    hours = {
        'men' : [0 for _ in range(24)],
        'women' : [0 for _ in range(24)]
    }
    
    is_zero = True
    
    print(months_list[month_to_check])
    
    for index in range(len(df.index)):
        city = full_path.split('\\')[1]
        date_format = get_date_format(city, full_path.split('\\')[2], month_to_check)
        if city == 'SanFrancisco':
            if len(df['stop_time'][index]) == 24:
                hour = datetime.strptime(df['stop_time'][index], date_format).hour
            else:
                hour = datetime.strptime(df['stop_time'][index], '%Y-%m-%d %H:%M:%S').hour
        else:
            hour = datetime.strptime(df['stop_time'][index], date_format).hour
        if df['gender'][index] == 'man' or df['gender'][index] == 'Male' or df['gender'][index] == 1 or df['gender'][index] == '1':
            is_zero = False
            hours['men'][hour] += 1
        if df['gender'][index] == 'woman' or df['gender'][index] == 'Female' or df['gender'][index] == 2 or df['gender'][index] == '2':
            is_zero = False
            hours['women'][hour] += 1
    
    if not is_zero:
        x = np.arange(len(hours['men']))
        width = 0.24
        
        fig, ax = plt.subplots(layout='constrained')
        
        max_man = max(hours['men'])
        min_man = min(hours['men'])
        max_woman = max(hours['women'])
        min_woman = min(hours['women'])
        
        for value in hours['men']:
            if value == max_man:
                print('Maximum value for men: ' + str(hours['men'].index(value)))
            elif value == min_man:
                print('Minimum value for men: ' + str(hours['men'].index(value)))
        
        for value in hours['women']:
            if value == max_woman:
                print('Maximum value for women: ' + str(hours['women'].index(value)))
            elif value == min_woman:
                print('Minimum value for women: ' + str(hours['women'].index(value)))
        
        plt.bar(x - 0.12, hours['men'], width, color='lightskyblue', label='men')
        plt.bar(x + 0.12, hours['women'], width, color='salmon', label='women')
        
        plt.legend(loc='upper right', ncol=2)
        title = 'Number of Trips for every hour of ' + city + ' in ' + year + ' for the month of ' + months_list[month_to_check]
        plt.title(title)
        plt.xlabel('Hours of the Day')
        plt.ylabel('Number of Trips')
        plt.show()

def plot_gender_per_hour(city_to_analyse, year_to_analyse, month_to_analyse):
    '''
    function to plot the number of men and women for every hour of the day
    
    Inputs:
        - city_to_analyse: the city to analyse
        - year_to_analyse: the year to analyse
        - month_to_analyse: the month to analyse
    '''
    for city in os.listdir(data_dir):
        
        if city == city_to_analyse:
            
            city_path = os.path.join(data_dir, city)
            
            for year in os.listdir(city_path):
                
                if year == year_to_analyse:
                    
                    year_path = os.path.join(city_path, year)
                    
                    for month_file in os.listdir(year_path):
                        
                        month = int(month_file[4:6]) - 1
                        if month == month_to_analyse:
                            full_path = os.path.join(year_path, month_file)
                            
                            compare_gender_per_hour(full_path, month)

# ----------------- STATION ANALYSIS -----------------

def get_number_trips(path):
    '''
    function to get the number of trips for each station
    
    Inputs:
        - path: str, the path of the file
    
    Outputs:
        - stations: dict, the stations with the number of trips starting and ending at each station
    '''
    stations = dict()
    
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        df = pd.read_csv(full_path, dtype=object)
        
        if debug:
            print('-' * 50)
            print('File:', file)
            print('-' * 50)
        
        for index in range(len(df.index)):
            
            if 'latitude_start' in df.columns:
                start_station = df['station_start'][index]
                end_station = df['station_end'][index]
                start_lat = df['latitude_start'][index]
                start_lon = df['longitude_start'][index]
                end_lat = df['latitude_end'][index]
                end_lon = df['longitude_end'][index]
                
                if start_station not in stations:
                    
                    if debug:
                        print("\t Add new station:", start_station)
                    
                    stations[start_station] = {
                        'lat': start_lat,
                        'lon': start_lon,
                        'start' : 1,
                        'end' : 0
                    }
                else:
                    stations[start_station]['start'] += 1
                if end_station not in stations:
                    
                    if debug:
                        print("\t Add new station:", end_station)
                    
                    stations[end_station] = {
                        'lat': end_lat,
                        'lon': end_lon,
                        'start' : 0,
                        'end' : 1
                    }
                else:
                    stations[end_station]['end'] += 1
    
    if debug:
        print('-' * 50)
    
    return stations

# ----------------- MAIN -----------------

if __name__ == '__main__':
    
    function = sys.argv[1]
    city = sys.argv[2]
    year = sys.argv[3]
    
    city_path = os.path.join(data_dir, city)
    year_path = os.path.join(city_path, year)
    
    if function == 'hour':
        path = os.path.join(year_path, sys.argv[4])
        compare_trip_for_hour(path, month)
    elif function == 'gender':
        path = os.path.join(year_path, sys.argv[4])
        compare_gender_per_hour(path, month)
    elif function == 'month':
        compare_trip_for_month(year_path)
        
    elif function == 'station':
        get_number_trips(year_path)