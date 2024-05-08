import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Point;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.HashSet;
import java.util.Set;

import javax.swing.JFrame;
import javax.swing.JPanel;

@SuppressWarnings("serial")
public class Pong extends JFrame {	

	static final int SIZE = 24;
	
	static final int MOVE = 4;
	
	JPanel panel;
	
	Ball ball;
	
	Point walls;
	
	public Pong() {
		super("Pong");
		
		ball = new Ball();
		
		setResizable(true);
		setSize(new Dimension(800, 600));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		panel = new JPanel() {
			
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				
				g.setColor(Color.LIGHT_GRAY);
				g.fillRect(walls.x, 0, SIZE, getHeight());
				g.fillRect(0, walls.y - SIZE, getWidth(), SIZE);
				
				g.setColor(Color.BLACK);
				g.fillOval(ball.position.x - SIZE / 2, ball.position.y - SIZE / 2, SIZE, SIZE);
			}
			
		};
		panel.setBackground(Color.WHITE);
		add(panel);
		
		panel.setFocusable(true);
		panel.addKeyListener(new KeyAdapter() {
			
			Set<Integer> keys = new HashSet<Integer>();

			@Override
			public synchronized void keyPressed(KeyEvent e) {
				keys.add(e.getKeyCode());
				
				for (int key: keys) 
					switch (key) {
					case KeyEvent.VK_LEFT:
						walls.x = Math.max(walls.x - MOVE, panel.getWidth() / 2);
						break;
					case KeyEvent.VK_RIGHT:
						walls.x = Math.min(walls.x + MOVE, panel.getWidth());
						break;
					case KeyEvent.VK_UP:
						walls.y = Math.max(walls.y - MOVE, 0);
						break;
					case KeyEvent.VK_DOWN:
						walls.y = Math.min(walls.y + MOVE, panel.getHeight() / 2);
						break;
					default:
						break;
					}
			}
			
			@Override
		    public synchronized void keyReleased(KeyEvent e) {
		        keys.remove(e.getKeyCode());
		    }
			
		});
		
		setVisible(true);
		
		ball = new Ball(new Point(panel.getWidth() / 2, panel.getHeight() / 2));
		walls = new Point(3 * panel.getWidth() / 4, panel.getHeight() / 4);
	}
	
	public static void main(String[] args) throws InterruptedException {
		Pong pong = new Pong();
		
		while (true) {
			pong.ball.position.x += pong.ball.direction.x;
			pong.ball.position.y += pong.ball.direction.y;
			
			if (pong.ball.position.x < SIZE / 2 || pong.ball.position.x > pong.walls.x - SIZE / 2) {
				pong.ball.position.x = Math.max(SIZE / 2, Math.min(pong.walls.x - SIZE / 2, pong.ball.position.x));
				pong.ball.direction.x *= -1;
			}
			
			if (pong.ball.position.y < pong.walls.y + SIZE / 2 || pong.ball.position.y > pong.panel.getHeight() - SIZE / 2) {
				pong.ball.position.y = Math.max(pong.walls.y + SIZE / 2, Math.min(pong.panel.getHeight() - SIZE / 2, pong.ball.position.y));
				pong.ball.direction.y *= -1;
			}
			
			pong.repaint();

			Thread.sleep(50);
		}
	}

}

class Ball {
	
	Point position;
	
	Point direction;
	
	public Ball() {
		this(new Point());
	}
	
	public Ball(Point position) {
		this(position, 2.0 * Math.PI * Math.random());
	}
	
	public Ball(Point position, double angle) {
		this(position, new Point((int)(Math.cos(angle) * Pong.SIZE), (int)(Math.sin(angle) * Pong.SIZE)));
	}

	public Ball(Point position, Point direction) {
		super();

		this.position = position;
		this.direction = direction;
	}
	
}
