import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os
from datetime import datetime


# DURATION ANALYSIS

def get_time(file, df, file_name):
    
    if file == 'data/NYC' or file == 'data/Boston':
        start = df['starttime']
        end = df['stoptime']
        
        durations = list()
        
        if int(file_name[4:6]) < 4 and file == 'data/Boston':
            format = "%Y-%m-%d %H:%M:%S"
        else:
            format = "%Y-%m-%d %H:%M:%S.%f"
        for index in range(len(end)):
            time = datetime.strptime(end[index], format) - datetime.strptime(start[index], format)
            durations.append(time.total_seconds())
    elif file == 'data/Philly':
        start = df['start_time']
        end = df['end_time']
        
        durations = list()
        
        for index in range(len(end)):
            time = datetime.strptime(end[index], "%Y/%-m/%-d %H:%M") - datetime.strptime(start[index], "%Y/%-m/%-d %H:%M")
            durations.append(time.total_seconds())
    elif file == 'data/Washington' or file == 'data/SanFrancisco' or file == 'data/Columbus' or file == 'data/Chicago':
        start = df['started_at']
        end = df['ended_at']
        
        durations = list()
        
        for index in range(len(end)):
            time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
            durations.append(time.total_seconds())
    elif file == 'data/Austin':
        duration = df['trip_duration_ID']
        durations = [time * 60 for time in duration]
    
    durations.sort()
    return durations

def get_duration_info(df, number, axs, fig, file, file_name):
    df = df.sort_values(by='tripduration')
    #durations = df['tripduration']
    durations = get_time(file, df, file_name)

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

def data_integration_for_month():
    data_dir = 'data/Boston'

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
            get_duration_info(integrated_df, month, ax, fig, data_dir, previous_file)
            month += 1
            dfs.clear()
        dfs.append(df)
        
        previous_file = file
    
    integrated_df = pd.concat(dfs, ignore_index=True)
    get_duration_info(integrated_df, month, ax, fig, data_dir, previous_file)

    plt.show()
    
def data_integration_for_year():
    '''
    to adjust
    '''
    data_dir = 'data/NYC'

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
            if len(dfs) != 0:
                integrated_df = pd.concat(dfs, ignore_index=True)
                get_duration_info(integrated_df, year, ax)
                dfs.clear()
                year += 1
            else:
                get_duration_info(df, year, ax)
                year += 1
        else:
            dfs.append(df)
        
        previous_file = file
        
    get_duration_info(integrated_df, year, ax)

    # Show plot
    plt.show()

# GENDER ANALYSIS

def data_integration_for_gender():
    data_dir = 'data/Boston'

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
    

def data_integration_for_usertype():
    data_dir = 'data/NYC'

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
    
data_integration_for_usertype()