import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.interpolate import griddata


def main():
    contour_map()


def contour_map():
    # Read in data
    data = pd.read_csv(filepath_or_buffer='top_out.csv', header=None)
    data_size = len(data)

    # Get lat and lon bin vals
    lat = []
    lon = []
    for i in range(1,data_size, 28):
        lat.append(data.iloc[i,0])
    for i in range(1, 29):
        lon.append(data.iloc[i,1])

    # Create np array of z vals
    alt = np.empty((0,28), int)
    z_list = []
    start = 1
    end = 29
    for i in range(28):
        for j in range(start, end):
           z_list.append(data.iloc[j,2])
        alt = np.append(alt, np.array([z_list]), axis=0)
        start = end
        end+=28
        z_list.clear()
    # Create plot
    fig, ax = plt.subplots()
    ax.contourf(lon, lat, alt)
    plt.show()
    
    

def contour_test():
    df = pd.read_csv('test.csv', header=None)

    lon = df.iloc[0,1:]
    lat = df.iloc[1:,0]
    elv = df.iloc[1:,1:]
    levels = [600,650,700,750,800,850,900,950,1000,1050,1100,1200,1400]
    
    fig, ax = plt.subplots()
    ax.contourf(lon, lat, elv, levels)

    plt.show()

if __name__ == '__main__':
    main()