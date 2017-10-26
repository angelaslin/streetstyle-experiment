#!/usr/bin/env python

import sqlite3
import simplekml

def fetch_by_city_id(city_id, cursor):
    # make the query
    return cursor.execute("SELECT * FROM streetstyle27k WHERE city_id=" + repr(city_id))

def write_kml(kml_name, positions):
    kml = simplekml.Kml()
    for p in positions:
        pnt = kml.newpoint(coords=[p])
        pnt.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png"
        pnt.style.iconstyle.scale = 0.5
    kml.save(kml_name)

def main():
    db_name = '../data/streetstyle27k.db'
    city_id = 15
    kml_name = '../results/kml_city_id_' + repr(city_id) + '.kml'
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    entries = fetch_by_city_id(city_id, cursor)
    positions = []
    for e in entries:
        positions.append((e[6],e[5]))
    write_kml(kml_name, positions)
    conn.close()

if __name__ == '__main__':
    main()
