import numpy as np
import networkx as nx
import operator
import matplotlib.pyplot as plt
from graphNetworkX import *
import itertools as it
import pandas as pd
import random

filepath = 'data/'

locations = pd.read_csv(filepath + 'location_csv.csv', delimiter=';', low_memory=False)
# locations = locations.drop(locations.columns[[5]], axis=1)

# with open(filepath + 'time_matrix.txt', 'r') as fobj:
#     times = [[num for num in it.islice(line.split(), 0, 50)] for line in it.islice(fobj, 0, 50)]
# times = np.array(times)

ls = locations.values[0:50]

nodes = []
for i in range(len(ls)-1):
    line = ls[i][0].split(',')
    nodes.append(Node(int(line[0]), int(line[0]), float(line[1]) ** 1.5 + (float(line[3]) * 15) ** 1.5, float(line[2])))
nodes[0] = Node(0,0,0,0)
ln.add_nodes_from(nodes)
time_limit = 200
t = 0
unused_nodes = set(nodes)
unused_nodes.remove(nodes[0])
prev = nodes[0] # Set first location to hotel

while True:
    new = random.sample(unused_nodes, 1)[0]

    if addTry(prev, new)[0] + t >= time_limit:
        break
    unused_nodes.remove(new)
    add(prev, new)
    t = nodes[0].tour_length
    print("Time is: " + str(int(t)), "Total risk is: " + str(int(nodes[0].tour_profit)))
    prev = new
    if len(unused_nodes) == 0:
        break
    plt.xlabel("Time is: " + str(int(t)) + "       Total risk is: " + str(int(nodes[0].tour_profit)))
    display()

display()
print(nodes[0].tour_length)
