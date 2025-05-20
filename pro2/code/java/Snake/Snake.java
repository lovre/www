import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Point;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JFrame;
import javax.swing.JPanel;

public class Snake {

	public static final int SIZE = 16;

	public static List<Point> snake = new ArrayList<Point>();

	public static void main(String[] args) throws InterruptedException {
		JFrame frame = new JFrame("Snake");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(new Dimension(800, 600));
		frame.setResizable(true);

		JPanel panel = new JPanel() {
			private static final long serialVersionUID = 1L;
			@Override
			public void paint(Graphics g) {
				super.paint(g);
				Graphics2D graphics = (Graphics2D)g;

				graphics.setColor(Color.BLACK);
				graphics.setStroke(new BasicStroke(4.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));

        if (snake.size() > 0) {
          graphics.fillOval(snake.get(0).x - SIZE / 2, snake.get(0).y - SIZE / 2, SIZE, SIZE);
          for (int i = 0; i < snake.size() - 1; i++)
            graphics.drawLine(snake.get(i).x, snake.get(i).y, snake.get(i + 1).x, snake.get(i + 1).y);
        }
			}
		};
		panel.setBackground(Color.WHITE);
		frame.add(panel);

		frame.setVisible(true);

		Point head = new Point(panel.getWidth() / 2, panel.getHeight() / 2);
		for (int i = 0; i < SIZE; i++)
			snake.add(new Point(head.x + i * SIZE, head.y));

		while (true) {
			head = snake.get(0);

			List<Point> moves = new ArrayList<Point>();
			for (Point move: new Point[] { new Point(head.x + SIZE, head.y), new Point(head.x - SIZE, head.y), new Point(head.x, head.y + SIZE), new Point(head.x, head.y - SIZE) })
				if (move.x >= 0 && move.x < panel.getWidth() && move.y >= 0 && move.y < panel.getHeight() && !snake.contains(move))
					moves.add(move);

			if (moves.size() > 0) {
				snake.add(0, moves.get((int)(Math.random() * moves.size())));
				snake.remove(snake.size() - 1);
			}

			panel.repaint();

			Thread.sleep(100);
		}
	}

}
