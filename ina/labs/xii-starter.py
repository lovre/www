import networkx as nx

from cdlib import viz
from cdlib import algorithms

import matplotlib.pyplot as plt

def read(name, path = "."):
  G = nx.Graph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
    file.readline()

    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.strip().split("\"")
        G.add_node(int(node[0]) - 1, label = node[1], cluster = int(node[2]) if len(node) > 2 and node[2].strip().isdigit() else 0)

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
    S = G if type(G) == nx.Graph else nx.Graph(G)
  
    C = sorted(nx.connected_components(S), key = len, reverse = True)

    print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

    print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(S)))
    
    C = algorithms.leiden(G)
    Q = C.newman_girvan_modularity().score
      
    print("{:>12s} | {:.4f} ({:,d})".format('Modularity', Q, len(C.communities)))
  print()

def plot_wiring_diagram(G, layout = None, C = None, S = None, label = "wiring"):
  if layout is None:
    layout = nx.spring_layout(G)
    
  colors = None
  if C is not None:
    colors = [0] * len(G)
    for c, comm in enumerate(C.communities):
      for i in comm:
        colors[i] = c
    
  sizes = None
  if S is not None:
    sizes = [100 * len(G)] * len(G)
    for i in G.nodes():
      sizes[i] *= S[i]
  
  labels = {i: "" if G.nodes[i]['label'].isdigit() else G.nodes[i]['label'] for i in G.nodes()}
  
  plt.figure()

  nx.draw(G, pos = layout, node_color = colors, node_size = sizes, labels = labels, font_size = 5, edge_color = 'gray')
  
  plt.savefig(G.name + "." + label + ".pdf", bbox_inches = 'tight')
  plt.close()

def plot_block_model(G, C):
  plt.figure()
  
  C = sorted(C.communities, key = len)
  nodes = [i for c in C for i in c]
  A = nx.adjacency_matrix(G, nodelist = nodes).todense()
  
  plt.imshow(A, cmap = 'binary', interpolation = 'nearest')
  
  xy = 0
  for c in C[:-1]:
    xy += len(c)
    
    plt.plot([xy - 0.5, xy - 0.5], [-0.5, len(G) - 0.5], '-g')
    plt.plot([-0.5, len(G) - 0.5], [xy - 0.5, xy - 0.5], '-g')

  plt.yticks(range(len(G)), labels = [G.nodes[i]['label'] for i in nodes], size = 2)
  plt.xticks([])
  
  plt.savefig(G.name + ".blocks.pdf", bbox_inches = 'tight')
  plt.close()

for name in ["karate_club", "southern_women", "dolphins", "american_football", "highways", "foodweb_littlerock"]:
  G = read(name)
  
  info(G)

  # plot_wiring_diagram(G)
  
  # plot_block_model(G, algorithms.infomap(G))
