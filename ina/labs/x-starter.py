import os
import math
import random

import networkx as nx
from cdlib import algorithms

from scipy import stats
import matplotlib.pyplot as plt
  
def read(name, path = "."):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        if line.startswith("*arcs"):
          G = nx.MultiDiGraph(G)
        break
      else:
        node = line.strip().split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], value = float(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else 0)

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

    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(S)))
    
    C = algorithms.leiden(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()

###
### Node degree mixing in networks
###

for name in ["karate_club", "java", "darknet", "social", "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = read(name)

  info(G)

###
### Structurally disassortative networks by degree
###

def to_hash(i, j):
  if i <= j:
    i, j = j, i
  return i * (i - 1) // 2 + j

def rewired_graph(G, swaps = 100):
  H = set()
  edges = []
  for edge in G.edges():
    i, j = edge
    h = to_hash(i, j)
    if h not in H:
      edges.append([i, j])
      H.add(h)

  for _ in range(swaps):
    eij = random.randint(0, len(edges) - 1)
    euv = random.randint(0, len(edges) - 1)
    if eij != euv:
      i, j = edges[eij]
      u, v = edges[euv]

      if random.random() < 0.5:
        if i != v and u != j:
          hiv = to_hash(i, v)
          huj = to_hash(u, j)
          if hiv not in H and huj not in H:
            edges[eij][1] = v
            edges[euv][1] = j
            H.remove(to_hash(i, j))
            H.remove(to_hash(u, v))
            H.add(hiv)
            H.add(huj)
      else:
        if i != u and j != v:
          hiu = to_hash(i, u)
          hjv = to_hash(j, v)
          if hiu not in H and hjv not in H:
            edges[eij][1] = u
            edges[euv][0] = j
            H.remove(to_hash(i, j))
            H.remove(to_hash(u, v))
            H.add(hiu)
            H.add(hjv)

  G = nx.empty_graph(len(G))
  G.add_edges_from(edges)

  return G
  
for name in ["karate_club", "java", "darknet", "social", "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = read(name)

  info(G, fast = True)

###
### Node mixing by not degree
###

pass

###
### Graphlet degree distributions
###

def plot(G, orbits):
  fig, axs = plt.subplots(3, 5)
  fig.suptitle(G.name)

  for o in range(15):
    nk = {}
    for i in range(len(G)):
      k = orbits[i][o]
      if k not in nk:
        nk[k] = 0
      nk[k] += 1
    ks = sorted(nk.keys())

    axs[o // 5, o % 5].loglog(ks, [nk[k] / len(G) for k in ks], 'ok', markersize = 1)
    axs[o // 5, o % 5].set_xticks([])
    axs[o // 5, o % 5].set_yticks([])

  plt.savefig(G.name + ".pdf", bbox_inches = 'tight')
  plt.close()

def orca(G, path = "."):
  with open(G.name + ".in", 'w') as file:
    file.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")

    for i, j in G.edges():
      file.write(str(i) + " " + str(j) + "\n")

  os.system("./orca node 4 " + G.name + ".in " + path + "/" + G.name + ".orca")
  os.remove(G.name + ".in")

  orbits = []
  with open(path + "/" + name + ".orca", 'r') as file:
    for line in file:
      orbits.append([int(k) for k in line.split()])

  return orbits

for name in ["java" , "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = nx.Graph(read(name))

  info(G)
