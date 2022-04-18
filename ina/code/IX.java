/**
 * 
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.awt.Color;
import java.awt.Font;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Clustering;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.Layout;
import si.lj.uni.fri.lna.entity.graph.Metric;
import si.lj.uni.fri.lna.entity.graph.Node;
import si.lj.uni.fri.lna.entity.utility.Pair;
import si.lj.uni.fri.lna.io.graph.Readers;
import si.lj.uni.fri.lna.logic.graph.Clusters;
import si.lj.uni.fri.lna.logic.graph.Communities;
import si.lj.uni.fri.lna.logic.graph.Components;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Groups;
import si.lj.uni.fri.lna.logic.graph.Layouts;
import si.lj.uni.fri.lna.logic.graph.Metrics;
import si.lj.uni.fri.lna.logic.graph.Nodes;
import si.lj.uni.fri.lna.logic.utility.Comparison;
import si.lj.uni.fri.lna.logic.utility.Generation;
import si.lj.uni.fri.lna.logic.utility.Implementation;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.logic.utility.Visualization;
import si.lj.uni.fri.lna.utility.Complexity;
import si.lj.uni.fri.lna.utility.Uncertainty;
import si.lj.uni.fri.lna.utility.Utility;
import de.erichseifert.vectorgraphics2d.PDFGraphics2D;

/**
 * @author Lovro Subelj
 *
 */
public class IX {
	
	public static void main(String[] args) throws Exception {
		LNA.init();
		
		/* implementations of stochastic block models & Infomap method */
		List<Implementation<Clustering>> implementations = new ArrayList<Implementation<Clustering>>();
		implementations.add(new Implementation<Clustering>("Truth") {
			public Clustering run(Graph graph) throws Exception { return Clusters.clustering(graph); }});
		implementations.add(new Implementation<Clustering>("Infomap") { 
			public Clustering run(Graph graph) throws Exception { return Communities.infomap(graph); }});
		implementations.add(new Implementation<Clustering>("SBM") { 
			public Clustering run(Graph graph) throws Exception { return Groups.blocks(graph, false); }});
		implementations.add(new Implementation<Clustering>("DCSBM") { 
			public Clustering run(Graph graph) throws Exception { return Groups.blocks(graph, true); }});

		String folder = "/Users/lovre/Documents/office/coding/repositories/www/ina/";
		
		/* small social networks with sociological partitioning */
		List<Graph> graphs = new ArrayList<Graph>();
		graphs.add(Readers.pajek(folder + "karate_club.net")); 
		/* graphs.add(Readers.pajek(folder + "southern_women.net")); */
		graphs.add(Generators.women());
		
		/* stochastic blockmodeling & community detection in social networks */
		for (Graph graph: graphs)
			Comparison.metrics(info(graph), implementations, 100);
		
		/* visualizes results of stochastic blockmodeling & community detection */
		for (Graph graph: graphs) {
			Layout layout = Layouts.LGL(graph); Utility.SIZE = 32; Utility.LABEL = 10;
			PDFGraphics2D graphics = new PDFGraphics2D(0, 0, 2 * layout.getWidth(), 2 * layout.getHeight()); 
			graphics.setColor(Color.WHITE); graphics.fillRect(0, 0, 2 * layout.getWidth(), 2 * layout.getHeight());  
			for (int i = 0; i < implementations.size(); i++) {
				int x = i % 2 == 1? layout.getWidth(): 0, y = i >= 2? layout.getHeight(): 0;
				graphics.setColor(Color.BLACK); graphics.setFont(new Font(Utility.FONT, Font.BOLD, 24));
				graphics.drawString(implementations.get(i).getName(), x + 48, y + 48);
				Visualization.layout(graph, layout, Visualization.coloring(implementations.get(i).run(graph)), x, y, graphics);
			}
			FileOutputStream stream = new FileOutputStream("/Users/lovre/Desktop/" + graph.getName() + ".pdf");
			stream.write(graphics.getBytes()); stream.flush(); stream.close();
		}
		
		/* stochastic blockmodeling & community detection in SB synthetic graphs */
		Comparison.metrics(new Generation("SB", 11) { 
			public String name() { return "Mixing"; } public String name(int index) { return String.format("%12.2f | ", 0.05 * index); } 
			public Graph graph(int index) throws Exception { return Generators.array(SB(0.05 * index)); }
		}, implementations, Metric.NMI, 10);
		
		/* larger networks with node labels */ graphs.clear();
		graphs.add(Readers.pajek(folder + "cdn_jung.net"));
		graphs.add(Readers.pajek(folder + "cdn_java.net"));
		graphs.add(Readers.pajek(folder + "wikileaks.net"));
		graphs.add(Readers.pajek(folder + "collaboration_imdb.net"));
		
		/* k-core decomposition of larger networks */
		for (Graph graph: graphs) {
			Graph cores = Generators.map(graph = info(graph));
			Information.println("\n         ... | ANALYSIS\n"); 
			int k = 0; while (true) {
				Pair<Integer> WCCs = Metrics.WCCs(cores = cores(cores, k));
				Information.println(String.format("%6d-cores | %d (%d nodes)", k, WCCs.getFirst(), WCCs.getFirst() == 0? 0: WCCs.getSecond()));
				if (WCCs.getFirst() == 0) { k--; break; } else k++;
			}
			cores = cores(Generators.map(graph), k);
			List<Set<Integer>> WCCs = Components.WCCs(cores);
			for (int i = 0; i < WCCs.size(); i++) {
				List<String> labels = new ArrayList<String>();
				for (int node: WCCs.get(i)) labels.add(cores.getNode(node).getLabel());
				Collections.sort(labels);
				for (int j = 0; j < labels.size(); j++)
					Information.print((j == 0? i == 0? String.format("\n%6d-cores | {", k): "             | {": "") + labels.get(j) + (j == labels.size() - 1? "}\n": "; "));
			}
			Complexity.poc();
		}
		
		LNA.exit();
	}
	
	static Graph info(Graph graph) throws Exception {
		graph = Generators.array(graph);
		
		Information.println("\n         ... | GRAPH"); 
		Information.print(graph, true); Complexity.poc();
		
		return graph;
	}
	
	static Graph cores(Graph graph, int k) {
		boolean removed = true; 
		while (removed) {
			removed = false; 
			for (int node: Nodes.nodes(graph))
				if (graph.getNode(node).getDegree() < k) {
					graph.removeNode(node);
					removed = true;
				}
		}
		
		return graph;
	}
	
	static Graph SB(double random) {
		Graph graph = Generators.isolate("SB_benchmark", 128);
		for (Node node: graph.getNodes())
			node.setCluster(node.getIndex() / 32 + 1);

		for (int i = 0; i < 128; i++)
			for (int j = i + 1; j < 128; j++)
				if (i < 64 && j < 64) {
					if (Uncertainty.binary(i / 32 == j / 32? 16.0 * (1.0 - random) / 31.0: random / 6.0))
						graph.addEdge(i, j);
				}
				else if (i >= 64 && j >= 64) {
					if (Uncertainty.binary(i / 32 != j / 32? 0.5 - 0.5 * random: random / 6.0))
						graph.addEdge(i, j);
				}
				else if (Uncertainty.binary(random / 6.0))
					graph.addEdge(i, j);

		return graph;
	}

}
