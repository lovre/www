/**
 * 
 */
package si.lj.uni.fri.lna.test.ina.labs;

import java.awt.Color;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.List;

import de.erichseifert.vectorgraphics2d.PDFGraphics2D;
import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Edge;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.Layout;
import si.lj.uni.fri.lna.entity.graph.Node;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Layouts;
import si.lj.uni.fri.lna.logic.graph.Nodes;
import si.lj.uni.fri.lna.logic.utility.Configuration;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.logic.utility.Visualization;
import si.lj.uni.fri.lna.utility.Complexity;
import si.lj.uni.fri.lna.utility.Uncertainty;
import si.lj.uni.fri.lna.utility.Utility;

/**
 * @author Lovro Subelj
 *
 */
public class VI {

	public static void main(String[] args) throws Exception {
		LNA.init();
		
		/* selected parameters of scale-free graphs */
		double[] gammas = new double[] {2.01, 2.33, 2.66, 3.0, 4.0, 5.0};
		int n = 1000000; double k = 16.0; int number = 25;
		
		/* prints out basic statistics of Price graph */
		Information.info(price(n, k, 2.5), true);
		
		/* visualizes Price scale-free graphs */
		for (double gamma: gammas)
			visualize(price(250, 8.0, gamma), gamma);
		
		/* prints out basic statistics of Barabasi graph */
		Information.info(barabasi(n, k), true);
		
		/* visualizes Barabasi scale-free graph */
		visualize(barabasi(250, 8.0));
		
		/* computes statistics and plots scale-free graphs */
		scalefree(n, k, gammas, number);
		
		LNA.exit();
	}
	
	static void scalefree(int n, double k, double[] gammas, int number) throws Exception {
		Information.println("\n         ... | GRAPH"); 
		
		/* prints out default statistics of scale-free graph */
		Information.print(Generators.array(scalefree(n, k))); 
		
		Complexity.poc();
		
		Information.println("\n         ... | COMPARE"); Information.print(number);
		Information.println("\n       a (c) | 2+a/c  Gamma");
		
		/* prints out power-law exponents of scale-free graphs */
		List<Graph> graphs = new ArrayList<Graph>(); String[] labels = new String[gammas.length];
		for (double gamma: gammas) {
			Information.print(String.format("%8.2f (%d) | ", 0.5 * k * gamma - k, (int)Math.round(0.5 * k)));
			
			double exponent = 0.0;
			for (int i = 0; i < number; i++) {
				/* generates scale-free graph with given parameters */
				Graph graph = scalefree(n, k, gamma);
				
				/* computes power-law exponent of generated scale-free graph */
				exponent += gamma(graph) / number;
				
				if (i == 0) {
					/* stores generated scale-free graph for plotting */
					graphs.add(graph); labels[graphs.size() - 1] = " " + graph.getName() + " (" + String.format("%.2f", gamma) + ")";
				}
			}
			
			/* prints out power-law exponents of generated scale-free graphs */
			Information.println(String.format("%5.3f %6.3f", gamma, exponent));
		}
		
		Utility.COLORS[0] = new Color(173, 120, 64); Utility.COLORS[2] = new Color(74, 128, 156);
		
		/* plots degree distributions of scale-free graphs */
		Configuration.distributions(graphs, labels);
		
		Complexity.poc();
	}
	
	static Graph scalefree(int n, double k, double gamma) {
		return price(n, k, gamma).setName("scalefree");
	}
	
	static Graph scalefree(int n, double k) {
		return scalefree(n, k, 2.5);
	}
	
	static Graph price(int n, double k, double gamma) {
		return price(n, (int)Math.round(0.5 * k), 0.5 * k * gamma - k);
	}
	
	static Graph price(int n, int c, double a) {
		Graph graph = Generators.complete("price", c).setDirected();
		
		List<Node> nodes = new ArrayList<Node>(n * c);
		for (Edge edge: graph.getEdges())
			nodes.add(edge.getSecond());
				
		for (int i = graph.getN(); i < n; i++) {
			graph.addNode();
			
			for (int j = 0; j < c; j++) {
				int node = Uncertainty.binary(c / (c + a))? Uncertainty.random(nodes).getIndex(): Uncertainty.random(i);
				nodes.add(graph.addEdge(i, node).getSecond());
			}
		}
		
		return graph;
	}

	static Graph barabasi(int n, double k) {
		return barabasi(n, (int)Math.round(0.5 * k));
	}

	static Graph barabasi(int n, int c) {
		return price(n, c, c).setName("barabasi").setUndirected();
	}
	
	static double gamma(Graph graph) {
		return gamma(graph, 25);
	}
	
	static double gamma(Graph graph, int cut) {
		double gamma = 0.0; int n = 0;
		for (Node node: graph.getNodes())
			if (node.getDegree() >= cut) {
				gamma += Math.log(node.getDegree()); 
				n++;
			}
		
		return 1.0 + 1.0 / (gamma / n - Math.log(cut - 0.5));
	}

	static void visualize(Graph graph) throws Exception {
		visualize(graph, 0.0);
	}
	
	static void visualize(Graph graph, double gamma) throws Exception {
		Utility.WIDTH = 1200; Utility.HEIGHT = 800; Utility.SIZE = 12; Utility.LABEL = 0; 
		Utility.COLORS[0] = new Color(116, 181, 51); Utility.COLORS[2] = new Color(86, 21, 115);

		Layout layout = Layouts.LGL(Generators.simple(graph.setUndirected())); if (gamma > 0.0) graph.setDirected();

		PDFGraphics2D graphics = new PDFGraphics2D(0, 0, layout.getWidth(), layout.getHeight());
		graphics.setColor(Color.WHITE); graphics.fillRect(0, 0, layout.getWidth(), layout.getHeight());
		Visualization.layout(graph, layout, Visualization.coloring(graph, Nodes.degrees(graph).getFirst()), 0, 0, graphics);

		FileOutputStream stream = new FileOutputStream("/Users/lovre/Desktop/" + graph.getName() + (gamma > 0.0? "_" + String.format("%.2f", gamma): "") + ".pdf");
		stream.write(graphics.getBytes()); stream.flush(); stream.close();
	}
	
}
