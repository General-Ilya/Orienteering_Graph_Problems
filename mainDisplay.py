import numpy as np
import networkx as nx
import operator
import matplotlib.pyplot as plt
from graphNetworkX import *
import itertools as it
import pandas as pd
import random
import time

filepath = 'data/'

locations = pd.read_csv(filepath + 'location_csv.csv', delimiter=';', low_memory=False)
# locations = locations.drop(locations.columns[[5]], axis=1)

# with open(filepath + 'time_matrix.txt', 'r') as fobj:
#     times = [[num for num in it.islice(line.split(), 0, 50)] for line in it.islice(fobj, 0, 50)]
# times = np.array(times)
times = pd.read_pickle("topPickle").index.values
ln = nx.DiGraph()

ls=[]
for i in range(1,len(times)):
    ls.append(locations.values[times[i]])
# ls = locations.values[0:50]

nodes = [Node(0,0,0,0)]
# save  ** 1.5 + (float(line[3]) * 15) ** 1.5
for i in range(len(ls)-1):
    line = ls[i][0].split(',')
    nodes.append(Node(int(line[0]), i+1, float(line[1]), float(line[2])))

ln.add_nodes_from(nodes)
ln.add_node(Node("Hotel",0,0,0))
time_limit = 8

unused_nodes = set(nodes)
unused_nodes.remove(nodes[0])
used_nodes = set()
prev = nodes[0] # Set first location to hotel


def addFill(curr_time, max_tick):
    prev = nodes[0] if len(used_nodes) == 0 else random.sample(used_nodes, 1)[0]  # Set first location to hotel
    t = curr_time
    tick = 0
    while tick<max_tick:
        new = random.sample(unused_nodes, 1)[0]
        #print("Next move would cost: " + str(addTry(prev, new)[1]))
        if addTry(prev, new)[1] + t < time_limit:
            unused_nodes.remove(new)
            used_nodes.add(new)
            add(prev, new)
            t = nodes[0].tour_length
            print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)) + "      Expected dt: " +  str(addTry(prev, new)[1]))
            prev = new
            if len(unused_nodes) == 0:
                break
            plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
            #display(0.1)
            tick = 0

        tick += 1
    return t
def swapOptimal(max_tick):
    tick = 0
    t = 0
    while tick < max_tick:
        first = random.sample(used_nodes, 1)[0]
        second = random.sample(used_nodes.difference(set([first])), 1)[0]
        if first is nodes[0] or second is nodes[0]:
            raise Exception("No")
        if swapTry(first, second)[1] < 0 and swapTry(first, second)[0] >= 0:
            swap(first, second)
            t = nodes[0].tour_length
            print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
            plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
            #display(0.1)
            tick = 0
        tick += 1
    t = nodes[0].tour_length
    return t

def switchOptimal(max_tick):
    tick = 0
    t = 0
    while tick < max_tick:
        first = random.sample(used_nodes, 1)[0]
        second = random.sample(unused_nodes, 1)[0]

        if switchTry(first, second)[1] < 0 and switchTry(first, second)[0] >= 0:
            used_nodes.remove(first)
            unused_nodes.add(first)
            unused_nodes.remove(second)
            used_nodes.add(second)
            switch(first, second)

            t = nodes[0].tour_length
            print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
            plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
            #display(0.1)
            tick = 0
        tick += 1
    t = nodes[0].tour_length
    return t

def swapRandom(max_tick):
    tick = 0
    t = 0
    while tick < max_tick:
        first = random.sample(used_nodes, 1)[0]
        second = random.sample(used_nodes.difference(set([first])), 1)[0]
        swap(first, second)
        t = nodes[0].tour_length
        print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
        plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
        #display(0.1)
        tick += 1
    t = nodes[0].tour_length
    return t

def switchRandom(max_tick):
    tick = 0
    t = 0
    while tick < max_tick:
        first = random.sample(used_nodes, 1)[0]
        second = random.sample(unused_nodes, 1)[0]
        used_nodes.remove(first)
        unused_nodes.add(first)
        unused_nodes.remove(second)
        used_nodes.add(second)
        switch(first, second)

        t = nodes[0].tour_length
        print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
        plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
        #display(0.1)
        tick += 1
    t = nodes[0].tour_length
    return t


tt = [0]
rt = [0]
term = 0
for j in range(10):
    for i in range(10):
        term = addFill(term, 10000)
        tt.append(term)
        rt.append(nodes[0].tour_profit)
        term = swapOptimal(10000)
        tt.append(term)
        rt.append(nodes[0].tour_profit)
        term = switchOptimal(10000)
        tt.append(term)
        rt.append(nodes[0].tour_profit)
    swapRandom(2)
    switchRandom(2)
term = addFill(term, 10000)
tt.append(term)
rt.append(nodes[0].tour_profit)
term = swapOptimal(10000)
tt.append(term)
rt.append(nodes[0].tour_profit)
term = switchOptimal(10000)
tt.append(term)
rt.append(nodes[0].tour_profit)
term = addFill(term, 10000)
tt.append(term)
rt.append(nodes[0].tour_profit)

plt.title("FINAL GRAPH")
plt.xlabel("Time is: " + str(round(term, 2)) + "       Total risk is: " + str(round(nodes[0].tour_profit, 2)))
display(0.5, True)
print(nodes[0].tour_length)

plt.clf()
plt.plot(tt)
plt.plot(rt)
plt.show()