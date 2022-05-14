import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TFIDF {

	public static void main(String[] args) {
		List<File> documents = new ArrayList<File>();

		for (File document: new File("texts").listFiles())
			if (document.getName().endsWith(".txt"))
				documents.add(document);
		
		analysis(documents, 8);
	}
	
	public static void analysis(List<File> documents, int number) {
		// computes raw frequency of terms in each document

		Map<File, Map<String, Integer>> frequency = new HashMap<File, Map<String, Integer>>();

		for (File document: documents)
			try {
				frequency.put(document, frequency(document));
			} catch (IOException e) {
				e.printStackTrace();
			}

		// computes inverse document frequency over all documents

		Map<String, Double> inverseDocumentFrequency = inverseDocumentFrequency(frequency);

		for (File document: documents) {

			// computes term frequency of considered document

			Map<String, Double> termFrequency = termFrequency(frequency.get(document));

			// computes TF-IDF of terms in considered document

			Map<String, Double> TFIDF = termFrequencyInverseDocumentFrequency(termFrequency, inverseDocumentFrequency);

			// finds top TF-IDF terms in considered document

			List<String> terms = topTerms(TFIDF, number);

			// prints top TF-IDF terms in considered document

			System.out.format("%16s | '%s'\n", "Document", document.getName());
			for (String term: terms)
				System.out.format("%16s | %.8f\n", "'" + term + "'", TFIDF.get(term));
			System.out.println();
		}
	}

	public static List<String> topTerms(Map<String, ? extends Number> values, int number) {
		List<String> terms = new ArrayList<String>(values.keySet());

		Collections.sort(terms, new Comparator<String>() {
			@Override
			public int compare(String first, String second) {
				if (values.get(first).doubleValue() < values.get(second).doubleValue())
					return 1;
				else if (values.get(first).doubleValue() == values.get(second).doubleValue())
					return 0;
				return -1;
			}
		});

		return terms.subList(0, number);
	}

	public static Map<String, Integer> frequency(File document) throws IOException {
		Map<String, Integer> frequency = new HashMap<String, Integer>();

		BufferedReader reader = new BufferedReader(new FileReader(document));

		String line;
		while ((line = reader.readLine()) != null) {
			String[] terms = line.toLowerCase().replaceAll("[^a-zčšžA-ZČŠŽ]", " ").split(" ");

			for (String term: terms)
				if (term.length() > 0)
					if (frequency.containsKey(term))
						frequency.put(term, frequency.get(term) + 1);
					else
						frequency.put(term, 1);
		}

		reader.close();

		return frequency;
	}

	public static Map<String, Double> termFrequency(Map<String, Integer> frequency) {
		int maximum = 0;
		for (int value: frequency.values())
			if (value > maximum)
				maximum = value;

		Map<String, Double> termFrequency = new HashMap<String, Double>();

		for (String term: frequency.keySet())
			termFrequency.put(term, 0.5 + 0.5 * frequency.get(term) / maximum);

		return termFrequency;
	}

	public static Map<String, Double> inverseDocumentFrequency(Map<File, Map<String, Integer>> frequency) {
		Map<String, Double> inverseDocumentFrequency = new HashMap<String, Double>();

		for (File file: frequency.keySet())
			for (String term: frequency.get(file).keySet())
				if (!inverseDocumentFrequency.containsKey(term)) {
					int documents = 0;
					for (File document: frequency.keySet())
						if (frequency.get(document).containsKey(term))
							documents++;

					inverseDocumentFrequency.put(term, Math.log(1.0 * frequency.size() / documents));
				}

		return inverseDocumentFrequency;
	}

	public static Map<String, Double> termFrequencyInverseDocumentFrequency(Map<String, Double> termFrequency, Map<String, Double> inverseDocumentFrequency) {
		Map<String, Double> TFIDF = new HashMap<String, Double>();

		for (String term: termFrequency.keySet())
			TFIDF.put(term, termFrequency.get(term) * inverseDocumentFrequency.get(term));

		return TFIDF;
	}

}
