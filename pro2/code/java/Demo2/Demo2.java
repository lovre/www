import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Demo2 {

	public static void main(String[] args) {
		XY xy = new XY(1, 2);
		System.out.println(xy);
		System.out.println(new XY());
		System.out.println(new XY(1).equals(xy));
		System.out.println(new XYZ(1, 2, 3));

		Point point = null; // prazna vrednost
		point = new Point(1, 2, 3);
		point.print();
		XYZ xyz = point;
		System.out.println(xyz);

		List<Double> list = new ArrayList<Double>();
		list.add(1.0);
		list.add(0, 1.1);
		list.set(0, 0.9);
		System.out.println(list.size());
		System.out.println(list.get(1));
		for (double value: list)
			System.out.println(value);
		list.remove(0);

		for (int i = 0; i < 3; i++)
			list.add(Math.random());
		Collections.sort(list);
		for (double value: list)
			System.out.println(value);

		Set<Double> set = new HashSet<Double>();
		set.add(1.0);
		set.addAll(list);
		System.out.println(set.size());
		System.out.println(set.contains(1.0));
		for (double value: set)
			System.out.println(value);
		set.remove(1.0);

		Map<String, Integer> map = new HashMap<String, Integer>();
		map.put("foo", 0);
		map.put("bar", 1);
		map.put("baz", 1);
		System.out.println(map.size());
		System.out.println(map.get("baz"));
		System.out.println(map.containsKey("foo"));
		for (String key: map.keySet())
			System.out.println(key + " " + map.get(key));
		map.remove("baz");

		double[] array = new double[3];
		for (int i = 0; i < array.length; i++) {
			System.out.println(array[i]);
			array[i] = Math.random();
			System.out.println(array[i]);
		}

		array = new double[] {0.0, 1.0, 2.0}; // začetne vrednosti
		for (double value: array)
			System.out.println(value);

		int[][] array2 = new int[4][7];
		for (int i = 0; i < array2.length; i++) {
			for (int j = 0; j < array2[i].length; j++) {
				array2[i][j] = i * array2[i].length + j + 1;
				System.out.format("%3d", array2[i][j]);
			}
			System.out.println();
		}

		try {
			BufferedReader reader = new BufferedReader(new FileReader("lorem.txt"));
			int i = 1; String line;
			while ((line = reader.readLine()) != null) {
				System.out.println(i + ". " + line);
				i++;
			}
			reader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

		try {
			BufferedWriter writer = new BufferedWriter(new FileWriter("array.txt"));
			for (int i = 0; i < array2.length; i++) {
				for (int j = 0; j < array2[i].length; j++)
					writer.write(String.format("%3d", array2[i][j]));
				writer.write("\n");
			}
			writer.flush();
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}

class XY {

	private int x;

	private int y;

	public XY() {
		this(0);
	}

	public XY(int x) {
		this(x, 1);
	}

	public XY(int x, int y) {
		super();

		this.x = x;
		this.y = y;
	}

	public int getX() {
		return x;
	}

	public int getY() {
		return y;
	}

	@Override
	public String toString() {
		return "x = " + getX() + ", y = " + getY();
	}

	@Override
	public boolean equals(Object object) {
		if (!(object instanceof XY)) // preverjanje tipov
			return false;

		XY xy = (XY)object; // pretvarjanje tipov
		return getX() == xy.getX() && getY() == xy.getY();
	}

}

class XYZ extends XY {

	private int z;

	public XYZ(int x, int y, int z) {
		super(x, y);

		this.z = z;
	}

	public int getZ() {
		return z;
	}

	@Override
	public String toString() {
		return super.toString() + ", z = " + getZ();
	}

	@Override
	public boolean equals(Object object) {
		if (!super.equals(object) || !(object instanceof XYZ))
			return false;

		return getZ() == ((XYZ)object).getZ();
	}

}

interface Printable {

	public void print();

}

class Point extends XYZ implements Printable {

	public Point(int x, int y, int z) {
		super(x, y, z);
	}

	@Override
	public void print() {
		System.out.println(toString());
	}

}
