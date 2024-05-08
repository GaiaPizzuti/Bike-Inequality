import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os
from datetime import datetime


def get_missing_data(df, data_dir):
    # Get the number of missing data points per column
    missing_values_count = df.isnull().sum()

    # How many total missing values do we have?
    total_cells = np.prod(df.shape)
    total_missing = missing_values_count.sum()

    # Percent of data that is missing
    percent_missing = (total_missing/total_cells) * 100
    
    """ if 'Gender' in df:
        df = df.rename(columns={'Gender': 'gender'})
        df.to_csv(data_dir, index=False)
    elif 'gender' not in df:
        df['gender'] = ['unknown' for i in range(len(df))]
        df.to_csv(data_dir, index=False)
    
    if 'user_type' in df:
        df = df.rename(columns={'user_type': 'usertype'})
        df.to_csv(data_dir, index=False)
    elif 'member_casual' in df:
        df = df.rename(columns={'member_casual': 'usertype'})
        df.to_csv(data_dir, index=False)
    elif 'User Type' in df:
        df = df.rename(columns={'User Type': 'usertype'})
        df.to_csv(data_dir, index=False)
    elif 'Member type' in df:
        df = df.rename(columns={'Member type': 'usertype'})
        df.to_csv(data_dir, index=False)
    elif 'usertype' not in df:
        df['usertype'] = ['unknown' for i in range(len(df))]
        df.to_csv(data_dir, index=False) """

    return percent_missing

# DURATION ANALYSIS

def get_time(file, df, month_to_analyse):
    '''
    get the duration of the trip for each file
    '''
    durations = list()
    if 'trip_duration_seconds' in df or 'trip_duration_minutes' in df:
        if 'trip_duration_seconds' in df:
            duration = df['trip_duration_seconds']
            durations = [time for time in duration]
        else:
            duration = df['trip_duration_minutes']
            durations = [time * 60 for time in duration]
    else:
        start = df['start_time']
        end = df['stop_time']
        if file[:8] == 'data\\NYC':
            for index in range(len(end)):
                time = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(start[index], '%Y-%m-%d %H:%M:%S.%f')
                durations.append(time.total_seconds())
        elif file[:11] == 'data\\Philly':
            for index in range(len(end)):
                month = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S').month
                if month_to_analyse == month:
                    time = datetime.strptime(end[index], "%Y/%-m/%-d %H:%M") - datetime.strptime(start[index], "%Y/%-m/%-d %H:%M")
                    durations.append(time.total_seconds())
        elif file[:12] == 'data\\Columbus':
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif file[:12] == 'data\\Chicago':        
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        
    durations.sort()
    return durations

def get_duration_info(df, number, axs, fig, file):
    '''
    function to get the duration information for each file, cluster them and plot the frequency of each cluster
    '''
    durations = get_time(file, df, number)

    # Define a function to determine the cluster for each number
    def get_cluster(num):
        if type(num) == str:
            num = int(float(num.replace(',', '')))
        if num < 500:
            return "<500"
        elif num < 1000:
            return "<1000"
        elif num < 10000:
            return "<10000"
        elif num < 100000:
            return "<100000"
        else:
            return ">100000"

    # Group numbers into clusters
    clusters = [get_cluster(num) for num in durations]

    # Calculate frequency of each cluster
    frequency = Counter(clusters)

    # Extract cluster names and their frequencies
    for key in frequency:
        frequency[key] /= sum(frequency.values())
    
    return frequency

def prepare_plot(axs, fig, frequency, number):
    x = number // 3
    y = number % 3
    cluster_names = list(frequency.keys())
    cluster_frequencies = list(frequency.values())
    axs[x, y].bar(cluster_names, cluster_frequencies)
    for index in range(len(cluster_names)):
        axs[x, y].text(index, cluster_frequencies[index], str(round(cluster_frequencies[index], 5)), ha='center')

    # Add labels and title
    for ax in axs.flat:
        ax.set(xlabel='Trip duration', ylabel='Frequency')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    fig.suptitle('Frequency of Trip Duration')

# Read the CSV file into a DataFrame

def data_for_month(data_dir):

    data_files = os.listdir(data_dir)
    month = 0

    fig, ax = plt.subplots(4, 3)

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        
        if data_dir[:11] == 'data\\Philly':
            for _ in range(3):
                frequency = get_duration_info(df, month, ax, fig, data_dir)
                prepare_plot(ax, fig, frequency, month)
                month += 1
        else:
            month = int(file[4:6]) - 1
            frequency = get_duration_info(df, month, ax, fig, data_dir)
            prepare_plot(ax, fig, frequency, month)
    
    plt.title(data_dir)
    plt.show()
    
def data_for_year(data_dir):
    '''
    function to plot the data for each year
    '''

    fig, ax = plt.subplots(2, 3)
    yearly_frequency = {
        '<500': 0,
        '<1000': 0,
        '<10000': 0,
        '<100000': 0,
        '>100000': 0
    }
    
    
    for year in os.listdir(data_dir):
        year_path = os.path.join(data_dir, year)
        for file in os.listdir(year_path):
            file_path = os.path.join(year_path, file)
            df = pd.read_csv(file_path)
            frequency = get_duration_info(df, year, ax, fig, data_dir)
            for key in frequency:
                yearly_frequency[key] += frequency[key]
        year = int(year) - 2018
        for key in yearly_frequency:
            yearly_frequency[key] /= sum(yearly_frequency.values())
        prepare_plot(ax, fig, yearly_frequency, year)
        frequency.clear()
    
    # Show plot
    plt.show()


# GENDER ANALYSIS

def data_for_gender(data_dir):

    data_files = os.listdir(data_dir)
    genders_infos = {
        'unknown': 0,
        'men': 0,
        'women': 0,
    }

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        count = df['gender'].value_counts()
        print(count)
        # plot the percentage of each data
        if 'unknown' in count:
            genders_infos['unknown'] += count.loc['unknown']
        if 1 in count:
            genders_infos['unknown'] += count[0]
            genders_infos['men'] += count[1]
            genders_infos['women'] += count[2]
    
    fig, ax = plt.subplots()
    plt.title(data_dir)
    plt.pie(genders_infos.values(), labels=genders_infos.keys(),  autopct='%1.1f%%')
    plt.show()
    

def data_for_usertype(data_dir):

    data_files = os.listdir(data_dir)
    usertypes_infos = {
        'unknown': 0,
        'customers': 0,
        'subscribers': 0,
    }

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        count = df['usertype'].value_counts()
        if 'unknown' in count:
            usertypes_infos['unknown'] += count['unknown']
        if 'Customer' in count:
            usertypes_infos['customers'] += count['Customer']
            usertypes_infos['subscribers'] += count['Subscriber']
        if 'member' in count:
            usertypes_infos['customers'] += count['casual']
            usertypes_infos['subscribers'] += count['member']
        if 'Member' in count:
            usertypes_infos['customers'] += count['Casual']
            usertypes_infos['subscribers'] += count['Member']
    
    fig, ax = plt.subplots()
    plt.title(data_dir)
    plt.pie(usertypes_infos.values(), labels=usertypes_infos.keys(),  autopct='%1.1f%%')
    plt.legend(loc='upper right')
    plt.show()

def prepare_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    '''
    correct_names = {
        'usertype': ['Membership or Pass Type', 'passholder_type', 'User Type', 'Member type'],
        'bike_type': ['Bike Type', 'rideable_type'],
        'stop_time': ['Checkout Datetime', 'stoptime', 'ended_at', 'Stop Time and Date', 'stoptime', 'end_time', 'End Date'],
        'start_time': ['starttime', 'started_at', 'Start Time and Date', 'starttime', 'Start Date'],
        'trip_duration_minutes': ['Trip Duration Minutes', 'duration'],
        'trip_duration_seconds': ['tripduration', 'duration_sec', 'Duration'],
        'gender': ['Gender']
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

if __name__ == '__main__':
    data_dir = 'data'
    missing_data = list()
    for file in os.listdir(data_dir):
        print('City:', file)
        data_dir_city = os.path.join(data_dir, file)
        for city_file in os.listdir(data_dir_city):
            print('Year:', city_file)
            data_dir_city_year = os.path.join(data_dir_city, city_file)
            
            for year in os.listdir(data_dir_city_year):
                file_path = os.path.join(data_dir_city_year, year)
                df = pd.read_csv(file_path)
                prepare_data(df, file_path)
                missing_data.append(get_missing_data(df, file_path))
                
        
        """
        data_files = os.listdir(data_dir_city)
        for year in data_files:
            data_dir_city_year = os.path.join(data_dir_city, year)
            data_files = os.listdir(data_dir_city_year)
            for file in data_files:
                file_path = os.path.join(data_dir_city_year, file)
                df = pd.read_csv(file_path)
                prepare_data(df, file_path)
                missing_data.append(get_missing_data(df, file_path))
        """
        
        print('Missing data:', sum(missing_data) / len(missing_data))
        missing_data.clear()
        
        """ # plot date for each month
        for year in os.listdir(data_dir_city):
            print('Year:', year)
            data_dir_city_year = os.path.join(data_dir_city, year)
            data_for_month(data_dir_city_year) """
        
        # plot data for each year
        data_for_year(data_dir_city)
        
        # plot data for gender
        #data_for_gender(data_dir_city)
        
        # plot data for usertype
        #data_for_usertype(data_dir_city)
    
    """ data_dir = 'data/Washington'
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        cancel_column(df, file_path) """