from networks import Graph
import operator as op
import random

def DC(G):
  """
  Compute degree centrality of all nodes in graph represented by class Graph.
  Function returns list of degree centralities of nodes represented by their indices.
  """
  DCs = [0] * G.get_n() # initialize centralities
  
  for i in G.get_nodes(): # compute centralities
    DCs[i] = G.get_degree(i) / (G.get_n() - 1)
  
  return DCs

def EC(G):
  """
  Compute eigenvector centrality of all nodes in graph represented by class Graph.
  Function returns list of eigenvector centralities of nodes represented by their indices.
  """
  ECs = [1 / G.get_n()] * G.get_n() # initialize centralities

  for _ in range(25):
    nECs = [0] * G.get_n() # initialize new/updated centralities

    for i in G.get_nodes(): # compute centralities
      for j in G.get_neighbours(i):
        nECs[i] += ECs[j]

    sEC = sum(nECs)
    ECs = [ec / sEC for ec in nECs] # normalize centralities

  return ECs

def PR(G, alpha = 0.85):
  """
  Compute PageRank score of all nodes in graph represented by class Graph.
  Function returns list of PageRank scores of nodes represented by their indices.
  """
  PRs = [1 / G.get_n()] * G.get_n() # initialize scores

  for _ in range(25):
    nPRs = [0] * G.get_n() # initialize new/updated scores

    for i in G.get_nodes(): # compute scores
      for j in G.get_neighbours(i):
        nPRs[i] += PRs[j] * alpha / G.get_degree(j)

    sPR = sum(nPRs)
    PRs = [pr + (1 - sPR) / G.get_n() for pr in nPRs] # normalize scores

  return PRs
  
def tops(G, C, label = 'Centrality', n = 12):
  """
  Print out top centrality nodes in graph G represented by class Graph.
  Method prints out top n nodes according to centrality measure C.
  """
  print("{:>25s} | {:s}".format('Node', label))
  for i, (l, c) in enumerate(sorted({G.get_label(i): c for i, c in enumerate(C)}.items(), key = op.itemgetter(1), reverse = True)):
    if i < n:
      print("{:>25s} | {:.8f}".format("'" + l + "'", c))
  print()

for name in ['got_kills', 'imdb_actors']:
  G = Graph.read(name)

  print(G)
  
  tops(G, DC(G), 'Degree')
  tops(G, EC(G), 'Eigenvector')
  tops(G, PR(G), 'PageRank')
