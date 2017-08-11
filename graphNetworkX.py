import numpy as np
import networkx as nx
import operator
import matplotlib.pyplot as plt
import operator
import itertools as it
import pandas as pd
import pickle
from time import sleep
# filepath = 'data/'
# with open(filepath + 'time_matrix.txt', 'r') as fobj:
#     times = [[num for num in it.islice(line.split(), 0, 50)] for line in it.islice(fobj, 0, 50)]
# times = np.array(times)
times = np.load("top.npy")
ln = nx.DiGraph()
# information_file = 'data/location_csv.csv'
# time_matrix = 'data/time_matrix.txt'
#
# infos = pd.read_csv(information_file, delimiter=';', low_memory = False)
# with open('data/distance_matrix.txt', 'r') as fobj:
#     distances = [[float(num) for num in line.split()] for line in fobj]
# distance=np.array(distances)
# distance = pd.DataFrame(distance)
#
# with open(time_matrix, 'r') as fobj:
#     times = [[float(num) for num in line.split()] for line in fobj]
# time_matrix=np.array(times)
# time_matrix = pd.DataFrame(time_matrix)
#
# #Separate the three matrices of interest
# index = 4673
# locations_time = time_matrix.iloc[0:index,0:index]
# cities_time = time_matrix.iloc[0:index,index:len(time_matrix)]
# cities_locations = time_matrix.iloc[index:,0:index]
# index = 4673
# locations_time = time_matrix.iloc[0:index,0:index]
# cities_time = time_matrix.iloc[0:index,index:len(time_matrix)]
# cities_locations = time_matrix.iloc[index:,0:index]
# argmins = []
# time_close = []
# for i in range(0,cities_time.shape[0]-1):
#     argmins.append(cities_time.iloc[i,:].argmin()-index)
#     time_close.append(cities_time.iloc[i,argmins[i]])
#
# closest = distance.iloc[0:len(argmins),0:3]
# for i in range(0,cities_time.shape[0]-1):
#     closest.iloc[i,0]=int(cities_time.iloc[i,:].argmin()-index)
#     closest.iloc[i,1]=cities_time.iloc[i,argmins[i]]
#     closest.iloc[i,2] = i
# closest.columns = ['closest city', 'time', 'location']
# closest = closest[['location', 'closest city', 'time']]
#
# #get rid of all cities not assigned to a location
# final_cities=closest.iloc[:,1].unique()
#
#
# locpercity_less5 = []
# for j in range(0,len(final_cities)):
#     locpercity_less5.append([])
# for j in range(0,len(final_cities)):
#     locpercity_less5[j] = np.where(cities_locations.iloc[int(final_cities[j]),:]<4)[0]
# j = 5
# city_index = final_cities[j]
# print('ville no: ',city_index+index)
# liste = []
# liste = np.append(city_index+index,locpercity_less5[j])
# print('nb de locations:  ',len(liste)-1)
# top = time_matrix.iloc[np.append(city_index+index,locpercity_less5[j]),np.append(city_index+index,locpercity_less5[j])]
#
# top.to_pickle("topPickle")
# top.to_pickle("topPickles.pkl")



class Node(object):
    def __init__(self, name, index, risk_score, service_time):
        self.name = name
        self.index = index
        self.risk_score = risk_score
        self.service_time = service_time
        self.tour_length = 0
        self.tour_profit = 0


def prev(node):
    ln.add_node(node)
    return ln.predecessors(node)[0] if len(ln.predecessors(node)) is 1 else None


def next(node):
    ln.add_node(node)
    return ln.successors(node)[0] if len(ln.successors(node)) is 1 else None


def addTry(node_first, node_second=None):
    if node_second is None:
        return [0, 0]
    if next(node_first) is None:
        ori = [node_first]
        new = [node_first, node_second, node_first]
    else:
        ori = [prev(node_first), node_first, next(node_first)]
        new = [prev(node_first), node_first, node_second, next(node_first)]
    return evaluateDifference(ori, new)


def add(node_first, node_second=None):  # Node second added after node first
    if len(ln.successors(node_first)) == 0:
        ln.add_edge(node_second, node_first, weight=time(node_second, node_first))
        ln.add_edge(node_first, node_second, weight=time(node_first, node_second))
    else:
        b = next(node_first)
        ln.add_edge(node_first, node_second, weight=time(node_first, node_second))
        ln.add_edge(node_second, b, weight=time(node_second, b))
        ln.remove_edge(node_first, b)
    evaluateTourTime(node_first)
    evaluateTourProfit(node_first)


def swapTry(old_node, new_node):
    # Special case if they're adjacent
    if next(old_node) is new_node:
        ori = [prev(old_node), old_node, new_node, next(new_node)]
        new = [prev(old_node), new_node, old_node, next(new_node)]
        return evaluateDifference(ori, new)
    elif next(new_node) is old_node:
        ori = [prev(new_node), new_node, old_node, next(old_node)]
        new = [prev(new_node), old_node, new_node, next(old_node)]
        return evaluateDifference(ori, new)

    orig1 = [prev(old_node), old_node, next(old_node)]
    new1 = [prev(old_node), new_node, next(old_node)]
    orig2 = [prev(new_node), new_node, next(new_node)]
    new2 = [prev(new_node), old_node, next(new_node)]
    d1 = evaluateDifference(orig1, new1)
    d2 = evaluateDifference(orig2, new2)
    return [d1[0] + d2[0], d1[1] + d2[1]]


def swap(old_node, new_node):
    o1 = prev(old_node)
    o2 = next(old_node)
    n1 = prev(new_node)
    n2 = next(new_node)
    if o2 is new_node:
        ln.remove_edges_from([(o1, old_node), (old_node, o2), (o2, n2)])
        ln.add_edge(o1, new_node, weight=time(o1, new_node))
        ln.add_edge(new_node, old_node, weight=time(new_node, old_node))
        ln.add_edge(old_node, n2, weight=time(old_node, n2))

    elif n2 is old_node:
        ln.remove_edges_from([(n1, new_node), (new_node, n2), (n2, o2)])
        ln.add_edge(n1, n2, weight=time(n1, n2))
        ln.add_edge(n2, new_node, weight=time(n2, new_node))
        ln.add_edge(new_node, o2, weight=time(new_node, o2))

    else:
        ln.remove_edges_from([(o1, old_node), (old_node, o2)])
        ln.remove_edges_from([(n1, new_node), (new_node, n2)])
        ln.add_edge(o1, new_node, weight=time(o1, new_node))
        ln.add_edge(new_node, o2, weight=time(new_node, o2))
        ln.add_edge(n1, old_node, weight=time(n1, old_node))
        ln.add_edge(old_node, n2, weight=time(old_node, n2))
        evaluateTourProfit(old_node)
        evaluateTourTime(old_node)

    evaluateTourProfit(new_node)
    evaluateTourTime(new_node)


def switchTry(old_node, new_node):
    orig = [prev(old_node), old_node, next(old_node)]
    new = [prev(old_node), new_node, next(old_node)]
    return evaluateDifference(orig, new)


def switch(old_node, new_node):
    o1 = prev(old_node)
    o2 = next(old_node)
    ln.remove_edges_from([(o1, old_node), (old_node, o2)])
    ln.add_edge(o1, new_node, weight=time(o1, new_node))
    ln.add_edge(new_node, o2, weight=time(new_node, o2))
    evaluateTourProfit(new_node)
    evaluateTourTime(new_node)


def evaluateTourProfit(node):
    tour_profit_total = 0
    curr = node
    while True:
        if next(curr) is None:
            return
        tour_profit_total += curr.risk_score
        curr = next(curr)
        if curr is node:
            break

    curr = node
    while True:
        curr.tour_profit = tour_profit_total
        curr = next(curr)
        if curr is node:
            break


def evaluateTourTime(node):
    tour_length_total = 0
    curr = node
    while True:
        if next(curr) is None:
            return
        tour_length_total += curr.service_time
        s = next(curr)
        tour_length_total += float(ln.get_edge_data(curr, next(curr))["weight"])
        curr = next(curr)
        if curr is node:
            break

    curr = node
    while True:
        curr.tour_length = tour_length_total
        curr = next(curr)
        if curr is node:
            break


# Returns array of [Difference in profit if done, Difference in time if done] for a move
def evaluateDifference(nodes_old, nodes_new):
    dt = evaluatePathTime(nodes_new) - evaluatePathTime(nodes_old)
    dp = evaluatePathProfit(nodes_new) - evaluatePathProfit(nodes_old)
    return [dp, dt]


def evaluatePathTime(nodes):
    path_length = 0
    for i in range(len(nodes) - 1):
        path_length += float(nodes[i].service_time)
        path_length += float(time(nodes[i], nodes[i + 1]))
    path_length += nodes[-1].service_time
    return path_length


def evaluatePathProfit(nodes):
    path_profit = 0
    for node in nodes:
        path_profit += node.risk_score
    return path_profit


def time(node_first, node_second):
    t = times[node_first.index][node_second.index]
    return t


def printGraph(t, n):
    print("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(n.tour_profit, 2)))
    plt.xlabel("Time is: " + str(round(t, 2)) + "       Total risk is: " + str(round(n.tour_profit, 2)))
    # display(0.1)

def display(interval, hold=False):
    G = ln
    pos = nx.fruchterman_reingold_layout(G, scale=1000, center=[0,0])
    labels = {}
    n = sorted(G.nodes(), key=operator.attrgetter('index'))
    l = [i.name if int(i.name) > 0 else "Hotel" for i in n]
    for i in range(len(l)):
        labels[n[i]] = l[i]
    nx.draw_networkx_nodes(G, pos, alpha=0.7, node_color='lightblue', node_size=100)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=10, edge_color='lightgreen')
    nx.draw_networkx_labels(G, pos, labels, font_size=11)

    # plt.show()

    if not hold:
        plt.pause(interval)
        plt.clf()
    else:
        plt.show()
    # plt.close()
    #plt.close()
    #
    #
    # ln = nx.DiGraph()
    # node0 = Node(0, 0, 0, 0)
    # node1 = Node(1, 1, 2, 2)
    # node2 = Node(2, 2, 3, 3)
    # node3 = Node(3, 3, 4, 4)
    # node4 = Node(4, 4, 5, 5)
    # times = np.array([[0, 1, 4, 2, 3], [1, 0, 7, 1, 10], [4, 7, 0, 8, 11], [2, 1, 8, 0, 0.5], [3, 10, 11, 0.5, 0]])
    # ln.add_nodes_from([node0, node1, node2, node3, node4])
    #
    # add(node0, node1)
    # add(node1, node2)
    # # add(node2, node3)
    # # add(node3, node4)
    #
    # print(node0.tour_profit)
    # print(node0.tour_length)
    # display()
    # print(addTry(node2, node3))
    # add(node2, node3)
    # print(node0.tour_profit)
    # print(node0.tour_length)
    # display()
    # print(swapTry(node2, node1))
    # swap(node2, node1)
    # print(node0.tour_profit)
    # print(node0.tour_length)
    # display()
    # print(switchTry(node2, node4))
    # switch(node2, node4)
    # print(node0.tour_profit)
    # print(node0.tour_length)
    # display()
