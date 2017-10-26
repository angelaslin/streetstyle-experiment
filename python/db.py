#!/usr/bin/env python

import sqlite3

def fetch_entry(line):
    split = line.split(',')
    if len(split) == 25:
        # primary key is integer
        split[0] = int(split[0])
        # remove the newline
        split[-1] = split[-1][:-1]
        # generate a local url
        split[1] = '../data/streetstyle27k/' + split[1][33] + '/' + split[1][34] + '/' + split[1][35] + '/' + split[1][33:]
        return tuple(split)
    else:
        return None

def store_to_db(manifest_file, db_name):
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # build tables from schema
    cursor.executescript(database_schema)
    # fill the tables
    with open(manifest_file) as fid:
        # read first line as header, ignore
        fid.readline()
        # create a tuple entry for each line in manifest
        for line in fid:
            entry = fetch_entry(line)
            if entry is not None:
                cursor.execute("INSERT OR REPLACE INTO streetstyle27k VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                entry)
    conn.commit()
    conn.close()
    return

database_schema = """
                        CREATE TABLE IF NOT EXISTS streetstyle27k (
                                    id integer PRIMARY KEY,
                                    url TEXT,
                                    created_time TEXT,
                                    city_id TEXT,
                                    month_id TEXT,
                                    lat TEXT,
                                    lon TEXT,
                                    x1 TEXT,
                                    y1 TEXT,
                                    x2 TEXT,
                                    y2 TEXT,
                                    width TEXT,
                                    height TEXT,
                                    clothing_pattern TEXT,
                                    major_color TEXT,
                                    wearing_necktie TEXT,
                                    collar_presence TEXT,
                                    wearing_scarf TEXT,
                                    sleeve_length TEXT,
                                    neckline_shape TEXT,
                                    clothing_category TEXT,
                                    wearing_jacket TEXT,
                                    wearing_hat TEXT,
                                    wearing_glasses TEXT,
                                    multiple_layers TEXT
                                );
"""

def main():
    manifest_file = '../data/streetstyle27k.manifest'
    db_name = '../data/streetstyle27k.db'
    store_to_db(manifest_file, db_name)

if __name__ == '__main__':
    main()
