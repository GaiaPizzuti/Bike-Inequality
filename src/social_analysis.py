import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def get_incomes(df, city, year):
    '''
    function to get the incomes from the social data and plot it into a bar charts
    '''
    
    estimates = list()
    margins = list()
    
    for i in range(1, 11):
        
        for type in ['household', 'family', 'married', 'nonfamily']:
            
            # obtain the value from the percentage
            estimate = float(df[type + '_estimates'][i][:-1])
            margin = float(df[type + '_margins'][i][1:-1])
            
            # append to the list
            estimates.append(estimate)
            margins.append(margin)
    
    # plot the data
    plt.figure(figsize=(10, 5))
    for i in range(4):
        plt.bar(np.arange(10) + i * 0.2, estimates[i * 10: (i + 1) * 10], width=0.2, label=['household', 'family', 'married', 'nonfamily'][i])
        plt.errorbar(np.arange(10) + i * 0.2, estimates[i * 10: (i + 1) * 10], yerr=margins[i * 10: (i + 1) * 10], fmt='o', color='black', capsize=5)
    plt.xticks(np.arange(10), ['<10k', '10-15k', '15-25k', '25-35k', '35-50k', '50-75k', '75-100k', '100-150k', '150-200k', '>200k'])
    plt.legend()
    plt.title(f'{city} incomes in {year}')
    plt.show()


if __name__ == '__main__':
    
    # load date
    data = 'data\\social'
    
    for city in os.listdir(data):
        print(city)
        
        # load city
        city_path = os.path.join(data, city)
        
        for year in os.listdir(city_path):
            
            # load year
            year_path = os.path.join(city_path, year)
            
            for file in os.listdir(year_path):
                
                # load file
                file_path = os.path.join(year_path, file)
                
                # read file
                df = pd.read_csv(file_path)
                
                # get incomes
                get_incomes(df, city, year)