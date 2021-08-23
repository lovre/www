import java.util.Arrays;
import java.util.List;

public class Interval {
	
	private int lower;
	
	private int upper;
	
	public Interval(int lower, int upper) {
		this.lower = lower;
		this.upper = upper;
	}
	
	public boolean includes(int number) {
		return number >= lower && number <= upper;
	}
	
	public boolean includes(List<Integer> numbers) {
		for (int number: numbers)
			if (!includes(number))
				return false;
		return true;
	}
	
	public boolean includes(Interval interval) {
		return interval.lower >= lower && interval.upper <= upper;
	}
	
	public static Interval merge(Interval first, Interval second) {
		return new Interval(Math.min(first.lower, second.lower), Math.max(first.upper, second.upper));
	}

	@Override
	public String toString() {
		return "[" + lower + ", " + upper + "]";
	}

	public static void main(String[] args) {
		Interval interval = new Interval(2, 7);
		System.out.println(interval);
		System.out.println(interval.includes(4));
		System.out.println(interval.includes(Arrays.asList(new Integer[] {3, 4, 5})));
		System.out.println(interval.includes(new Interval(-1, 5)));
		System.out.println(Interval.merge(interval, new Interval(5, 9)));
	}

}
