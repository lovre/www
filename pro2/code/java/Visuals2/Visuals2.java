import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.Polygon;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.JTextField;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

public class Visuals2 {
	
	public static Point ball = new Point();
	
	public static void main(String[] args) {
		JFrame frame = new JFrame("Visuals2");
		frame.setSize(new Dimension(1024, 720));
		frame.setMinimumSize(new Dimension(800, 600));
		frame.setResizable(true);
		
		JPanel panel = new Panel2(); // new JPanel();
		// panel.setBackground(Color.WHITE);
		frame.add(panel);
		
		frame.setLayout(new BorderLayout());
		frame.add(panel, BorderLayout.CENTER);
		JPanel north = new JPanel();
		frame.add(north, BorderLayout.NORTH);
		JPanel south = new JPanel();
		frame.add(south, BorderLayout.SOUTH);
		
		north.add(new JLabel("Football  "));

		JButton button = new JButton("Center");
		button.setPreferredSize(new Dimension(96, 40));
		button.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
			}
		});
		north.add(button);
		
		JSlider slider = new JSlider(1, 100, 50);
		slider.addChangeListener(new ChangeListener() {
			@Override
			public void stateChanged(ChangeEvent e) {
				panel.repaint();
			}
		});
		north.add(slider);
		
		JCheckBox checkbox = new JCheckBox("Animate", true);
		checkbox.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				panel.repaint();
			}
		});
		north.add(checkbox);
		
		JTextField field = new JTextField();
		field.setPreferredSize(new Dimension(128, 24));
		field.addKeyListener(new KeyListener() {
			@Override
			public void keyPressed(KeyEvent e) {
				if (e.getKeyCode() == KeyEvent.VK_ENTER)
					field.setText("");
			}
			@Override
			public void keyReleased(KeyEvent e) { }
			@Override
			public void keyTyped(KeyEvent e) { }
		});
		north.add(field);
		
		south.setLayout(new GridLayout(3, 1));
		for (int i = 0; i < 3; i++) {
			float rgb = (i + 1) / 4.0f;
			Color color = new Color(rgb, rgb, rgb);
			JPanel subsouth = new JPanel();
			subsouth.setBackground(color);
			south.add(subsouth);
		}
		
		// frame.getRootPane().putClientProperty("apple.awt.brushMetalLook", true);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setVisible(true);
		
		ball = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
		Point direction = new Point(8, -8);
		while (true) {
			if (checkbox.isSelected()) {
				ball.setLocation(ball.getX() + direction.getX(), ball.getY() + direction.getY());
				if (ball.getX() <= 32) {
					ball.setLocation(32, ball.getY());
					direction.setLocation(-direction.getX(), direction.getY());
				}
				else if (ball.getX() >= panel.getWidth() - 32) {
					ball.setLocation(panel.getWidth() - 32, ball.getY());
					direction.setLocation(-direction.getX(), direction.getY());
				}
				if (ball.getY() <= 32) {
					ball.setLocation(ball.getX(), 32);
					direction.setLocation(direction.getX(), -direction.getY());
				}
				else if (ball.getY() >= panel.getHeight() - 32) {
					ball.setLocation(ball.getX(), panel.getHeight() - 32);
					direction.setLocation(direction.getX(), -direction.getY());
				}
			}
      
			frame.repaint(); // ponoven izris okna
			try {
				Thread.sleep(slider.getValue()); // Thread.sleep(50); // počakaj 50 ms
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
}

@SuppressWarnings("serial")
class Panel2 extends JPanel {

	public Panel2() {
		super();
		setBackground(Color.WHITE);
	}

	@Override
	public void paint(Graphics g) {
		super.paint(g); // klic metode nadrazreda
		Graphics2D graphics = (Graphics2D)g; // pretvarjanje tipov
		int indent = 32, size = 96; // pomožne spremenljivke

		int x = indent, y = indent;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawLine(x, y, x + size, y);
		
		y += indent;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillRect(x, y, size, size);
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawRect(x, y, size, size);
		x += indent + size;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		graphics.drawRoundRect(x, y, size, size, size / 5, size / 5);
		
		x = indent; y += indent + size;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawOval(x, y, 2 * size + indent, size);
		y += indent + size;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillOval(x, y, size, size);
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawOval(x, y, size, size);
		
		x += indent + size;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		graphics.drawArc(x, y, size, size, 90, 270);
		x += indent + size;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillArc(x, y, size, size, 20, 320);
		graphics.setColor(Color.WHITE);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.fillOval(x + size / 2, y + size / 5, size / 8, size / 8);
		
		x = indent; y += indent + size;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		Polygon quadrilateral = new Polygon();
		quadrilateral.addPoint(x, y); quadrilateral.addPoint(x + 2 * size + indent, y + size / 2);
		quadrilateral.addPoint(x, y + size); quadrilateral.addPoint(x + size + indent, y);
		graphics.drawPolygon(quadrilateral);
		x += 2 * (indent + size);
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		Polygon polygon = new Polygon();
		for (int i = 0; i < 12; i++)
			polygon.addPoint((int)(x + Math.random() * size), (int)(y + Math.random() * size));
		graphics.fillPolygon(polygon);
		
		y = 2 * indent;
		try { // shrani sliko v spremenljivko ali konstanto!
			graphics.drawImage(ImageIO.read(new File("images", "cats.jpg")), x, y, size, size, null);
		} catch (IOException e) {
			e.printStackTrace();
		}

		x = 2 * indent + size; y = indent;
		String string = getWidth() + "x" + getHeight();
		graphics.setColor(Color.BLACK);
		graphics.setFont(new Font("Montserrat", Font.BOLD, 11));
		graphics.drawString(string, x, y);
		x += size / 2; y += indent + size / 2;
		graphics.setColor(Color.GRAY);
		graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, 14));
		FontMetrics metrics = graphics.getFontMetrics();
		graphics.drawString(string, x - metrics.stringWidth(string) / 2, y + metrics.getAscent() / 2);
		
		int width = (getWidth() / 2 - 4 * indent) / 3;
		int height = (getHeight() - 6 * indent) / 4;
		
		x = getWidth() / 2 + indent; y = indent;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawLine(x, y, x + width, y);
		
		y += indent;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillRect(x, y, width, height);
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawRect(x, y, width, height);
		x += indent + width;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		graphics.drawRoundRect(x, y, width, height, width / 5, height / 5);
		
		x = getWidth() / 2 + indent; y += indent + height;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawOval(x, y, 2 * width + indent, height);
		y += indent + height;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillOval(x, y, width, height);
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.drawOval(x, y, width, height);
		
		x += indent + width;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		graphics.drawArc(x, y, width, height, 90, 270);
		x += indent + width;
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(1.0f));
		graphics.fillArc(x, y, width, height, 20, 320);
		graphics.setColor(Color.WHITE);
		graphics.setStroke(new BasicStroke(2.0f));
		graphics.fillOval(x + width / 2, y + height / 5, width / 8, height / 8);
		
		x = getWidth() / 2 + indent; y += indent + height;
		graphics.setColor(Color.BLACK);
		graphics.setStroke(new BasicStroke(2.0f));
		quadrilateral = new Polygon();
		quadrilateral.addPoint(x, y); quadrilateral.addPoint(x + 2 * width + indent, y + height / 2);
		quadrilateral.addPoint(x, y + height); quadrilateral.addPoint(x + width + indent, y);
		graphics.drawPolygon(quadrilateral);
		x += 2 * (indent + width);
		graphics.setColor(Color.GRAY);
		graphics.setStroke(new BasicStroke(4.0f));
		polygon = new Polygon();
		for (int i = 0; i < 12; i++)
			polygon.addPoint((int)(x + Math.random() * width), (int)(y + Math.random() * height));
		graphics.fillPolygon(polygon);
		
		y = 2 * indent;
		try { // shrani sliko v spremenljivko ali konstanto!
			graphics.drawImage(ImageIO.read(new File("images", "cats.jpg")), x, y, width, height, null);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		x = getWidth() / 2 + 2 * indent + width; y = indent;
		graphics.setColor(Color.BLACK);
		graphics.setFont(new Font("Montserrat", Font.BOLD, 11));
		graphics.drawString(string, x, y);
		x += width / 2; y += indent + height / 2;
		graphics.setColor(Color.GRAY);
		graphics.setFont(new Font(Font.SANS_SERIF, Font.BOLD, (int)Math.round(0.15 * width)));
		metrics = graphics.getFontMetrics();
		graphics.drawString(string, x - metrics.stringWidth(string) / 2, y + metrics.getAscent() / 2);		
		
		try { // shrani sliko v spremenljivko ali konstanto!
			graphics.drawImage(ImageIO.read(new File("images", "football.png")), (int)Visuals2.ball.getX() - 32, (int)Visuals2.ball.getY() - 32, 64, 64, null);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
