# Bike-Inequality
This project aims to delve into the evolution of BSS across five major US cities, analysing their development trajectories and underlying policies to unearth their impact on social inclusivity.

## Technologies used
- Programming Languages: Python
- Libraries: Pandas, NumPy, Matplotlib, geopandas, shapely
- Tools: Jupyter Notebook
- Data Sources:
    [NYC Bikes](https://citibikenyc.com/system-data)
    [Boston Bikes](https://bluebikes.com/system-data)
    [Washington DC](https://capitalbikeshare.com/system-data)
    [San Francisco Bikes](https://www.lyft.com/bikes/bay-wheels/system-data)
    [Columbus Bikes](https://cogobikeshare.com/system-data)
    [Austin Bikes](https://data.austintexas.gov/Transportation-and-Mobility/Austin-MetroBike-Trips/tyfh-5r8s/about_data)
    [Chicago Bikes](https://divvybikes.com/system-data)
    [Philadelphia Bikes](https://www.rideindego.com/about/data/ )
    [US Census](https://www.census.gov/data/developers/data-sets/acs-5year.html)

### Prerequisites
pip install -r requirements.txt

### Repository Structure

├── data/
│   ├── bikes/                      # Bikes usage data
│   ├── destinations/               # SMI calculated for social type after the movement
│   ├── differences/                # difference SMI calculated for social type
│   ├── filtered_destinations/      # SMI calculated for social type after the movement (filtered: removed turists trips)
│   ├── filtered_trips/             # trips data (filtered: removed turists trips)
│   ├── indedes/                    # SMI calculated for social type
│   ├── osm/                        # OpenStreetMap data
│   ├── self_loops/                 # Self Loop data
│   ├── social/                     # Social data (gender, age, income and race)
│   ├── stations/                   # Station usage data
│   └── trips/                      # Trips data
│
├── scr/
│   ├── notebook/    
│       ├── general_trip_analysis.py       # Trips Analysis (seasons, day, year)
│       ├── pearson.py                     # Pearson Correlation Analysis
│       ├── social_mixing.py               # Social Mixing Analysis
│       ├── social.py                      # Social Analysis (gender, age, income and race)
│       ├── trips_analysis.py              # Trips Analysis over the years
│       ├── trips_zones.py                 # Trips Analysis based on the zipcode
│       ├── turism_analysis.py             # Trips made by turists
│       ├── zip_analysis.py                # Social analysis based on the zipcode
│   ├── util/
│       ├── create_destination_file.py     # script for the destination folder
│       ├── create_difference_file.py      # script for the difference folder
│       ├── create_self_loop_file.py       # script for the self_loops folder
│       ├── create_station_file.py         # script for the station folder
│       ├── create_trips_file.py           # script for the trips folder
│       ├── data_cleaning.py               # script for data's initial cleaning
│       └── divide_file.py                 # script for dividing the bikes file into months
│
├── .gitignore
├── requirements.txt
└── README.md
