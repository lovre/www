"""network analysis utilities"""

from cdlib.classes import NodeClustering
from collections import defaultdict, deque
import math
import networkx as nx
from matplotlib import pyplot as plt
from typing import *
import random
import numpy as np
import os
from tqdm import tqdm
import re

DEFAULT_DATA_FOLDER = "../networks"


def read_edgelist(filename: str, data_folder=DEFAULT_DATA_FOLDER, progress_bar=False) -> nx.Graph:
    """Reads a network in edgelist (.adj) format. Assumes directed links
    unless the term `undirected` is stated in the header."""
    filename = os.path.splitext(filename)[0]
    
    edges: List[Tuple[int, int]] = []

    with open(os.path.join(data_folder, f"{filename}.adj")) as f:
        comments = ""
        for line in f:
            if line[0] == '#': comments += line[1:]
            else: break

        directed = ("undirected" not in comments)

        if progress_bar and (match := re.search(r"([\d,]+) edges", comments)):
            # get the first edge
            i, j = (int(x) - 1 for x in line.split())
            edges.append((i, j))
            
            m = int(match.group(1).replace(',', ''))
            # get the rest
            for _ in tqdm(range(m - 1), desc=f"reading {filename}"):
                i, j = (int(x) - 1 for x in next(f).split())
                edges.append((i, j))
        else:
            for line in f:
                i, j = (int(x) - 1 for x in line.split())
                edges.append((i, j))

    if directed:
        return nx.DiGraph(edges, name=filename)
    else:
        return nx.Graph(edges, name=filename)


def read_pajek(filename: str, data_folder=DEFAULT_DATA_FOLDER,
               label_parser: Callable[[str, str], Dict[str, Any]] = None) -> nx.Graph:
    """Reads a graph in Pajek (.net) format with at most one value
    attached to each node (aside from the label). Note that this doesn't entirely
    comply with the Pajek format specification, see
    http://vlado.fmf.uni-lj.si/pub/networks/pajek/doc/draweps.htm

    - label_parser: a function that takes a node's label and value (default None),
    and returns a dictionary of node attributes to be stored in graph. By default,
    labels will be stored in attribute 'label', and values (if present) in 'value'."""
    
    filename = os.path.splitext(filename)[0]

    if label_parser is None:
        def label_parser(lab, val): return \
            {"label": lab} if val is None else {"label": lab, "value": val}

    with open(os.path.join(data_folder,  f"{filename}.net"), encoding="UTF-8") as file:
        file.readline() # skip header
        nodes = [] # OPT pre-allocate given header

        for line in file:
            if line.startswith("*"):
                match line.split()[0][1:]: # TODO extract m for optional progressbar
                    case "edges": G = nx.MultiGraph(name=filename)
                    case "arcs": G = nx.MultiDiGraph(name=filename)
                    case link_type: raise SyntaxError(f"invalid link type: {link_type}")
                break
            else: # add node
                match line.strip().split("\""):
                    case num, lab:
                        nodes.append((int(num) - 1, label_parser(lab, None)))
                    case num, lab, val:
                        nodes.append((int(num) - 1, label_parser(lab, val)))
                    case _:
                        raise SyntaxError("failed to parse " + line)

        G.add_nodes_from(nodes)

        for line in file:
            i, j = (int(x) - 1 for x in line.split()[:2])
            G.add_edge(i, j)

    return G


def lcc(G: nx.Graph) -> float:
    """relative size of the largest connected component (between 0 and 1)"""
    if G.is_directed(): G = nx.Graph(G)

    return len(max(nx.connected_components(G), key=len)) / len(G)


def distances(G: nx.Graph, n=100) -> List[float]:
    """computes lengths of shortest paths from n randomly chosen
    nodes to all other nodes"""
    D = []
    for i in G.nodes() if len(G) <= n else random.sample(list(G.nodes()), n):
        D.extend(d for d in nx.shortest_path_length(G, source=i).values() if d > 0)
    return D


def info(G: nx.Graph, distance_sample: int | None = None,
         clustering_sample: int | None = 10_000) -> None:
    """Prints basic information on the provided graph.
    - If distance_sample is given, distance statistics will be computed from
    a sample of nodes (of given size).
    - If clustering_sample is given, average clustering will be computed from
    a sample of nodes (of given size).
    """
    print("{:>12s} | '{:s}'".format(str(G).split()[0], G.name))

    n = G.number_of_nodes()
    m = G.number_of_edges()

    print("{:>12s} | {:,d} (iso={:,d})".format(
        'Nodes', n, nx.number_of_isolates(G)))
    print("{:>12s} | {:,d} (loop={:,d})".format(
        'Edges', m, nx.number_of_selfloops(G)))

    if G.is_directed():
        print("{:>12s} | {:.2f} max(in={:d}, out={:d})".format(
            'Degree', m / n, max(k for _, k in G.in_degree()),
            max(k for _, k in G.out_degree())))
    else:
        print("{:>12s} | {:.2f} (max={:,d})".format(
            'Degree', 2 * m / n, max((k for _, k in G.degree()))))

    C = list(nx.connected_components(nx.Graph(G) if G.is_directed else G))
    largest_comp = max(C, key=len)

    print("{:>12s} | {:.1f}% (n={:,d})".format(
        'LCC', 100 * len(largest_comp) / n, len(C)))

    if distance_sample is not None:
        G_lcc = G.subgraph(largest_comp)
        if n <= distance_sample:
            mean = nx.average_shortest_path_length(G_lcc)
            diam = nx.diameter(G_lcc)
        else:
            D = distances(G_lcc, n=distance_sample)
            mean = np.mean(D)
            diam = max(D)

        print("{:>12s} | {:.2f} (max={:,d})".format('Distance', mean, diam))

    if clustering_sample is not None:
        if isinstance(G, nx.MultiGraph):
            G = nx.Graph(G)

        clustering_on = G.nodes if n <= clustering_sample \
            else random.sample(list(G.nodes), k=clustering_sample)

        print("{:>12s} | {:.4f}".format(
            'Clustering', nx.average_clustering(G, clustering_on)))
    print()


def plot_degree(G: nx.Graph, save_path: str | None = None) -> None:
    """Plots degree distribution(s) on a log-log plot.
    If save_path is given, the plot will be saved in given folder/file
    instead of being shown."""
    plt.clf()
    plt.title(G.name + " degree distribution")
    plt.ylabel('$p_k$')
    plt.xlabel('$k$')
    n = G.number_of_nodes()

    def aux(degree_view: Iterable, k_min: int, **kwargs):
        degree_count = Counter(k for _, k in degree_view)
        k_max = max(degree_count.keys())

        x = list(range(k_min, k_max + 1))
        y = [degree_count[i] / n for i in x]
        plt.loglog(x, y, 'o', **kwargs)

    if G.is_directed():
        aux(G.out_degree, k_min=0, label="outdegree", color="pink")
        aux(G.in_degree, k_min=0, label="indegree", color="purple", alpha=0.5)
        plt.legend()
    else:
        aux(G.degree, k_min=1, color="gray")

    if save_path is None:
        plt.show()
    else:
        if len(os.path.splitext(save_path)[1]) == 0: # no extension
            plt.savefig(os.path.join(save_path, f"{G.name}_degree_distro.pdf"))
        else:
            plt.savefig(save_path)


def power_law(G: nx.Graph, kmin=10):
    """Maximum-likelihood estimate of gamma for a power-law degree
    distribution. If G is not a scale-free network, this estimate is
    effectively useless."""
    # see equation (4.41) in http://networksciencebook.com/chapter/4#advanced-c
    n = 0
    sumk = 0
    for _, k in G.degree():
        if k >= kmin:
            sumk += math.log(k)
            n += 1
    return 1 + 1 / (sumk / n - math.log(kmin - 0.5)) if n > 0 else math.nan


def draw_graph(G: nx.Graph, **kwargs):
    plt.title(G.name)
    nx.draw(G, with_labels=True, **kwargs)
    plt.show()


def find_node(G: nx.Graph, label: str):
    """Finds node with given label in G."""
    for i, data in G.nodes(data=True):
        if data['label'] == label:
            return i
    raise ValueError(f"node '{label}' not found in {G.name}")


def top_nodes(G: nx.Graph, C: Dict[Any, float], centrality: str, n=15) -> List[Any]:
    """prints and returns top n nodes by given measure of centrality"""

    # OPT take callable instead of dict, only compute centrality on non-mode nodes
    # OPT np.argpartition instead of sort
    print("{:>12s} | '{:s}'".format('Centrality', centrality))
    nodes = []
    for i, c in sorted(C.items(), key=lambda item: (item[1], G.degree[item[0]]), reverse=True):
        if not G.nodes[i]['label'].startswith('m-'):
            nodes.append(G.nodes[i])
            print("{:>12.6f} | '{:s}' ({:,d})".format(
                c, G.nodes[i]['label'], G.degree[i]))
            n -= 1
            if n == 0:
                break
    print()
    return nodes


def top_edges(G: nx.Graph, C: Dict[Tuple[Any, Any], float], centrality: str, n=15) -> List[Any]:
    """prints and returns top n edges by given measure of centrality"""
    print("{:>12s} | '{:s}'".format('Centrality', centrality))
    # OPT np.argpartition instead of sort
    for (i, j), c in sorted(C.items(), key = lambda item: item[1], reverse = True)[:n]:
        line = "{:>12.6f} | '{:s}' - '{:s}'".format(c, G.nodes[i]['label'], G.nodes[j]['label'])
        
        try: line += "({:,.0f})".format((G.nodes[i]['value'] + G.nodes[j]['value']) / 2)
        except: pass # no numeric values
        print(line)
    print()


def actor_names(nodes) -> List[str]:
    """Parses labels of nodes in collaboration_imdb.net into
    a nicer format. Try pasting the ouput of this function into
    chatGPT if you have trouble classifying the actors."""
    names = []
    for n in nodes:
        try:
            last, fst = n["label"].split(", ")
            if fst[-1] == ')':
                fst = fst[:fst.index('(') - 1]

            names.append(f"{fst} {last}")
        except ValueError: # failed unpacking
            names.append(n["label"])

    return names


def pagerank(G: nx.Graph, alpha=0.85, eps=1e-6, teleport: Set | None = None):
    P = [1 / len(G)] * len(G)
    diff = 1
    while diff > eps:
        U = [sum([P[j] * alpha / G.degree(j) for j in G[i]])
             for i in G.nodes()]
        u = sum(U)
        if teleport is not None:
            for i in teleport:
                U[i] += (1 - u) / len(teleport)
        else:
            U = [U[i] + (1 - u) / len(G) for i in G.nodes()]
        diff = sum([abs(P[i] - U[i]) for i in G.nodes()])
        P = U
    return {i: P[i] for i in range(len(P))}


def ER_random_graph(n: int, m: int) -> nx.MultiGraph:
    """Returns Erdős–Rényi random graph with n nodes and m edges."""
    G = nx.MultiGraph(name="ER")
    for i in range(n):
        G.add_node(i)

    edges = []
    while m > 0:
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        if i != j:
            # G.add_edge(i, j)
            edges.append((i, j))
            m -= 1

    G.add_edges_from(edges)  # avoids checking presence of edges
    return G


def known_clustering(G: nx.Graph, cluster_attr="value") -> NodeClustering:
    """Extracts known node clustering from their attrubute with supplied name."""

    C = defaultdict(list)
    for i, data in G.nodes(data=True):
        C[data[cluster_attr]].append(i)

    return NodeClustering(list(C.values()), G, "Known")


def CD_comparison(G: nx.Graph, algs: Dict[str, Callable[..., NodeClustering]], runs=1) -> None:
    """Compare quality of community-detection algorithms on G.
    Algorithms must conform to the cdlib format (returning a NodeClustering object)."""
    K = known_clustering(G)

    print("{:>12s} | {:5s} {:^6s}  {:^5s}  {:^5s}  {:^5s}".format(
        'Algorithm', 'Count', 'Q', 'NMI', 'ARI', 'VI'))

    for alg in algs:
        s, Q, NMI, ARI, VI = 0, 0, 0, 0, 0

        for _ in range(runs):
            C = algs[alg](G)
            s += len(C.communities) / runs # C.communities is a list of lists of node IDs
            Q += C.newman_girvan_modularity().score / runs
            NMI += K.normalized_mutual_information(C).score / runs
            ARI += K.adjusted_rand_index(C).score / runs
            VI += K.variation_of_information(C).score / runs

        print("{:>12s} | {:>5.0f} {:6.3f}  {:5.3f}  {:5.3f}  {:5.3f}".format(
            '\'' + alg + '\'', s, Q, NMI, ARI, VI))
    print()


def fast_label_propagation(G):
    assert (type(G) == nx.MultiGraph)

    N = list(G.nodes())
    random.shuffle(N)

    Q = deque(N)
    S = [True] * len(G)

    C = [i for i in range(len(G))]

    while Q:
        i = Q.popleft()
        S[i] = False

        if len(G[i]) > 0:
            L = {}
            for j in G[i]:
                if C[j] not in L:
                    L[C[j]] = 0
                L[C[j]] += len(G[i][j])

            maxl = max(L.values())
            c = random.choice([c for c in L if L[c] == maxl])

            if C[i] != c:
                C[i] = c

                for j in G[i]:
                    if C[j] != c and not S[j]:
                        Q.append(j)
                        S[j] = True

    L = {}
    for i in N:
        if C[i] in L:
            L[C[i]].append(i)
        else:
            L[C[i]] = [i]

    return NodeClustering(list(L.values()), G)
