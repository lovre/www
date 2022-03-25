import time
import math
import random
import operator

import networkx as nx
import matplotlib.pyplot as plt

def distances(G, n = 100):
  D = []
  for i in G.nodes() if len(G) <= n else random.sample(list(G.nodes()), n):
    D.extend([d for d in nx.shortest_path_length(G, source = i).values() if d > 0])
  return D
  
def price(n, c, a):
  G = nx.MultiDiGraph(name = "price")
  edges = []
  G.add_node(0)
  for i in range(1, c + 1):
    G.add_node(i)
    edges.append((0, i))
  for i in range(len(G), n):
    G.add_node(i)
    for _ in range(c):
      if random.random() < c / (c + a):
        edges.append((i, random.choice(edges)[1]))
      else:
        edges.append((i, random.randint(0, i)))
  G.add_edges_from(edges)
  return G
  
def barabasi_albert(n, c):
  return nx.MultiGraph(price(n, c, c), name = "barabasi_albert")
  
def power_law(G, kmin = 1):
  n = 0
  sumk = 0
  for _, k in G.degree():
    if k >= kmin:
      # sumk += math.log(k / (kmin - 0.5))
      sumk += math.log(k)
      n += 1
  # return 1 + n / sumk if n > 0 else math.nan
  return 1 + 1 / (sumk / n - math.log(kmin - 0.5)) if n > 0 else math.nan
  
def read(name, path = "/Users/lovre/Downloads"):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
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
  
def info(G, kmin = 5, fast = False):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  tic = time.time()
  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
  
  print("{:>12s} | {:.2f} ({:d})".format('Gamma', power_law(G, kmin), kmin))
  
  if not fast:
    if isinstance(G, nx.DiGraph):
      G = nx.MultiGraph(G)

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

for name in ["karate_club", "darknet", "collaboration_imdb", "wikileaks", "enron", "www_google"]:
  G = read(name, path = "/Users/lovre/Documents/office/coding/repositories/www/ina/nets")

  info(G)
  plot(G)

  n = G.number_of_nodes()
  m = G.number_of_edges()
  c = round(m / n)

  gamma = power_law(G, kmin = 5)
  a = c if gamma <= 2 else c * (gamma - 2)

  G = price(n, c, a)

  info(G)
  plot(G)

  G = barabasi_albert(n, c)
  # G = nx.barabasi_albert_graph(n, c)

  info(G)
  plot(G)

n = 100000
c = 10

for gamma in [2.01, 2.25, 2.5, 2.75, 3.0, 4.0, 5.0]:
  G = price(n, c, c * (gamma - 2))
  G.name += "_" + str(gamma)

  info(G, kmin = 25)
  plot(G)
