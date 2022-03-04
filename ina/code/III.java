package si.lj.uni.fri.lna.test.ina.labs;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

import si.lj.uni.fri.lna.LNA;
import si.lj.uni.fri.lna.entity.graph.Graph;
import si.lj.uni.fri.lna.entity.graph.ListGraph;
import si.lj.uni.fri.lna.io.graph.Readers;
import si.lj.uni.fri.lna.logic.utility.Information;
import si.lj.uni.fri.lna.test.bib.Complexity;

public class III {

	public static void main(String[] args) throws Exception {
		LNA.init();
		
		for (String file: new String[] { "toy", "karate_club", "collaboration_imdb", "www_google" }) {
			Complexity.pic();
			
			Graph graph = Readers.pajek("/Users/lovre/Downloads/" + file + ".net");
			
			info(graph);
			
			info(random(graph));
			
			Complexity.poc();
		}
		
		LNA.exit();
	}
	
	public static void info(Graph graph) throws Exception {
		int n0 = 0, n1 = 0, delta = 0;
		for (int i = 0; i < graph.getN(); i++) {
			if (graph.getDegree(i) == 0)
				n0++;
			else if (graph.getDegree(i) == 1)
				n1++;
			if (graph.getDegree(i) > delta)
				delta = graph.getDegree(i);
		}
		
		List<List<Integer>> Cs = components(graph);
		int S = 0;
		for (List<Integer> C: Cs)
			if (C.size() > S)
				S = C.size();
		
		int diameter = 0;
		double distance = Double.NaN;
		if (graph.getN() < 100000) {
			int[][] Ds = distances(graph);
			distance = 0.0; diameter = 0;
			for (int i = 0; i < graph.getN(); i++)
				for (int j = 0; j < graph.getN(); j++) {
					distance += 1.0 * Ds[i][j] / graph.getN() / graph.getN();
					if (Ds[i][j] > diameter)
						diameter = Ds[i][j];
				}
		}
		
		Information.println(String.format("\n%12s | '%s'", "Graph", graph.getName()));
		Information.println(String.format("%12s | %,d (%,d, %,d)", "Nodes", graph.getN(), n0, n1));
		Information.println(String.format("%12s | %,d", "Edges", graph.getM()));
		Information.println(String.format("%12s | %.3f (%,d)", "Degree", graph.getDegree(), delta));
		Information.println(String.format("%12s | %.3e", "Density", graph.getDensity()));
		Information.println(String.format("%12s | %.3f (%,d)", "Distance", distance, diameter));
		Information.println(String.format("%12s | %.1f%% (%,d)", "LCC", 100.0 * S / graph.getN(), Cs.size()));
	}
	
	public static List<List<Integer>> components(Graph graph) {
		Set<Integer> N = new HashSet<Integer>();
		for (int i = 0; i < graph.getN(); i++)
			N.add(i);
		
		List<List<Integer>> Cs = new LinkedList<List<Integer>>();
		while (!N.isEmpty())
			Cs.add(component(graph, N, N.iterator().next()));
		
		return Cs;
	}
	
	public static List<Integer> component(Graph graph, Set<Integer> N, int i) {
		List<Integer> C = new LinkedList<Integer>();
		List<Integer> S = new LinkedList<Integer>();
		
		S.add(i);
		N.remove(i);
		
		while (!S.isEmpty()) {
			i = S.remove(0);
			C.add(i);
			
			for (int j: graph.getNeighbors(i))
				if (N.remove(j))
					S.add(0, j);
		}
		
		return C;
	}
	
	public static int[][] distances(Graph graph) {
		int[][] Ds = new int[graph.getN()][];
		for (int i = 0; i < graph.getN(); i++)
			Ds[i] = distance(graph, i);
		
		return Ds;
	}
	
	public static int[] distance(Graph graph, int i) {
		int[] D = new int[graph.getN()];
		for (int j = 0; j < graph.getN(); j++)
			D[j] = -1;
		List<Integer> Q = new LinkedList<Integer>();
		
		D[i] = 0;
		Q.add(i);
		
		while (!Q.isEmpty()) {
			i = Q.remove(0);
			
			for (int j: graph.getNeighbors(i))
				if (D[j] == -1) {
					D[j] = D[i] + 1;
					Q.add(j);
				}
		}
		
		for (int j = 0; j < graph.getN(); j++)
			if (D[j] == -1)
				D[j] = 0;
		
		return D;
	}
	
	public static Graph random(Graph graph) {
		Graph random = new ListGraph("erdos_renyi");
		
		for (int i = 0; i < graph.getN(); i++)
			random.addNode();
		
		while (random.getM() < graph.getM()) {
			int i = (int)(Math.random() * random.getN());
			int j = (int)(Math.random() * random.getN());
			
			if (i != j)
				random.addEdge(i, j);
		}
		
		return random;
	}

}
