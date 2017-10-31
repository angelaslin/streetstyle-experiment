#/usr/bin/env python

import sqlite3
import numpy as np
from sklearn.cluster import KMeans
from collections import defaultdict
import matplotlib.pyplot as plt

attributes = {}
attributes['clothing_pattern'] = ['Solid','Graphics','Striped','Floral','Plaid','Spotted','']
attributes['major_color'] = ['Black','White','More than 1 color','Blue','Gray','Red','Pink','Green','Yellow','Brown','Purple','Orange','Cyan','']
attributes['wearing_necktie'] = ['Yes','No','']
attributes['collar_presence'] = ['Yes','No','']
attributes['wearing_scarf'] = ['Yes','No','']
attributes['sleeve_length'] = ['Long sleeve','Short sleeve','No sleeve','']
attributes['neckline_shape'] = ['Round','Folded','V-shape','']
attributes['clothing_category'] = ['Shirt','Outerwear','T-shirt','Dress','Tank top','Suit','Sweater','']
attributes['wearing_jacket'] = ['Yes','No','']
attributes['wearing_hat'] = ['Yes','No','']
attributes['wearing_glasses'] = ['Yes','No','']
attributes['multiple_layers'] = ['One layer','Multiple layers']
markers = ['ro','go','bo','yo','co','r^','g^','b^','y^','c^','rv','gv','bv','yv','cv','rs','gs','bs','ys','cs']

def plot_location_cluster(locations,labels):
    for i,l in enumerate(labels):
        plt.plot(locations[i][1],locations[i][0],markers[l])
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def main():
    # specify settings
    db_name = '../data/streetstyle27k.db'
    city_id = 19
    num_clusters = 10
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # get all entries from a city
    entries = cursor.execute("SELECT lat,long FROM streetstyle27k WHERE city_id=" + repr(city_id))
    # get locations of all images
    locations = np.zeros((0,2))
    for e in entries:
        locations = np.concatenate((locations,np.array([e[0],e[1]]).reshape((1,2))))
    # cluster by location
    kmeans = KMeans(n_clusters=num_clusters).fit(locations)
    # generate a plot of location clusters
    plot_location_cluster(locations,list(kmeans.labels_))
    # get frequency of different attributes per cluster
    cluster_attributes = {}
    for a in attributes.keys():
        cluster_dict = defaultdict(list)
        entries = cursor.execute("SELECT id," + a + " FROM streetstyle27k WHERE city_id=" + repr(city_id))
        for e,l in zip(entries,list(kmeans.labels_)):
            # store as a tuple of image id and attribute value
            cluster_dict[l].append((e[0],e[1]))
        cluster_attributes[a] = cluster_dict
    conn.close()

if __name__ == '__main__':
    main()
