import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.TreeMap;
import java.util.List;
import java.util.Map;

public class Mathematics {
	
	public static void main(String[] args) throws IOException {
		Map<Mathematic, Integer> papers = new HashMap<Mathematic, Integer>();
		/* Map<Mathematic, Integer> papers = new TreeMap<Mathematic, Integer>(); */

		BufferedReader reader = new BufferedReader(new FileReader("mathematics.tab")); // 1986-2010

		String line = reader.readLine();
		while ((line = reader.readLine()) != null) {
			String[] array = line.split("\t");

			if (array[14].equals("1.01")) {
				Mathematic mathematic = new Mathematic(Integer.parseInt(array[2]), array[0] + " " + array[1]);

				if (papers.containsKey(mathematic))
					papers.put(mathematic, papers.get(mathematic) + 1);
				else
					papers.put(mathematic, 1);
			}
		}
		
		reader.close();

		List<Mathematic> list = new ArrayList<Mathematic>(papers.keySet());
		Collections.sort(list, new Comparator<Mathematic>() {

			@Override
			public int compare(Mathematic fst, Mathematic snd) {
				if (papers.get(fst) == papers.get(snd))
					return fst.compareTo(snd);
				
				return -new Integer(papers.get(fst)).compareTo(papers.get(snd));
			}
      
		});

		for (int i = 0; i < list.size(); i++)
			System.out.format("%4d | %s\n", papers.get(list.get(i)), list.get(i));
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
