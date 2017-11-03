#/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pylab as pylab
params = {'legend.fontsize': 'x-large',
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}
pylab.rcParams.update(params)

IOU = np.load("IOU.npy")
print(np.max(IOU), np.min(IOU))
n, bins, patches = plt.hist(IOU)
plt.title("IOU for Duplicate Pairs")
plt.xlabel("IOU")
plt.ylabel("Number of Duplicate Pairs")
plt.show()

counts = np.load("counts.npy")
print(np.max(counts), np.min(counts))
n, bins, patches = plt.hist(counts, 3)
plt.title("Counts for Duplicate Pairs")
plt.xlabel("Counts")
plt.ylabel("Number of Duplicate Pairs")
plt.xticks(range(2, 5))
plt.show()