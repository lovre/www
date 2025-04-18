import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Pixel extends JFrame {

	public static int SIZE = 16;

	private Point pixel;

	public Pixel() {
		super();

		pixel = new Point(256, 256);

		setTitle("Pixel");
		setSize(new Dimension(1024, 768));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		JPanel panel = new JPanel() {
			@Override
			public void paint(Graphics g) {
				super.paint(g);

				g.fillRect(pixel.x - SIZE / 2, pixel.y - SIZE / 2, SIZE, SIZE);
			}
		};

		panel.addKeyListener(new KeyListener() {

			@Override
			public void keyPressed(KeyEvent e) {
				switch (e.getKeyCode()) {
				case KeyEvent.VK_LEFT:
					pixel.x -= SIZE;
					break;
				case KeyEvent.VK_RIGHT:
					pixel.x += SIZE;
					break;
				case KeyEvent.VK_UP:
					pixel.y -= SIZE;
					break;
				case KeyEvent.VK_DOWN:
					pixel.y += SIZE;
					break;
				default:
					break;
				}

				panel.repaint();
			}

			@Override
			public void keyReleased(KeyEvent e) { }

			@Override
			public void keyTyped(KeyEvent e) { }

		});

		panel.setFocusable(true);
		add(panel);
	}

	public static void main(String[] args) {
		new Pixel().setVisible(true);
	}

}
