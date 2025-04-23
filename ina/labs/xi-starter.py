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
### Estimation by random-walk sampling
###

for name in ["java", "facebook", "nec", "enron", "www_google"]:
  G = read(name)

  info(G, fast = True)

###
### Sampling Facebook social network
###

pass

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

#for label, measure in MEASURES.items():
#  Ds = dists(Gs, measure)
#  
#  map(Gs, Ds, label)
