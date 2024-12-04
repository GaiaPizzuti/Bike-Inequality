from station_analysis import *
from social_mixing import *
from comparison_stations import *

city = sys.argv[1]

is_zipcode = False
is_mean = True
is_type = True

if not is_mean:
    
    if len(sys.argv) > 2:
        zipcode = str(sys.argv[2])
        is_zipcode = True
    
    df = get_mean_zipcode(city, zipcode)
    df = get_mean_all_zipcodes(city)

    plot_heatmap(df, city, zipcode=is_zipcode)

else:
    df = get_each_zipcode_mean(city)
    df = get_percentage_values(df)
    print(df)
    
    if is_type:
        type = sys.argv[2]
        plot_heatmap_on_map(df, type, city)
    else:
        plot_zipcode_heatmap(df, city)