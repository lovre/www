import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class Mathematics {

	public static void main(String[] args) throws IOException {
		Map<Mathematic, Double> papers = new HashMap<Mathematic, Double>();
		/* Map<Mathematic, Double> papers = new TreeMap<Mathematic, Double>(); */ 

		BufferedReader reader = new BufferedReader(new FileReader("mathematics.csv"));
		
		String line = reader.readLine();
		while ((line = reader.readLine()) != null) {
			String[] array = line.split(",");

			Mathematic mathematic = new Mathematic(Integer.parseInt(array[0]), array[1] + " " + array[2]);
			double value = Double.parseDouble(array[6]);

			if (papers.containsKey(mathematic))
				papers.put(mathematic, papers.get(mathematic) + value);
			else
				papers.put(mathematic, value);
		}

		reader.close();

		List<Mathematic> list = new ArrayList<Mathematic>(papers.keySet());
		Collections.sort(list, new Comparator<Mathematic>() {

			@Override
			public int compare(Mathematic fst, Mathematic snd) {
				if (papers.get(fst) == papers.get(snd))
					return fst.compareTo(snd);

				return -new Double(papers.get(fst)).compareTo(papers.get(snd));
			}

		});

		for (int i = 0; i < list.size(); i++)
			System.out.format("%8.1f | %s\n", papers.get(list.get(i)), list.get(i));
	}

}

class Mathematic implements Comparable<Mathematic> {

	private int id;

	private String name;

	public Mathematic(int id, String name) {
		super();

		this.id = id;
		this.name = name.trim();
	}

	@Override
	public int hashCode() {
		return id;
	}

	@Override
	public String toString() {
		return name + " [" + id + "]";
	}

	@Override
	public boolean equals(Object obj) {
		if (!(obj instanceof Mathematic))
			return false;

		return id == ((Mathematic)obj).id;
	}

	@Override
	public int compareTo(Mathematic mathematic) {
		return new Integer(id).compareTo(mathematic.id);
	}

}
