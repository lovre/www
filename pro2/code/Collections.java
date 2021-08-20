import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.TreeSet;

public class Collections {
	
	public static final int SIZE = (int)1e7;
	
	public static void main(String[] args) {
		System.gc();
		
		/* collection("LinkedList", new LinkedList<Double>(), SIZE / 100); */
		collection("ArrayList", new ArrayList<Double>(), SIZE / 100);
		
		collection("TreeSet", new TreeSet<Double>(), SIZE);
		collection("HashSet", new HashSet<Double>(), SIZE);
	}
	
	public static void collection(String label, Collection<Double> collection, int size) {
		long tic = System.currentTimeMillis();
		long mic = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
		
		// fills collection with randomly selected numbers
		
		for (int i = 0; i < size; i++)
			collection.add(Math.random());
		
		// tests if randomly selected numbers are in collection
		
		for (int i = 0; i < size; i++)
			collection.contains(Math.random());
		
		// prints out collection label and expected running time
		
		System.out.format("\n%12s | '%s'", "Collection", label);
		System.out.format("\n%12s | %,d", "Size", SIZE);
		System.out.format("\n%12s | %.2f min", "Time", (System.currentTimeMillis() - tic) / 60000.0 / collection.size() * SIZE);
		System.out.format("\n%12s | %.3f GB\n", "Space", (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory() - mic) / Math.pow(2.0, 30.0) / collection.size() * SIZE);
		
		// clears collection and runs garbage collector
		
		collection.clear();
		collection = null;
		
		System.gc();
	}
	
}
