/**
 * 
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.util.ArrayList;
import java.util.List;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.utility.Pair;
import si.lj.uni.fri.lna.io.graph.Readers;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.utility.Complexity;

/**
 * @author Lovro Subelj
 *
 */
public class XII {

	public static void main(String[] args) throws Exception {
		LNA.init();
		
		String folder = "/Users/lovre/Documents/office/coding/repositories/www/ina/nets/";
		
		/* samples of Internet, Facebook, Enron and Google */
		List<Graph> graphs = new ArrayList<Graph>();
		graphs.add(Readers.pajek(folder + "nec.net"));
		graphs.add(Readers.pajek(folder + "facebook.net"));
		graphs.add(Readers.pajek(folder + "enron.net"));
		graphs.add(Readers.pajek(folder + "www_google.net"));
		
		/* degree estimation by random-walk sampling */
		double sample = 0.15; for (Graph graph: graphs) {
			Pair<Double> estimation = estimation(graph = info(graph, true), sample); Information.println("\n         ... | ESTIMATION\n");
			Information.println(String.format("%12s | %.1f%%\n%12s | %.2f", "Sample", 100 * sample, "Degree", graph.getDegree()));
			Information.println(String.format("%12s | %.2f\n%12s | %.2f", "Estimate", estimation.getFirst(), "Corrected", estimation.getSecond()));
			Complexity.poc();
		}
		
		/* snowball and rejection samples of Facebook */
		info(Readers.list(folder + "facebook_1.adj"));
		info(Readers.list(folder + "facebook_2.adj"));
		
		LNA.exit();
	}
	
	static Graph info(Graph graph) throws Exception {
		return info(graph, false);
	}
	
	static Graph info(Graph graph, boolean normal) throws Exception {
		graph = Generators.array(normal? Generators.normal(graph.setUndirected(), true): graph);
		
		Information.println("\n         ... | GRAPH"); 
		Information.print(graph, true); Complexity.poc();
		
		return graph;
	}
	
	static Pair<Double> estimation(Graph graph, double sample) {
		int node = graph.getNode(), nodes = 0;
		double estimate = 0.0, corrected = 0.0;
		while (nodes++ < sample * graph.getN()) {
			node = graph.getNeighbor(node);
			
			estimate += graph.getDegree(node);
			corrected += 1.0 / graph.getDegree(node);
		}
		
		return new Pair<Double>(estimate / nodes, nodes / corrected);
	}
	
}
