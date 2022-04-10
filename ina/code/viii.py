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
  
def girvan_newman(mu = 0.5):
  G = nx.Graph(name = "girvan_newman")
  for i in range(128):
    G.add_node(i, cluster = i // 32 + 1)
  for i in range(128):
    for j in range(i + 1, 128):
      if G.nodes[i]['cluster'] == G.nodes[j]['cluster']:
        if random.random() < 16 * (1 - mu) / 31:
          G.add_edge(i, j)
      else:
        if random.random() < mu / 6:
          G.add_edge(i, j)
  return G
  
def compare(G, algs, P, num = 1):
  print("{:>12s} | {:5s} {:^6s}  {:^5s}  {:^5s}  {:^5s}".format('Algorithm', 'Count', 'Q', 'NMI', 'ARI', 'VI'))
  for alg in sorted(algs.keys(), reverse = True):
    c, Q, NMI, ARI, VI = 0, 0, 0, 0, 0
    for _ in range(num):
      C = algs[alg](G)
      c += len(C.communities) / num
      Q += C.newman_girvan_modularity().score / num
      NMI += C.normalized_mutual_information(P).score / num
      ARI += C.adjusted_rand_index(P).score / num
      VI += C.variation_of_information(P).score / num
    print("{:>12s} | {:>5.0f} {:6.3f}  {:5.3f}  {:5.3f}  {:5.3f}".format('\'' + alg + '\'', c, Q, NMI, ARI, VI))
  print()

def benchmarks(algs, mus = [0.05 * i for i in range(1, 13)], num = 1):
  info(girvan_newman())
  print("{:>12s} |".format('Mixing'), end = "")
  for mu in mus:
    print(" {:^5.3f}".format(mu), end = "")
  print()
  for alg in sorted(algs.keys(), reverse = True):
    print("{:>12s} |".format('\'' + alg + '\''), end = "")
    for mu in mus:
      NMI = 0
      for _ in range(num):
        G = girvan_newman(mu)
        C = algs[alg](G)
        NMI += C.normalized_mutual_information(partition(G)).score / num
      print(" {:5.3f}".format(NMI), end = "")
    print()
  print()

def randoms(algs, n = 2500, ks = list(range(1, 24, 3)), num = 1):
  G = nx.gnm_random_graph(n, n * ks[len(ks) // 2] // 2)
  G.name = "erdos_renyi"
  info(G)
  print("{:>12s} |".format('Degree'), end = "")
  for k in ks:
    print(" {:^5d}".format(k), end = "")
  print()
  for alg in sorted(algs.keys(), reverse = True):
    print("{:>12s} |".format('\'' + alg + '\''), end = "")
    for k in ks:
      VI = 0
      for _ in range(num):
        G = nx.gnm_random_graph(n, n * k // 2)
        C = algs[alg](G)
        VI += C.variation_of_information(components(G)).score / num
      print(" {:5.3f}".format(VI), end = "")
    print()
  print()
  
def partition(G):
  P = {}
  for node in G.nodes(data = True):
    if node[1]['cluster'] not in P:
      P[node[1]['cluster']] = []
    P[node[1]['cluster']].append(node[0])
  return NodeClustering(list(P.values()), G, 'Truth')
  
def components(G):
  return NodeClustering(list(nx.connected_components(G)), G)
  
algs = {"Truth": lambda G: partition(G), "Louvain": algorithms.louvain, "Infomap": algorithms.infomap, "LPA": algorithms.label_propagation, "EB": lambda G: algorithms.girvan_newman(G, level = 1), "SBM": algorithms.sbm_dl_nested}

for name in ["karate_club", "southern_women", "dolphins", "american_football"]:
  G = read(name)

  info(G)

  P = partition(G)

  compare(G, algs, P, num = 100)

  # viz.plot_network_clusters(G, algs["Truth"](G), nx.spring_layout(G))
  # plt.show()

algs.pop("EB")

benchmarks(algs, num = 100)

algs.pop("SBM")

for name in ["cdn_java", "dormitory", "wikileaks", "youtube"]:
  G = read(name)

  info(G)

  P = partition(G)

  compare(G, algs, P, num = 10)

algs.pop("Truth")

randoms(algs, num = 10)
