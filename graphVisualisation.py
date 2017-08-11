from graphTraversal import Node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

node0 = Node([0, 0, 0], "Hotel")
node1 = Node([1, 1.5, 0], "1")
node2 = Node([2, 0.5, 0], "2")
node3 = Node([3, 2.5, 0], "3")
node4 = Node([4, 3.5, 0], "4")
times = np.array([[0,1,4,2,3],[1,0,7,1,10],[4,7,0,8,11],[2,1,8,0,0.5],[3,10,11,0.5,0]])
G = nx.from_numpy_matrix(times)
# nx.draw_spectral(G, node_color='blue', with_labels=True, alpha=0.5, linewidths=0.01)
# plt.show()
print(G.edges())
val_map = {'A': 1.0,
           'D': 0.5714285714285714,
           'H': 0.0}


values = [val_map.get(node, 0.25) for node in G.nodes()]


# Specify the edges you want here
tour = [0,1,2,4,3]
red_edgesMaster = []
for i in range(len(tour) - 1):
    red_edgesMaster.append((tour[i], tour[i+1]))
red_edgesMaster.append((tour[-1], tour[0]))

for i in range(5):
    red_edges = red_edgesMaster[0:i+1]
    edge_colours = ['white' if not edge in red_edges else 'red'
                    for edge in G.edges()]
    #black_edges = [edge for edge in G.edges() if edge not in red_edges]

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    pos = nx.spectral_layout(G)
    nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color = values, alpha=0.7, linewidths=10)
    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True, linewidths=100)
    #nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
    nx.draw_networkx_labels(G, pos, font_size=15, font_color='white')
    plt.show()