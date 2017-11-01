#/usr/bin/env python

import sqlite3
from PIL import Image
import os.path

def crop_image(image_id,image_path, x1, y1, x2, y2):
    im = Image.open(image_path)
    cropped = im.crop((x1, y1, x2, y2))
    root, ext = os.path.splitext(image_path)
    new_image_path = root + "_cropped_" + str(image_id) + ext
    cropped.save(new_image_path)
    im.close()
    cropped.close()

def crop_all_images():
    db_name = '../data/streetstyle27k.db'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # loop over all fields
    entries = cursor.execute("SELECT id, url, x1, y1, x2, y2 FROM streetstyle27k")
    for e in entries:
        if e[0] != '' and e[1] != '' and e[2] != '' and e[3] != '' and e[4] != '' and e[5] != '':
            crop_image(int(e[0]), e[1], int(e[2]), int(e[3]), int(e[4]), int(e[5]))
    print('Done')
    conn.close()

if __name__ == '__main__':
    crop_all_images()
