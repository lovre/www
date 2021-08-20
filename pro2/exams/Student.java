import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Student implements Comparable<Student> {
	
	private static final String[] NAMES = new String[] { "Franc", "Janez", "Marko", "Marija", "Ana", "Maja"};
	
	private static final String[] SURNAMES = new String[] { "Novak", "Horvat", "Kovačič", "Krajnc", "Zupančič", "Kovač" };
	
	private int SID;
	
	private String name;
	
	private String surname;
	
	public Student() {
		this(27191000 + (int)(1000 * Math.random()), NAMES[(int)(Math.random() * NAMES.length)], SURNAMES[(int)(Math.random() * SURNAMES.length)]);
	}
	
	public Student(int SID, String name, String surname) {
		this.SID = SID;
		this.name = name;
		this.surname = surname;
	}
	
	@Override
	public int compareTo(Student student) {
		return new Integer(SID).compareTo(student.SID);
	}

	@Override
	public String toString() {
		return "[" + SID + "] " + name + " " + surname;
	}

	public static void main(String[] args) {
		List<Student> students = new ArrayList<Student>();

		for (int i = 0; i < 10; i++)
			students.add(new Student());
		
		Collections.sort(students);
		
		for (Student student: students)
			System.out.println(student);
	}

}
