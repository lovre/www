package si.lj.uni.fri.lna.test.ina.labs;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

public class II {

	@SuppressWarnings("unchecked")
	public static void main(String[] args) throws Exception {
		for (String file: new String[] {"toy", "karate_club", "www_google"}) {
			BufferedReader reader = new BufferedReader(new FileReader("/Users/lovre/Downloads/" + file + ".net"));

			int n = Integer.parseInt(reader.readLine().split(" ")[1]);

			List<Integer>[] G = new ArrayList[n];
			for (int i = 0; i < n; i++)
				G[i] = new ArrayList<Integer>();

			while (!reader.readLine().startsWith("*"));

			int m = 0; String line;
			while ((line = reader.readLine()) != null) {
				String[] nodes = line.split(" ");
				int i = Integer.parseInt(nodes[0]) - 1;
				int j = Integer.parseInt(nodes[1]) - 1;

				G[i].add(j);
				G[j].add(i);
				m++;
			}

			reader.close();
			
			int n0 = 0, n1 = 0, delta = 0;
			for (int i = 0; i < G.length; i++) {
				if (isolated(G, i))
					n0++;
				else if (G[i].size() == 1)
					n1++;
				if (G[i].size() > delta)
					delta = G[i].size();
			}
			
			List<List<Integer>> Cs = components(G);
			int S = 0;
			for (List<Integer> C: Cs)
				if (C.size() > S)
					S = C.size();
			
			System.out.println(String.format("%10s | '%s'", "Graph", file));
			System.out.println(String.format("%10s | %,d (%,d, %,d)", "Nodes", n, n0, n1));
			System.out.println(String.format("%10s | %,d", "Edges", m));
			System.out.println(String.format("%10s | %.2f (%,d)", "Degree", 2.0 * m / n, delta));
			System.out.println(String.format("%10s | %.2e", "Density", 2.0 * m / n / (n - 1)));
			System.out.println(String.format("%10s | %.1f%% (%,d)", "LCC", 100.0 * S / n, Cs.size()));
			System.out.println();
		}
	}
	
	static boolean isolated(List<Integer>[] G, int i) {
		for (int j: G[i])
			if (j != i)
				return false;
		
		return true;
	}
	
	static List<List<Integer>> components(List<Integer>[] G) {
		Set<Integer> N = new HashSet<Integer>();
		for (int i = 0; i < G.length; i++)
			N.add(i);
		
		List<List<Integer>> Cs = new LinkedList<List<Integer>>();
		while (!N.isEmpty())
			Cs.add(component(G, N, N.iterator().next()));
		
		return Cs;
	}
	
	static List<Integer> component(List<Integer>[] G, Set<Integer> N, int i) {
		List<Integer> C = new LinkedList<Integer>();
		List<Integer> S = new LinkedList<Integer>();
		
		S.add(i);
		N.remove(i);
		
		while (!S.isEmpty()) {
			i = S.remove(0);
			C.add(i);
			
			for (int j: G[i])
				if (N.remove(j))
					S.add(0, j);
		}
		
		return C;
	}

}
