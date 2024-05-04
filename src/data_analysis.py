import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os
from datetime import datetime


def get_missing_data(df):
    # Get the number of missing data points per column
    missing_values_count = df.isnull().sum()

    # How many total missing values do we have?
    total_cells = np.prod(df.shape)
    total_missing = missing_values_count.sum()

    # Percent of data that is missing
    percent_missing = (total_missing/total_cells) * 100
    if percent_missing == 0.0:
        print("No missing data")
    else:
        print(missing_values_count[:])

    return percent_missing

# DURATION ANALYSIS

def get_time(file, df):
    '''
    get the duration of the trip for each file
    '''
    if file == 'data/NYC':
        start = df['starttime']
        end = df['stoptime']
        
        durations = list()
        
        for index in range(len(end)):
            time = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(start[index], '%Y-%m-%d %H:%M:%S.%f')
            durations.append(time.total_seconds())
    elif file == 'data/Philly':
        start = df['start_time']
        end = df['end_time']
        
        durations = list()
        
        for index in range(len(end)):
            time = datetime.strptime(end[index], "%Y/%-m/%-d %H:%M") - datetime.strptime(start[index], "%Y/%-m/%-d %H:%M")
            durations.append(time.total_seconds())
    elif file == 'data/SanFrancisco' or file == 'data/Columbus' or file == 'data/Chicago':
        start = df['started_at']
        end = df['ended_at']
        
        durations = list()
        
        for index in range(len(end)):
            time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
            durations.append(time.total_seconds())
    elif file == 'data/Boston':
        duration = df['tripduration']
        durations = [time for time in duration]
    elif file == 'data/Washington':
        duration = df['Duration']
        durations = [time for time in duration]
    elif file == 'data/Austin':
        duration = df['trip_duration_ID']
        durations = [time * 60 for time in duration]
    
    durations.sort()
    return durations

def get_duration_info(df, number, axs, fig, file):
    '''
    function to get the duration information for each file, cluster them and plot the frequency of each cluster
    '''
    if file == 'data/NYC' or file == 'data/Boston':
        df = df.sort_values(by='tripduration')
    elif file == 'data/Washington':
        df = df.sort_values(by='Duration')
    durations = get_time(file, df)

    # Define a function to determine the cluster for each number
    def get_cluster(num):
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
            get_duration_info(integrated_df, month, ax, fig, data_dir)
            month += 1
            dfs.clear()
        dfs.append(df)
        
        previous_file = file
    
    integrated_df = pd.concat(dfs, ignore_index=True)
    get_duration_info(integrated_df, month, ax, fig, data_dir)

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
        genders_infos['unknown'] += count[0]
        genders_infos['men'] += count[1]
        genders_infos['women'] += count[2]
    
    fig, ax = plt.subplots()
    plt.pie(genders_infos.values(), labels=genders_infos.keys(),  autopct='%1.1f%%')
    plt.show()
    

def data_for_usertype(data_dir):

    data_files = os.listdir(data_dir)
    usertypes_infos = {
        'customers': 0,
        'subscribers': 0,
    }

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        count = df['usertype'].value_counts()
        usertypes_infos['customers'] += count['Customer']
        usertypes_infos['subscribers'] += count['Subscriber']
    
    fig, ax = plt.subplots()
    plt.pie(usertypes_infos.values(), labels=usertypes_infos.keys(),  autopct='%1.1f%%')
    plt.show()


if __name__ == '__main__':
    data_dir = 'data'
    for file in os.listdir(data_dir):
        print('City:', file)
        data_dir_city = os.path.join(data_dir, file)
        data_files = os.listdir(data_dir_city)
        for file in data_files:
            file_path = os.path.join(data_dir_city, file)
            df = pd.read_csv(file_path)
            print(get_missing_data(df))
        #data_for_month(data_dir_city)
        #data_for_gender(data_dir_city)
        #data_for_usertype(data_dir_city)