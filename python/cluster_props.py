#/usr/bin/env python

import sqlite3
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from pdb import set_trace

def main():
    # specify settings
    db_name = '../data/streetstyle27k.db'
    city_id = 19
    num_clusters = 10
    markers = ['ro','go','bo','yo','co','r^','g^','b^','y^','c^','rv','gv','bv','yv','cv','rs','gs','bs','ys','cs']
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # get all entries from a city
    entries = cursor.execute("SELECT * FROM streetstyle27k WHERE city_id=" + repr(city_id))
    # get locations of all images
    locations = np.zeros((0,2))
    for e in entries:
        locations = np.concatenate((locations,np.array([e[5],e[6]]).reshape((1,2))))
    # cluster by location
    kmeans = KMeans(n_clusters=num_clusters).fit(locations)
    # TODO plot frequency of different attributes per cluster
    # plot clusters
    for i,l in enumerate(kmeans.labels_):
        plt.plot(locations[i][1],locations[i][0],markers[l])
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    conn.close()

if __name__ == '__main__':
    main()
