import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.io.PrintStream;
import java.lang.IndexOutOfBoundsException;
import java.lang.Math;
import java.util.Scanner;

public class youtube_getVideosLinks {

    public static void main(String[] args) throws IOException {

		(new Scanner(System.in)).nextLine();
		
		String channelPath = "youtube\\channel";
		String htmlPath = channelPath + "\\html";
		String linkPath = channelPath + "\\link";

		File htmlDirectory = new File(htmlPath);
		File linkDirectory = new File(linkPath);

		if (!htmlDirectory.exists()) {
			htmlDirectory.mkdirs();
		}

		if (!linkDirectory.exists()) {
			linkDirectory.mkdirs();
		}

		if (htmlDirectory.exists() && htmlDirectory.isDirectory()) {
            File[] htmlFiles = htmlDirectory.listFiles();
            if (htmlFiles != null) {

				int n = 30;
				int counter = 0;

                for (File htmlFile : htmlFiles) {
                    if (htmlFile.isFile()) {
						
						ArrayList<String> links = new ArrayList<>();

						Document document = Jsoup.parse(htmlFile, "UTF-8", "");
						Element scroll = document.select("div[id=scroll-container]").first();
						Element header = scroll.parent().parent().parent().parent();
						Element tmp = header.nextElementSibling();
						while (!tmp.id().equals("contents")) {
							tmp = tmp.nextElementSibling();
						}
						Elements videos = tmp.select("ytd-rich-item-renderer");
						for (Element video : videos) {
							Element a = video.select("a[id=video-title-link]").first();
							links.add("https://www.youtube.com" + a.attr("href"));
						}

						if (links.size() < n) {
							counter++;
							continue;
						}

						String nome = htmlFile.getName();
						File linksFile = new File(linkPath + "\\" + nome.substring(0, nome.length() - 5) + ".txt");
						try (BufferedWriter writer = new BufferedWriter(new FileWriter(linksFile))) {
							for (String link : links) {
								writer.write(link + '\n');
							}
						} catch (IOException e) {
							e.printStackTrace();
						}
						
					}
				}

				System.out.println("< " + n + " : " + counter);

			}
		}
		

    }
    
}