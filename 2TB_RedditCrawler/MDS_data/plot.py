from sklearn.manifold import mds
import numpy as np
import networkx as nx
import sys
import pickle

def save_obj(obj, name ):
    with open( name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open( name , 'rb') as f:
        return pickle.load(f)

edges = np.load(sys.argv[1])
#d = pkl.load(open(sys.argv[2], "rb"))
count = 0
for i in range(len(edges)):
	for j in range(len(edges[i])):
		if(edges[i][j] != -1):
			count+=1
print(count)
'''
d= load_obj(sys.argv[2])
vertices = len(edges)
g = nx.Graph()
for i in range(vertices):
    g.add_node(i)

for i in range(vertices):
    for j in range(i + 1, vertices):
        if edges[i][j] >= 0:
            g.add_edge(i, j, weight=edges[i][j])

print("Number of vertices: ", vertices, "\nConnected status: ",
      nx.is_connected(g), "\nNumber of edges: ", len(g.edges))

components = sorted(nx.connected_components(g), key=len, reverse=True)
print("Number of connected components = ", len(components))

complete_ = list(nx.all_pairs_dijkstra_path_length(g))

complete = [[0] * len(edges) for i in range(len(edges))]

for i in range(len(complete_)):
    s = complete_[i][0]
    for j in range(len(complete_)):
        complete[s][j] = complete_[i][1][j]

'''
