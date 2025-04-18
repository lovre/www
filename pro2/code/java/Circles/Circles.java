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

	public static int SIZE = 48;

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

				for (Point circle: circles)
					g.fillOval(circle.x - SIZE / 2, circle.y - SIZE / 2, SIZE, SIZE);
			}

		};

		panel.addMouseListener(new MouseAdapter() {

			@Override
			public void mousePressed(MouseEvent e) {
				for (int i = 0; i < circles.size(); i++)
					if (Math.sqrt(Math.pow(e.getX() - circles.get(i).x, 2.0) + Math.pow(e.getY() - circles.get(i).y, 2.0)) <= SIZE / 2.0) {
						selected = i;
						break;
					}

				if (selected == -1)
					circles.add(new Point(e.getX(), e.getY()));

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
					circles.get(selected).setLocation(e.getX(), e.getY());

				repaint();
			}

		});

		add(panel);
	}

	public static void main(String[] args) {
		new Circles().setVisible(true);
	}

}
