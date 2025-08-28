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

public class ReadFilesInDirectory {

    public static void main(String[] args) {

		String postPath = "facebook\\post\\";
		
        File htmlDirectory = new File(postPath + "html\\");
		File dateDirectory = new File(postPath + "date\\");
		File linkDirectory = new File(postPath + "link\\");

		if (!dateDirectory.exists()) {
			dateDirectory.mkdirs();
		}

		if (!linkDirectory.exists()) {
			linkDirectory.mkdirs();
		}

		int _10 = 0;
		int _100 = 0;

        if (htmlDirectory.exists() && htmlDirectory.isDirectory()) {
            File[] htmlFiles = htmlDirectory.listFiles();

            if (htmlFiles != null) {
                for (File htmlFile : htmlFiles) {
                    if (htmlFile.isFile()) {
						try {

							String fileName = htmlFile.getName().substring(0, htmlFile.getName().length() - 5);
							File dateFile = new File(postPath + "date\\" + fileName + ".txt");
							File linkFile = new File(postPath + "link\\" + fileName + ".txt");

							if (!dateFile.exists() || !linkFile.exists()) {

								Document document = Jsoup.parse(htmlFile, "UTF-8", "");
								
								//seleziona post;
								Elements posts = document.select("div[role=main]").first().child(3).child(1).child(0).child(1).child(0).children();
								ArrayList<Element> dateList = new ArrayList<>();
								ArrayList<Boolean> span_or_a = new ArrayList<>();
								
								//seleziona span del link per ogni post;
								for (int i = 0; i < posts.size() - 3; i++) {
									Elements els = posts.get(i).select("a[role=link] > span");
									Element el;
									if ((els.size() > 0) && ((el = els.get(0)).select("span:not([class])").size() > 0)) {
										dateList.add(el);
										span_or_a.add(false);
									} else {
										el = posts.get(i).select("a[role=link]").get(3);
										dateList.add(el);
										span_or_a.add(true);
									}
								}
								System.out.println(fileName + " " + dateList.size());
								
								//conta post;
								if (dateList.size() >= 10) {
									_10++;
								}
								if (dateList.size() >= 100) {
									_100++;
								}

								//scrivi i span su file (se il file non esiste);
								try {
									if (!dateFile.exists()) {
										PrintStream ps = new PrintStream(dateFile);
										for (int i = 0; i < dateList.size(); i++) {
											ps.println(dateList.get(i).text());
										}
										ps.close();
									}
								} catch (FileNotFoundException e) {
									e.printStackTrace();
								}

								//scrivi i link su file (se il file non esiste);
								try {
									if (!linkFile.exists()) {
										PrintStream ps = new PrintStream(linkFile);
										for (int i = 0; i < dateList.size(); i++) {
											String link;
											if (span_or_a.get(i) == false) {
												link = dateList.get(i).parent().attr("href");
											} else {
												link = dateList.get(i).attr("href");
											}
											link = link.substring(0, link.indexOf("__cft__[0]"));
											if (!isMainPage(link, fileName)) {
												ps.println(link);
											} else {
												System.out.println("---Main Page: " + link + " " + i);
											}
										}
										ps.close();
									}
								} catch (FileNotFoundException e) {
									e.printStackTrace();
								}

							}

						} catch (IOException e) {
							e.printStackTrace();
						}

                    }
                }
            }
        }

		System.out.println("10: " + _10 + ", 100: " + _100);

    }

	public static boolean isMainPage(String link, String fileName) {
		return link.equals("https://www.facebook.com/" + fileName + "?");
	}

}