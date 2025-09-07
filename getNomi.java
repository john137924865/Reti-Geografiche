import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;

public class getNomi {
    public static void main(String[] args) {
        try {
            File input = new File("Hot 100 Artists.htm");
            Document doc = Jsoup.parse(input, "UTF-8");

            // Seleziona tutti i nomi degli artisti
            Elements artists = doc.select("h3.c-title");

            int count = 0;
            int skip = 2;
            for (Element artist : artists) {
                if (skip > 0) {
                    skip--;
                    continue;
                }
                String name = artist.text().trim();
                if (!name.isEmpty()) {
                    System.out.println((count + 1) + ". " + name);
                    count++;
                    if (count >= 100) break; // solo i primi 100
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
