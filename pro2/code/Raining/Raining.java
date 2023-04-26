import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class Raining {
	
	public static boolean[][] raindrops;
	
	public static void main(String[] args) throws InterruptedException {
		JFrame frame = new JFrame("Raining");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(new Dimension(800, 600));
		frame.setResizable(false);
		
		JPanel panel = new JPanel() {
			private static final long serialVersionUID = 1L;
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				Graphics2D graphics = (Graphics2D)g;
				
				graphics.setColor(new Color(196, 211, 223));
				graphics.setStroke(new BasicStroke(1.0f));
				
				for (int i = 0; i < raindrops.length; i++)
					for (int j = 0; j < raindrops[i].length; j++)
						if (raindrops[i][j])
							graphics.fillRect(j, i, 1, 1);
				
				/* graphics.setColor(Color.BLACK);
				graphics.setStroke(new BasicStroke(0.25f));
				
				graphics.drawLine(0, (int)Math.round(0.5 * getHeight()), getWidth(), (int)Math.round(0.5 * getHeight())); */
			}
		};
		panel.setBackground(Color.WHITE);
		frame.add(panel);
		
		frame.setVisible(true);
		
		raindrops = new boolean[panel.getHeight()][panel.getWidth()];
		
		while (true) {			
			for (int j = 0; j < raindrops[0].length; j++)
				raindrops[0][j] = Math.random() < 0.25;
			
			for (int i = raindrops.length - 1; i > 0; i--)
				for (int j = 0; j < raindrops[i].length; j++)
					if (!raindrops[i][j] && raindrops[i - 1][j]) {
						raindrops[i][j] = true;
						raindrops[i - 1][j] = false;
					}

			panel.repaint();
			
			int water = 0;
			for (int j = 0; j < raindrops[0].length; j++)
				for (int i = raindrops.length - 1; i >= 0; i--)
					if (raindrops[i][j])
						water++;
					else
						break;
            
			if (water >= 0.5 * raindrops.length * raindrops[0].length)
				break;

			Thread.sleep(5);
		}
	}

}
