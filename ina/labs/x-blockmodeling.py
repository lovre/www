import math
import random
import numpy as np

import networkx as nx
import graph_tool.all as gt

from cdlib import viz, algorithms
from cdlib.classes import NodeClustering

from matplotlib import pyplot as plt
  
def read(name, path = "../nets"):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.strip().split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], cluster = int(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else 0)

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G.add_edge(i, j)

  return G
  
def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max(k for _, k in G.degree())))
  
  C = sorted(nx.connected_components(G), key = len, reverse = True)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

  if isinstance(G, nx.MultiGraph):
    G = nx.Graph(G)

  print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  print()
  
  return G

###
### Blockmodeling of small social networks
###

def SBM(G, dc = False):
  g = gt.Graph(directed = False)
  g.add_vertex(len(G))
  g.add_edge_list(G.edges())
  
  state = gt.minimize_blockmodel_dl(g, state_args = {'deg_corr': dc})
  for _ in range(1000):
    state.multiflip_mcmc_sweep(beta = np.inf, niter = 10)

  C = {}
  for i in G.nodes():
    if state.b[i] not in C:
      C[state.b[i]] = []
    C[state.b[i]].append(i)
    
  return NodeClustering(list(C.values()), G, ('DC' if dc else '') + 'SBM')
  
def clustering(G):
  C = {}
  for i, data in G.nodes(data = True):
    c = data['cluster']
    if c not in C:
      C[c] = []
    C[c].append(i)
    
  return NodeClustering(list(C.values()), G, 'Known')
  
def comparison(G, algs, runs = 1):
  K = clustering(G)
  
  print("{:>12s} | {:>7s} {:^6s}  {:^5s}  {:^5s}  {:^5s}".format('Algorithm', 'Count', 'Q', 'NMI', 'ARI', 'NVI'))
  
  for alg in algs:
    s, Q, NMI, ARI, NVI = 0, 0, 0, 0, 0
    
    for _ in range(runs):
      C = algs[alg](G)
      s += len(C.communities) / runs
      Q += C.newman_girvan_modularity().score / runs
      NMI += K.normalized_mutual_information(C).score / runs
      ARI += K.adjusted_rand_index(C).score / runs
      NVI += K.variation_of_information(C).score / math.log(len(G)) / runs
      
    print("{:>12s} | {:>7.1f} {:6.3f}  {:5.3f}  {:5.3f}  {:5.3f}".format('\'' + alg + '\'', s, Q, NMI, ARI, NVI))
  print()
  
algs = {"Known": lambda G: clustering(G), "Graph": lambda G: NodeClustering([range(len(G))], G, 'Graph'), "Isolates": lambda G: NodeClustering([[i] for i in range(len(G))], G, 'Isolates'), "Infomap": algorithms.infomap, "Louvain": algorithms.louvain, "Leiden": algorithms.leiden, "LPA": algorithms.label_propagation, "FLPA": lambda G: NodeClustering([list(c) for c in nx.community.fast_label_propagation_communities(G)], G, 'FLPA'), "MCL": algorithms.markov_clustering, "EM2": lambda G: algorithms.em(G, k = 2), "EM4": lambda G: algorithms.em(G, k = 4), "SBM": SBM, "DCSBM": lambda G: SBM(G, True)}

for name in ["karate_club", "southern_women"]:
  G = read(name)

  info(G)

  comparison(G, algs, runs = 100)
  
  #viz.plot_network_clusters(G, algs["Known"](G), nx.spring_layout(G), plot_labels = True)
  #plt.show()
  
###
### Blockmodeling of Šubelj-Bajec benchmark graphs
###

def subelj_bajec(mu = 0.1):
  G = nx.MultiGraph(name = "subelj_bajec")
  for i in range(128):
    G.add_node(i, cluster = i // 32 + 1)
    
  for i in range(128):
    for j in range(i + 1, 128):
      if G.nodes[i]['cluster'] <= 2 and G.nodes[j]['cluster'] <= 2:
        if G.nodes[i]['cluster'] == G.nodes[j]['cluster']:
          if random.random() < 16 * (1 - mu) / 31:
            G.add_edge(i, j)
        else:
          if random.random() < mu / 6:
            G.add_edge(i, j)
      elif G.nodes[i]['cluster'] >= 3 and G.nodes[j]['cluster'] >= 3:
        if G.nodes[i]['cluster'] != G.nodes[j]['cluster']:
          if random.random() < (1 - mu) / 2:
            G.add_edge(i, j)
        else:
          if random.random() < 16 * mu / 95:
            G.add_edge(i, j)
      elif random.random() < mu / 6:
        G.add_edge(i, j)
        
  return G

info(subelj_bajec())

runs = 100
mus = np.arange(0, 1, 0.05)

plt.figure()

for alg in algs:
  NMI = [0 for _ in range(len(mus))]

  for r in range(runs):
    for i, mu in enumerate(mus):
      G = subelj_bajec(mu)

      K = clustering(G)
      C = algs[alg](G)

      NMI[i] += K.normalized_mutual_information(C).score / runs
      
      print(alg, r, i)

  plt.plot(mus, NMI, label = alg)

plt.xlabel(r"Mixing $\mu$")
plt.ylabel("NMI")
plt.legend()

plt.show()

###
### Network k-core decomposition
###

def k_core(G, k):
  changed = True
  while changed:
    changed = False

    for i in list(G.nodes()):
      if G.degree(i) < k:
        G.remove_node(i)
        changed = True

  return G

def k_cores(G, k):
  return sorted(nx.connected_components(k_core(G, k)), key = len, reverse = True)

for name in ["cdn_java", "cdn_jung", "wikileaks", "collaboration_imdb"]:
  G = read(name)

  info(G)

  print("{:>12s} | # (nodes)".format(''))

  k, K = 0, nx.MultiGraph(G)
  while True:
    C = k_cores(K, k)

    if len(C) == 0:
      k -= 1
      print()
      break

    print("{:>7d}-core | {:d} ({:s})".format(k, len(C), ", ".join([str(len(c)) for c in C[:10]])))
    k += 1

  k_core(G, k)
  # G = nx.k_core(nx.Graph(G), k)

  print("{:>7d}-core | {:s}\n".format(k, "; ".join(sorted(data['label'] for _, data in G.nodes(data = True)))))
