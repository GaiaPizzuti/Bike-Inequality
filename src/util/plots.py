import matplotlib.pyplot as plt
import numpy as np

def plot_indexes_per_types(indexes):
    """
    Function to plot the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    X = np.random.randn(1000, 6)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    
    fig, ax = plt.subplots(2, 3, sharex=True, sharey=True)
    # make a hist plot to represent how the data is distributed
    for index, (key, values) in enumerate(indexes.items()):
        ax[index // 3, index % 3].hist(values, bins=10, histtype='bar', color=colors[index % 6])
        ax[index // 3, index % 3].set_title(key)
    
    # add the title to the plot
    fig.suptitle('SMI Distribution')
    # add x and y labels
    fig.supxlabel('Social Mixing Index')
    fig.supylabel('Frequency')
    plt.show()

def subplot_indexes_per_types(indexes, type=None):
    """
    Function to plot the social mixing index of a specific location and for each type of data.

    Args:
        indexes (dict): dictionary with the indexes of a specific type of data from each city
    """
    
    X = np.random.randn(1000, 8)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    
    fig, ax = plt.subplots(2, 4, sharex=True, sharey=True)
    
    fig.delaxes(ax[1, 3])
    # make a hist plot to represent how the data is distributed
    for index, (key, values) in enumerate(indexes.items()):
            ax[index // 4, index % 4].hist(values, bins=20, histtype='bar', color=colors[index % 8])
            ax[index // 4, index % 4].set_title(key)
    
    # add the title to the plot
    if type:
        fig.suptitle('SMI Distribution for ' + type)
    else:
        fig.suptitle('SMI Distribution')
    # add x and y labels
    fig.supxlabel('Social Mixing Index')
    fig.supylabel('Frequency')
    plt.show()

def plot_density_indexes(indexes, type=None):
    """
    Function to plot the social mixing index of a specific location and for each type of data.
    
    Input:
        - indexes: list containing the Social Distancing Index (SDI) for each type
    """
    
    import seaborn as sns
    
    sns.displot(indexes, kind='kde')
    
    if type:
        plt.title('SMI Density Plot for ' + type)
    else:
        plt.title('SMI Density Plot')
    plt.xlabel('Social Mixing Index')
    plt.ylabel('Density')
    
    plt.show()
    
def plot_stations_indexes(bikes_indexes):
    """
    Function to plot the distribution of bike stations with a specific social mixing index.
    
    Input:
        - bikes_indexes: dict indicating the number of stations with a specific social mixing index
    """
    
    X = np.random.randn(1000, 8)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    
    # create a subplot for each type of data
    fig, ax = plt.subplots(2, 3, sharey=True)
    
    for index, (key, values) in enumerate(bikes_indexes.items()):
        ax[index // 3, index % 3].hist(values.keys(), bins=10, histtype='bar', color=colors[index % 8])
        ax[index // 3, index % 3].set_title(key)
    
    fig.suptitle('Bike Stations Social Mixing Index')
    fig.supxlabel('Social Mixing Index')
    fig.supylabel('Number of Stations')
    
    plt.show()

def plot_stations_differences(differences, city):
    """
    Function to plot the differences between the stations' indexes

    Args:
        differences (list): list of differences between the stations' indexes
    """
    
    X = np.random.randn(1000, 8)
    cmap = plt.get_cmap('viridis')
    colors = cmap([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    
    # create a subplot for each type of data
    fig, ax = plt.subplots(2, 3, sharey=True)
    
    for index, (key, values) in enumerate(differences.items()):
        ax[index // 3, index % 3].hist(values.keys(), bins=20, histtype='bar', color=colors[index % 8])
        ax[index // 3, index % 3].set_title(key)
    
    fig.suptitle('Differences between Trips Indexes in ' + city)
    fig.supxlabel('Index Difference')
    fig.supylabel('Number of Trips')
    
    
    plt.show()    

def plot_heatmap(df, city, zipcode):
    """
    Function to plot the heatmap of the social mixing index for the city's stations
    
    Input:
        - city: string with the city name
    """
    import seaborn as sns
    
    colors = sns.color_palette("viridis", as_cmap=True)
    
    # get the columns with the indexes
    indexes = df.columns[2:]
    
    # create a heatmap with the indexes
    annotation = False
    if zipcode:
        annotation = True
    sns.heatmap(df[indexes], cmap=colors, yticklabels=df['station'], annot=annotation, fmt=".2f", linewidths=.5, linecolor='black')
    plt.suptitle('Social Mixing Index for ' + city)
    if zipcode:
        plt.title('Zipcode: ' + df['zipcode'].iloc[0])
    plt.xlabel('Index Type')
    plt.ylabel('Station')
    plt.show()

def plot_zipcode_heatmap(df, city):
    """
    Function to plot the heatmap of the social mixing index for the city's stations
    
    Input:
        - city: string with the city name
    """
    import seaborn as sns
    
    colors = sns.color_palette("viridis", as_cmap=True)
    
    # get the columns with the indexes
    indexes = df.columns[1:]
    
    # create a heatmap with the indexes
    sns.heatmap(df[indexes], cmap=colors, yticklabels=df['zipcode'], annot=False, fmt=".2f", linewidths=.5, linecolor='black')
    plt.title('Social Mixing Index for ' + city)
    plt.xlabel('Index Type')
    plt.ylabel('Station')
    plt.show()