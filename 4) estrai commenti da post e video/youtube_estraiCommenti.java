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
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Scanner;
import java.util.Vector;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.io.PrintStream;
import java.lang.IndexOutOfBoundsException;
import java.lang.Math;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
//import org.w3c.dom.Document;
//import org.w3c.dom.Element;

public class youtube_estraiCommenti {

    public static void main(String[] args) throws IOException, ParserConfigurationException, TransformerException {
		
		// gli ultimi 25 video con almeno 20 commenti;

		String htmlVideoPath = "E:\\youtube\\video\\html";
		File htmlVideoDir = new File(htmlVideoPath);

		String xmlFolderString = "E:\\youtube\\xml\\";
		File xmlFolder = new File(xmlFolderString);
		if (!xmlFolder.exists()) {
			xmlFolder.mkdir();
		}

		if (htmlVideoDir.isDirectory()) {
            File[] nomiDir = htmlVideoDir.listFiles();
            if (nomiDir != null) {
                for (File nomeDir : nomiDir) {
                    if (nomeDir.isDirectory()) {
                        String name = nomeDir.getName(); //nome canale esatto: "@nome"
						extractComments(htmlVideoPath, nomeDir, name);

						//System.exit(0);
                    }
                }
			}
		}

    }

	static void extractComments(String htmlVideoPath, File nomeDir, String name) throws ParserConfigurationException, TransformerException {

		/* Creazione xml name root */
		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();

		org.w3c.dom.Document nameDocument = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
		org.w3c.dom.Element nameElement = nameDocument.createElement("Name_" + name);
		nameDocument.appendChild(nameElement);

		File[] videos = nomeDir.listFiles();

		Arrays.sort(videos, new Comparator<File>() {
			@Override
			public int compare(File f1, File f2) {
				int num1 = extractNumber(f1.getName());
				int num2 = extractNumber(f2.getName());
				return Integer.compare(num1, num2);
			}

			private int extractNumber(String name) {
				String numberPart = name.split("\\.")[0];
				return Integer.parseInt(numberPart);
			}
		});

		if (videos != null) {
			int n = 0;
			for (File video : videos) {
				if (video.isFile()) {

					n++;
					if (n > 25) {
						break;
					}
					String htmlFileName = video.getName();

					// aggiungo file a xml
					org.w3c.dom.Element videoFile = nameDocument.createElement("File_" + htmlFileName);
					nameElement.appendChild(videoFile);

					/* estrazione commenti */
					ArrayList<String> commenti = new ArrayList<>();

					File htmlFile = new File(htmlVideoPath + "\\" + name + "\\" + htmlFileName);
					Document document = null;
					try {
						document = Jsoup.parse(htmlFile, "UTF-8", "");
					} catch (IOException e) {}
					Elements commentiEl = document.select("ytd-comments[id=comments]").first().select("ytd-item-section-renderer")
							.select("> div[id=contents]").select("> ytd-comment-thread-renderer");
					for (Element commentoEl : commentiEl) {
						Element mainEl = commentoEl.select("> ytd-comment-view-model").first().select("> div[id=body]").first()
								.select("> div[id=main]").first();
						Element autoreEl = mainEl.select("div[id=header-author]").first().select("a[id=author-text]").first();
						String autore = autoreEl.attr("href").substring(2);
						Element commentoTestoEl = mainEl.select("> ytd-expander").first().select("> div[id=content]").first()
								.select("> yt-attributed-string").first().select("> span").first();
						String commento = commentoTestoEl.text();
						if (!autore.equals(name)) {
							commenti.add(commento);
						}
					}

					// aggiungo attributo a file
					videoFile.setAttribute("commenti", commenti.size() + "");
					String s = (n < 10) ? ("0" + n) : (n + "");
					nameElement.setAttribute("_" + s, commenti.size() + "");
					for (int i = 0; i < commenti.size(); i++) {
						org.w3c.dom.Element commentoFile = nameDocument.createElement("Commento_" + (i + 1));
						videoFile.appendChild(commentoFile);
						commentoFile.setAttribute("testo", commenti.get(i));
					}

				}
			}
		}
		
		DOMSource domSource = new DOMSource(nameDocument);
		StreamResult streamResult = new StreamResult(new File("E:\\youtube\\xml\\_" + name + ".xml"));
		transformer.transform(domSource, streamResult);

	}
    
}