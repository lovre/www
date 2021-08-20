import java.util.Collections;
import java.util.ArrayList;
import java.util.List;

import java.util.HashSet;
import java.util.Set;

import java.util.HashMap;
import java.util.Map;

import java.io.*;

public class Demo {

  /**
    Javadoc komentar
  */
  public static void main(String[] args) {
    System.out.println("Pozdravljeni pri predmetu PRO2!"); // vrstični komentar
    /* bločni komentar */
    
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
    
    array = new double[] {0.0, 1.0, 2.0};
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
  
  public static void method(int x, double y) {
    System.out.println("Vrednost produkta x*y je enaka " + x * y);
  }

  static void method(int x) {
    method(x, 1.0);
  }

  static void method(double y) {
    method(42, y);
  }

  static void method() {
    method(42);
  }
  
  public static int function(int i) {
    System.out.println("Vrednost vhodnega argumenta funkcije je enaka " + i);
    i += 13;
    System.out.println("Vrednost rezultata funkcije je enaka " + i);
    return i;
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
