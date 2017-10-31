#/usr/bin/env python

import sqlite3
from datetime import datetime
from pytz import timezone
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle

timezones = [timezone('Asia/Bangkok'),
             timezone('Asia/Shanghai'),
             timezone('America/Bogota'),
             timezone('America/Argentina/Buenos_Aires'),
             timezone('Africa/Cairo'),
             timezone('Asia/Calcutta'),
             timezone('Asia/Dhaka'),
             timezone('Asia/Shanghai'),
             timezone('Europe/Istanbul'),
             timezone('Asia/Jakarta'),
             timezone('Asia/Karachi'),
             timezone('Asia/Kolkata'),
             timezone('Africa/Lagos'),
             timezone('Europe/London'),
             timezone('US/Pacific'),
             timezone('Asia/Manila'),
             timezone('America/Mexico_City'),
             timezone('Asia/Kolkata'),
             timezone('US/Eastern'),
             timezone('Japan'),
             timezone('Brazil/West'),
             timezone('America/Sao_Paulo'),
             timezone('Asia/Seoul'),
             timezone('Asia/Shanghai'),
             timezone('Asia/Shanghai'),
             timezone('Japan'),
             timezone('Europe/Paris'),
             timezone('Europe/Berlin'),
             timezone('Europe/Madrid'),
             timezone('Europe/Kiev'),
             timezone('Europe/Rome'),
             timezone('Europe/Budapest'),
             timezone('Europe/Paris'),
             timezone('Europe/Sofia'),
             timezone('Africa/Nairobi'),
             timezone('Australia/Sydney'),
             timezone('Europe/Moscow'),
             timezone('Africa/Johannesburg'),
             timezone('America/Toronto'),
             timezone('America/Vancouver'),
             timezone('America/Chicago'),
             timezone('US/Central'),
             timezone('US/Pacific'),
             timezone('Asia/Singapore')]
colors = cycle(['r', 'b', 'g', 'c', 'm', 'y', 'k'])
markers = cycle(('o','^','v','s'))

def get_all_uploads(cursor):
    entries = cursor.execute("SELECT id,city_id,created_time FROM streetstyle27k")
    # create a dict of time bins
    num_bins = 24*7
    time_bins = defaultdict(list)
    gmt = timezone('GMT')
    for e in entries:
        if e[1] != '':
            # fetch local day and time for the city_id
            t = e[2][:-3]
            dt = datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
            dt_gmt = gmt.localize(dt)
            tz = timezones[e[1]-1]
            dt_local = dt_gmt.astimezone(tz)
            # compute the time as a frac week -- 0 is Monday midnight, 6 is Sunday midnight
            frac_week = (dt_local.weekday() + dt_local.hour/24.0 + dt_local.minute/(24.0*60.0) + dt_local.second/(24.0*60.0*60.0))/7.0
            # assign to weekly grid based on number of bins
            time_bins[int(num_bins*frac_week)].append(e[0])
    return [len(tb) for tb in time_bins.values()]

def main():
    # specify settings
    db_name = '../data/streetstyle27k.db'
    fields = ['neckline_shape','neckline_shape']
    values = ['\'Round\'','\'Folded\'']
    num_bins = 24*7
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # get total image uploads at time bins to normalize trends
    total = get_all_uploads(cursor)
    # loop over all fields
    gmt = timezone('GMT')
    for f,v,m,c in zip(fields,values,markers,colors):
        entries = cursor.execute("SELECT id,city_id,created_time FROM streetstyle27k WHERE " + f + " IS " + v)
        # create a dict of time bins
        time_bins = defaultdict(list)
        for e in entries:
            if e[1] != '':
                # fetch local day and time for the city_id
                t = e[2][:-3]
                dt = datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
                dt_gmt = gmt.localize(dt)
                tz = timezones[e[1]-1]
                dt_local = dt_gmt.astimezone(tz)
                # compute the time as a frac week -- 0 is Monday midnight, 6 is Sunday midnight
                frac_week = (dt_local.weekday() + dt_local.hour/24.0 + dt_local.minute/(24.0*60.0) + dt_local.second/(24.0*60.0*60.0))/7.0
                # assign to weekly grid based on number of bins
                time_bins[int(num_bins*frac_week)].append(e[0])
        # plot as fractional days to easily visualize daily trends
        x_vals = [tb/(num_bins/7.0) for tb in time_bins.keys()]
        normal_y_vals = [len(tb)/float(tot) for tb,tot in zip(time_bins.values(),total)]
        plt.plot(x_vals, normal_y_vals, c+m, label=v)
        z = np.poly1d(np.polyfit(np.array(x_vals), np.array(normal_y_vals),2))
        plt.plot(x_vals, [z(x) for x in x_vals], c)
    plt.grid(True)
    plt.xlabel('Day of week')
    plt.xticks(range(7), ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], rotation='vertical')
    plt.ylabel('Positive samples')
    plt.title('Round Neckline for Weekends')
    plt.legend(loc='upper left')
    plt.show()
    conn.close()

if __name__ == '__main__':
    main()
