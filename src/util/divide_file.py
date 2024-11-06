import pandas as pd
import os
import numpy as np
import csv
from datetime import datetime

def get_date_format(city, year, month):
    year = int(year)
    month = int(month)
    if city == 'Austin':
        return '%m/%d/%Y %I:%M:%S %p'
    elif city == 'Boston':
        if year == 2018 and month < 3:
            return '%Y-%m-%d %H:%M:%S'
        else:
            return '%Y-%m-%d %H:%M:%S.%f'
    elif city == 'Chicago' or city == 'Columbus' or city == 'Washingtnon':
        return '%Y-%m-%d %H:%M:%S'
    elif city == 'NYC':
        if year <= 2020 or (year == 2021 and month <= 1):
            return '%Y-%m-%d %H:%M:%S.%f'
        return '%m/%d/%Y %H:%M:%S'
    elif city == 'Philly':
        if year == 2018 or (year == 2019 and month == 0) or (year == 2019 and month == 3) or (year == 2019 and month == 9):
            return '%Y-%m-%d %H:%M:%S'
        return '%m/%d/%Y %H:%M'
    elif city == 'SanFrancisco':
        if year < 2020 or (year == 2020 and month <= 4):
            return '%Y-%m-%d %H:%M:%S.%f'
        return '%Y-%m-%d %H:%M:%S'

def divide_file(full_path, folder):
    '''
    function to divide the file containing data of three month into three smaller files containing data of one month
    
    Input:
        - full_path: str, the path to the file containing data of three month
        - folder: str, the path to the folder containing the file
    '''
    
    df = pd.read_csv(full_path, dtype='object')
    
    year = folder.split('\\')[-1]
    city = folder.split('\\')[1]
    quarter = int(full_path.split('\\')[-1].split('.')[0][-1])
    
    start_month = (quarter - 1) * 3
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
    file_1 = year + months[start_month] + '.csv'
    file_2 = year + months[start_month + 1] + '.csv'
    file_3 = year + months[start_month + 2] + '.csv'
    
    with open(os.path.join(folder, file_3), 'w', newline='') as f, open(os.path.join(folder, file_2), 'w', newline='') as g, open(os.path.join(folder, file_1), 'w', newline='') as h:
        write1 = csv.writer(h)
        write1.writerow(df.columns)
        
        write2 = csv.writer(g)
        write2.writerow(df.columns)
        
        write3 = csv.writer(f)
        write3.writerow(df.columns)
        
        date_format = get_date_format(city, year, start_month)
        for index in range(len(df.index)):
            month = datetime.strptime(df.iloc[index]['stop_time'], date_format).month
            if df.iloc[index]['start_time'] != 'unknown':
                month_start = datetime.strptime(df.iloc[index]['start_time'], date_format).month
            else:
                month_start = -1
            if month == start_month + 1 and month_start == start_month + 1:
                write1.writerow(df.iloc[index])
            elif month == start_month + 2 and month_start == start_month + 2:
                write2.writerow(df.iloc[index])
            elif month == start_month + 3 and month_start == start_month + 3:
                write3.writerow(df.iloc[index])


if __name__ == '__main__':
    divide_file('data\\Philly\\2023\\2023Q3.csv', 'data\\Philly\\2023')
    print('done 3 2023')
    divide_file('data\\Philly\\2023\\2023Q4.csv', 'data\\Philly\\2023')
    print('done 4 2023')
