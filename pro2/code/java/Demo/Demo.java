public class Demo {

	/** Javadoc komentar */
	public static void main(String[] args) {
		System.out.println("Pozdravljeni pri predmetu PRO2!"); // vrstični komentar
		/* 
			večvrstični ali bločni komentar 
		*/
		
		int x = 1;
		double y;
		y = 1.23 * 9;
		char ch = 'a'; // enojni narekovaji '.'
		String str = "niz znakov"; // dvojni narekovaji "..."
		boolean b = x > 1;

		final float G = 9.81f;

		int z = (int)y; // celi del števila
		double w = (double)x; // 1.0 * x
		z = Integer.parseInt("7");
		w = Double.parseDouble("1.23");
		str = "Vrednost spremenljivke w je enaka " + w; // konkatenacija nizov
		str = String.format("Vrednost spremenljivke w je enaka %.3f", w); // formatiranje nizov
		System.out.println(x + " " + y + " " + z + " " + w + " " + str);

		System.out.println(x + y * z / w);
		System.out.println(x % z); // ostanek pri deljenju
		System.out.println(Math.pow(y, 2.0)); // potenciranje števil
		System.out.println(42.0 * Math.random()); // naključno število iz [0, 42)
		System.out.println((int)(3.0 * Math.random())); // naključno število iz {0, 1, 2}

		if (x < 1) {
			System.out.println("Vrednost spremenljivke x je manjša od 1");
		}
		else if (x < 2)
			System.out.println("Vrednost spremenljivke x je med 1 in 2");
		else
			System.out.println("Vrednost spremenljivke x je večja ali enaka 2");

		System.out.println("Vrednost spremenljivke x je " + (x < 1? "manjša od ": "večja ali enaka ") + 1);

		if (x == 1 || x == 2)
			System.out.println("Vrednost spremenljivke x je enaka 1 ali 2");
		if (x == 1 && x == 2)
			System.out.println("To ni mogoče!");
		if (x != 1 && x != 2) // if (!(x == 1 || x == 2))
			System.out.println("Vrednost spremenljivke x ni enaka 1 ali 2");

		switch (x) {
		case 1:
			System.out.println("Vrednost spremenljivke x je enaka 1");
			break;
		case 2:
			System.out.println("Vrednost spremenljivke x je enaka 2");
			break;
		default:
			System.out.println("Vrednost spremenljivke x ni enaka 1 ali 2");
			break;
		}

		switch (ch) {
		case 'a':
			System.out.println("Vrednost spremenljivke ch je enaka 'a'");
			break;
		default:
			System.out.println("Vrednost spremenljivke ch ni enaka 'a'");
			break;
		}

		for (int i = 0; i < 3; i += 1) {
			System.out.println("Vrednost spremenljivke i je enaka " + i);
		}

		int ind = 0;
		while (ind < 3) {
			System.out.println("Vrednost spremenljivke ind je enaka " + ind);
			ind++; // ind += 1;
		}

		for (String arg: args)
			System.out.println(arg);

		method(7, 1.23);
		method(7);
		method(1.23);
		method();
		function(42);
	}

	public static void method(int x, double y) {
		System.out.println("Vrednost produkta x*y je enaka " + x * y);
	}

	static void method(int x) {
		method(x, 2.0);
	}

	static void method(double y) {
		method(42, y);
	}

	static void method() {
		method(1);
	}

	public static int function(int i) {
		System.out.println("Vrednost vhodnega argumenta funkcije je enaka " + i);
		i += 13;
		System.out.println("Vrednost rezultata funkcije je enaka " + i);
		return i;
	}

}
