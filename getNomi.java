import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.util.*;
import java.io.File;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.io.IOException;

public class getNomi {

    public static void main(String[] args) {

        String directoryPath = "E:\\Giovanni\\Desktop\\html";
        File directory = new File(directoryPath);

        if (directory.exists() && directory.isDirectory()) {
            File[] files = directory.listFiles();

            if (files != null) {
                for (File file : files) {
                    if (file.isFile()) {
						try {

							Document document = Jsoup.parse(file, "UTF-8", "");
							ArrayList<String> nomi = new ArrayList<>();

							Elements h3Elements = document.select("li.o-chart-results-list__item h3");
							for (Element h3Element : h3Elements) {
								nomi.add(h3Element.text());
							}
							
							try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
								for (String nome : nomi) {
									writer.write(nome + '\n');
								}
							} catch (IOException e) {
								e.printStackTrace();
							}

						} catch (IOException e) {
							e.printStackTrace();
						}

                    }
                }
            }
        }
    }
}