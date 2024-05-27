import os
import random

import networkx as nx
from cdlib import algorithms
from node2vec import Node2Vec
from node2vec.edges import HadamardEmbedder

def read(name, path = "."):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.split("\"")
        G.add_node(node[0].strip(), label = node[1], _class = int(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else 0)

    for line in file:
      G.add_edge(*line.split()[:2], weight = 1)

  return G
  
def info(G, fast = False):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))

  if not fast:
    C = sorted(nx.connected_components(nx.MultiGraph(G)), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G if type(G) == nx.Graph else nx.Graph(G))))
    
    C = algorithms.louvain(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()
  
Gs = []
for name in ["karate_club", "southern_women", "american_football", "sicris_collaboration", "cdn_java", "board_directors"]:
  G = read(name)
  Gs.append(G)

  info(G)
  
###
### Node classification with features
###
  
def node_features(G, path = "."):
  PR = nx.pagerank(G)
  DC = nx.degree_centrality(G)
  CC = nx.closeness_centrality(G)
  
  g = nx.Graph(G)
  
  BC = nx.betweenness_centrality(g)
  C = nx.clustering(g)
  
  louvain = {}
  for c, comm in enumerate(algorithms.louvain(G, randomize = 2024).communities):
    for i in comm:
      louvain[i] = c
      
  infomap = {}
  for c, comm in enumerate(algorithms.infomap(G).communities):
    for i in comm:
      infomap[i] = c
      
  with open(path + "/" + G.name + ".nodes.features.tab", 'w') as file:
    file.write("mS#id\tmS#node\tC#degree\tC#pagerank\tC#closeness\tC#betweenness\tC#clustering\tD#louvain\tD#infomap\tcD#class\n")
    for i, node in G.nodes(data = True):
      file.write("{:s}\t{:s}\t{:f}\t{:f}\t{:f}\t{:f}\t{:f}\t{:d}\t{:d}\t{:d}\n".format(i, node['label'], DC[i], PR[i], CC[i], BC[i], C[i], louvain[i], infomap[i], node['_class']))
      
for G in Gs:
  node_features(G)

###
### Node classification with graphlets
###

def node_orbits(G, size = 5, path = "."):
  with open(G.name + ".in", 'w') as file:
    file.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
      file.write(str(int(edge[0]) - 1) + " " + str(int(edge[1]) - 1) + "\n")
      
  os.system("./orca node " + str(size) + " " + G.name + ".in " + G.name + ".orca")
  
  orbits = {}
  with open(G.name + ".orca", 'r') as file:
    for i, line in enumerate(file):
      orbits[str(i + 1)] = [int(k) for k in line.split()]
  
  os.remove(G.name + ".in")
  os.remove(G.name + ".orca")
      
  with open(path + "/" + G.name + ".nodes.graphlets_" + str(size) + ".tab", 'w') as file:
    file.write("mS#id\tmS#node\t" + "\t".join(["C#orbit-" + str(i) for i in range(len(next(iter(orbits.values()))))]) + "\tcD#class\n");
    for i, node in G.nodes(data = True):
      file.write(i + "\t" + node['label'] + "\t" + "\t".join([str(v) for v in orbits[i]]) + "\t" + str(node['_class']) + "\n")

for G in Gs:
  G = nx.Graph(G)
  node_orbits(G, 4)
  node_orbits(G, 5)

###
### Node classification with embeddings
###

def node_embeddings(G, path = ".", dims = 32, p = 1, q = 1, walks = 32, length = 32):
  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv

  with open(path + "/" + G.name + ".nodes.node2vec.tab", 'w') as file:
    file.write("mS#id\tmS#node\t" + "\t".join(["C#n2v-" + str(i) for i in range(dims)]) + "\tcD#class\n");
    for i, node in G.nodes(data = True):
      file.write(i + "\t" + node['label'] + "\t" + "\t".join([str(v) for v in n2v[i]]) + "\t" + str(node['_class']) + "\n")

for G in Gs:
  node_embeddings(G)

###
### Link prediction with features
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
  
def jaccard(G, i, j):
  return next(nx.jaccard_coefficient(G, [(i, j)]))[2]
  
def adamic_adar(G, i, j):
  return next(nx.adamic_adar_index(G, [(i, j)]))[2]
  
def edge_features(G, edges, path = "."):
  louvain = {}
  for c, cluster in enumerate(algorithms.louvain(G).communities):
    for i in cluster:
      louvain[i] = c
      
  infomap = {}
  for c, cluster in enumerate(algorithms.infomap(G).communities):
    for i in cluster:
      infomap[i] = c
  
  with open(path + "/" + G.name + ".edges.features.tab", 'w') as file:
    file.write("mS#id1\tmS#id2\tmD#data\tC#preferential\tC#jaccard\tC#adamic_adar\tD#louvain\tD#infomap\tcD#class\n");
    for data in edges:
      for c in edges[data]:
        for i, j in edges[data][c]:
          file.write(i + "\t" + j + "\t" + data + "\t" + str(preferential(G, i, j)) + "\t" + str(jaccard(G, i, j)) + "\t" + str(adamic_adar(G, i, j)) + "\t" + ("1" if louvain[i] == louvain[j] else "0") + "\t" + ("1" if infomap[i] == infomap[j] else "0") + "\t" + str(c) + "\n")
          
for G in Gs:
  T, edges = train_test(G)
  edge_features(T, edges)

###
### Link prediction with embeddings
###

def edge_embeddings(G, edges, path = ".", dims = 32, p = 1, q = 1, walks = 32, length = 32):
  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv
  e2v = HadamardEmbedder(n2v, quiet = True)
  
  with open(path + "/" + G.name + ".edges.edge2vec.tab", 'w') as file:
    file.write("mS#id1\tmS#id2\tmD#data\t" + "\t".join(["C#e2v-" + str(i) for i in range(dims)]) + "\tC#e2d\tcD#class\n");
    for data in edges:
      for c in edges[data]:
        for i, j in edges[data][c]:
          file.write(i + "\t" + j + "\t" + data + "\t" + "\t".join([str(v) for v in e2v[(i, j)]]) + "\t" + str(sum(n2v[i][k] * n2v[j][k] for k in range(dims))) + "\t" + str(c) + "\n")

for G in Gs:
  T, edges = train_test(G)
  edge_embeddings(T, edges)
