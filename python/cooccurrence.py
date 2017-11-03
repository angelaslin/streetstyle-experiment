#/usr/bin/env python

import numpy as np
import os.path
import sqlite3
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
attributes = attributes_dict.keys()
total_entries = 27087

def get_cooccurrence_counts():
    db_name = '../data/streetstyle27k.db'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    query = "SELECT count() FROM streetstyle27k WHERE {}=? AND {}=?"
    cooccurrence_counts = dict()
    for attribute_index1 in range(len(attributes)):
        attribute1 = attributes[attribute_index1]
        cooccurrence_counts[attribute1] = dict()
        attribute1_dict = cooccurrence_counts[attribute1]
        for attribute_index2 in range(len(attributes)):
            if attribute_index1 == attribute_index2:
                continue
            attribute2 = attributes[attribute_index2]
            attribute1_dict[attribute2] = dict()
            attribute1_2_dict = attribute1_dict[attribute2]
            values1 = attributes_dict[attribute1]
            values2 = attributes_dict[attribute2]
            for value1 in values1:
                for value2 in values2:
                    entries = cursor.execute(query.format(attribute1, attribute2), (value1, value2))
                    count = 0
                    for entry in entries:
                        count = entry[0]
                    attribute1_2_dict[(value1, value2)] = count
    return cooccurrence_counts

def compute_highest_combo_counts(cooccurrence_counts):
    highest_combo_counts = []
    for attribute_index1 in range(len(attributes)):
        attribute1 = attributes[attribute_index1]
        for attribute_index2 in range(len(attributes)):
            if attribute_index1 == attribute_index2:
                continue
            attribute2 = attributes[attribute_index2]
            combo, count = filtered_max(cooccurrence_counts[attribute1][attribute2]) 
            highest_combo_counts.append((attribute1, attribute2, combo[0], combo[1], count))
    highest_combo_counts = sorted(highest_combo_counts, key=lambda x:x[4], reverse=True)
    return highest_combo_counts


def filtered_max(cooccurrence_dict):
    maximum_count = 0
    maximum_combination = None
    for value1, value2 in cooccurrence_dict:
        current_count = cooccurrence_dict[(value1, value2)]
        if current_count > maximum_count:
            maximum_combination = (value1, value2)
            maximum_count = current_count
    return maximum_combination, maximum_count

def normalize_counts(counts):
    normalized_counts = dict()
    for attribute_index1 in range(len(attributes)):
        attribute1 = attributes[attribute_index1]
        normalized_counts[attribute1] = dict()
        attribute1_dict = normalized_counts[attribute1]
        for attribute_index2 in range(len(attributes)):
            if attribute_index1 == attribute_index2:
                continue
            attribute2 = attributes[attribute_index2]
            attribute1_dict[attribute2] = dict()
            attribute1_2_dict = attribute1_dict[attribute2]
            for value1 in attributes_dict[attribute1]:
                attribute1_total = 0
                for value2 in attributes_dict[attribute2]:
                    current_count = counts[attribute1][attribute2][(value1, value2)]
                    attribute1_total += current_count
                    attribute1_2_dict[(value1, value2)] =  current_count / float(total_entries)
                probability_of_attribute1 = attribute1_total / float(total_entries)
                for value2 in attributes_dict[attribute2]:
                    attribute1_2_dict[(value1, value2)] =  attribute1_2_dict[(value1, value2)] / probability_of_attribute1
    return normalized_counts

if __name__ == '__main__':
    counts = get_cooccurrence_counts()
    normalized_counts = normalize_counts(counts)
    highest_combo_counts = compute_highest_combo_counts(normalized_counts)
    for entry in highest_combo_counts:
        attribute1, attribute2, value1, value2, probability = entry
        print("P({} = {} | {} = {}) = {}.".format(attribute2, value2, attribute1, value1, probability))
