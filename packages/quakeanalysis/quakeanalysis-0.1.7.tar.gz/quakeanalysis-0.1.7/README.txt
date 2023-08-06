This is prototype to analyse earthquake data from 

https://earthquake.usgs.gov/

https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php



enter a place name to get distance from nearest earthquake

earthquake_distance('place')


enter a place name to get time of nearest earthquake

earthquake_time('place')

enter a place name to get place of nearest earthquake

earthquake_place('place')

enter a place name to get longitude of nearest earthquake

earthquake_longitude('place')

enter a place name to get latitude of nearest earthquake

earthquake_latitude('place')


get the magnitude of nearest earthquake

earthquake_magnitude('place')


To get dataframe list of all recent earthquakes and their distance from place

earthquake_df('place')


To get dataframe list of all recent earthquakes and their distance from place, where distance less than 5000
earthquake_less_than('Tokyo', 5000)

Check out how to use this library

https://betterprogramming.pub/python-library-for-finding-nearest-earthquake-8c96f97c9ddb

https://github.com/g00387822/quakeanalysis