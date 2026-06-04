import random
import numpy as np
from collections import deque

import networkx as nx
from cdlib import algorithms

import portrait_divergence as pd
import simplified_dmeasure as dm
import graphlet_aggrement as ga

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def read(name, path = "../nets"):
  G = nx.Graph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        G.add_node(int(line.strip().split("\"")[0]) - 1)

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      if i != j:
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
    C = sorted(nx.connected_components(G), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('Components', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G if type(G) == nx.Graph else nx.Graph(G))))
    
    C = algorithms.leiden(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()

###
### Estimation by random-walk sampling
###

def lcc(G):
  return nx.convert_node_labels_to_integers(G.subgraph(max(nx.connected_components(G), key = len)))

def estimate_k(G, sample = 0.15):
  g = [list(G[i]) for i in G.nodes()]

  i = random.randint(0, len(g) - 1)
  sumk, sumk_1 = len(g[i]), 1 / len(g[i])
  s = 1

  while s < sample * len(g):
    i = random.choice(g[i])
    sumk += len(g[i])
    sumk_1 += 1 / len(g[i])
    s += 1

  return sumk / s, s / sumk_1

for name in ["java", "facebook", "nec", "enron", "www_google"]:
  G = lcc(read(name))

  info(G, fast = True)

  k, c = estimate_k(G)

  print("{:>12s} | {:.2f}".format('Estimated', k))
  print("{:>12s} | {:.2f}".format('Corrected', c))
  
  nodes = random.choices(list(G), k = int(0.15 * len(G)))
  
  print("{:>12s} | {:.2f}".format('Random', sum(G.degree(i) for i in nodes) / len(nodes)))
  print()

###
### Sampling Facebook social network
###

def plot(G):
  nk = {}
  for _, k in G.degree():
    if k not in nk:
      nk[k] = 0
    nk[k] += 1
  ks = sorted(nk.keys())
  
  plt.loglog(ks, [nk[k] / len(G) for k in ks], '*k')
  plt.title(G.name)
  plt.ylabel('$p_k$')
  plt.xlabel('$k$')
  
  plt.show()
  plt.close()

for fb in [1, 2]:
  G = nx.read_edgelist("../nets/facebook_" + str(fb) + ".adj", nodetype = int)
  G = nx.convert_node_labels_to_integers(G)
  G.name = "facebook_" + str(fb)

  info(G)
  plot(G)

###
### Networks and models comparison
###

def map(Gs, Ds, label):
  fig = plt.figure()
  
  plt.imshow(Ds, cmap = LinearSegmentedColormap.from_list('', ['yellow', 'gray', 'white']))
  
  for i in range(len(Gs)):
    for j in range(len(Gs)):
      plt.text(j, i, "{:.2f}".format(Ds[i][j]), ha = 'center', va = 'center', fontsize = 4)
  
  plt.title(label)
  plt.xticks(ticks = [])
  plt.yticks(ticks = range(len(Gs)), labels = [G.name for G in Gs], fontsize = 7)
  
  clb = plt.colorbar()
  clb.ax.tick_params(labelsize = 7)
  
  fig.savefig(label + ".pdf", bbox_inches = 'tight')
  plt.close(fig)

def dists(Gs, measure):
  Ds = [[0] * len(Gs) for _ in range(len(Gs))]
  
  for i in range(len(Gs)):
    for j in range(i, len(Gs)):
      Ds[i][j] = measure(Gs[i], Gs[j])
      Ds[j][i] = Ds[i][j]
      
  return Ds

MEASURES = {"dmeasure": dm.dmeasure, "portraits": pd.portrait_divergence, "graphlets": ga.graphlet_disaggrement} # "edit": nx.algorithms.similarity.graph_edit_distance

Gs = []
for name in ["karate_club", "dolphins", "american_football", "foodweb_littlerock", "foodweb_baydry", "foodweb_baywet"]:
  G = read(name)
  Gs.append(G)
  
  info(G)
  
for i in range(3):
  G = nx.gnm_random_graph(500, 1500)
  G.name = "erdos_renyi_" + str(i + 1)
  Gs.append(G)
  
  if i == 0:
    info(G)

for i in range(3):
  G = nx.barabasi_albert_graph(500, 3)
  G.name = "barabasi_albert_" + str(i + 1)
  Gs.append(G)
  
  if i == 0:
    info(G)

for i in range(3):
  G = nx.watts_strogatz_graph(500, 6, 0.1)
  G.name = "watts_strogatz_" + str(i + 1)
  Gs.append(G)
  
  if i == 0:
    info(G)

for label, measure in MEASURES.items():
  Ds = dists(Gs, measure)
  
  map(Gs, Ds, label)

###
### Network sampling methods
###

def random_nodes(G, sample = 0.5, by_degree = False):
  nodes = sorted(G)
  if by_degree:
    weights = np.array([k for _, k in sorted(G.degree())]) / (2 * G.number_of_edges())
    g = G.subgraph(np.random.choice(nodes, size = int(sample * len(G)), replace = False, p = weights)).copy()
    g.name = G.name + "_rnd"
  else:
    g = G.subgraph(random.sample(nodes, k = int(sample * len(G)))).copy()
    g.name = G.name + "_rns"
  return g
  
def random_links(G, sample = 0.25):
  g = nx.Graph(name = G.name + "_rls")
  g.add_edges_from(random.sample(list(G.edges()), k = int(sample * G.number_of_edges())))
  return g
  
def random_walk_sample(G, sample = 0.5):
  i = random.randint(0, len(G) - 1)
  nodes = {i}
  while len(nodes) < sample * len(G):
    i = random.choice(list(G[i]))
    nodes.add(i)
  g = G.subgraph(nodes).copy()
  g.name = G.name + "_rws"
  return g
  
def depth_first_search(G, sample = 0.5):
  nodes = []
  visited = [False] * len(G)
  i = random.randint(0, len(G) - 1)
  visited[i] = True
  stack = [i]
  while len(nodes) < sample * len(G):
    i = stack.pop()
    nodes.append(i)
    for j in G[i]:
      if not visited[j]:
        visited[j] = True
        stack.append(j)
  g = G.subgraph(nodes).copy()
  g.name = G.name + "_dfs"
  return g
  
def breadth_first_search(G, sample = 0.5):
  nodes = []
  visited = [False] * len(G)
  i = random.randint(0, len(G) - 1)
  visited[i] = True
  queue = deque([i])
  while len(nodes) < sample * len(G):
    i = queue.popleft()
    nodes.append(i)
    for j in G[i]:
      if not visited[j]:
        visited[j] = True
        queue.append(j)
  g = G.subgraph(nodes).copy()
  g.name = G.name + "_bfs"
  return g
  
def community_aggregation(G, alg = algorithms.leiden):
  g = nx.quotient_graph(G, [set(c) for c in alg(G).communities], relabel = True)
  g.name = G.name + "_comms"
  return g
  
SAMPLERS = [random_nodes, lambda G: random_nodes(G, by_degree = True), random_links, random_walk_sample, depth_first_search, breadth_first_search, community_aggregation]
  
G = lcc(read("social"))
Gs = [G]

info(G)

for sampler in SAMPLERS:
  for i in range(2):
    g = nx.convert_node_labels_to_integers(sampler(G))
    g.name += "_" + str(i + 1)
    Gs.append(g)
  
    if i == 0:
      info(g)

for label, measure in MEASURES.items():
  Ds = dists(Gs, measure)

  map(Gs, Ds, label)
