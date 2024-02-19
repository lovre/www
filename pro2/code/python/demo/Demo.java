public class Demo {

  public static void main(String[] args) {
    System.out.println("Pozdravljeni pri predmetu PRO2!");
    
    int x = 1;
    double y;
    y = 1.23;
    boolean z = true;
    char ch = 'a';
    String st = "niz znakov";

    final double G = 9.81;

    if (x < 1) {
      System.out.println("Vrednost spremenljivke x je manjša od 1");
    }
    else if (x < 2) {
      System.out.println("Vrednost spremenljivke x je med 1 in 2");
    }
    else
      System.out.println("Vrednost spremenljivke x je večja ali enaka 2");
     
    for (int i = 0; i < 5; i++)
      System.out.println("Vrednost spremenljivke i je enaka " + i);
     
    int i = 0;
    while (i < 5) {
      System.out.println("Vrednost spremenljivke i je enaka " + i);
      i++;
    }
    
    method(7);
    
    function(2);
  }
      
  public static void method(int i) {
    System.out.println("Vrednost parametra i je enaka " + i);
  }

  public static int function(int i) {
    System.out.println("Vrednost parametra i je enaka " + i);
    i *= 7;
    System.out.println("Vrednost rezultata funkcije je enaka " + i);
    return i;
  }
  
}
