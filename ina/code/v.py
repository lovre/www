import time
import math
import random
import operator
import networkx as nx

def distances(G, n = 100):
  D = []
  for i in G.nodes() if len(G) <= n else random.sample(G.nodes(), n):
    D.extend([d for d in nx.shortest_path_length(G, source = i).values() if d > 0])
  return D
  
def watts_strogatz(n, k, p):
  G = nx.MultiGraph(name = "watts_strogatz")
  for i in range(n):
    G.add_node(i)
  edges = []
  for i in range(n):
    for j in range(i + 1, i + k // 2 + 1):
      edges.append((i, random.randint(0, n - 1) if random.random() < p else j % n))
  G.add_edges_from(edges)
  return G
  
def read(name):
  G = nx.MultiGraph(name = name)
  with open("/Users/lovre/Downloads/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.split("\"")
        G.add_node(int(node[0]) - 1, label = node[1])

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G.add_edge(i, j)
      
  return G
  
def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  tic = time.time()
  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
      
  C = list(nx.connected_components(G))

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  
  D = distances(G)

  print("{:>12s} | {:.2f} ({:,d})".format('Distance', sum(D) / len(D), max(D)))

  if isinstance(G, nx.MultiGraph):
    G = nx.Graph(G)

  print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()
  
  return G

def tops(G, centrality, label, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', label))
  
  tic = time.time()
  C = centrality(G)
  
  for p, ((i, j), c) in enumerate(sorted(C.items(), key = operator.itemgetter(1), reverse = True)):
    if p < n:
      print("{:>12.6f} | '{:s}' - '{:s}'".format(c, G.nodes[i]['label'], G.nodes[j]['label']))
      
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()

for name in ["highways", "euroroads"]:
  G = read(name)

  info(G)

  tops(G, nx.edge_betweenness_centrality, "betweenness")

for name in ["karate_club", "darknet", "collaboration_imdb", "www_google"]:
  G = read(name)

  n = G.number_of_nodes()
  m = G.number_of_edges()
  k = round(m / n) * 2

  G = info(G)

  p = 1 - (nx.transitivity(G) * 4 / 3 * (k - 1) / (k - 2))**(1/3)

  G = watts_strogatz(n, k, p)
  # G = nx.watts_strogatz_graph(n, k, p)

  info(G)

n = 10000
k = 10

print("{:>12s} | {:7s} {:8s}".format('Mixing', 'Cluster', 'Distance'))

for p in [0.0, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]:
  G = watts_strogatz(n, k, p)

  D = distances(G)

  print("{:>12.4f} | {:6.3f}  {:7.2f}".format(p, nx.average_clustering(nx.Graph(G)), sum(D) / len(D)))

print()
