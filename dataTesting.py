import numpy as np
import scipy
import random
import math
import pandas as pd
import itertools as it
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import seaborn as sns
import string
import networkx as nx

filepath = 'data/'

locations = pd.read_csv(filepath + 'location_csv.csv', delimiter=';', low_memory=False)
#locations = locations.drop(locations.columns[[5]], axis=1)

with open(filepath + 'distance_matrix.txt', 'r') as fobj:
    distances = [[num for num in it.islice(line.split(), 4674, 7530)] for line in it.islice(fobj, 0, 4674)]
distance = np.array(distances)

# with open(filepath + 'time_matrix.txt', 'r') as fobj:
#     times = [[num for num in line.split()] for line in fobj]
# time = np.array(times)

# distance = pd.DataFrame(distance)
# time = pd.DataFrame(time)
minDistance = np.zeros(2857)
minDict = {}
for num, row in enumerate(distance):
    #row = rowRaw.copy()
    #row = np.append(row[0:num], row[num+1:])
    minCity = np.argmin(row)
    minDistance[minCity] = minDistance[minCity] + 1
    minDict[num] = minCity

plt.plot(minDistance)
plt.show()
print(np.count_nonzero(minDistance))

