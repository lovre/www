import math
import random
from scipy import stats

import networkx as nx
from cdlib import algorithms
  
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
    C = sorted(nx.connected_components(nx.MultiGraph(G)), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G if type(G) == nx.Graph else nx.Graph(G))))
    
    C = algorithms.leiden(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()

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

    print("{:>12s} | {:d} ({:s})".format(str(k) + '-core', len(C), ", ".join([str(len(c)) for c in C[:10]])))
    k += 1

  k_core(G, k)
  # G = nx.k_core(nx.Graph(G), k)

  print("{:>12s} | {:s}\n".format(str(k) + '-core', "; ".join(sorted(data["label"] for _, data in G.nodes(data = True)))))

###
### Node degree mixing in networks
###

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

Gs = []
for name in ["karate_club", "java", "darknet", "social", "collaboration_imdb", "gnutella", "facebook", "nec"]:
  G = read(name)
  Gs.append(G)

  info(G)

print("{:>21s} | {:^7s} {:^7s} {:^7s} {:^7s} {:^7s}".format('Graph', 'r', 'r(ii)', 'r(io)', 'r(oi)', 'r(oo)'))

for G in Gs:
  r = degree_mixing(G)
  # r = nx.degree_assortativity_coefficient(G)

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

print("{:>21s} | {:^7s} {:^7s} {:^7s}".format('Graph', 'r', 'r\'', 'r(er)'))

for G in Gs:
  n = G.number_of_nodes()
  m = G.number_of_edges()

  r = degree_mixing(G)

  R = rewired_graph(G, 10 * m)
  # R = nx.Graph(G)
  # for _ in range(10 * m):
  #   nx.double_edge_swap(R)
  rp = degree_mixing(R)

  rer = degree_mixing(nx.gnm_random_graph(n, m))

  print("{:>21s} | {:^7.3f} {:^7.3f} {:^7.3f}".format("'" + G.name + "'", r, rp, rer))
print()

###
### Node mixing by not degree
###

print("{:>21s} | {:^7s} {:^7s}".format('Graph', 'r(d)', 'r(n)'))

for name in ["karate_club", "southern_women", "cdn_java", "cdn_jung", "wikileaks", "highways"]:
  G = read(name)

  rd = nx.attribute_assortativity_coefficient(G, 'value')
  rn = nx.numeric_assortativity_coefficient(G, 'value')

  print("{:>21s} | {:^7.3f} {:^7.3f}".format("'" + G.name + "'", rd, rn))
print()
