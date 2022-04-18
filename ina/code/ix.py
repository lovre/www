import random

import networkx as nx
from cdlib.classes import *
from cdlib import viz, algorithms

from matplotlib import pyplot as plt

PATH = "/Users/lovre/Downloads"

def read(name, path = PATH):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.split("\"")
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
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
  print()
  
def subelj_bajec(mu = 0.5):
  G = nx.Graph(name = "subelj_bajec")
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
  
def compare(G, algs, P, num = 1):
  print("{:>12s} | {:5s} {:^6s}  {:^5s}  {:^5s}  {:^5s}".format('Algorithm', 'Count', 'Q', 'NMI', 'ARI', 'VI'))
  for alg in algs:
    c, Q, NMI, ARI, VI = 0, 0, 0, 0, 0
    for _ in range(num):
      C = algs[alg](G)
      c += len(C.communities) / num
      Q += C.newman_girvan_modularity().score / num
      NMI += C.normalized_mutual_information(P).score / num
      ARI += C.adjusted_rand_index(P).score / num
      VI += C.variation_of_information(P).score / num
    print("{:>12s} | {:>5.1f} {:6.3f}  {:5.3f}  {:5.3f}  {:5.3f}".format('\'' + alg + '\'', c, Q, NMI, ARI, VI))
  print()

def benchmarks(algs, mus = [0.05 * i for i in range(1, 13)], num = 1):
  info(subelj_bajec())
  print("{:>12s} |".format('Mixing'), end = "")
  for mu in mus:
    print(" {:^5.3f}".format(mu), end = "")
  print()
  for alg in sorted(algs.keys(), reverse = True):
    print("{:>12s} |".format('\'' + alg + '\''), end = "")
    for mu in mus:
      NMI = 0
      for _ in range(num):
        G = subelj_bajec(mu)
        C = algs[alg](G)
        NMI += C.normalized_mutual_information(partition(G)).score / num
      print(" {:5.3f}".format(NMI), end = "")
    print()
  print()
  
def partition(G):
  P = {}
  for node in G.nodes(data = True):
    if node[1]['cluster'] not in P:
      P[node[1]['cluster']] = []
    P[node[1]['cluster']].append(node[0])
  return NodeClustering(list(P.values()), G, 'Truth')
  
def k_core(G, k):
  changed = True
  while changed:
    changed = False
    for i in list(G.nodes()):
      if G.degree[i] < k:
        G.remove_node(i)
        changed = True
        
def k_cores(G, k):
  k_core(G, k)
  return sorted(nx.connected_components(G), key = len, reverse = True)
  
algs = {"Truth": lambda G: partition(G), "Louvain": algorithms.louvain, "Infomap": algorithms.infomap, "(DC)SBM": algorithms.sbm_dl, "(N)SBM": algorithms.sbm_dl_nested, "EM(MM)": lambda G: algorithms.em(G, k = 2)}

for name in ["karate_club", "southern_women"]:
  G = read(name)

  info(G)

  P = partition(G)

  compare(G, algs, P, num = 100)

#  viz.plot_network_clusters(G, algs["(DC)SBM"](G), nx.spring_layout(G))
#  plt.show()

algs["EM(MM)"] = lambda G: algorithms.em(G, k = 4)

benchmarks(algs, num = 100)

for name in ["cdn_jung", "cdn_java", "wikileaks", "collaboration_imdb"]:
  G = read(name)

  info(G)

  k, K = 0, nx.MultiGraph(G)
  print("             | # (nodes)")
  while True:
    C = k_cores(K, k)
    if len(C) == 0:
      k -= 1
      break
    print("{:>12s} | {:d} ({:s})".format(str(k) + '-cores', len(C), ", ".join([str(len(c)) for c in C[:5]]) + ("..." if len(C) > 5 else "")))
    k += 1
  print()
  
  k_core(G, k)

  print("{:>12s} | {:s}\n".format(str(k) + '-cores', "; ".join(sorted(node["label"] for _, node in G.nodes(data = True)))))
