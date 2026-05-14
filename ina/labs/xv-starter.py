import os
import random
import numpy as np

import networkx as nx
from cdlib import algorithms
from cdlib.classes import NodeClustering

def read(name, path = "../nets"):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.strip().split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], _class = int(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else 0)

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G.add_edge(i, j)

  return G
  
def info(G, fast = False):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))

  if not fast:
    S = G if type(G) == nx.Graph else nx.Graph(G)
  
    C = sorted(nx.connected_components(S), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('Components', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.3f}".format('Clustering', nx.average_clustering(S)))
    
    if len(C) > 0:
      LCC = S.subgraph(C[0])
    
    print("{:>12s} | {:.2f} ({:,d})".format('Distances', nx.average_shortest_path_length(LCC), nx.diameter(LCC)))
    
    try:
      C = algorithms.leiden(G)
    except:
      C = algorithms.louvain(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.3f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()
  
Gs = []
for name in ["karate_club", "southern_women", "american_football", "sicris_collaboration", "cdn_java", "board_directors"]:
  G = read(name)
  Gs.append(G)

  info(G)
  
###
### Node classification with network features
###
  
def node_features(G, path = "../nets"):
  PR = nx.pagerank(G)

  louvain = {}
  for c, comm in enumerate(algorithms.louvain(G, randomize = 2026).communities):
    for i in comm:
      louvain[i] = c
      
  with open(path + "/" + G.name + ".nodes.features.tab", 'w') as file:
    file.write("mS#id\tmS#node\tC#pagerank\tD#louvain\tcD#class\n")
    for i, node in G.nodes(data = True):
      file.write("{:d}\t{:s}\t{:f}\t{:d}\t{:d}\n".format(i, node['label'], PR[i], louvain[i], node['_class']))
      
for G in Gs:
  node_features(G)

###
### Node classification with graphlet orbits
###

def node_orbits(G, size = 4, path = "../nets"):
  with open(G.name + ".in", 'w') as file:
    file.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
      file.write(str(edge[0]) + " " + str(edge[1]) + "\n")
      
  os.system("./orca node " + str(size) + " " + G.name + ".in " + G.name + ".orca")
  
  orbits = []
  with open(G.name + ".orca", 'r') as file:
    for line in file:
      orbits.append([int(k) for k in line.split()])
  
  os.remove(G.name + ".in")
  os.remove(G.name + ".orca")
      
  with open(path + "/" + G.name + ".nodes.orbits.tab", 'w') as file:
    file.write("mS#id\tmS#node\t" + "\t".join(["C#orbit-" + str(i) for i in range(len(orbits[0]))]) + "\tcD#class\n");
    for i, node in G.nodes(data = True):
      file.write(str(i) + "\t" + node['label'] + "\t" + "\t".join([str(v) for v in orbits[i]]) + "\t" + str(node['_class']) + "\n")

for G in Gs:
  node_orbits(nx.Graph(G))

###
### Node classification with node2vec embeddings
###

#from node2vec import Node2Vec
#
#def node_embeddings(G, dims = 32, p = 1, q = 1, walks = 32, length = 32, path = "../nets"):
#  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv
#
#  with open(path + "/" + G.name + ".nodes.node2vec.tab", 'w') as file:
#    file.write("mS#id\tmS#node\t" + "\t".join(["C#n2v-" + str(i) for i in range(dims)]) + "\tcD#class\n");
#    for i, node in G.nodes(data = True):
#      file.write(str(i) + "\t" + node['label'] + "\t" + "\t".join([str(v) for v in n2v[i]]) + "\t" + str(node['_class']) + "\n")
#
#for G in Gs:
#  node_embeddings(G)

###
### Link prediction with network features
###

def train_test(G, train = 0.8):
  nodes = list(G.nodes())
  edges = list(G.edges())
  random.shuffle(edges)
  
  non_edges = set()
  while len(non_edges) < len(edges):
    i = random.choice(nodes)
    j = random.choice(nodes)
    i, j = min(i, j), max(i, j)
    if i != j and not G.has_edge(i, j):
      non_edges.add((i, j))
  non_edges = list(non_edges)
  random.shuffle(non_edges)
  
  t = int(train * len(edges))
  T = nx.Graph(G)
  T.remove_edges_from(edges[t:])
  
  return T, {"train": {1: edges[:t], 0: non_edges[:t]}, "test": {1: edges[t:], 0: non_edges[t:]}}
  
def preferential(G, i, j):
  return next(nx.preferential_attachment(G, [(i, j)]))[2]
  
def adamic_adar(G, i, j):
  return next(nx.adamic_adar_index(G, [(i, j)]))[2]
  
def edge_features(G, edges, path = "../nets"):
  louvain = {}
  for c, comm in enumerate(algorithms.louvain(G, randomize = 2026).communities):
    for i in comm:
      louvain[i] = c
  
  with open(path + "/" + G.name + ".edges.features.tab", 'w') as file:
    file.write("mS#id1\tmS#id2\tmD#data\tC#preferential\tC#adamic_adar\tD#louvain\tcD#class\n");
    for data in edges:
      for c in edges[data]:
        for i, j in edges[data][c]:
          file.write(str(i) + "\t" + str(j) + "\t" + data + "\t" + str(preferential(G, i, j)) + "\t" + str(adamic_adar(G, i, j)) + "\t" + ("1" if louvain[i] == louvain[j] else "0") + "\t" + str(c) + "\n")
          
for G in Gs:
  edge_features(*train_test(G))

###
### Link prediction with node2vec embeddings
###

#from node2vec.edges import HadamardEmbedder
#
#def edge_embeddings(G, edges, dims = 32, p = 1, q = 1, walks = 32, length = 32, path = "../nets"):
#  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv
#  e2v = HadamardEmbedder(n2v, quiet = True)
#  
#  with open(path + "/" + G.name + ".edges.node2vec.tab", 'w') as file:
#    file.write("mS#id1\tmS#id2\tmD#data\t" + "\t".join(["C#e2v-" + str(i) for i in range(dims)]) + "\tC#e2d\tcD#class\n");
#    for data in edges:
#      for c in edges[data]:
#        for i, j in edges[data][c]:
#          file.write(str(i) + "\t" + str(j) + "\t" + data + "\t" + "\t".join([str(v) for v in e2v[(i, j)]]) + "\t" + str(sum(n2v[i][k] * n2v[j][k] for k in range(dims))) + "\t" + str(c) + "\n")
#
#for G in Gs:
#  edge_embeddings(*train_test(G))
