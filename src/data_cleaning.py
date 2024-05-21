import numpy as np

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