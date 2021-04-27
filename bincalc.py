import pandas as pd
import csv
import googlemaps
import config
import requests
import json
import urllib.request


def main():
    get_elv()
    

def elev_response(latitude, longitude):
    ''' 
    Retrieves the elevation data from Google Maps Elevation API json object
        @params: 
            latitude(float), longitude(float)
        @return:
            Returns elevation for the specified coordinates
    '''

    # Build url for API call
    ELEVATION_BASE_URL = 'https://maps.google.com/maps/api/elevation/json'
    URL_PARAMS = "locations={lat},{lon}&key={key}".format(lat=latitude, lon=longitude, key=config.ELEV_API_KEY)
    url = ELEVATION_BASE_URL + "?" + URL_PARAMS

    # Read the contents of the generated url and decode the result
    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode())
    status = response["status"]
    if status == "OK":
        result = response["results"][0]
        elevation_data = float(result["elevation"])
    else:
        elevation_data = None
    return elevation_data


def get_elv():
    ''' 
    Retrieves elevation data based off bin generated lat/lon data
    and writes to file
        @return:
            elev_data(DataFrame): Data Frame object that is written to file
    '''

    # Read bin values from file
    bin_data = pd.read_csv(filepath_or_buffer='top.csv')
    bin_size = len(bin_data)

    # Initialize list values
    lat_list = []
    lon_list = []
    elev_list = []

    # Make api calls and parse for elevation data
    for i in range(bin_size):
        lat = bin_data.iloc[i][0]
        lon = bin_data.iloc[i][1]
        elevation = elev_response(latitude=lat, longitude=lon)
        lat_list.append(lat)
        lon_list.append(lon)
        elev_list.append(elevation)
        
    # Add list values to a new dataframe
    elev_data = pd.DataFrame(data=None, columns=['Latitude', 'Longitude', 'Elevation'])
    elev_data['Latitude'] = lat_list
    elev_data['Longitude'] = lon_list
    elev_data['Elevation'] = elev_list
    elev_data.to_csv(path_or_buf='top_out.csv', index=False)
    return elev_data


def generate_points():
    ''' 
    Generates lat/lon bins based off various conversion factors
    In this case, it creates 28 quarter nautical mile bins
    '''

    # Conversion factors
    NM2STAT = 1.15078
    NMDEGLONG92 = 42.70
    NMDEGLAT = 60.00

    # Increments
    LONINC = (0.25* NM2STAT / NMDEGLONG92) # ~0.0067
    LATINC = (0.25 * NM2STAT / NMDEGLAT)   # ~0.00479

    # Starting pos for lat and lon
    START_LAT = 44.48 # 15 pt diff
    END_LAT = 44.61
    START_LON = -92.63
    END_LON = -92.44

    # Iterators and Lists
    lat = START_LAT
    lon = START_LON
    lat_list = []
    lon_list = []
    i = 0
    j = 0

    # Creates a 27 x 27 table
    while (lat <= END_LAT and i <= 27):
        while (lon <= END_LON and j <= 27):
            #print('lat: {} lon: {}\n'.format(lat,lon))
            lon_list.append(lon)
            lat_list.append(lat)
            lon += LONINC
            j+=1
        lat += LATINC
        lon = START_LON
        j=0
        i+=1
    # Create data frame and write to file
    df = pd.DataFrame(data=None, columns=['Lat','Lon'])
    df['Lat'] = lat_list
    df['Lon'] = lon_list
    df.to_csv(path_or_buf='top2.csv', index=False)


if __name__ == '__main__':
    main()