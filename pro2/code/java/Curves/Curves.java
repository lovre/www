import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Curves extends JFrame {
	
	final Color[] COLORS = new Color[] { Color.CYAN, Color.YELLOW, Color.MAGENTA };

	List<Curve> curves = new ArrayList<Curve>();

	public Curves() {
		super();

		setTitle("Curves");
		setLayout(new BorderLayout());
		setSize(new Dimension(1024, 768));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    
		JPanel panel = new JPanel() {
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				Graphics2D graphics = (Graphics2D)g;
				graphics.setStroke(new BasicStroke(4.0f));
				
				for (Curve curve: curves) {
					graphics.setColor(curve.color);
					for (int i = 0; i < curve.points.size() - 1; i++)
						graphics.drawLine(curve.points.get(i).x, curve.points.get(i).y, curve.points.get(i + 1).x, curve.points.get(i + 1).y);
				}
			}

		};
		panel.setBackground(Color.WHITE);
		add(panel, BorderLayout.CENTER);

		panel.addMouseListener(new MouseAdapter() {
			@Override
			public void mousePressed(MouseEvent e) {				
				curves.add(new Curve(e.getX(), e.getY(), COLORS[(int)(Math.random() * COLORS.length)]));
				repaint();
			}
		});
		
		panel.addMouseMotionListener(new MouseMotionAdapter() {
			@Override
			public void mouseDragged(MouseEvent e) {
				curves.get(curves.size() - 1).points.add(new Point(e.getX(), e.getY()));
				repaint();
			}
		});
		
		JPanel console = new JPanel();
		console.setBackground(Color.WHITE);
	    add(console, BorderLayout.NORTH);
	    
	    JButton delete = new JButton("Delete");
	    delete.addActionListener(new ActionListener() {
	    	@Override
	    	public void actionPerformed(ActionEvent e) {
	    		curves.clear();
	    		repaint();
	    	}
	    });
	    console.add(delete);
	}

	public static void main(String[] args) {
		new Curves().setVisible(true);
	}

}

class Curve {

	public List<Point> points;

	public Color color;

	public Curve(int x, int y, Color color) {
		points = new ArrayList<Point>();
		points.add(new Point(x, y));
		
		this.color = color;
	}

}
