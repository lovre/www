/**
 * 
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Deque;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Counting;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.ListGraph;
import si.lj.uni.fri.lna.entity.graph.Neighbors;
import si.lj.uni.fri.lna.entity.graph.Node;
import si.lj.uni.fri.lna.entity.graph.Ranking;
import si.lj.uni.fri.lna.entity.graph.Weighting;
import si.lj.uni.fri.lna.entity.utility.Pair;
import si.lj.uni.fri.lna.io.graph.Writers;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Nodes;
import si.lj.uni.fri.lna.logic.utility.Estimation;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.utility.Complexity;

/**
 * @author Lovro Subelj
 *
 */
public class IV {

	public static void main(String[] args) throws Exception {
		LNA.init();

		/* reads iMDB actors network */
		Graph graph = Generators.array(Generators.iMDB());
		
		/* computes and prints basic statistics */
		Information.println("\n         ... | GRAPH"); 
		Information.print(graph, true); Complexity.poc();
		
		/* finds and prints top random nodes */
		print(graph, randoms(graph), "random");
		
		/* finds and prints top degree nodes */
		print(graph, degrees(graph), "degree");
		
		/* finds and prints top clustering nodes */
		Pair<Ranking> clusterings = clusterings(graph);
		print(graph, clusterings.getFirst(), "clustering");
		print(graph, clusterings.getSecond(), "µ-clustering");
		
		/* finds and prints top eigenvector nodes */
		print(graph, eigenvectors(graph, 10e-12), "eigenvector");
		
		/* finds and prints top PageRank nodes */
		print(graph, pageranks(graph, 0.85, 10e-12), "PageRank");
		
		/* reduces network to largest WCC */
		graph = Generators.array(Generators.WCC(graph));
		
		/* computes and prints basic statistics */
		Information.println("\n         ... | GRAPH"); 
		Information.print(graph, true); Complexity.poc();
		
		/* finds and prints top closeness nodes */
		print(graph, closenesses(graph), "closeness");
		
		/* finds and prints top betweenness nodes */
		print(graph, Nodes.betweennesses(graph), "betweenness");
		
		LNA.exit();
	}
	
	static Ranking randoms(Graph graph) {
		Ranking randoms = new Ranking(graph);
		for (Node node: graph.getNodes())
			randoms.put(node, Math.random());
		
		return randoms;
	}
	
	static Ranking degrees(Graph graph) {
		Ranking degrees = new Ranking(graph);
		for (Node node: graph.getNodes())
			degrees.put(node, 1.0 * node.getDegree());
		
		return degrees;
	}
	
	static Pair<Ranking> clusterings(Graph graph) {
		return clusterings(graph, neighbors(graph));
	}
	
	static Pair<Ranking> clusterings(Graph graph, Neighbors neighbors) {
		Counting triads = triads(graph, neighbors);
		
		double mu = Estimation.maximum(triads.getWeights());
		
		Ranking clusterings = new Ranking(graph), dlusterings = new Ranking(graph);
		for (Node node: graph.getNodes())
			if (neighbors.get(node).size() > 1) {
				clusterings.put(node, triads.get(node) / (neighbors.get(node).size() * (neighbors.get(node).size() - 1.0)));
				dlusterings.put(node, triads.get(node) / (neighbors.get(node).size() * mu));
			}
			else {
				clusterings.put(node, 0.0);
				dlusterings.put(node, 0.0);
			}

		return new Pair<Ranking>(clusterings, dlusterings);
	}

	static Counting triads(Graph graph, Neighbors neighbors) {
		Counting triads = new Counting(graph);

		for (Node node: graph.getNodes())
			triads.put(node, 0);

		for (Node node: graph.getNodes())
			if (neighbors.get(node).size() > 1)
				for (int neighbor: neighbors.get(node))
					if (node.getIndex() < neighbor && neighbors.get(neighbor).size() > 1)
						if (neighbors.get(node).size() < neighbors.get(neighbor).size()) {
							for (int other: neighbors.get(node))
								if (neighbor != other && neighbors.get(neighbor).contains(other)) {
									triads.put(node, triads.get(node) + 1);
									triads.put(neighbor, triads.get(neighbor) + 1);
								}
						}
						else
							for (int other: neighbors.get(neighbor))
								if (node.getIndex() != other && neighbors.get(node).contains(other)) {
									triads.put(node, triads.get(node) + 1);
									triads.put(neighbor, triads.get(neighbor) + 1);
								}
		
		return triads;
	}
	
	static Neighbors neighbors(Graph graph) {
		Neighbors neighbors = new Neighbors(graph);
		
		for (Node node: graph.getNodes()) {
			neighbors.put(node, node.getUniqueNeighbors());
			neighbors.get(node).remove(node.getIndex());
		}
		
		return neighbors;
	}

	static Ranking eigenvectors(Graph graph, double epsilon) {
		Ranking eigenvectors = new Ranking(graph);
		for (Node node: graph.getNodes())
			eigenvectors.put(node, 1.0);
		
		double difference, normalization;
		do {
			difference = 0.0; normalization = 0.0;
			
			Ranking updated = new Ranking(graph);
			for (Node node: graph.getNodes()) {
				updated.put(node, 0.0);
				if (graph.isDirected())
					for (int predecessor: graph.getPredecessors(node))
						updated.put(node, updated.get(node) + eigenvectors.get(predecessor));
				else {
					for (int predecessor: graph.getPredecessors(node))
						updated.put(node, updated.get(node) + eigenvectors.get(predecessor));

					for (int successor: graph.getSuccessors(node))
						updated.put(node, updated.get(node) + eigenvectors.get(successor));
				}
				
				normalization += updated.get(node);
			}	
			
			for (Node node: graph.getNodes())
				updated.put(node, updated.get(node) * graph.getN() / normalization);
			
			for (Node node: graph.getNodes())
				difference += Math.abs(updated.get(node) - eigenvectors.get(node));
			
			eigenvectors = updated;
		} while (difference >= epsilon);
		
		return eigenvectors;
	}
	
	static Ranking pageranks(Graph graph, double damping, double epsilon) {
		Ranking pageranks = new Ranking(graph);
		for (Node node: graph.getNodes())
			pageranks.put(node, 1.0 / graph.getN());
		
		double difference, unleaked;
		do {
			difference = 0.0; unleaked = 0.0;
			
			Ranking updated = new Ranking(graph);
			for (Node node: graph.getNodes()) {
				updated.put(node, 0.0);
				if (graph.isDirected())
					for (int predecessor: graph.getPredecessors(node))
						updated.put(node, updated.get(node) + damping * pageranks.get(predecessor) / graph.getOutDegree(predecessor));
				else {
					for (int predecessor: graph.getPredecessors(node))
						updated.put(node, updated.get(node) + damping * pageranks.get(predecessor) / graph.getDegree(predecessor));

					for (int successor: graph.getSuccessors(node))
						updated.put(node, updated.get(node) + damping * pageranks.get(successor) / graph.getDegree(successor));
				}

				unleaked += updated.get(node);
			}	
			
			for (Node node: graph.getNodes())
				updated.put(node, updated.get(node) + (1.0 - unleaked) / graph.getN());
			
			for (Node node: graph.getNodes())
				difference += Math.abs(updated.get(node) - pageranks.get(node));
			
			pageranks = updated;
		} while (difference >= epsilon);
		
		return pageranks;
	}
	
	static Ranking closenesses(Graph graph) {
		Ranking closenesses = new Ranking(graph);
		
		for (Node source: graph.getNodes()) {
			double closeness = 0.0;
			
			Counting distances = new Counting(graph); distances.put(source, 0);
			Deque<Integer> nodes = new ArrayDeque<Integer>(Arrays.asList(new Integer[] { source.getIndex() }));
			while (nodes.size() > 0) {
				int node = nodes.remove();
				
				for (int neighbor: graph.getNeighbors(node))
					if (!distances.contains(neighbor)) {
						distances.put(neighbor, distances.get(node) + 1);
						nodes.add(neighbor);
						
						closeness += 1.0 / distances.get(neighbor);
					}
			}
			
			closenesses.put(source.getIndex(), closeness / (graph.getN() - 1.0));
		}
		
		return closenesses;
	}
	
	static void parse() throws Exception {
		/* creates an empty graph */
		Graph graph = new ListGraph("iMDB");

		/* map of node indices */
		Map<Integer, Integer> nodes = new HashMap<Integer, Integer>();
		
		/* creates node for each actor */
		BufferedReader reader = new BufferedReader(new FileReader("/Users/lovre/Downloads/imdb_actors_key.tsv"));
		
		String line = reader.readLine();
		while ((line = reader.readLine()) != null) {
			String[] array = line.split("\t");
			
			int node = graph.addNode(array[1].substring(1, array[1].length() - 1));
			
			nodes.put(Integer.parseInt(array[0]), node);
		}
		
		reader.close();
		
		/* creates links based on actor collaborations */
		reader = new BufferedReader(new FileReader("/Users/lovre/Downloads/imdb_actor_edges.tsv"));
		
		while ((line = reader.readLine()) != null) {
			String[] array = line.split("\t");
			
			graph.addEdge(nodes.get(Integer.parseInt(array[0])), nodes.get(Integer.parseInt(array[1])));
		}
		
		reader.close();
		
		/* saves graph in LNA format */
		Writers.net(graph);
	}
	
	public static void print(final Graph graph, final Weighting<?> ranking, String title) throws Exception {
		/* creates list of nodes */
		List<Integer> nodes = new ArrayList<Integer>();
		for (Node node: graph.getNodes())
			nodes.add(node.getIndex());
		
		/* sorts nodes due to ranks */
		Collections.sort(nodes, new Comparator<Integer>() {
			@Override
			public int compare(Integer first, Integer second) {
				if (ranking.get(first).equals(ranking.get(second))) {
					if (graph.getNode(first).getDegree() == graph.getNode(second).getDegree())
						return graph.getNode(first).getLabel().compareTo(graph.getNode(second).getLabel());
					return -new Integer(graph.getNode(first).getDegree()).compareTo(graph.getNode(second).getDegree());
				}
				return -new Double(ranking.get(first).doubleValue()).compareTo(ranking.get(second).doubleValue());
			}
		});
		
		/* prints top ranked nodes */
		Information.println("\n         ... | " + title.toUpperCase() + "\n");
		for (int i = 0; i < 25; i++)
			Information.println(String.format("  %10f | '%s' (%d)", ranking.get(nodes.get(i)).doubleValue(), graph.getNode(nodes.get(i)).getLabel(), graph.getNode(nodes.get(i)).getDegree()));
		
		/* prints time and memory */
		Complexity.poc();
	}
	
}
