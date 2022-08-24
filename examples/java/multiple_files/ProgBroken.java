import java.util.Scanner;

public class ProgBroken {
	public static void main(String[] args) {
		switch ((int)(Math.random() * 4)) {
			case 0: // correct 
				Logic.func();
			break;
			case 1: // incorrect
				System.out.println("grapefruit");
			break;
			case 2: // timeouted
				try { Thread.sleep(100 * 1000); } catch (InterruptedException ex) {}
			break;
			case 3: // couldn't execute
				System.err.println("RNGesus decided this should be an error");
				System.exit(17);
			break;
		}
	}
}