import os
import random

import networkx as nx
from cdlib import algorithms

import portrait_divergence as pd
import simplified_dmeasure as dm
import graphlet_aggrement as ga

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def read(name, path = "."):
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
    C = sorted(nx.connected_components(nx.MultiGraph(G)), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G if type(G) == nx.Graph else nx.Graph(G))))
    
    C = algorithms.leiden(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()

###
### Graphlet degree distributions
###

def plot(G, orbits):
  fig, axes = plt.subplots(3, 5)
  fig.suptitle(G.name)

  for o in range(15):
    nk = {}
    for i in range(len(G)):
      k = orbits[i][o]
      if k not in nk:
        nk[k] = 0
      nk[k] += 1
    ks = sorted(nk.keys())

    axes[o // 5, o % 5].loglog(ks, [nk[k] / len(G) for k in ks], 'ok', markersize = 1)
    axes[o // 5, o % 5].set_xticks([])
    axes[o // 5, o % 5].set_yticks([])

  plt.savefig(G.name + ".png", bbox_inches = 'tight')
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
  G = read(name)

  info(G)

  orbits = orca(G)

  plot(G, orbits)

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

for name in ["java", "nec", "facebook", "enron", "www_google"]:
  G = lcc(read(name))

  info(G, fast = True)

  k, c = estimate_k(G)

  print("{:>12s} | {:.2f}".format('Estimated', k))
  print("{:>12s} | {:.2f}".format('Corrected', c))
  print()

###
### Sampling Facebook social network
###

for fb in [1, 2]:
  G = nx.read_edgelist("facebook_" + str(fb) + ".adj", nodetype = int)
  G = nx.convert_node_labels_to_integers(G)
  G.name = "facebook_" + str(fb)

  info(G)

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
for name in ["karate_club", "southern_women", "dolphins", "foodweb_littlerock", "foodweb_baydry", "foodweb_baywet"]:
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
