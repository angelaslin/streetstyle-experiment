#/usr/bin/env python

import sqlite3
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

attributes = {}
attributes['clothing_pattern'] = ['Solid','Graphics','Striped','Floral','Plaid','Spotted']
attributes['major_color'] = ['Black','White','More than 1 color','Blue','Gray','Red','Pink','Green','Yellow','Brown','Purple','Orange','Cyan']
attributes['wearing_necktie'] = ['Yes','No']
attributes['collar_presence'] = ['Yes','No']
attributes['wearing_scarf'] = ['Yes','No']
attributes['sleeve_length'] = ['Long sleeve','Short sleeve','No sleeve']
attributes['neckline_shape'] = ['Round','Folded','V-shape']
attributes['clothing_category'] = ['Shirt','Outerwear','T-shirt','Dress','Tank top','Suit','Sweater']
attributes['wearing_jacket'] = ['Yes','No']
attributes['wearing_hat'] = ['Yes','No']
attributes['wearing_glasses'] = ['Yes','No']
attributes['multiple_layers'] = ['One layer','Multiple layers']
markers = ['ro','go','bo','yo','co','r^','g^','b^','y^','c^','rv','gv','bv','yv','cv','rs','gs','bs','ys','cs']

def plot_location_cluster(locations,labels):
    for i,l in enumerate(labels):
        plt.plot(locations[i][1],locations[i][0],markers[l])
    plt.grid(True)
    plt.axis('equal')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Location Distribution of Uploads')

def plot_cluster_attributes(cluster_dict,attr):
    num_attr = len(attributes.get(attr))
    fig, ax = plt.subplots(nrows=1, ncols=2)
    for k in range(2):
        vals = [v[1] for v in cluster_dict.get(k)]
        total = float(len(vals))
        ax = plt.subplot(1, 2, k+1)
        for j,a in enumerate(attributes.get(attr)):
            num_instances = len([i for i,x in enumerate(vals) if x == a])
            plt.bar(j-0.5, num_instances/total, width=0.8, color=markers[k][:-1])
        plt.xticks(range(num_attr), attributes.get(attr), rotation='vertical')
        ax.set_ylim([0,0.4])
        plt.title('Total images in cluster: ' + repr(int(total)))
        plt.grid(True)
        plt.ylabel('Positive samples')

def cluster_by_location(locations,lat_range,lon_range):
    labels = []
    for i in range(locations.shape[0]):
        lat = locations[i,0]
        lon = locations[i,1]
        if lat_range[0] < lat < lat_range[1] and lon_range[0] < lon < lon_range[1]:
            labels.append(0)
        else:
            labels.append(1)
    return labels

def main():
    # specify settings
    db_name = '../data/streetstyle27k.db'
    city_id = 15
    attr = 'major_color'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # get all entries from a city
    entries = cursor.execute("SELECT lat,lon FROM streetstyle27k WHERE city_id=" + repr(city_id))
    # get locations of all images
    locations = np.zeros((0,2))
    for e in entries:
        locations = np.concatenate((locations,np.array([e[0],e[1]]).reshape((1,2))))
    # cluster by location
    labels = cluster_by_location(locations,[34.0,34.125],[-118.4,-118.2]) # LA
    # labels = cluster_by_location(locations,[40.7,40.8],[-74.015,-73.95]) # NYC
    # generate a plot of location clusters
    plot_location_cluster(locations,labels)
    # get frequency of different attributes per cluster
    cluster_dict = defaultdict(list)
    entries = cursor.execute("SELECT id," + attr + " FROM streetstyle27k WHERE city_id=" + repr(city_id))
    for e,l in zip(entries,list(labels)):
        # store as a tuple of image id and attribute value
        cluster_dict[l].append((e[0],e[1]))
    plot_cluster_attributes(cluster_dict,attr)
    plt.show()
    conn.close()

if __name__ == '__main__':
    main()
