#/usr/bin/env python

import sqlite3
from datetime import datetime
from pytz import timezone
from collections import defaultdict
import matplotlib.pyplot as plt

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

def main():
    # specify settings
    db_name = '../data/streetstyle27k.db'
    fields = ['major_color','major_color']
    values = ['\'Black\'','\'White\'']
    markers = ['ro','go']
    num_bins = 24*7
    # open sqlite3 database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # loop over all fields
    gmt = timezone('GMT')
    for f,v,m in zip(fields,values,markers):
        entries = cursor.execute("SELECT id,city_id,created_time FROM streetstyle27k WHERE " + f + "=" + v)
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
                frac_week = (dt_local.weekday() + dt_local.hour/24.0)/7.0
                # assign to weekly grid based on number of bins
                time_bins[int(num_bins*frac_week)].append(e[0])
        # plot as fractional days to easily visualize daily trends
        plt.plot([tb/(num_bins/7.0) for tb in time_bins.keys()], [len(tb) for tb in time_bins.values()], m)
    plt.grid(True)
    plt.show()
    conn.close()

if __name__ == '__main__':
    main()
