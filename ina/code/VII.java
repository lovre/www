/**
 *
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.util.ArrayList;
import java.util.List;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Edge;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.Node;
import si.lj.uni.fri.lna.entity.graph.Ranking;
import si.lj.uni.fri.lna.entity.utility.Pair;
import si.lj.uni.fri.lna.entity.utility.Quintuple;
import si.lj.uni.fri.lna.io.graph.Readers;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Nodes;
import si.lj.uni.fri.lna.logic.utility.Estimation;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.utility.Complexity;
import si.lj.uni.fri.lna.utility.Uncertainty;
import si.lj.uni.fri.lna.utility.Utility;

/**
 * @author Lovro Subelj
 *
 */
public class VII {
	
	static List<Graph> graphs = new ArrayList<Graph>();

	public static void main(String[] args) throws Exception {
		LNA.init();
		
		String folder = "/Users/lovre/Documents/office/coding/repositories/www/ina/nets";
		
		/* networks from labs */
		info(Readers.pajek(folder + "/toy.net"));
		info(Readers.pajek(folder + "/karate_club.net").setName("karate"));
		info(Readers.pajek(folder + "/java.net"));
		info(Readers.pajek(folder + "/collaboration_imdb.net").setName("imdb"));
		info(Readers.pajek(folder + "/facebook.net"));
		info(Readers.pajek(folder + "/nec.net").setName("internet"));
		info(Readers.pajek(folder + "/www_google.net").setName("google"));
		
		/* toy example network */
		Graph estrada = Generators.isolate("estrada", 8);
		estrada.addEdge(0, 1); estrada.addEdge(0, 3); estrada.addEdge(0, 5);
		estrada.addEdge(1, 2); estrada.addEdge(1, 4); estrada.addEdge(2, 3);
		estrada.addEdge(2, 5); estrada.addEdge(3, 4); estrada.addEdge(4, 5);
		estrada.addEdge(3, 6); /* estrada.addEdge(6, 7); */ info(estrada);
		
		/* small social networks */
		info(Generators.football().setName("football"));
		info(Generators.women().setName("women"));
		
		/* random graph models */
		info(Generators.random(10000, 16.0).setName("random"));
		// info(Generators.forestfire(10000, 16.0).setName("forestfire"));
		info(Generators.scalefree(10000, 16.0).setName("scalefree"));
		info(Generators.copying(10000, 16.0).setName("copying"));
		
		/* social collaboration networks */
		info(Readers.net(Utility.NETWORK_FOLDER + "/copurchase_amazon").setName("amazon"));
		
		/* citation & reference networks */
		// info(Readers.net(Utility.NETWORK_FOLDER + "/citation_wiki_embs").setDirected().setName("wikileaks"));
		info(Readers.net(Utility.NETWORK_FOLDER + "/citation_aps").setDirected().setName("aps"));
		
		/* protein-protein interaction network */
		info(Readers.net(Utility.NETWORK_FOLDER + "/ppi_homo_all1").setName("proteins"));
		
		/* Internet & P2P technological networks */
		info(Readers.net(Utility.NETWORK_FOLDER + "/p2p_gnutella").setDirected().setName("gnutella"));
		
		/* software dependency networks */
		info(Readers.net(Utility.NETWORK_FOLDER + "/cdn_lucene").setDirected().setName("lucene"));
		
		/* web graph network */
		info(Readers.net(Utility.NETWORK_FOLDER + "/www_petrol").setDirected().setName("petrol"));
		
		/* analysis of node degree and clustering mixing */
		Information.println("\n         ... | MIXING");
		
		int number = 10; Information.print(number);
		
		/* analysis of undirected degree mixing */
		Information.println("\n     Network |    r     r(S)   r(M)");

		for (Graph graph: graphs)
			if (number == 0 || graph.getM() < 1.5e6){
				Information.print(String.format("%12s | ", "'" + graph.getName() + "'"));

				/* computes undirected degree mixing */
				Information.print(String.format("%6.3f ", mixing(graph = simple(graph))));

				/* degree mixing after simple graph rewiring */
				double simple = 0.0;
				for (int i = 0; i < number; i++)
					simple += mixing(rewire(graph, true));

				Information.print(String.format("%6.3f ", simple / number));

				/* degree mixing after multigraph rewiring */
				double multi = 0.0;
				for (int i = 0; i < number; i++)
					multi += mixing(rewire(graph, false));

				Information.println(String.format("%6.3f", multi / number));
			}

		Complexity.poc();
		
		/* analysis of directed degree mixing */
		Information.println("\n     Network |    r    r(ii)  r(io)  r(oi)  r(oo)");

		for (Graph graph: graphs)
			if (graph.isDirected()) {
				Information.print(String.format("%12s | ", "'" + graph.getName() + "'"));

				/* computes directed degree mixings */
				Quintuple<Double> mixings = mixings(graph);

				Information.println(String.format("%6.3f %6.3f %6.3f %6.3f %6.3f", mixings.getFirst(), mixings.getSecond(), mixings.getThird(), mixings.getFourth(), mixings.getFifth()));
			}

		Complexity.poc();
		
		/* analysis of (corrected) clustering mixing */
		Information.println("\n     Network |    r      C        D      r(C)   r(D)");

		for (Graph graph: graphs) {
			Information.print(String.format("%12s | ", "'" + graph.getName() + "'"));
			
			/* computes undirected degree mixing */
			Information.print(String.format("%6.3f ", mixing(graph)));

			/* computes (corrected) clustering mixings */
			Pair<Ranking> clusterings = Nodes.clusterings(graph);
			
			Information.println(String.format("%6.3f %9.6f %6.3f %6.3f", Estimation.average(clusterings.getFirst()), Estimation.average(clusterings.getSecond()), mixing(graph, clusterings.getFirst()), mixing(graph, clusterings.getSecond())));
		}

		Complexity.poc();
		
		LNA.exit();
	}
	
	static void info(Graph graph) throws Exception {
		graphs.add(graph = Generators.array(graph));
		
		Information.println("\n         ... | GRAPH");
		Information.print(graph, false); Complexity.poc();
	}
	
	static Graph simple(Graph graph) {
		if (graph.isUndirected())
			return Generators.simple(graph);
		
		Graph simple = Generators.simple(graph.setUndirected());
		graph.setDirected();
		
		return simple;
	}
	
	static Graph rewire(Graph graph, boolean simple) {
		Graph rewire = Generators.bag(graph);
		
		/* stores nodes degree times */
		List<Integer> nodes = new ArrayList<Integer>();
		for (Node node: rewire.getNodes())
			for (int i = 0; i < node.getDegree(); i++)
				nodes.add(node.getIndex());
		
		/* randomly rewires links in network */
		Pair<Edge> edges; int rewirings = 0, node;
		while (rewirings < 10 * rewire.getM()) {
			/* randomly selects two distinct links */
			Edge first = new Edge(node = Uncertainty.random(nodes), rewire.getNeighbor(node), rewire), second;
			do second = new Edge(node = Uncertainty.random(nodes), rewire.getNeighbor(node), rewire); while (first.equals(second));
			
			/* randomly constructs two rewired links */
			if (Uncertainty.binary())
				edges = new Pair<Edge>(new Edge(first.getFirst(), second.getSecond(), rewire), new Edge(second.getFirst(), first.getSecond(), rewire));
			else
				edges = new Pair<Edge>(new Edge(first.getFirst(), second.getFirst(), rewire), new Edge(first.getSecond(), second.getSecond(), rewire));
			
			/* if required ensures simple graph */
			if (!simple || (!edges.getFirst().isLoop() && !edges.getSecond().isLoop() && !rewire.isEdge(edges.getFirst()) && !rewire.isEdge(edges.getSecond()))) {
				/* updates rewired links in network */
				rewire.addEdge(edges.getFirst()); rewire.addEdge(edges.getSecond());
				rewire.removeEdge(first); rewire.removeEdge(second);
			}
			
			rewirings++;
		}
		
		return rewire;
	}

	static Quintuple<Double> mixings(Graph graph) {
		List<Double> first = new ArrayList<Double>(), second = new ArrayList<Double>();
		for (Edge edge: graph.getEdges()) {
			first.add(1.0 * edge.getFirst().getDegree()); first.add(1.0 * edge.getSecond().getDegree());
			second.add(1.0 * edge.getSecond().getDegree()); second.add(1.0 * edge.getFirst().getDegree());
		}
		
		double mixing = pearson(first, second);
		
		first.clear(); second.clear();
		for (Edge edge: graph.getEdges()) {
			first.add(1.0 * edge.getFirst().getInDegree());
			second.add(1.0 * edge.getSecond().getInDegree());
		}
		
		double inInMixing = pearson(first, second);
		
		second.clear();
		for (Edge edge: graph.getEdges())
			second.add(1.0 * edge.getSecond().getOutDegree());
		
		double inOutMixing = pearson(first, second);
		
		first.clear();
		for (Edge edge: graph.getEdges())
			first.add(1.0 * edge.getFirst().getOutDegree());
		
		double outOutMixing = pearson(first, second);
		
		second.clear();
		for (Edge edge: graph.getEdges())
			second.add(1.0 * edge.getSecond().getInDegree());
		
		return new Quintuple<Double>(mixing, inInMixing, inOutMixing, pearson(first, second), outOutMixing);
	}
	
	public static double mixing(Graph graph, Ranking ranking) {
		List<Double> first = new ArrayList<Double>(), second = new ArrayList<Double>();
		for (Edge edge: graph.getEdges()) {
			first.add(ranking.get(edge.getFirst())); second.add(ranking.get(edge.getSecond()));
			first.add(ranking.get(edge.getSecond())); second.add(ranking.get(edge.getFirst()));
		}
		
		return pearson(first, second);
	}
	
	static double mixing(Graph graph) {
		List<Double> first = new ArrayList<Double>(), second = new ArrayList<Double>();
		for (Edge edge: graph.getEdges()) {
			first.add(1.0 * edge.getFirst().getDegree()); second.add(1.0 * edge.getSecond().getDegree());
			first.add(1.0 * edge.getSecond().getDegree()); second.add(1.0 * edge.getFirst().getDegree());
		}
		
		return pearson(first, second);
	}
	
	static double mean(List<Double> values) {
		double sum = 0.0;
		for (int i = 0; i < values.size(); i++)
			sum += values.get(i);
		
		return sum / values.size();
	}
	
	static double deviation(List<Double> values, double mean) {
		double variance = 0.0;
		for (int i = 0; i < values.size(); i++)
			variance += (values.get(i) - mean) * (values.get(i) - mean);
		
		return Math.sqrt(variance / values.size());
	}
	
	static double pearson(List<Double> first, List<Double> second) {
		double product = 0.0;
		for (int i = 0; i < first.size(); i++)
			product += first.get(i) * second.get(i);
		
		double firstMean = mean(first), secondMean = mean(second);
		return (product / first.size() - firstMean * secondMean) / (deviation(first, firstMean) * deviation(second, secondMean));
	}
	
}
