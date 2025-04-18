import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.TreeSet;

public class Collections {

	public static final int SIZE = 10000000;

	public static void main(String[] args) {
		System.gc();

		evaluate(new ArrayList<Double>(), SIZE / 100);
		/* evaluate(new LinkedList<Double>(), SIZE / 100); */

		evaluate(new TreeSet<Double>(), SIZE);
		evaluate(new HashSet<Double>(), SIZE);
	}

	public static void evaluate(Collection<Double> collection, int size) {
		long mic = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();

		// fills collection with randomly selected numbers

		for (int i = 0; i < size; i++)
			collection.add(Math.random());
		
		long tic = System.currentTimeMillis();

		// tests if randomly selected numbers are in collection

		for (int i = 0; i < size; i++)
			collection.contains(Math.random());

		// prints out collection label and expected running time

		System.out.format("\n%12s | %s", "Collection", collection.getClass().getSimpleName());
		System.out.format("\n%12s | %,d", "Size", SIZE);
		System.out.format("\n%12s | %.2f min", "Time", (System.currentTimeMillis() - tic) / 60000.0 / collection.size() * SIZE);
		System.out.format("\n%12s | %.3f GB\n", "Space", (Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory() - mic) / Math.pow(2.0, 30.0) / collection.size() * SIZE);

		// clears collection and runs garbage collector

		collection.clear();
		collection = null;

		System.gc();
	}

}
