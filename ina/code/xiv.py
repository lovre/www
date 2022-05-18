import random

import networkx as nx
from cdlib import algorithms

from node2vec import Node2Vec
from node2vec.edges import HadamardEmbedder

PATH = "/Users/lovre/Documents/office/coding/repositories/www/ina/nets"

def read(name, path = PATH):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.split("\"")
        G.add_node(node[0].strip(), label = node[1], cluster = int(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else 0)

    for line in file:
      G.add_edge(*line.split()[:2], weight = 1)
      
  return G

def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  
  C = list(nx.connected_components(G))
    
  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()
  
  return G
  
def train_graph(G, train = 0.8):
  nodes = list(G.nodes())
  edges = list(G.edges())
  random.shuffle(edges)
  
  non_edges = []
  while len(non_edges) < len(edges):
    i = random.choice(nodes)
    j = random.choice(nodes)
    if i != j and not G.has_edge(i, j):
      non_edges.append((i, j))
  
  train = int(train * len(edges))
  G = nx.Graph(G)
  G.remove_edges_from(edges[train:])
  
  return G, {"train": {1: edges[:train], 0: non_edges[:train]}, "test": {1: edges[train:], 0: non_edges[train:]}}

def node_features(G, path = PATH):
  PR = nx.pagerank(G)
  DC = nx.degree_centrality(G)
  CC = nx.closeness_centrality(G)
  BC = nx.betweenness_centrality(G)
  C = nx.clustering(nx.Graph(G))
  
  louvain = {}
  for c, cluster in enumerate(algorithms.louvain(G).communities):
    for i in cluster:
      louvain[i] = c
      
  infomap = {}
  for c, cluster in enumerate(algorithms.infomap(G).communities):
    for i in cluster:
      infomap[i] = c
      
  sbm = {}
  for c, cluster in enumerate(algorithms.sbm_dl(G).communities):
    for i in cluster:
      sbm[i] = c
      
  with open(path + "/" + name + ".nodes.features.tab", 'w') as file:
    file.write("mS#id\tmS#node\tC#degree\tC#pagerank\tC#closeness\tC#betweenness\tC#clustering\tD#louvain\tD#infomap\tD#sbm\tcD#class\n")
    for i, node in G.nodes(data = True):
      file.write("{:s}\t{:s}\t{:f}\t{:f}\t{:f}\t{:f}\t{:f}\t{:d}\t{:d}\t{:d}\t{:d}\n".format(i, node['label'], DC[i], PR[i], CC[i], BC[i], C[i], louvain[i], infomap[i], sbm[i], node['cluster']))

def node_embeddings(G, dims = 32, p = 1, q = 1, walks = 32, length = 32, path = PATH):
  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv

  with open(path + "/" + name + ".nodes.node2vec.tab", 'w') as file:
    file.write("mS#id\tmS#node\t" + "\t".join(["C#n2v-" + str(i) for i in range(dims)]) + "\tcD#class\n");
    for i, node in G.nodes(data = True):
      file.write(i + "\t" + node['label'] + "\t" + "\t".join([str(v) for v in n2v[i]]) + "\t" + str(node['cluster']) + "\n")

def preferential(G, i, j):
  return next(nx.preferential_attachment(G, [(i, j)]))[2]
  
def jaccard(G, i, j):
  return next(nx.jaccard_coefficient(G, [(i, j)]))[2]
  
def adamic_adar(G, i, j):
  return next(nx.adamic_adar_index(G, [(i, j)]))[2]
  
def edge_features(G, edges, path = PATH):
  louvain = {}
  for c, cluster in enumerate(algorithms.louvain(G).communities):
    for i in cluster:
      louvain[i] = c
      
  infomap = {}
  for c, cluster in enumerate(algorithms.infomap(G).communities):
    for i in cluster:
      infomap[i] = c
      
  sbm = {}
  for c, cluster in enumerate(algorithms.sbm_dl(G).communities):
    for i in cluster:
      sbm[i] = c
  
  with open(path + "/" + name + ".edges.features.tab", 'w') as file:
    file.write("mS#id1\tmS#id2\tmD#data\tC#preferential\tC#jaccard\tC#adamic_adar\tD#louvain\tD#infomap\tD#sbm\tcD#class\n");
    for data in edges:
      for c in edges[data]:
        for i, j in edges[data][c]:
          file.write(i + "\t" + j + "\t" + data + "\t" + str(preferential(G, i, j)) + "\t" + str(jaccard(G, i, j)) + "\t" + str(adamic_adar(G, i, j)) + "\t" + ("1" if louvain[i] == louvain[j] else "0") + "\t" + ("1" if infomap[i] == infomap[j] else "0") + "\t" + ("1" if sbm[i] == sbm[j] else "0") + "\t" + str(c) + "\n")

def edge_embeddings(G, edges, dims = 32, p = 1, q = 1, walks = 32, length = 32, path = PATH):
  n2v = Node2Vec(G, dimensions = dims, p = p, q = q, num_walks = walks, walk_length = length, workers = 8, quiet = True).fit().wv
  e2v = HadamardEmbedder(n2v, quiet = True)
  
  with open(path + "/" + name + ".edges.node2vec.tab", 'w') as file:
    file.write("mS#id1\tmS#id2\tmD#data\t" + "\t".join(["C#e2v-" + str(i) for i in range(dims)]) + "\tcD#class\n");
    for data in edges:
      for c in edges[data]:
        for i, j in edges[data][c]:
          file.write(i + "\t" + j + "\t" + data + "\t" + "\t".join([str(v) for v in e2v[(i, j)]]) + "\t" + str(c) + "\n")

for name in ["karate_club", "southern_women", "american_football", "sicris_collaboration", "cdn_java", "board_directors"]:
  G = read(name)

  info(G)
  
  node_features(G)

  node_embeddings(G)
  
  G, edges = train_graph(G)
  
  edge_features(G, edges)

  edge_embeddings(G, edges)
