import os
import math
import random

import networkx as nx

from scipy import stats
import matplotlib.pyplot as plt

PATH = "/Users/lovre/Downloads"

def distances(G, n = 100):
  D = []
  for i in G.nodes() if len(G) <= n else random.sample(list(G.nodes()), n):
    D.extend([d for d in nx.shortest_path_length(G, source = i).values() if d > 0])
  return D
  
def power_law(G, kmin = 1):
  n = 0
  sumk = 0
  for _, k in G.degree():
    if k >= kmin:
      sumk += math.log(k)
      n += 1
  return 1 + 1 / (sumk / n - math.log(kmin - 0.5)) if n > 0 else math.nan

def degree_mixing(G, source = None, target = None):
  x, y = [], []
  for i, j in G.edges():
    if source != None and target != None:
      x.append(G.out_degree(i) if source == 'out' else G.in_degree(i))
      y.append(G.in_degree(j) if target == 'in' else G.out_degree(j))
    else:
      x.append(G.degree(i))
      y.append(G.degree(j))
      x.append(G.degree(j))
      y.append(G.degree(i))
  return stats.pearsonr(x, y)[0]
  
def to_hash(i, j):
  if i <= j:
    i, j = j, i
  return i * (i - 1) // 2 + j

def rewired_graph(G, num = 100):
  H = set()
  edges = []
  for edge in G.edges():
    i, j = edge
    h = to_hash(i, j)
    if h not in H:
      edges.append([i, j])
      H.add(h)
  for _ in range(num):
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

def read(name, path = PATH):
  G = nx.MultiGraph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        if line.startswith("*arcs"):
          G = nx.MultiDiGraph(G)
        break
      else:
        node = line.split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], weight = float(node[2]) if len(node) > 2 and len(node[2].strip()) > 0 else None)

    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G.add_edge(i, j)
      
  return G
  
def info(G, kmin = 10, fast = True):
  print("{:>12s} | '{:s}'".format('Graph', G.name))
  print("{:>12s} | {:s}".format('Type', type(G).__name__))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
  
  if not fast:
    print("{:>12s} | {:.2f} ({:d})".format('Gamma', power_law(G, kmin), kmin))
    print("{:>12s} | {:.4f}".format('Mixing', degree_mixing(G)))
  print()

def plot(G, orbits):
  fig = plt.figure()
  fig.suptitle(G.name)
  
  for o in range(15):
    nk = {}
    for i in range(len(G)):
      k = orbits[i][o]
      if k not in nk:
        nk[k] = 0
      nk[k] += 1
    ks = sorted(nk.keys())

    plt.subplot(3, 5, o + 1)
    plt.loglog(ks, [nk[k] / len(G) for k in ks], 'ok', markersize = 1)
    plt.xticks([])
    plt.yticks([])
    
  plt.show()
  
def orca(G, path = PATH):
  with open(G.name + ".in", 'w') as file:
    file.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
      file.write(str(edge[0]) + " " + str(edge[1]) + "\n")

  os.system("./orca node 4 " + G.name + ".in " + path + "/" + G.name + ".orca")
  os.remove(G.name + ".in")
  
Gs = []
for name in ["karate_club", "dolphins", "java", "darknet", "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = read(name)
  Gs.append(G)

  info(G, fast = False)

print("{:>21s} | {:^7s} {:^7s} {:^7s} {:^7s} {:^7s}".format('Graph', 'r', 'r(ii)', 'r(io)', 'r(oi)', 'r(oo)'))

for G in Gs:
  r = degree_mixing(G)
  # r = nx.degree_assortativity_coefficient(nx.MultiGraph(G))

  rii = math.nan
  if isinstance(G, nx.DiGraph):
    rii = degree_mixing(G, 'in', 'in')

  rio = math.nan
  if isinstance(G, nx.DiGraph):
    rio = degree_mixing(G, 'in', 'out')

  roi = math.nan
  if isinstance(G, nx.DiGraph):
    roi = degree_mixing(G, 'out', 'in')

  roo = math.nan
  if isinstance(G, nx.DiGraph):
    roo = degree_mixing(G, 'out', 'out')

  print("{:>21s} | {:^7.3f} {:^7.3f} {:^7.3f} {:^7.3f} {:^7.3f}".format("'" + G.name + "'", r, rii, rio, roi, roo))
print()

print("{:>21s} | {:^7s} {:^7s}".format('Graph', 'r', 'r\''))

for G in Gs:
  n = G.number_of_nodes()
  m = G.number_of_edges()

  r = degree_mixing(G)

  rp = degree_mixing(rewired_graph(G, 10 * m))

  rer = degree_mixing(nx.gnm_random_graph(n, m))

  print("{:>21s} | {:^7.3f} {:^7.3f} {:^7.3f}".format("'" + G.name + "'", r, rp, rer))
print()

print("{:>21s} | {:^7s}".format('Graph', 'r(w)'))

for name in ["highways"]:
  G = read(name)

  rw = nx.numeric_assortativity_coefficient(G, "weight")

  print("{:>21s} | {:^7.3f}".format("'" + G.name + "'", rw))
print()

for name in ["java" , "darknet", "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = nx.Graph(read(name))

  info(G)

  orca(G)

  orbits = []
  with open(PATH + "/" + name + ".orca", 'r') as file:
    for line in file:
      orbits.append([int(k) for k in line.split()])

  plot(G, orbits)
