import numpy as np
import pandas as pd
import itertools as it

filepath = 'data/'

locations = pd.read_csv(filepath + 'location_csv.csv', delimiter=';', low_memory=False)
#locations = locations.drop(locations.columns[[5]], axis=1)

with open(filepath + 'time_matrix.txt', 'r') as fobj:
    times = [[num for num in it.islice(line.split(), 0, 4674)] for line in it.islice(fobj, 4674, 7530)]
time = np.array(times)