import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Circles extends JFrame {
	
	private List<Point> circles;
	
	private int selected;
	
	public Circles() {
		super();
		
		circles = new ArrayList<Point>();
		selected = -1;
		
		setTitle("Circles");
		setSize(new Dimension(1024, 768));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		JPanel panel = new JPanel() {
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				for (Point circle: circles) {
					g.setColor(Color.GRAY);
					g.fillOval((int)circle.getX(), (int)circle.getY(), 32, 32);
					g.setColor(Color.BLACK);
					g.drawOval((int)circle.getX(), (int)circle.getY(), 32, 32);
				}
			}
		};
		
		panel.addMouseListener(new MouseAdapter() {
			@Override
			public void mousePressed(MouseEvent e) {
				for (int i = 0; i < circles.size(); i++)
					if (Math.sqrt(Math.pow(e.getX() - 16 - circles.get(i).getX(), 2.0) + Math.pow(e.getY() - 16 - circles.get(i).getY(), 2.0)) <= 16) {
						selected = i;
						break;
					}
				if (selected == -1)
					circles.add(new Point(e.getX() - 16, e.getY() - 16));
				repaint();
			}
			@Override
			public void mouseReleased(MouseEvent e) {
				selected = -1;
			}
		});
		
		panel.addMouseMotionListener(new MouseMotionAdapter() {
			@Override
			public void mouseDragged(MouseEvent e) {
				if (selected != -1)
					circles.get(selected).setLocation(e.getX() - 16, e.getY() - 16);
				repaint();
			}
		});
		
		add(panel);
	}

	public static void main(String[] args) {
		new Circles().setVisible(true);
	}

}
