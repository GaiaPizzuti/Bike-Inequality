import numpy as np
import pandas as pd
import os
import sys

def get_missing_data(df, data_dir):
    '''
    function to get the missing data in the dataframe
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    # Get the number of missing data points per column
    missing_values_count = df.isnull().sum()

    # How many total missing values do we have?
    total_cells = np.prod(df.shape)
    total_missing = missing_values_count.sum()
    
    if total_missing != 0:
        print('Missing data:', missing_values_count)

    # Percent of data that is missing
    percent_missing = (total_missing/total_cells) * 100

    return percent_missing

def prepare_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    correct_names = {
        'usertype': ['Membership or Pass Type', 'passholder_type', 'User Type', 'Member type', 'member_casual'],
        'bike_type': ['Bike Type', 'rideable_type'],
        'stop_time': ['Checkout Datetime', 'stoptime', 'ended_at', 'Stop Time and Date', 'stoptime', 'end_time', 'End Date', '01 - Rental Details Local End Time', 'End date'],
        'start_time': ['starttime', 'started_at', 'Start Time and Date', 'starttime', 'Start Date', '01 - Rental Details Local Start Time', 'Start date'],
        'trip_duration_minutes': ['Trip Duration Minutes', 'duration'],
        'trip_duration_seconds': ['tripduration', 'duration_sec', 'Duration', '01 - Rental Details Duration In Seconds Uncapped'],
        'gender': ['Gender', 'Member Gender'],
        'latitude_start': ['Latitude Start', 'start_lat', 'start station latitude'],
        'longitude_start': ['Longitude Start', 'start_lng', 'start station longitude', 'start_lon'],
        'latitude_end': ['Latitude End', 'end_lat', 'end station latitude', 'end_lat'],
        'longitude_end': ['Longitude End', 'end_lng', 'end station longitude', 'end_lon'],
        'station_start': ['start_station', 'start station name', '03 - Rental Start Station Name', 'from_station_name', 'start_station_name', 'Checkout Kiosk', 'Start station'],
        'station_end': ['end_station', 'end station name', '02 - Rental End Station Name', 'to_station_name', 'end_station_name', 'Return Kiosk', 'End station'],
    }
    
    for column in correct_names:
        for name in correct_names[column]:
            if name in df:
                df = df.rename(columns={name: column})
                df.to_csv(data_dir, index=False)
    
    for column in correct_names:
        if column not in df and column != 'trip_duration_seconds' and column != 'trip_duration_minutes' and column != 'latitude_start' and column != 'longitude_start' and column != 'latitude_end' and column != 'longitude_end':
            df[column] = ['unknown' for i in range(len(df))]
            df.to_csv(data_dir, index=False)

def prepare_income_data(df, data_dir):
    '''
    fuction to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    correct_names = ['label', 'household_estimates', 'household_margins', 'family_estimates', 'family_margins',
                    'married_estimates', 'married_margins', 'nonfamily_estimates', 'nonfamily_margins']
    counter = 0
    for column in df:
        df.rename(columns={df.columns[counter]: correct_names[counter]}, inplace=True)
        df.to_csv(data_dir, index=False)
        counter += 1

def prepare_gender_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    correct_names = ['label', 'total_estimates', 'total_margins', 'total_percent_estimates', 'total_percent_margins',
                    'male_estimates', 'male_margins', 'male_percent_estimates', 'male_percent_margins',
                    'female_estimates', 'female_margins', 'female_percent_estimates', 'female_percent_margins']
    counter = 0
    for column in df:
        df.rename(columns={df.columns[counter]: correct_names[counter]}, inplace=True)
        df.to_csv(data_dir, index=False)
        counter += 1

def prepare_race_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    for column in df:
        if column.endswith('Margin of Error'):
            df = df.rename(columns={column: 'margin'})
            df.to_csv(data_dir, index=False)
        elif column.endswith('Estimate'):
            df = df.rename(columns={column: 'total_estimates'})
            df.to_csv(data_dir, index=False)
        elif column.endswith('Label (Grouping)'):
            df = df.rename(columns={column: 'label'})
            df.to_csv(data_dir, index=False)

def prepare_zipcode_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    if data_dir.endswith('gender.csv'):
        prepare_gender_data(df, data_dir)
    elif data_dir.endswith('income.csv'):
        prepare_income_data(df, data_dir)
    elif data_dir.endswith('race.csv'):
        prepare_race_data(df, data_dir)

def cancel_column(df, data_dir):
    '''
    function to cancel column that were added by the function get_missing_data
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    if 'gender' in df:
        df.drop(columns=['gender'], inplace=True)
        df.to_csv(data_dir, index=False)
    if 'bike_type' in df:
        df.drop(columns=['bike_type'], inplace=True)
        df.to_csv(data_dir, index=False)
    if 'stop_time' in df:
        df.drop(columns=['stop_time'], inplace=True)
        df.to_csv(data_dir, index=False)
    if 'start_time' in df:
        df.drop(columns=['start_time'], inplace=True)
        df.to_csv(data_dir, index=False)

def first_read_data(data_dir_city):
    '''
    function to read the data for the first time and prepare it for the analysis
    
    Inputs:
        - data_dir_city: str, data directory
    '''
    for city_file in os.listdir(data_dir_city):
        data_dir_city_year = os.path.join(data_dir_city, city_file)
        for year in os.listdir(data_dir_city_year):
            file_path = os.path.join(data_dir_city_year, year)
            df = pd.read_csv(file_path, dtype='object')
            prepare_data(df, file_path)
            missing_data.append(get_missing_data(df, file_path))
    
    print('Missing data:', sum(missing_data) / len(missing_data))
    missing_data.clear()
    
def unify_general_data(full_path):
    '''
    function to unify the data for the general data
    
    Inputs:
        - full_path: str, full path of the data
    '''
    df = pd.read_csv(full_path, dtype='object')
            
    # rename "Label (Grouping)" to "label"
    if 'Label (Grouping)' in df:
        df = df.rename(columns={'Label (Grouping)': 'label'})
        df.to_csv(full_path, index=False)
    
    # rename "estimate" to "total_estimates"
    if 'estimate' in df:
        df = df.rename(columns={'estimate': 'total_estimates'})
        df.to_csv(full_path, index=False)
        

if __name__ == '__main__':
    
    
    path = 'data\\social'
    for city in os.listdir(path):
        data_dir_city = os.path.join(path, city)
        
        for year in os.listdir(data_dir_city):
            data_dir_city_year = os.path.join(data_dir_city, year)
            
            for location in os.listdir(data_dir_city_year):
                if location == "race.csv":
                    full_path = os.path.join(data_dir_city_year, location)
                    unify_general_data(full_path)