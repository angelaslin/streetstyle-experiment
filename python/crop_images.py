#/usr/bin/env python

import sqlite3
from datetime import datetime
from pytz import timezone
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image
import os.path

def crop_image(image_path, x1, y1, x2, y2):
    im = Image.open(image_path)
    cropped = im.crop((x1, y1, x2, y2))
    root, ext = os.path.splitext(image_path)
    new_image_path = root + "_cropped" + ext
    cropped.save(new_image_path)
    im.close()
    cropped.close()

def crop_all_images():
    db_name = '../data/streetstyle27k.db'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # loop over all fields
    entries = cursor.execute("SELECT url, x1, y1, x2, y2 FROM streetstyle27k")
    for e in entries:
        if e[1] != '':
            crop_image(e[0], int(e[1]), int(e[2]), int(e[3]), int(e[4]))
	else:
            print("Hi")
    print('Done')
    conn.close()


if __name__ == '__main__':
    crop_all_images()
