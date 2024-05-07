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
        if file == 'data\\NYC':
            for index in range(len(end)):
                time = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(start[index], '%Y-%m-%d %H:%M:%S.%f')
                durations.append(time.total_seconds())
        elif file == 'data\\Philly':
            for index in range(len(end)):
                month = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S').month
                if month_to_analyse == month:
                    time = datetime.strptime(end[index], "%Y/%-m/%-d %H:%M") - datetime.strptime(start[index], "%Y/%-m/%-d %H:%M")
                    durations.append(time.total_seconds())
        elif file == 'data\\Columbus':
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif file == 'data\\Chicago':        
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
            return "< 500"
        elif num < 1000:
            return "< 1000"
        elif num < 10000:
            return "< 10000"
        elif num < 100000:
            return "< 100000"
        else:
            return "> 100000"

    # Group numbers into clusters
    clusters = [get_cluster(num) for num in durations]

    # Calculate frequency of each cluster
    frequency = Counter(clusters)

    # Extract cluster names and their frequencies
    cluster_names = list(frequency.keys())
    cluster_frequencies = list(frequency.values())
    total = sum(cluster_frequencies)
    for value in range(len(cluster_frequencies)):
        cluster_frequencies[value] /= total
    
    x = number // 3
    y = number % 3
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

    dfs = list()
    previous_file = ""
    month = 0

    fig, ax = plt.subplots(4, 3)

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        if file[0:4] != previous_file[0:4] and previous_file != "":
            break
        
        # if file is different from the the previous one then we can integrathe the file in the list
        if file[0:6] != previous_file[0:6] and previous_file != "":
            integrated_df = pd.concat(dfs, ignore_index=True)
            if data_dir == 'data\\Philly':
                for _ in range(3):
                    get_duration_info(integrated_df, month, ax, fig, data_dir)
                    month += 1
            else:
                month = int(previous_file[4:6]) - 1
                get_duration_info(integrated_df, month, ax, fig, data_dir)
            dfs.clear()
        dfs.append(df)
        
        previous_file = file
    
    if data_dir == 'data\\Philly':
        for _ in range(3):
            get_duration_info(integrated_df, month, ax, fig, data_dir)
            month += 1
    else:
        month = int(previous_file[4:6]) - 1
        integrated_df = pd.concat(dfs, ignore_index=True)
        get_duration_info(integrated_df, month, ax, fig, data_dir)
    
    plt.title(data_dir)
    plt.show()
    
def data_for_year(data_dir):
    '''
    to adjust
    '''

    data_files = os.listdir(data_dir)

    dfs = list()
    previous_file = ""
    year = 0

    fig, ax = plt.subplots(4, 3)

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        if file[0:4] != previous_file[0:4] and previous_file != "":
            integrated_df = pd.concat(dfs, ignore_index=True)
            get_duration_info(integrated_df, year, ax)
            dfs.clear()
            year += 1
        dfs.append(df)
        
        previous_file = file
        
    integrated_df = pd.concat(dfs, ignore_index=True)
    get_duration_info(integrated_df, year, ax)

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
        data_files = os.listdir(data_dir_city)
        for file in data_files:
            file_path = os.path.join(data_dir_city, file)
            df = pd.read_csv(file_path)
            prepare_data(df, file_path)
            missing_data.append(get_missing_data(df, file_path))
        
        print('Missing data:', sum(missing_data) / len(missing_data))
        missing_data.clear()
        data_for_month(data_dir_city)
        #data_for_gender(data_dir_city)
        #data_for_usertype(data_dir_city)
    
    """ data_dir = 'data/Washington'
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        cancel_column(df, file_path) """