import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Polygon;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class IceCream {
	
	public static Flavour flavour = Flavour.NONE;

	public static void main(String[] args) {
		JFrame frame = new JFrame("Ice Cream");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
		frame.setSize(new Dimension(800, 600));
		frame.setResizable(true);
		
		JPanel panel = new JPanel() {
			private static final long serialVersionUID = 1L;
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				Graphics2D graphics = (Graphics2D)g;
				int width = getWidth(), height = getHeight();
				
				graphics.setColor(new Color(110, 78, 80));
				graphics.setStroke(new BasicStroke(5.0f));
				graphics.fillRoundRect((int)Math.round(0.05 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				graphics.setColor(Color.DARK_GRAY);
				graphics.drawRoundRect((int)Math.round(0.05 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				
				graphics.setColor(new Color(206, 145, 165));
				graphics.fillRoundRect((int)Math.round(0.275 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				graphics.setColor(Color.DARK_GRAY);
				graphics.drawRoundRect((int)Math.round(0.275 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				
				graphics.setColor(new Color(220, 215, 205));
				graphics.fillRoundRect((int)Math.round(0.5 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				graphics.setColor(Color.DARK_GRAY);
				graphics.drawRoundRect((int)Math.round(0.5 * width), (int)Math.round(0.3 * height), (int)Math.round(0.175 * width), (int)Math.round(0.4 * height), 16, 16);
				
				Polygon cornet = new Polygon();
				cornet.addPoint((int)Math.round(0.75 * width), (int)Math.round(0.3 * height));
				cornet.addPoint((int)Math.round(0.95 * width), (int)Math.round(0.3 * height));
				cornet.addPoint((int)Math.round(0.85 * width), (int)Math.round(0.7 * height));
				graphics.setColor(new Color(169, 113, 55, 192));
				graphics.fillPolygon(cornet);
				
				switch (flavour) {
				case NONE: default:
					graphics.setColor(Color.WHITE);
					break;
				case CHOCOLATE:
					graphics.setColor(new Color(110, 78, 80));
					break;
				case STRAWBERRY:
					graphics.setColor(new Color(206, 145, 165));
					break;
				case VANILLA:
					graphics.setColor(new Color(220, 215, 205));
					break;
				}
				graphics.fillArc((int)Math.round(0.75 * width), (int)Math.round(0.3 * height - 0.1 * width), (int)Math.round(0.2 * width), (int)Math.round(0.2 * width), 0, 180);
			}
		};
		panel.addMouseListener(new MouseListener() {
			@Override
			public void mouseReleased(MouseEvent e) {}
			@Override
			public void mousePressed(MouseEvent e) {}
			@Override
			public void mouseExited(MouseEvent e) {}
			@Override
			public void mouseEntered(MouseEvent e) {}
			@Override
			public void mouseClicked(MouseEvent e) {
				if (e.getX() >= (int)Math.round(0.05 * panel.getWidth()) && e.getY() >= (int)Math.round(0.3 * panel.getHeight()) &&
						e.getX() <= (int)Math.round(0.225 * panel.getWidth()) && e.getY() <= (int)Math.round(0.7 * panel.getHeight()))
					flavour = Flavour.CHOCOLATE;
				else if (e.getX() >= (int)Math.round(0.275 * panel.getWidth()) && e.getY() >= (int)Math.round(0.3 * panel.getHeight()) &&
						e.getX() <= (int)Math.round(0.45 * panel.getWidth()) && e.getY() <= (int)Math.round(0.7 * panel.getHeight()))
					flavour = Flavour.STRAWBERRY;
				else if (e.getX() >= (int)Math.round(0.5 * panel.getWidth()) && e.getY() >= (int)Math.round(0.3 * panel.getHeight()) &&
						e.getX() <= (int)Math.round(0.675 * panel.getWidth()) && e.getY() <= (int)Math.round(0.7 * panel.getHeight()))
					flavour = Flavour.VANILLA;
				else
					flavour = Flavour.NONE;
				panel.repaint();
			}
		});
		panel.setBackground(Color.WHITE);
		frame.add(panel);
		
		frame.setVisible(true);
	}

}

enum Flavour {
	
	NONE,
	CHOCOLATE,
	STRAWBERRY,
	VANILLA
	
}
