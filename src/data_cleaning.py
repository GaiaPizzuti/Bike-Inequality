import numpy as np
import pandas as pd
import os

def get_missing_data(df, data_dir):
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
    '''
    correct_names = {
        'usertype': ['Membership or Pass Type', 'passholder_type', 'User Type', 'Member type', 'member_casual'],
        'bike_type': ['Bike Type', 'rideable_type'],
        'stop_time': ['Checkout Datetime', 'stoptime', 'ended_at', 'Stop Time and Date', 'stoptime', 'end_time', 'End Date', '01 - Rental Details Local End Time', 'End date'],
        'start_time': ['starttime', 'started_at', 'Start Time and Date', 'starttime', 'Start Date', '01 - Rental Details Local Start Time', 'Start date'],
        'trip_duration_minutes': ['Trip Duration Minutes', 'duration'],
        'trip_duration_seconds': ['tripduration', 'duration_sec', 'Duration', '01 - Rental Details Duration In Seconds Uncapped'],
        'gender': ['Gender', 'Member Gender']
    }
    
    for column in correct_names:
        for name in correct_names[column]:
            if name in df:
                df = df.rename(columns={name: column})
                df.to_csv(data_dir, index=False)
    
    for column in correct_names:
        if column not in df and column != 'trip_duration_seconds' and column != 'trip_duration_minutes':
            df[column] = ['unknown' for i in range(len(df))]
            df.to_csv(data_dir, index=False)

def prepare_income_data(df, data_dir):
    '''
    fuction to prepare the data by changing the column names
    '''
    correct_names = {
        'label': ['Label (Grouping)'],
        'household_estimates': ['New York city, New York!!Households!!Estimate', "Columbus city, Ohio!!Households!!Estimate",
                                "Chicago city, Illinois!!Households!!Estimate", "Boston city, Massachusetts!!Households!!Estimate",
                                "Austin city, Texas!!Households!!Estimate", "San Francisco city, California!!Households!!Estimate",
                                "Washington city, District of Columbia!!Households!!Estimate", "Philadelphia city, Pennsylvania!!Households!!Estimate"],
        'household_margins': ['New York city, New York!!Households!!Margin of Error', "Columbus city, Ohio!!Households!!Margin of Error",
                            "Chicago city, Illinois!!Households!!Margin of Error", "Boston city, Massachusetts!!Households!!Margin of Error",
                            "Austin city, Texas!!Households!!Margin of Error", "San Francisco city, California!!Households!!Margin of Error",
                            "Washington city, District of Columbia!!Households!!Margin of Error", "Philadelphia city, Pennsylvania!!Households!!Margin of Error"],
        'family_estimates': ['New York city, New York!!Families!!Estimate', "Columbus city, Ohio!!Families!!Estimate",
                            "Chicago city, Illinois!!Families!!Estimate", "Boston city, Massachusetts!!Families!!Estimate",
                            "Austin city, Texas!!Families!!Estimate", "San Francisco city, California!!Families!!Estimate",
                            "Washington city, District of Columbia!!Families!!Estimate", "Philadelphia city, Pennsylvania!!Families!!Estimate"],
        'family_margins': ['New York city, New York!!Families!!Margin of Error', "Columbus city, Ohio!!Families!!Margin of Error",
                        "Chicago city, Illinois!!Families!!Margin of Error", "Boston city, Massachusetts!!Families!!Margin of Error",
                        "Austin city, Texas!!Families!!Margin of Error", "San Francisco city, California!!Families!!Margin of Error",
                        "Washington city, District of Columbia!!Families!!Margin of Error", "Philadelphia city, Pennsylvania!!Families!!Margin of Error"],
        'married_estimates': ['New York city, New York!!Married-couple families!!Estimate', "Columbus city, Ohio!!Married-couple families!!Estimate",
                            "Chicago city, Illinois!!Married-couple families!!Estimate", "Boston city, Massachusetts!!Married-couple families!!Estimate",
                            "Austin city, Texas!!Married-couple families!!Estimate", "San Francisco city, California!!Married-couple families!!Estimate",
                            "Washington city, District of Columbia!!Married-couple families!!Estimate", "Philadelphia city, Pennsylvania!!Married-couple families!!Estimate"],
        'married_margins': ['New York city, New York!!Married-couple families!!Margin of Error', "Columbus city, Ohio!!Married-couple families!!Margin of Error",
                            "Chicago city, Illinois!!Married-couple families!!Margin of Error", "Boston city, Massachusetts!!Married-couple families!!Margin of Error",
                            "Austin city, Texas!!Married-couple families!!Margin of Error", "San Francisco city, California!!Married-couple families!!Margin of Error",
                            "Washington city, District of Columbia!!Married-couple families!!Margin of Error", "Philadelphia city, Pennsylvania!!Married-couple families!!Margin of Error"],
        'nonfamily_estimates': ['New York city, New York!!Nonfamily households!!Estimate', "Columbus city, Ohio!!Nonfamily households!!Estimate",
                                "Chicago city, Illinois!!Nonfamily households!!Estimate", "Boston city, Massachusetts!!Nonfamily households!!Estimate",
                                "Austin city, Texas!!Nonfamily households!!Estimate", "San Francisco city, California!!Nonfamily households!!Estimate",
                                "Washington city, District of Columbia!!Nonfamily households!!Estimate", "Philadelphia city, Pennsylvania!!Nonfamily households!!Estimate"],
        'nonfamily_margins': ['New York city, New York!!Nonfamily households!!Margin of Error', "Columbus city, Ohio!!Nonfamily households!!Margin of Error",
                            "Chicago city, Illinois!!Nonfamily households!!Margin of Error", "Boston city, Massachusetts!!Nonfamily households!!Margin of Error",
                            "Austin city, Texas!!Nonfamily households!!Margin of Error", "San Francisco city, California!!Nonfamily households!!Margin of Error",
                            "Washington city, District of Columbia!!Nonfamily households!!Margin of Error", "Philadelphia city, Pennsylvania!!Nonfamily households!!Margin of Error"],
    }
    
    for column in correct_names:
        for name in correct_names[column]:
            if name in df:
                df = df.rename(columns={name: column})
                df.to_csv(data_dir, index=False)

def prepare_gender_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    correct_names = {
        'label': ['Label (Grouping)'],
        'total_estimates': ['New York city, New York!!Total!!Estimate', 'Austin city, Texas!!Total!!Estimate',
                            'Chicago city, Illinois!!Total!!Estimate', 'Columbus city, Ohio!!Total!!Estimate',
                            'Boston city, Massachusetts!!Total!!Estimate', 'Philadelphia city, Pennsylvania!!Total!!Estimate',
                            'San Francisco city, California!!Total!!Estimate', 'Washington city, District of Columbia!!Total!!Estimate'],
        'total_margins': ['New York city, New York!!Total!!Margin of Error', 'Austin city, Texas!!Total!!Margin of Error',
                        'Chicago city, Illinois!!Total!!Margin of Error', 'Columbus city, Ohio!!Total!!Margin of Error',
                        'Boston city, Massachusetts!!Total!!Margin of Error', 'Philadelphia city, Pennsylvania!!Total!!Margin of Error',
                        'San Francisco city, California!!Total!!Margin of Error', 'Washington city, District of Columbia!!Total!!Margin of Error'],
        'total_percent': ['New York city, New York!!Percent!!Estimate', 'Austin city, Texas!!Percent!!Estimate',
                        'Chicago city, Illinois!!Percent!!Estimate', 'Columbus city, Ohio!!Percent!!Estimate',
                        'Boston city, Massachusetts!!Percent!!Estimate', 'Philadelphia city, Pennsylvania!!Percent!!Estimate',
                        'San Francisco city, California!!Percent!!Estimate', 'Washington city, District of Columbia!!Percent!!Estimate'],
        'total_percent_margins': ['New York city, New York!!Percent!!Margin of Error', 'Austin city, Texas!!Percent!!Margin of Error',
                                'Chicago city, Illinois!!Percent!!Margin of Error', 'Columbus city, Ohio!!Percent!!Margin of Error',
                                'Boston city, Massachusetts!!Percent!!Margin of Error', 'Philadelphia city, Pennsylvania!!Percent!!Margin of Error',
                                'San Francisco city, California!!Percent!!Margin of Error', 'Washington city, District of Columbia!!Percent!!Margin of Error'],
        'male_estimates': ['New York city, New York!!Male!!Estimate', 'Austin city, Texas!!Male!!Estimate',
                        'Chicago city, Illinois!!Male!!Estimate', 'Columbus city, Ohio!!Male!!Estimate',
                        'Boston city, Massachusetts!!Male!!Estimate', 'Philadelphia city, Pennsylvania!!Male!!Estimate',
                        'San Francisco city, California!!Male!!Estimate', 'Washington city, District of Columbia!!Male!!Estimate'],
        'male_margins': ['New York city, New York!!Male!!Margin of Error', 'Austin city, Texas!!Male!!Margin of Error',
                        'Chicago city, Illinois!!Male!!Margin of Error', 'Columbus city, Ohio!!Male!!Margin of Error',
                        'Boston city, Massachusetts!!Male!!Margin of Error', 'Philadelphia city, Pennsylvania!!Male!!Margin of Error',
                        'San Francisco city, California!!Male!!Margin of Error', 'Washington city, District of Columbia!!Male!!Margin of Error'],
        'male_percent': ['New York city, New York!!Percent Male!!Estimate', 'Austin city, Texas!!Percent Male!!Estimate',
                        'Chicago city, Illinois!!Percent Male!!Estimate', 'Columbus city, Ohio!!Percent Male!!Estimate',
                        'Boston city, Massachusetts!!Percent Male!!Estimate', 'Philadelphia city, Pennsylvania!!Percent Male!!Estimate',
                        'San Francisco city, California!!Percent Male!!Estimate', 'Washington city, District of Columbia!!Percent Male!!Estimate'],
        'male_percent_margins': ['New York city, New York!!Percent Male!!Margin of Error', 'Austin city, Texas!!Percent Male!!Margin of Error',
                                'Chicago city, Illinois!!Percent Male!!Margin of Error', 'Columbus city, Ohio!!Percent Male!!Margin of Error',
                                'Boston city, Massachusetts!!Percent Male!!Margin of Error', 'Philadelphia city, Pennsylvania!!Percent Male!!Margin of Error',
                                'San Francisco city, California!!Percent Male!!Margin of Error', 'Washington city, District of Columbia!!Percent Male!!Margin of Error'],
        'female_estimates': ['New York city, New York!!Female!!Estimate', 'Austin city, Texas!!Female!!Estimate',
                            'Chicago city, Illinois!!Female!!Estimate', 'Columbus city, Ohio!!Female!!Estimate',
                            'Boston city, Massachusetts!!Female!!Estimate', 'Philadelphia city, Pennsylvania!!Female!!Estimate',
                            'San Francisco city, California!!Female!!Estimate', 'Washington city, District of Columbia!!Female!!Estimate'],
        'female_margins': ['New York city, New York!!Female!!Margin of Error', 'Austin city, Texas!!Female!!Margin of Error',
                        'Chicago city, Illinois!!Female!!Margin of Error', 'Columbus city, Ohio!!Female!!Margin of Error',
                        'Boston city, Massachusetts!!Female!!Margin of Error', 'Philadelphia city, Pennsylvania!!Female!!Margin of Error',
                        'San Francisco city, California!!Female!!Margin of Error', 'Washington city, District of Columbia!!Female!!Margin of Error'],
        'female_percent': ['New York city, New York!!Percent Female!!Estimate', 'Austin city, Texas!!Percent Female!!Estimate',
                        'Chicago city, Illinois!!Percent Female!!Estimate', 'Columbus city, Ohio!!Percent Female!!Estimate',
                        'Boston city, Massachusetts!!Percent Female!!Estimate', 'Philadelphia city, Pennsylvania!!Percent Female!!Estimate',
                        'San Francisco city, California!!Percent Female!!Estimate', 'Washington city, District of Columbia!!Percent Female!!Estimate'],
        'female_percent_margins': ['New York city, New York!!Percent Female!!Margin of Error', 'Austin city, Texas!!Percent Female!!Margin of Error',
                                'Chicago city, Illinois!!Percent Female!!Margin of Error', 'Columbus city, Ohio!!Percent Female!!Margin of Error',
                                'Boston city, Massachusetts!!Percent Female!!Margin of Error', 'Philadelphia city, Pennsylvania!!Percent Female!!Margin of Error',
                                'San Francisco city, California!!Percent Female!!Margin of Error', 'Washington city, District of Columbia!!Percent Female!!Margin of Error']
    }
    
    for column in correct_names:
        for name in correct_names[column]:
            if name in df:
                df = df.rename(columns={name: column})
                df.to_csv(data_dir, index=False)

def prepare_race_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    
    Inputs:
        - df: pandas dataframe
        - data_dir: str, data directory
    '''
    correct_names = {
        'estimate': ['Austin city, Texas!!Estimate', 'Boston city, Massachusetts!!Estimate', 'Chicago city, Illinois!!Estimate',
                    'Columbus city, Ohio!!Estimate', 'New York city, New York!!Estimate', 'Philadelphia city, Pennsylvania!!Estimate',
                    'San Francisco city, California!!Estimate', 'Washington city, District of Columbia!!Estimate'],
        'margin': ['Austin city, Texas!!Margin of Error', 'Boston city, Massachusetts!!Margin of Error', 'Chicago city, Illinois!!Margin of Error',
                'Columbus city, Ohio!!Margin of Error', 'New York city, New York!!Margin of Error', 'Philadelphia city, Pennsylvania!!Margin of Error',
                'San Francisco city, California!!Margin of Error', 'Washington city, District of Columbia!!Margin of Error'],
    }
    
    for column in correct_names:
        for name in correct_names[column]:
            if name in df:
                df = df.rename(columns={name: column})
                df.to_csv(data_dir, index=False)

def cancel_column(df, data_dir):
    '''
    function to cancel column that were added by the function get_missing_data
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
    for city_file in os.listdir(data_dir_city):
        data_dir_city_year = os.path.join(data_dir_city, city_file)
        for year in os.listdir(data_dir_city_year):
            file_path = os.path.join(data_dir_city_year, year)
            df = pd.read_csv(file_path, dtype='object')
            prepare_data(df, file_path)
            missing_data.append(get_missing_data(df, file_path))
    
    print('Missing data:', sum(missing_data) / len(missing_data))
    missing_data.clear()

if __name__ == '__main__':
    data_dir = 'data\\social'
    
    for city in os.listdir(data_dir):
        
        city_path = os.path.join(data_dir, city)
        
        for year in os.listdir(city_path):
            
            year_path = os.path.join(city_path, year)
            
            for file in os.listdir(year_path):
                
                file_path = os.path.join(data_dir, city, year, file)
                df = pd.read_csv(file_path, dtype='object')
                prepare_race_data(df, file_path)