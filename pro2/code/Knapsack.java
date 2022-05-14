import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Knapsack {

	public static void main(String[] args) {
		wikipedia(15);
		
		mercator(60.0, 100, 100);
	}
	
	static void wikipedia(int weight) {
		int[] values = new int[] { 4, 2, 10, 1, 2 };
		int[] weights = new int[] { 12, 1, 4, 1, 2 };
		String[] items = new String[] { "green", "gray", "yellow", "orange", "blue" };
		
		Solution solution = knapsack(weight, values, weights);
		
		System.out.format("%12s | %d kg\n", "Weight", weight);
		System.out.format("%12s | $%d\n", "Value", solution.value);
		
		for (int i = 0; i < items.length; i++)
			if (solution.items[i])
				System.out.format("%12s | %s (%d kg)\n", "$" + values[i], items[i], weights[i]);
		
		System.out.println();
	}
	
	static void mercator(double volume, int stock, int granularity) {
		List<String> items = new ArrayList<String>();
		List<Double> prices = new ArrayList<Double>();
		List<Double> volumes = new ArrayList<Double>();
		
		for (int i = 0; i < stock; i++) {
			items.add("Mercator pivo");
			prices.add(0.79);
			volumes.add(0.5);
			
			items.add("Laško pivo"); // 6x
			prices.add(6.54);
			volumes.add(3.0);
			
			items.add("Union pivo"); // 6x
			prices.add(5.54);
			volumes.add(3.0);
			
			items.add("Punk IPA");
			prices.add(2.42);
			volumes.add(0.33);
			
			/* items.add("Zlata penina");
			prices.add(16.99);
			volumes.add(0.75);
			
			items.add("Srebna penina");
			prices.add(8.19);
			volumes.add(0.75); */
		}
		
		Solution solution = knapsack(volume, prices, volumes, granularity);
		
		System.out.format("%12s | %.1f L\n", "Volume", volume);
		System.out.format("%12s | %.1f €\n", "Price", 1.0 * solution.value / granularity);
		
		Map<String, Quantity> quantity = new HashMap<String, Quantity>();
		for (int i = 0; i < items.size(); i++)
			if (solution.items[i])
				if (!quantity.containsKey(items.get(i)))
					quantity.put(items.get(i), new Quantity(1, prices.get(i)));
				else
					quantity.get(items.get(i)).count++;
		
		for (String item: quantity.keySet())
			System.out.format("%10.1f € | %s (%dx)\n", quantity.get(item).count * quantity.get(item).price, item, quantity.get(item).count);

		System.out.println();
	}
	
	static Solution knapsack(double budget, List<Double> prices, List<Double> volumes, int granularity) {
		int n = prices.size();
		
		int[] values = new int[n];
		int[] weights = new int[n];
		
		for (int i = 0; i < n; i++) {
			values[i] = (int)Math.round(granularity * prices.get(i));
			weights[i] = (int)Math.round(granularity * volumes.get(i));
		}
		
		return knapsack((int)Math.round(granularity * budget), values, weights);
	}

	static Solution knapsack(int budget, int[] values, int[] weights) {
		int n = values.length;
		
		int[][] knapsack = new int[n + 1][budget + 1];
		boolean[][][] items = new boolean[n + 1][budget + 1][n];
		
		for (int i = 1; i <= n; i++)
			for (int j = 0; j <= budget; j++) {
				int current = knapsack[i - 1][j];
				
				int possible = -1;
				if (j - weights[i - 1] >= 0)
					possible = knapsack[i - 1][j - weights[i - 1]] + values[i - 1];
				
				if (current > possible) {
					knapsack[i][j] = current;
					items[i][j] = items[i - 1][j].clone();
				}
				else {
					knapsack[i][j] = possible;
					items[i][j] = items[i - 1][j - weights[i - 1]].clone();
					items[i][j][i - 1] = true;
				}
			}
		
		return new Solution(knapsack[n][budget], items[n][budget]);
	}
	
}

class Solution {
	
	int value;
	
	boolean[] items;

	public Solution(int value, boolean[] items) {
		this.value = value;
		this.items = items;
	}
	
}

class Quantity {
	
	int count;
	
	double price;

	public Quantity(int count, double price) {
		this.count = count;
		this.price = price;
	}
	
}
