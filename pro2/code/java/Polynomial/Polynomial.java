public class Polynomial {

	private double[] coefficients;

	public Polynomial(double[] coefficients) {
		this.coefficients = coefficients.length == 0? new double[1]: coefficients;
	}

	public double evaluate(double x) {
		double y = 0.0;
		for (int i = 0; i < coefficients.length; i++)
			y += coefficients[i] * Math.pow(x, i);

		return y;
	}

	public Polynomial derivative() {
		double[] derivative = new double[coefficients.length - 1];
		for (int i = 0; i < derivative.length; i++)
			derivative[i] = coefficients[i + 1] * (i + 1);

		return new Polynomial(derivative);
	}

	@Override
	public String toString() {
		String polynomial = "";
		for (int i = coefficients.length - 1; i >= 0; i--)
			if (coefficients[i] != 0.0) {
				if (polynomial.length() == 0)
					polynomial += String.format("%.1f", coefficients[i]);
				else
					polynomial += (coefficients[i] >= 0.0? " + ": " - ") + String.format("%.1f", Math.abs(coefficients[i])); 
				
				polynomial += i > 0? " * x" + (i > 1? "^" + i: ""): "";
			}

		return polynomial.length() > 0? polynomial: "0.0";
	}

	public static void main(String[] args) {
		double[] coefficients = new double[] { 4.0, 0.0, 2.0, 7.1, -1.3 };
		
		Polynomial polynomial = new Polynomial(coefficients);
		Polynomial derivative = polynomial.derivative();
		
		System.out.println(polynomial);
		System.out.println(derivative);
		
		System.out.println(polynomial.evaluate(3.14));
		System.out.println(derivative.evaluate(3.14));
	}

}
