public class Gambling {
	
	public static final int TRIES = 999;
	
	public static final String SYMBOLS = "♣♠♦♥♪♫◄☼☽xyz7";
	
	public static void main(String[] args) {
		for (int i = 0; i < TRIES; i++) {
			char s1 = symbol();
      char s2 = symbol();
      char s3 = symbol();
			
			System.out.println((i + 1) + ". " + s1 + " " + s2 + " " + s3);
			
			if (s1 == s2 && s2 == s3 && s3 == '7') {
				System.out.println("\nJackpot in " + (i + 1) + " tries :) Well done!");
				break;
			}
			
			if (i == TRIES - 1)
				System.out.println("\nNo jackpot :( Better luck next time!");
		}
	}
	
	public static char symbol() {
		return SYMBOLS.charAt((int)(Math.random() * SYMBOLS.length()));
	}
	
}
