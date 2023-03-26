from networks import Graph

def DC(G):
  """
  Compute the degree centrality of nodes in graph represented by class Graph.
  Function returns list of degree centralities of nodes represented by their indices.
  """
  
  DCs = [0] * G.get_n() # initialize centralities
  
  for i in G.get_nodes(): # compute centralities
    DCs[i] = G.get_degree(i) / (G.get_n() - 1)
  
  return DCs

def PR(G, alpha = 0.85):
  """
  Compute the PageRank score of nodes in graph represented by class Graph.
  Function returns list of PageRank scores of nodes represented by their indices.
  """
  
  PRs = [1 / G.get_n()] * G.get_n() # initialize scores

  for _ in range(10):
    newPRs = [0] * G.get_n() # initialize new scores

    for i in G.get_nodes(): # compute scores
      for j in G.get_neighbours(i):
        newPRs[i] += alpha * PRs[j] / G.get_degree(j)

    sumPR = sum(newPRs)
    PRs = [pr + (1 - sumPR) / G.get_n() for pr in newPRs] # correct scores

  return PRs
  
for name in ['imdb_actors', 'got_coappear', 'got_kills']:

  # construct graph representing real network
  
  G = Graph.read(name)

  print(G)

  # compute and print out degree centrality of network nodes

  DCs = sorted(list(enumerate(DC(G))), key = lambda item: -item[1])

  for i, dc in DCs[:10]:
    print("{:12.6f} | '{:s}'".format(dc, G.get_label(i)))
  print()

  # compute and print out PageRank scores of network nodes
    
  PRs = sorted(list(enumerate(PR(G))), key = lambda item: -item[1])

  for i, pr in PRs[:10]:
    print("{:12.6f} | '{:s}'".format(pr, G.get_label(i)))
  print()
