#/usr/bin/env python

import sqlite3
import os.path
from shutil import copyfile

attributes_dict = {
    'wearing_jacket' : ['Yes', 'No'],
    'collar_presence' : ['Yes', 'No'],
    'wearing_scarf' : ['Yes', 'No'],
    'wearing_necktie' : ['Yes', 'No'],
    'wearing_hat' : ['Yes', 'No'],
    'wearing_glasses' :  ['Yes', 'No'],
    'multiple_layers' : ['One layer', 'Multiple layers'],
    'major_color' : ['Black', 'White', 'More than 1 color', 'Blue', 'Gray', 'Red', 'Pink', 'Green',
                     'Yellow', 'Brown', 'Purple', 'Orange', 'Cyan'],
    'clothing_category' : ['Shirt', 'Outerwear', 'T-shirt', 'Dress', 'Tank top', 'Suit', 'Sweater'],
    'sleeve_length' : ['Long sleeve', 'Short sleeve', 'No sleeve'],
    'neckline_shape' : ['Round', 'Folded', 'V-shape'],
    'clothing_pattern' : ['Solid', 'Graphics', 'Striped', 'Floral', 'Plaid', 'Spotted']
}

def get_examples():
    db_name = '../data/streetstyle27k.db'
    examples_path = '../data/examples'
    try:
        os.mkdir(examples_path)
    except OSError:
        pass
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "SELECT id, url FROM streetstyle27k WHERE {}=? LIMIT 10"
    for attribute, values in attributes_dict.iteritems():
        attribute_path = os.path.join(examples_path, attribute)
        try:
            os.mkdir(attribute_path)
        except OSError:
            pass
        for value in values:
            value_path = os.path.join(attribute_path, value)
            try:
                os.mkdir(value_path)
            except OSError:
                pass
            entries = cursor.execute(query.format(attribute), value)   
            for entry in entries:
                image_path = entry[1]
                image_id = entry[0]
                if image_id != '' and image_path != '':
                    root, ext = os.path.splitext(image_path)
                    cropped_image_path = root + '_cropped_' + str(image_id) + ext
                    copyfile(image_path, os.path.join(value_path, os.path.basename(image_path)))
                    copyfile(cropped_image_path, os.path.join(value_path, os.path.basename(cropped_image_path)))
    print("Done processing examples")

if __name__ == '__main__':
    get_examples()
