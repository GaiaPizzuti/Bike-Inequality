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

    return percent_missing

# DURATION ANALYSIS

def get_time(df, number_to_analyse, full_path):
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
        format_dictionary = {
            'data\\NYC': {
                '202102': "%Y-%m-%d %H:%M:%S",
                'default': "%Y-%m-%d %H:%M:%S.%f"
            },
            'data\\Philly': {
                'default': "%Y-%m-%d %H:%M:%S"
            },
            'data\\Columbus': {
                'default': "%Y-%m-%d %H:%M:%S"
            },
            'data\\Chicago': {
                'default': "%Y-%m-%d %H:%M:%S"
            },
            'data\\Boston': {
                '202304': "%Y-%m-%d %H:%M:%S",
                'default': "%Y-%m-%d %H:%M:%S.%f"
            }
        }
        if 'NYC' in full_path:
            if full_path[14:20] >= '202102':
                date_format = "%Y-%m-%d %H:%M:%S"
            else:
                date_format = "%Y-%m-%d %H:%M:%S.%f"
            for index in range(len(end)):
                time = datetime.strptime(end[index], date_format) - datetime.strptime(start[index], date_format)
                durations.append(time.total_seconds())
        elif 'Philly' in full_path:
            for index in range(len(end)):
                month = datetime.strptime(end[index], '%Y-%m-%d %H:%M:%S').month
                if number_to_analyse == month:
                    time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                    durations.append(time.total_seconds())
        elif 'Columbus' in full_path:
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif 'Chicago' in full_path:        
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif 'Boston' in full_path:
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif 'SanFrancisco' in full_path:
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        elif 'Washington' in full_path:
            for index in range(len(end)):
                time = datetime.strptime(end[index], "%Y-%m-%d %H:%M:%S") - datetime.strptime(start[index], "%Y-%m-%d %H:%M:%S")
                durations.append(time.total_seconds())
        
    durations.sort()
    return durations

def get_duration_info(df, number, axs, fig, full_path):
    '''
    function to get the duration information for each file, cluster them and plot the frequency of each cluster
    '''
    durations = get_time(df, number, full_path)

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
    total = sum(frequency.values())
    for key in frequency:
        frequency[key] /= total
    
    return frequency

def prepare_plot(axs, fig, frequency, number, data_dir):
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
    title = 'Frequency of Trip Duration for ' + data_dir
    fig.suptitle(title)

# Read the CSV file into a DataFrame

def data_for_month(data_dir):

    data_files = os.listdir(data_dir)
    month = 0

    fig, ax = plt.subplots(4, 3)

    for file in data_files:
        # read data from each file into a DataFrame
        file_path = os.path.join(data_dir, file)
        
        df = pd.read_csv(file_path)
        
        if 'Philly' in data_dir or ('Chicago' in file_path and file_path[18:24] < '202004') or  ('Chicago' in file_path and '2020Q1' in file_path):
            month = (int(file[5:6]) - 1) * 3
            for _ in range(3):
                frequency = get_duration_info(df, month, ax, fig, file_path)
                prepare_plot(ax, fig, frequency, month, data_dir)
                month += 1
        else:
            month = int(file[4:6]) - 1
            frequency = get_duration_info(df, month, ax, fig, file_path)
            prepare_plot(ax, fig, frequency, month, data_dir)
    
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
            df = pd.read_csv(file_path, dtype='object')
            frequency = get_duration_info(df, year, ax, fig, file_path)
            for key in frequency:
                yearly_frequency[key] += frequency[key]
        year = int(year) - 2018
        total = sum(yearly_frequency.values())
        for key in yearly_frequency:
            yearly_frequency[key] /= total
        prepare_plot(ax, fig, yearly_frequency, year, year_path)
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

    for year in data_files:
        # read data from each file into a DataFrame
        year_path = os.path.join(data_dir, year)
        for file in os.listdir(year_path):
            
            file_path = os.path.join(year_path, file)
            
            df = pd.read_csv(file_path, dtype='object')
            count = df['gender'].value_counts()
            # plot the percentage of each data
            if 'unknown' in count:
                genders_infos['unknown'] += count.loc['unknown']
            if 1 in count:
                genders_infos['unknown'] += count[0]
                genders_infos['men'] += count[1]
                genders_infos['women'] += count[2]
    
    if genders_infos['men'] != 0 or genders_infos['women'] != 0:
        fig, ax = plt.subplots()
        plt.title(data_dir)
        plt.pie(genders_infos.values(), labels=genders_infos.keys(),  autopct='%1.1f%%')
        plt.show()
    else:
        print('Gender data not available in this city:', data_dir[6:])
    

def data_for_usertype(data_dir):
    
    data_files = os.listdir(data_dir)
    if 'Philly' in data_dir:
        usertypes_infos = {
            'Indego30': 0,
            'Indego365': 0,
            'Walk-up': 0,
            'Day Pass': 0,
            'IndegoFlex': 0,
        }
    elif 'Austin' in data_dir:
        usertypes_infos = {
            'Walk Up': 0,
            'Local365': 0,
            'Local30': 0,
            'Local365+Guest Pass': 0,
            'Republic Rider': 0,
        }
    else:
        usertypes_infos = {
            'unknown': 0,
            'customers': 0,
            'subscribers': 0,
        }

    for year in data_files:
        # read data from each file into a DataFrame
        year_path = os.path.join(data_dir, year)
        
        for file in os.listdir(year_path):
            file_path = os.path.join(year_path, file)
        
            df = pd.read_csv(file_path, dtype='object')
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
            if 'Philly' in file_path:
                if 'Indego30' in count:
                    usertypes_infos['Indego30'] += count['Indego30']
                if 'Indego365' in count:
                    usertypes_infos['Indego365'] += count['Indego365']
                if 'Walk-up' in count:
                    usertypes_infos['Walk-up'] += count['Walk-up']
                if 'Day Pass' in count:
                    usertypes_infos['Day Pass'] += count['Day Pass']
                if 'IndegoFlex' in count:
                    usertypes_infos['IndegoFlex'] += count['IndegoFlex']
            if 'Austin' in file_path:
                if 'Walk Up' in count:
                    usertypes_infos['Walk Up'] += count['Walk Up']
                if 'Local365' in count:
                    usertypes_infos['Local365'] += count['Local365']
                if 'Local30' in count:
                    usertypes_infos['Local30'] += count['Local30']
                if 'Local365+Guest Pass' in count:
                    usertypes_infos['Local365+Guest Pass'] += count['Local365+Guest Pass']
                if 'Republic Rider' in count:
                    usertypes_infos['Republic Rider'] += count['Republic Rider (Annual)']
    
    fig, ax = plt.subplots()
    plt.title(data_dir)
    print(usertypes_infos)
    plt.pie(usertypes_infos.values(), labels=usertypes_infos.keys(),  autopct='%1.1f%%')
    plt.show()

def prepare_data(df, data_dir):
    '''
    function to prepare the data by changing the column names
    '''
    correct_names = {
        'usertype': ['Membership or Pass Type', 'passholder_type', 'User Type', 'Member type', 'member_casual'],
        'bike_type': ['Bike Type', 'rideable_type'],
        'stop_time': ['Checkout Datetime', 'stoptime', 'ended_at', 'Stop Time and Date', 'stoptime', 'end_time', 'End Date', '01 - Rental Details Local End Time'],
        'start_time': ['starttime', 'started_at', 'Start Time and Date', 'starttime', 'Start Date', '01 - Rental Details Local Start Time'],
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
            data_dir_city_year = os.path.join(data_dir_city, city_file)
            for year in os.listdir(data_dir_city_year):
                file_path = os.path.join(data_dir_city_year, year)
                df = pd.read_csv(file_path, dtype='object')
                prepare_data(df, file_path)
                missing_data.append(get_missing_data(df, file_path))
        
        print('Missing data:', sum(missing_data) / len(missing_data))
        missing_data.clear()
        
        # plot date for each month
        """ for year in os.listdir(data_dir_city):
            print('Year:', year)
            data_dir_city_year = os.path.join(data_dir_city, year)
            data_for_month(data_dir_city_year) """
        
        # plot data for each year
        #data_for_year(data_dir_city)
        
        # plot data for gender
        #data_for_gender(data_dir_city)
        
        # plot data for usertype
        data_for_usertype(data_dir_city)
    
    """ data_dir = 'data/Washington'
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        df = pd.read_csv(file_path)
        cancel_column(df, file_path) """