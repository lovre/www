import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Mathematics {
	
	public static void main(String[] args) throws IOException {
		Map<Integer, Mathematic> mathematics = new HashMap<Integer, Mathematic>();

		BufferedReader reader = new BufferedReader(new FileReader("mathematics.tab"));

		String line = reader.readLine();
		while ((line = reader.readLine()) != null) {
			String[] array = line.split("\t");

			if (array[14].equals("1.01")) {
				int id = Integer.parseInt(array[2]);

				Mathematic mathematic = new Mathematic(id, array[0] + " " + array[1]);

				if (!mathematics.containsKey(id))
					mathematics.put(id, mathematic);
				else
					mathematic = mathematics.get(id);

				mathematic.addPaper();
			}
		}
		
		reader.close();

		List<Mathematic> list = new ArrayList<Mathematic>(mathematics.values());

		Collections.sort(list);

		System.out.format("%6s | %s\n", "Rank", "Mathematic");
		for (int i = 0; i < list.size(); i++)
			System.out.format("%6d | %s\n", i + 1, list.get(i));
	}
	
}

class Mathematic implements Comparable<Mathematic> {
	
	private int id;
	
	private String name;
	
	private int papers;
	
	public Mathematic(int id, String name) {
		super();
		
		this.id = id;
		this.name = name;
		
		papers = 0;
	}
	
	public void addPaper() {
		papers++;
	}

	@Override
	public int compareTo(Mathematic mathematic) {
		if (papers == mathematic.papers)
			return name.compareTo(mathematic.name);
		
		return -new Integer(papers).compareTo(mathematic.papers);
	}

	@Override
	public String toString() {
		return name + " [" + id + "]";
	}
	
}
