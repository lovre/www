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
import si.lj.uni.fri.lna.entity.graph.EdgeGraph;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.Layout;
import si.lj.uni.fri.lna.logic.graph.Generators;
import si.lj.uni.fri.lna.logic.graph.Layouts;
import si.lj.uni.fri.lna.logic.graph.Metrics;
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
public class V {

	public static void main(String[] args) throws Exception {
		LNA.init();
		
		/* selected parameters of small-world graphs */
		int nodes = 1000; int degree = 10; int number = 25;
		double[] probabilities = new double[] {0.0, 0.0001, 0.001, 0.01, 0.1, 0.25, 0.5, 1.0};
		
		/* computes statistics and visualizes small-world graphs */
		smallworld(nodes, degree, probabilities, number);
		
		LNA.exit();
	}
	
	static void smallworld(int nodes, int degree, double[] probabilities, int number) throws Exception {
		Information.println("\n         ... | GRAPH");
		
		/* prints out standard statistics of small-world graph */
		Information.print(Generators.array(smallworld(nodes, degree, 0.0)), true);
		
		Complexity.poc();
		
		Information.println("\n         ... | COMPARE"); Information.print(number);
		Information.println("\n      Mixing | Cluster Distance");
		
		/* prints out clustering and distances of small-world graphs */
		List<Graph> graphs = new ArrayList<Graph>();
		String[] labels = new String[probabilities.length];
		for (double probability: probabilities) {
			Information.print(String.format("%12.5f | ", probability));
			
			double clustering = 0.0, distance = 0.0;
			for (int i = 0; i < number; i++) {
				/* generates small-world graph with given parameters */
				Graph graph = smallworld(nodes, degree, probability);
				
				/* computes clustering and distances of generated small-world graph */
				clustering += Metrics.clustering(graph).getFirst() / number;
				distance += Metrics.distance(graph) / number;
				
				if (i == 0) {
					/* visualizes wiring diagram of generated small-world graph */
					visualize(graph, probability);
					graphs.add(graph);
					labels[graphs.size() - 1] = " SW (" + String.format("%.4f", probability ) + ")";
				}
			}
			
			/* computes clustering and distances of generated small-world graphs */
			Information.println(String.format(" %5.3f   %6.2f", clustering, distance));
		}
		
		/* plots degree distributions of small-world graphs */
		Configuration.distributions(graphs, labels);
		
		Complexity.poc();
	}
	
	static Graph smallworld(int nodes, int degree, double probability) {
		int[][] edges = new int[nodes * degree / 2][2];
		for (int i = 0; i < nodes; i++)
			for (int j = 1; j <= degree / 2; j++) {
				edges[i * degree / 2 + j - 1][0] = i;
				edges[i * degree / 2 + j - 1][1] = (i + j) % nodes;
			}

		for (int i = 0; i < nodes * degree / 2; i++)
			if (Uncertainty.binary(probability)) {
				edges[i][0] = Uncertainty.random(nodes);
				edges[i][1] = Uncertainty.random(nodes);
			}
		
		return Generators.list(new EdgeGraph("smallworld", edges, nodes));
	}
	
	static void visualize(Graph graph, double probability) throws Exception {
		Utility.WIDTH = 1200; Utility.HEIGHT = 800; Utility.SIZE = 8; Utility.LABEL = 0;
		Utility.COLORS[0] = new Color(116, 181, 51); Utility.COLORS[1] = new Color(126, 157, 78); Utility.COLORS[2] = new Color(86, 21, 115);
		
		Layout layout = Layouts.LGL(Generators.simple(graph));
		PDFGraphics2D graphics = new PDFGraphics2D(0, 0, layout.getWidth(), layout.getHeight());
		graphics.setColor(Color.WHITE); graphics.fillRect(0, 0, layout.getWidth(), layout.getHeight());
		Visualization.layout(graph, layout, Visualization.coloring(graph, Nodes.clusterings(graph).getFirst()), 0, 0, graphics);
		
		FileOutputStream stream = new FileOutputStream("/Users/lovre/Desktop/" + graph.getName() + "-" + probability + ".pdf");
		stream.write(graphics.getBytes()); stream.flush(); stream.close();
	}
	
}
