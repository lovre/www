import time
import random

import numpy as np
import networkx as nx
from cdlib.classes import *
from cdlib import algorithms

from collections import deque

PATH = "/Users/lovre/Downloads"

def read(name, path = PATH):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        G.add_node(int(line.split(" ")[0]) - 1)

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      if i != j:
        G.add_edge(i, j)
      
  return G
  
def info(G, fast = True):
  tic = time.time()
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d}".format('Nodes', n))
  print("{:>12s} | {:,d}".format('Edges', m))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  
  if not fast:
    C = list(nx.connected_components(G))
    
    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  
    # C = algorithms.label_propagation(G)
    C = fast_label_propagation(G)
  
    print("{:>12s} | {:.3f} ({:,d})".format('Q', C.newman_girvan_modularity().score, len(C.communities)))
  
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()
 
def lcc(G):
  return nx.convert_node_labels_to_integers(G.subgraph(max(nx.connected_components(G), key = len)))
 
def fast_label_propagation(G):
  N = list(G.nodes())
  random.shuffle(N)
  
  Q = deque(N)
  S = [True] * len(G)
  
  C = [i for i in range(len(G))]

  while Q:
    i = Q.popleft()
    S[i] = False
    
    if len(G[i]) > 0:
      N = {}
      for j in G[i]:
        if C[j] in N:
          N[C[j]] += 1 # len(G[i][j])
        else:
          N[C[j]] = 1 # len(G[i][j])

      maxn = max(N.values())
      c = random.choice([c for c in N if N[c] == maxn])
      
      if C[i] != c:
        C[i] = c
        for j in G[i]:
          if C[j] != c and not S[j]:
            Q.append(j)
            S[j] = True
            
  L = {}
  for i, c in enumerate(C):
    if c in L:
      L[c].append(i)
    else:
      L[c] = [i]
     
  return NodeClustering(list(L.values()), G, 'FLPA')
 
def estimate_k(G, size = 0.15):
  g = [[] for _ in range(len(G))]
  for i in G.nodes():
    for j in G[i]:
      g[i].extend([j] * len(G[i][j]))

  i = random.randint(0, len(g) - 1)
  sumk, sumk_1 = len(g[i]), 1 / len(g[i])
  s = 1
  
  while s < size * len(g):
    i = random.choice(g[i])
    sumk += len(g[i])
    sumk_1 += 1 / len(g[i])
    s += 1
    
  return sumk / s, s / sumk_1

for name in ["nec", "facebook", "enron", "www_google"]:
  G = lcc(read(name))

  info(G)

  tic = time.time()
  k, c = estimate_k(G)

  print("{:>12s} | {:.2f}".format('Estimated', k))
  print("{:>12s} | {:.2f}".format('Corrected', c))
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()

for fb in [1, 2]:
  G = nx.read_edgelist(PATH + "/facebook_" + str(fb) + ".adj", nodetype = int)
  G = nx.convert_node_labels_to_integers(G)
  G.name = "facebook_" + str(fb)

  info(G, fast = False)
