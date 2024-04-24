import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

def get_duration_info(df, number, axs):
    df = df.sort_values(by='tripduration')
    durations = df['tripduration']

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
    data_dir = 'data/NYC'

    data_files = os.listdir(data_dir)

    dfs = list()
    previous_file = ""
    month = 0

    fig, ax = plt.subplots(4, 3)

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        if file[0:6] != previous_file[0:6] and previous_file != "":
            if len(dfs) != 0:
                integrated_df = pd.concat(dfs, ignore_index=True)
                get_duration_info(integrated_df, month, ax)
                dfs.clear()
                month += 1
            else:
                get_duration_info(df, month, ax)
                month += 1
        else:
            dfs.append(df)
        
        previous_file = file
        
    get_duration_info(integrated_df, month, ax)

    # Show plot
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