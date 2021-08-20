import os
import numpy as np
import networkx as nx
from math import log, sqrt
import sklearn.manifold as mnf
import matplotlib.pyplot as plt
import portrait_divergence as pd

def pajek(file, path = '.'):
  """
  Reads undirected multigraph G from the specified file in Pajek format.
  """
  G = nx.MultiGraph(name = file, color = NETS[file] if file in NETS else 0)
  with open(os.path.join(path, file + '.net'), 'r') as file:
    nodes = {}
    for line in file:
      if line.startswith('*vertices'):
        continue
      elif line.startswith('*edges') or line.startswith('*arcs'):
        break
      else:
        node = line.strip().split('"')
        label = node[1].split('.')[-1]
        id = node[0].strip()
        nodes[id] = label
        G.add_node(label, id = int(id), label = label)
    for line in file:
      edge = line.strip().split(' ')
      G.add_edge(nodes[edge[0]], nodes[edge[1]])
  return G

def PDF(G, i):
  P = [0 for _ in range(G.number_of_nodes())]
  for j in nx.single_source_shortest_path_length(G, i).values():
    P[j] += 1 / G.number_of_nodes()
  return P

def PDFs(G):
  return [PDF(G, i) for i in G.nodes()]

def mus(Ps):
  return [sum(P[j] for P in Ps) / len(Ps) for j in range(len(Ps[0]))]

def JS(Ps, mu):
  return sum(Ps[i][j] * log(Ps[i][j] / mu[j]) for j in range(len(mu)) for i in range(len(Ps)) if Ps[i][j] > 0) / len(Ps)

def NND(Ps, mu):
  return JS(Ps, mu) / log(mu.index(0) + 1)

def JS2(Ps):
  if len(Ps[0]) < len(Ps[1]):
    Ps[1] = Ps[1][:len(Ps[0])]
  elif len(Ps[0]) > len(Ps[1]):
    Ps[0] = Ps[0][:len(Ps[1])]
  return JS(Ps, mus(Ps))

def dmeasure(P1, mu1, P2, mu2):
  return (sqrt(JS2([mu1, mu2]) / log(2)) + abs(sqrt(NND(P1, mu1)) - sqrt(NND(P2, mu2)))) / 2

def dmeasures(Gs):
  """
  Computes simplified D-measures between the specified undirected multigraphs Gs.
  Reference: Schieber et al., Nature Communications 8, 13928 (2017).
  """
  Ps = [PDFs(G) for G in Gs]
  mu = [mus(P) for P in Ps]
  DMs = np.zeros((len(Gs), len(Gs)))
  for i in range(len(Gs)):
    for j in range(i + 1, len(Gs)):
      DMs[i, j] = dmeasure(Ps[i], mu[i], Ps[j], mu[j])
      DMs[j, i] = DMs[i, j]
      print('dmeasure', i, j, DMs[i, j])
  return DMs

def portraits(Gs):
  """
  Computes portrait divergences between the specified undirected multigraphs Gs.
  Reference: Bagrow & Bollt, Applied Network Science 4(1), 45 (2019).
  """
  PDs = np.zeros((len(Gs), len(Gs)))
  for i in range(len(Gs)):
    for j in range(i + 1, len(Gs)):
      PDs[i, j] = pd.portrait_divergence(Gs[i], Gs[j])
      PDs[j, i] = PDs[i, j]
      print('portrait', i, j, PDs[i, j])
  return PDs

def edits(Gs):
  """
  Compute edit distances between the specified undirected multigraphs Gs.
  Reference: Abu-Aisheh et al., Proceedings of ICPRAM '15, Lisbon, Portugal (2015).
  """
  EDs = np.zeros((len(Gs), len(Gs)))
  for i in range(len(Gs)):
    for j in range(i + 1, len(Gs)):
      EDs[i, j] = nx.algorithms.similarity.graph_edit_distance(Gs[i], Gs[j])
      EDs[j, i] = EDs[i, j]
      print('edit', i, j, EDs[i, j])
  return EDs

def embedding(Ds, type = 'MDS'):
  """
  Computes MDS or tSNE embedding of multigraphs from the specified dissimilarities Ds.
  """
  if type == 'MDS':
    return mnf.MDS(n_components = 2, dissimilarity = 'precomputed').fit_transform(Ds)
  elif type == 'tSNE':
    return mnf.TSNE(n_components = 2, metric = 'precomputed').fit_transform(Ds)
  return None

def plot(Gs, Es, name):
  """
  Plots the specified embeddings Es of multigraphs Gs and stores them to a PDF file.
  """
  plt.scatter([E[0] for E in Es], [E[1] for E in Es], marker = '*', s = 50, c = [G.graph['color'] for G in Gs])
  for i, G in enumerate(Gs):
    plt.annotate(G.name, Es[i], fontsize = 7, color = 'k')
  plt.axis('off')
  plt.savefig(name + '.pdf')
  # plt.show()
  plt.close()

PATH = '/Users/lovre/Documents/office/coding/repositories/www/ina/nets'

NETS = {"toy": 0, "karate_club": 1, "dolphins": 1, "american_football": 1, "social": 1, "java": 2, "lucene": 2, "cdn_java": 2, "cdn_jung": 2, "highways": 3, "southern_women": 4}

# reads real networks from Pajek files

Gs = [pajek(file.split('.')[0], PATH) for file in os.listdir(PATH) if file.endswith('.net') and os.path.getsize(os.path.join(PATH, file)) <= 5e5]

# constructs different random model graphs

for i in range(3):
  G = nx.gnm_random_graph(1000, 5000)
  G.name = "random_" + str(i + 1)
  G.graph['color'] = -1
  Gs.append(G)
  
  G = nx.watts_strogatz_graph(1000, 10, 0.1)
  G.name = "small_world_" + str(i + 1)
  G.graph['color'] = -2
  Gs.append(G)
  
  G = nx.barabasi_albert_graph(1000, 5)
  G.name = "scale_free_" + str(i + 1)
  G.graph['color'] = -3
  Gs.append(G)

for G in Gs:
  print(G.name)

# computes and plots edit distance embedding of multigraphs

#plot(Gs, embedding(edits(Gs)), 'edit')

# computes and plots portrait divergence embedding of multigraphs

plot(Gs, embedding(portraits(Gs)), 'portrait')

# computes and plots simplified D-measure embedding of multigraphs

plot(Gs, embedding(dmeasures(Gs)), 'dmeasure')
