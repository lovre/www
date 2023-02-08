import networkx as nx
import matplotlib.pyplot as plt
  
#
# Construct simple undirected graph
#

G = nx.Graph(name = "toy")

#
# Add nodes and edges (with attributes)
#

G.add_node(1)
G.add_node(2, label = "John Doe")
G.add_node('foo', cluster = 1)
G.add_node('bar', value = 13.7)
G.add_node('baz')

G.add_edge(1, 2)
G.add_edge(1, 'foo', weight = 1.0)
G.add_edge(2, 'foo', weight = 2.0)
G.add_edge('foo', 'bar')
G.add_edge('foo', 'baz')

print(G)

#
# Draw graph with wiring diagram
#

def draw(G, **args):
  nx.draw(G, with_labels = True, font_size = 8, **args)
  plt.show()

draw(G)

#
# List graph nodes and edges
#

print(G.nodes())
print(G.nodes(data = True))

print(G.edges())
print(G.edges(data = True))

#
# List neighbors of a node
#

print(list(G.neighbors('foo')))
print(G['foo'])
print(G.edges('foo', data = True))

#
# Compute basic graph statistics
#

print(G.number_of_nodes()) # len(G)
print(G.number_of_edges())
print(G.degree())

#
# Remove nodes and/or edges
#

G.remove_node(1)
G.remove_edge('baz', 'foo')

print(G)
draw(G)

#
# Represent G with directed graph D
#

D = nx.DiGraph(G)
D.add_edge('foo', 'baz')

print(D)
draw(D)

print(D.edges())

print(list(D.neighbors('foo')))
print(list(D.predecessors('foo')))
print(list(D.successors('foo')))

#
# Represent G with multigraph M
#

M = nx.MultiGraph(G)
M.add_edge('foo', 'bar', label = "new")

print(M)
draw(M)

print(M.edges())

print(list(M.neighbors('foo')))
print(M['foo'])
print(M.edges('foo', data = True))

#
# Read network from Pajek file
#

G = nx.read_pajek("dolphins.net")

print(G)
draw(G)

#
# Convert node ids to integers
#

G = nx.convert_node_labels_to_integers(G, label_attribute = 'label')

print(G.nodes(data = True))

#
# Compute PageRank scores of nodes
#

scores = nx.pagerank(G)

sizes = [1e4 * scores[i] for i in G.nodes()]

draw(G, node_size = sizes)

#
# Find network community structure
#

comms = nx.algorithms.community.label_propagation_communities(G)

colors = [0] * len(G)
for c, comm in enumerate(comms):
  for i in comm:
    colors[i] = c

draw(G, node_color = colors)
