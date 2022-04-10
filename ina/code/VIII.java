/**
 * 
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.SortedMap;
import java.util.TreeMap;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Clustering;
import si.lj.uni.fri.lna.entity.graph.Edge;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.ListGraph;
import si.lj.uni.fri.lna.entity.graph.Metric;
import si.lj.uni.fri.lna.entity.graph.Node;
import si.lj.uni.fri.lna.entity.graph.Ranking;
import si.lj.uni.fri.lna.io.graph.Readers;
import si.lj.uni.fri.lna.logic.graph.Clusters;
import si.lj.uni.fri.lna.logic.graph.Communities;
import si.lj.uni.fri.lna.logic.graph.Components;
import si.lj.uni.fri.lna.logic.graph.Edges;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Nodes;
import si.lj.uni.fri.lna.logic.utility.Comparison;
import si.lj.uni.fri.lna.logic.utility.Estimation;
import si.lj.uni.fri.lna.logic.utility.Generation;
import si.lj.uni.fri.lna.logic.utility.Implementation;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.utility.Complexity;
import si.lj.uni.fri.lna.utility.Uncertainty;

/**
 * @author Lovro Subelj
 *
 */
public class VIII {
	
	public static void main(String[] args) throws Exception {
		LNA.init();
		
		/* implementations of community detection algorithms */
		List<Implementation<Clustering>> implementations = new ArrayList<Implementation<Clustering>>();
		implementations.add(new Implementation<Clustering>("Truth") {
			public Clustering run(Graph graph) throws Exception { return Clusters.clustering(graph); }});
		implementations.add(new Implementation<Clustering>("Labels") { 
			public Clustering run(Graph graph) throws Exception { return labels(graph); }});
		implementations.add(new Implementation<Clustering>("Louvain") {  
			public Clustering run(Graph graph) throws Exception { return Communities.louvain(graph); }});
		implementations.add(new Implementation<Clustering>("Infomap") { 
			public Clustering run(Graph graph) throws Exception { return Communities.infomap(graph); }});
		implementations.add(new Implementation<Clustering>("Graclus") { 
			public Clustering run(Graph graph) throws Exception { return Communities.graclus(graph); }});
		implementations.add(new Implementation<Clustering>("Between") { 
			public Clustering run(Graph graph) throws Exception { return betweenness(graph); }});
		
		String folder = "/Users/lovre/Documents/office/coding/repositories/www/ina/";
		
		/* small social networks with sociological partitioning */
		List<Graph> graphs = new ArrayList<Graph>();
		graphs.add(Readers.pajek(folder + "karate_club.net")); 
		graphs.add(Readers.pajek(folder + "american_football.net"));
		graphs.add(Readers.pajek(folder + "dolphins.net")); 
		graphs.add(Readers.pajek(folder + "southern_women.net"));  
		
		/* community detection in small social networks */
		for (Graph graph: graphs)
			Comparison.metrics(info(graph), implementations, 100);
		
		/* larger networks with node metadata */ graphs.clear();
		graphs.add(Readers.pajek(folder + "cdn_java.net"));
		graphs.add(Readers.pajek(folder + "dormitory.net"));
		graphs.add(Readers.pajek(folder + "wikileaks.net"));
		graphs.add(Readers.pajek(folder + "youtube.net"));
		
		/* community detection in larger networks */
		for (Graph graph: graphs)
			Comparison.metrics(info(graph), implementations.subList(0, 4), 10);
		
		/* community detection in GN synthetic graphs */
		Comparison.metrics(new Generation("GN", 11) { 
			public String name() { return "Mixing"; } public String name(int index) { return String.format("%12.2f | ", 0.05 * index); } 
			public Graph graph(int index) throws Exception { return Generators.array(GN(0.05 * index)); }
		}, implementations.subList(0, 4), Metric.NMI, 25);
		
		/* community detection in LFR synthetic graphs */
		Comparison.metrics(new Generation("LFR", 9) { 
			public String name() { return "Mixing"; } public String name(int index) { return String.format("%12.2f | ", 0.1 * index); } 
			public Graph graph(int index) throws Exception { return Generators.array(Generators.LFR(1000, 0.1 * index)); }
		}, implementations.subList(0, 4), Metric.NMI, 10);
		
		/* community detection in random graphs */
		Comparison.metrics(new Generation("ER", 9) { 
			public String name() { return "Degree"; } public String name(int index) { return String.format("%12.1f | ", 8.0 + 4.0 * index); } 
			public Graph graph(int index) throws Exception { return Generators.array(Generators.random(1000, 8.0 + 4.0 * index)); }}, 
			implementations.subList(0, 4), Metric.NMI, 10);
		
		LNA.exit();
	}
	
	static Graph info(Graph graph) throws Exception {
		graph = Generators.array(graph);
		
		Information.println("\n         ... | GRAPH"); 
		Information.print(graph, true); Complexity.poc();
		
		return graph;
	}

	static Graph GN(double random) {
		ListGraph graph = Generators.isolate("GN", 128);
		for (Node node: graph.getNodes())
			node.setCluster(node.getIndex() / 32);

		for (int i = 0; i < 128; i++)
			for (int j = i + 1; j < 128; j++)
				if (Uncertainty.binary(i / 32 == j / 32? 16.0 * (1.0 - random) / 31.0: random / 6.0))
					graph.addEdge(i, j);
				
		return graph;
	}
	
	static Clustering labels(Graph graph) {
		Clustering clustering = new Clustering(graph);
		
		Ranking ranking = new Ranking(graph);
		List<Integer> nodes = Nodes.nodes(graph);
		for (int node: nodes) {
			clustering.put(node, node);
			ranking.put(node, 1.0);
		}

		boolean converged = false;
		while (!converged) {
			Collections.shuffle(nodes);

			converged = true;
			for (int node: nodes) 
				if (graph.getDegree(node) > 0) {
					Map<Integer, Double> clusters = new HashMap<Integer, Double>();
					for (int neighbor: graph.getNeighbors(node))
						if (clusters.containsKey(clustering.get(neighbor)))
							clusters.put(clustering.get(neighbor), clusters.get(clustering.get(neighbor)) + ranking.get(neighbor));
						else
							clusters.put(clustering.get(neighbor), ranking.get(neighbor));

					double maximum = Estimation.maximum(clusters.values());
					if (!clusters.containsKey(clustering.get(node)) || clusters.get(clustering.get(node)) < maximum) {
						List<Integer> labels = new ArrayList<Integer>();
						for (int label: clusters.keySet())
							if (clusters.get(label) == maximum)
								labels.add(label);
						
						clustering.put(node, Uncertainty.random(labels));

						converged = false;
					}
				}
		}

		return clustering;
	}

	static Clustering betweenness(Graph graph) {
		Clustering clustering = new Clustering(graph);

		Graph copy = Generators.bag(graph).setUndirected();
		
		double Q = -Double.MAX_VALUE;
		while (copy.getM() > 0) {
			Map<Edge, Double> betweennesses = Edges.betweennesses(copy);
			double maximum = Estimation.maximum(betweennesses.values());
			
			List<Edge> edges = new ArrayList<Edge>();
			for (Edge edge: betweennesses.keySet())
				if (betweennesses.get(edge) == maximum)
					edges.add(edge);

			copy.removeEdge(Uncertainty.random(edges));

			SortedMap<Integer, Set<Integer>> clusters = new TreeMap<Integer, Set<Integer>>();
			for (Set<Integer> component: Components.WCCs(copy))
				clusters.put(clusters.size() + 1, component);

			double q = Clusters.Q(graph, clusters);
			if (q > Q) {
				clustering = Clusters.clustering(graph, clusters);
				Q = q;
			}
		}

		return clustering;
	}

}
