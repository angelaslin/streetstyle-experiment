#/usr/bin/env python

import sqlite3
from PIL import Image
import os.path
import numpy as np

def compute_area(x1, y1, x2, y2):
    if x2 < x1:
         return 0
    elif y2 < y1:
         return 0
    return (x2 - x1) * (y2 - y1)

def compute_IOU(a_x1, a_y1, a_x2, a_y2, b_x1, b_y1, b_x2, b_y2):
    intersection = compute_area(max(a_x1, b_x1), max(a_y1, b_y1), min(a_x2, b_x2), min(a_y2, b_y2))
    area_a = compute_area(a_x1, a_y1, a_x2, a_y2)
    area_b = compute_area(b_x1, b_y1, b_x2, b_y2)
    union = area_a + area_b - intersection
    if union == 0:
        return 0
    IOU = intersection / float(union)
    return IOU

def count_unique_images():
    db_name = '../data/streetstyle27k.db'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # loop over all fields
    entries = cursor.execute("SELECT COUNT(DISTINCT url) FROM streetstyle27k")
    for e in entries:
        print("The total number of distinct entries is {}.".format(e[0]))
    duplicate_counts = dict()
    entries = cursor.execute("SELECT url, COUNT(*) FROM streetstyle27k GROUP BY url HAVING COUNT(*) > 1")
    for e in entries:
        if e[0] != '' and e[1] != '':
            duplicate_counts[e[0]] = int(e[1])
    entries = cursor.execute("SELECT a.id, a.x1, a.y1, a.x2, a.y2, a.url " + 
        "FROM streetstyle27k AS a " + 
        "JOIN ( SELECT url " + 
                "FROM streetstyle27k " + 
                "GROUP BY url " +
               "HAVING COUNT(*) > 1) AS b " +
          "ON a.url = b.url ORDER BY a.url")
    print("Total number of images with duplicates is {}.".format(len(duplicate_counts.keys())))
    np.save("counts.npy", duplicate_counts.values())    
    print("Mean number of duplicates: {}, Standard deviation: {}".format(np.mean(duplicate_counts.values()), np.std(duplicate_counts.values())))
    duplicates = dict()
    for e in entries:
        x1, y1, x2, y2, url = int(e[1]), int(e[2]), int(e[3]), int(e[4]), e[5]
        if url in duplicates:
            duplicates[url].append((x1, y1, x2, y2))
        else:
            duplicates[url] = [(x1, y1, x2, y2)]
    IOU = []
    for url in duplicates:
        bounding_boxes = duplicates[url]
        for i in range(len(bounding_boxes)):
            for j in range(i + 1, len(bounding_boxes)):
                a_x1, a_y1, a_x2, a_y2 = bounding_boxes[i]
                b_x1, b_y1, b_x2, b_y2 = bounding_boxes[j]
                IOU.append(compute_IOU(a_x1, a_y1, a_x2, a_y2, b_x1, b_y1, b_x2, b_y2))
    np.save("IOU.npy", IOU)    
    conn.close()
    return duplicates

if __name__ == '__main__':
    count_unique_images()
