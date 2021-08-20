import os
import networkx as nx
from node2vec import Node2Vec
import matplotlib.pyplot as plt

def pajek(file, path = '.'):
  """
  Constructs undirected multigraph G from the specified file in Pajek format.
  """
  G = nx.MultiGraph(name = file)
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
        nodes[node[0].strip()] = label
        G.add_node(label, id = int(node[0]), label = label, cluster = int(node[2]) - 1 if len(node[2]) > 0 else 0)
    for line in file:
      edge = line.strip().split(' ')
      G.add_edge(nodes[edge[0]], nodes[edge[1]])
  return G

def node2vec(G, p = 1, q = 1, d = 8):
  """
  Computes node2vec node embedding of the specified undirected multigraph G.
  """
  return Node2Vec(G, dimensions = d, p = p, q = q , walk_length = 16, num_walks = 128).fit()

def wiring(G):
  """
  Plots wiring diagram of the specified graph G and stores into to PDF file.
  """
  nx.draw_kamada_kawai(G, node_size = 150, node_color = [node[1]['cluster'] for node in G.nodes(data = True)], cmap = 'Accent', font_size = 6, font_color = 'k', with_labels = True)
  plt.savefig(G.graph['name'] + '_net.pdf')
  # plt.show()
  plt.close()

def embedding(G, n2v):
  """
  Plots the specified node embedding of graph G and stores into to PDF file.
  """
  x = [n2v.wv.get_vector(node)[0] for node in G.nodes()]
  y = [n2v.wv.get_vector(node)[1] for node in G.nodes()]
  plt.scatter(x, y, s = 100, c = [node[1]['cluster'] for node in G.nodes(data = True)], cmap = 'Accent')
  for i, node in enumerate(G.nodes()):
    plt.annotate(node, (x[i], y[i]), fontsize = 4, color = 'k')
  plt.axis('off')
  plt.savefig(G.graph['name'] + '_emb.pdf')
  # plt.show()
  plt.close()

for file in ['karate_club', 'dolphins', 'american_football', 'southern_women', 'cdn_jung', 'cdn_java']:

  # constructs selected graph from Pajek format
  
  G = pajek(file, '/Users/lovre/Documents/office/coding/repositories/www/ina/nets')
  
  # plots wiring diagram of selected graph to PDF file
  
  wiring(G)
  
  # computes node2vec embeddings of selected graph
  
  n2v = node2vec(G)

  # plots node embeddings of selected graph to PDF file

  embedding(G, n2v)

  # computes node centralities of selected graph

  g = nx.Graph(G)
  PRs = nx.pagerank(g)
  Cs = nx.clustering(g)

  DCs = nx.degree_centrality(G)
  CCs = nx.closeness_centrality(G)
  BCs = nx.betweenness_centrality(nx.Graph(G))

  # stores node centralities of selected graph to TAB file

  with open(os.path.join('.', file + '.tab'), 'w') as file:
    file.write("m#id\tm#node\tC#DC\tC#CC\tC#BC\tC#PR\tC#C")
    for i in range(n2v.vector_size):
      file.write("\tC#n2v{:d}".format(i + 1))
    file.write("\tcD#class\n")
    for node in G.nodes(data = True):
      file.write("{:d}\t{:s}\t{:f}\t{:f}\t{:f}\t{:f}\t{:f}".format(node[1]['id'], node[0], DCs[node[0]], CCs[node[0]], BCs[node[0]], PRs[node[0]], Cs[node[0]]))
      for i in range(n2v.vector_size):
        file.write("\t{:f}".format(n2v.wv.get_vector(node[0])[i]))
      file.write("\t{:d}\n".format(node[1]['cluster']))
