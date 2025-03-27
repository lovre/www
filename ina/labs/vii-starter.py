import random
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

def read(name, path = "."):
  G = nx.Graph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.strip().split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], value = float(node[2]) if len(node) > 2 and len(node[2]) else 1)

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
  
  C = sorted(nx.connected_components(G), key = len, reverse = True)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))
  
  if not fast:
    if len(C) > 1:
      G = G.subgraph(C[0])

    print("{:>12s} | {:.2f} ({:,d})".format('Distance', nx.average_shortest_path_length(G), nx.diameter(G)))

    if isinstance(G, nx.MultiGraph):
      G = nx.Graph(G)

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  print()
  
  return G
  
#
#  Movie recommendations with PageRank
#

def pagerank(G, alpha = 0.85, eps = 1e-6):
  P = [1 / len(G)] * len(G)
  diff = 1
  while diff > eps:
    U = [sum([P[j] * alpha / G.degree(j) for j in G[i]]) for i in G.nodes()]
    u = sum(U)
    U = [U[i] + (1 - u) / len(G) for i in G.nodes()]
    diff = sum([abs(P[i] - U[i]) for i in G.nodes()])
    P = U
  return {i: P[i] for i in G.nodes()}

def top_nodes(G, C, centrality, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', centrality))
  for i, c in sorted(C.items(), key = lambda item: (item[1], G.degree(item[0])), reverse = True):
    if not G.nodes[i]['label'].startswith('m-'):
      print("{:>12.6f} | '{:s}' ({:,d})".format(c, G.nodes[i]['label'], G.degree[i]))
      n -= 1
      if n == 0:
        break
  print()

def find_node(G, label):
  for i, data in G.nodes(data = True):
    if data['label'] == label:
      return i
  raise Exception()
  
G = read("movies_graph")

info(G)

#top_nodes(G, nx.pagerank(G), 'pagerank')
top_nodes(G, pagerank(G), 'pagerank')

#
# Betweenness in transportation networks
#

def top_edges(G, C, centrality, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', centrality))
  for (i, j), c in sorted(C.items(), key = lambda item: item[1], reverse = True)[:n]:
    print("{:>12.6f} | '{:s}' - '{:s}' ({:,.0f})".format(c, G.nodes[i]['label'], G.nodes[j]['label'], (G.nodes[i]['value'] + G.nodes[j]['value']) / 2))
  print()

for name in ["highways", "euroroads"]:
  G = read(name)

  info(G)
 
#
# Errors and attacks on the Internet
#

def lcc(G):
  return len(sorted(nx.connected_components(G), key = len)[-1]) / len(G)

G = read("nec")
#G = nx.gnm_random_graph(G.number_of_nodes(), G.number_of_edges())

info(G, fast = True)
