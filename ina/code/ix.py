import math
import random
import numpy as np

import networkx as nx

from cdlib import viz, algorithms
from cdlib.classes import NodeClustering

from matplotlib import pyplot as plt
from collections import deque

def fast_label_propagation(G):
  assert(type(G) == nx.MultiGraph)
  
  N = list(G.nodes())
  random.shuffle(N)
  
  Q = deque(N)
  S = [True] * len(G)
  
  C = [i for i in range(len(G))]

  while Q:
    i = Q.popleft()
    S[i] = False
    
    if len(G[i]) > 0:
      L = {}
      for j in G[i]:
        if C[j] not in L:
          L[C[j]] = 0
        L[C[j]] += len(G[i][j])
    
      maxl = max(L.values())
      c = random.choice([c for c in L if L[c] == maxl])
      
      if C[i] != c:
        C[i] = c
        
        for j in G[i]:
          if C[j] != c and not S[j]:
            Q.append(j)
            S[j] = True
            
  L = {}
  for i in N:
    if C[i] in L:
      L[C[i]].append(i)
    else:
      L[C[i]] = [i]
      
  return NodeClustering(list(L.values()), G)
  
def read(name, path = "."):
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
  
def info(G, fast = False):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  
  C = sorted(nx.connected_components(G), key = len, reverse = True)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

  if isinstance(G, nx.MultiGraph):
    G = nx.Graph(G)

  print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  print()
  
  return G

###
### Community detection in small social networks
###
  
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
  
  print("{:>12s} | {:5s} {:^6s}  {:^5s}  {:^5s}  {:^5s}".format('Algorithm', 'Count', 'Q', 'NMI', 'ARI', 'VI'))
  
  for alg in algs:
    s, Q, NMI, ARI, VI = 0, 0, 0, 0, 0
    
    for _ in range(runs):
      C = algs[alg](G)
      s += len(C.communities) / runs
      Q += C.newman_girvan_modularity().score / runs
      NMI += K.normalized_mutual_information(C).score / runs
      ARI += K.adjusted_rand_index(C).score / runs
      VI += K.variation_of_information(C).score / runs
      
    print("{:>12s} | {:>5.0f} {:6.3f}  {:5.3f}  {:5.3f}  {:5.3f}".format('\'' + alg + '\'', s, Q, NMI, ARI, VI))
  print()
  
algs = {"Known": lambda G: clustering(G), "Infomap": algorithms.infomap, "Louvain": algorithms.louvain, "Leiden": algorithms.leiden, "LPA": algorithms.label_propagation, "FLPA": fast_label_propagation, "MCL": algorithms.markov_clustering, "EB": lambda G: algorithms.girvan_newman(G, level = 1)}

#for name in ["karate_club", "dolphins", "american_football"]:
#  G = read(name)
#
#  info(G)
#
#  comparison(G, algs, runs = 100)
#
#  #viz.plot_network_clusters(G, algs["Known"](G), nx.spring_layout(G))
#  #plt.show()

###
### Community detection in networks with node metadata
###

algs.pop("MCL")
algs.pop("EB")

#for name in ["cdn_java", "wikileaks", "dormitory"]:
#  G = read(name)
#
#  info(G)
#
#  comparison(G, algs, runs = 10)

###
### Community detection in Girvan-Newman benchmark graphs
###

#def girvan_newman(mu = 0.1):
#  G = nx.MultiGraph(name = "girvan_newman")
#  for i in range(128):
#    G.add_node(i, cluster = i // 32 + 1)
#
#  for i in range(128):
#    for j in range(i + 1, 128):
#      if G.nodes[i]['cluster'] == G.nodes[j]['cluster']:
#        if random.random() < 16 * (1 - mu) / 31:
#          G.add_edge(i, j)
#      else:
#        if random.random() < mu / 6:
#          G.add_edge(i, j)
#
#  return G
#
#info(girvan_newman())
#
#runs = 100
#mus = np.arange(0, 1, 0.05)
#
#plt.figure()
#
#for alg in algs:
#  NMI = [0 for _ in range(len(mus))]
#
#  for _ in range(runs):
#    for i, mu in enumerate(mus):
#      G = girvan_newman(mu)
#
#      K = clustering(G)
#      C = algs[alg](G)
#
#      NMI[i] += K.normalized_mutual_information(C).score / runs
#
#  plt.plot(mus, NMI, label = alg)
#
#plt.xlabel("Mixing $\mu$")
#plt.ylabel("NMI")
#plt.legend()
#
#plt.savefig("girvan_newman.pdf", bbox_inches = 'tight')

###
### Community detection in Erdos-Renyi random graphs
###

algs.pop("Leiden")

#def erdos_renyi(n = 1000, k = 10):
#  G = nx.MultiGraph(nx.gnm_random_graph(n, n * k // 2))
#  G.name = "erdos_renyi"
#
#  for c, C  in enumerate(nx.connected_components(G)):
#    for i in C:
#      G.nodes[i]['cluster'] = c
#
#  return G
#
#info(erdos_renyi())
#
#runs = 10
#ks = range(24)
#
#plt.figure()
#
#for alg in algs:
#  NVI = [0 for _ in range(len(ks))]
#
#  for _ in range(runs):
#    for i, k in enumerate(ks):
#      G = erdos_renyi(k = k)
#
#      K = clustering(G)
#      C = algs[alg](G)
#
#      NVI[i] += K.variation_of_information(C).score / math.log(len(G)) / runs
#
#  plt.plot(ks, NVI, label = alg)
#
#plt.xlabel("Degree $k$")
#plt.ylabel("NVI")
#plt.legend()
#
#plt.savefig("erdos_renyi.pdf", bbox_inches = 'tight')

###
### Blockmodeling of small social networks
###

#$(brew --prefix python@3.10)/bin/python3

algs.pop("Infomap")
algs["DCSBM"] = algorithms.sbm_dl

#for name in ["karate_club", "southern_women"]:
#  G = read(name)
#
#  info(G)
#
#  comparison(G, algs, runs = 100)

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

  for _ in range(runs):
    for i, mu in enumerate(mus):
      G = subelj_bajec(mu)

      K = clustering(G)
      C = algs[alg](G)

      NMI[i] += K.normalized_mutual_information(C).score / runs

  plt.plot(mus, NMI, label = alg)

plt.xlabel("Mixing $\mu$")
plt.ylabel("NMI")
plt.legend()

plt.savefig("subelj_bajec.pdf", bbox_inches = 'tight')
