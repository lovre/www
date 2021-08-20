import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

import javax.imageio.ImageIO;

public class Watermark {
	
	public static void main(String[] args) throws IOException {
		BufferedImage image = ImageIO.read(new File("images", "cats.jpg"));
		
		for (int i = 0; i < image.getWidth(); i++)
			for (int j = 0; j < image.getHeight(); j++)
				image.setRGB(i, j, new Color(image.getRGB(i, j)).brighter().getRGB());
		
		Graphics2D graphics = image.createGraphics();
		
		/* AffineTransform transform = graphics.getTransform(); */

		graphics.translate(image.getWidth() / 2, image.getHeight() / 2);
		graphics.rotate(-Math.PI / 4);
	
		graphics.setColor(new Color(0, 0, 0, 64));
		graphics.setFont(new Font(Font.MONOSPACED, Font.BOLD, 96));
		
		graphics.drawString("Watermark", -graphics.getFontMetrics().stringWidth("Watermark") / 2, graphics.getFontMetrics().getAscent() / 2);
		
		/* graphics.setTransform(transform); */
		
		ImageIO.write(image, "png", new File("images", "cats.png"));
	}
	
}
