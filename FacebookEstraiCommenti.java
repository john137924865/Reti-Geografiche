import java.io.File;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import org.jsoup.Jsoup;
import org.jsoup.select.Elements;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.io.PrintStream;
import java.lang.IndexOutOfBoundsException;
import java.lang.Math;
import java.nio.file.Files;
import java.util.Scanner;
import java.util.Comparator;
import java.util.List;

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
import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class FacebookEstraiCommenti {

    public static void main(String[] args) throws IOException, ParserConfigurationException, TransformerException {
		
        File postsFolder = new File("facebook\\commenti\\html\\");
		String xmlFolderString = "facebook\\commenti\\xml\\";
		File xmlFolder = new File(xmlFolderString);
		if (!xmlFolder.exists()) {
			xmlFolder.mkdir();
		}

		Document info = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
		Element infoRoot = info.createElement("info");
		info.appendChild(infoRoot);

		TransformerFactory transformerFactory = TransformerFactory.newInstance();
		Transformer transformer = transformerFactory.newTransformer();

        if (postsFolder.exists() && postsFolder.isDirectory()) {
            File[] postsList = postsFolder.listFiles();

			if (postsList != null) {

				for (File postsNameFolder : postsList) {

					if (postsNameFolder.isDirectory()) {

						System.out.println(postsNameFolder.getName());
						Document nameDocument = DocumentBuilderFactory.newInstance().newDocumentBuilder().newDocument();
						Element nameElement = nameDocument.createElement("Name_" + postsNameFolder.getName());
						nameDocument.appendChild(nameElement);
						
						File[] postsNameList = postsNameFolder.listFiles();
						
						Arrays.sort(postsNameList, new Comparator<File>() {
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

						//per ognuno dei 20 file estrai commenti per ogni cartella nome
						int n = 0;
						Element infoEl = info.createElement("Name_" + postsNameFolder.getName());
						for (File postHtml : postsNameList) {
							n++;
							String s = (n < 10) ? ("0" + n) : (n + "");
							ArrayList<String> commenti = estraiCommenti(postHtml);
							Element htmlFile = nameDocument.createElement("File_" + postHtml.getName());
							nameElement.appendChild(htmlFile);
							htmlFile.setAttribute("commenti", commenti.size() + "");
							nameElement.setAttribute("_" + s, commenti.size() + "");
							infoEl.setAttribute("_" + s, commenti.size() + "");
							infoRoot.appendChild(infoEl);
							for (int i = 0; i < commenti.size(); i++) {
								Element commentoFile = nameDocument.createElement("Commento_" + (i + 1));
								htmlFile.appendChild(commentoFile);
								commentoFile.setAttribute("testo", commenti.get(i));
							}
						}

						DOMSource domSource = new DOMSource(nameDocument);
						StreamResult streamResult = new StreamResult(new File("facebook\\commenti\\xml\\_" + postsNameFolder.getName() + ".xml"));
						transformer.transform(domSource, streamResult);

					}

				}

			}
		}

		DOMSource domSource2 = new DOMSource(info);
		StreamResult streamResult2 = new StreamResult(new File("facebook\\commenti\\info.xml"));
		transformer.transform(domSource2, streamResult2);

	}

	public static ArrayList<String> estraiCommenti(File commentoHtml) throws IOException {

		ArrayList<String> commentoLista = new ArrayList<>();

		org.jsoup.nodes.Document doc = Jsoup.parse(commentoHtml, "UTF-8");
		org.jsoup.nodes.Element span = doc.select("span:contains(Più pertinenti)").first();

		if (span != null) {
			org.jsoup.nodes.Element parent = span.parent().parent().parent();
			org.jsoup.nodes.Element nextSibling = parent.nextElementSibling();

			Elements commenti = nextSibling.select("> div[data-virtualized='false']");

			for (org.jsoup.nodes.Element commento : commenti) {
				
				String commentoStringa = "";

				Elements righe = commento.select("div");
				
				ArrayList<org.jsoup.nodes.Element> righeNew = new ArrayList<>();
				
				for (int i = 0; i < righe.size(); i++) {
					boolean hasDirAuto = "auto".equals(righe.get(i).attr("dir"));
					boolean hasStyleTextAlignStart = "text-align: start;".equals(righe.get(i).attr("style"));
					boolean hasNoClasses = righe.get(i).classNames().isEmpty();

					if (hasDirAuto && hasStyleTextAlignStart && hasNoClasses) {
						if (!righe.get(i).text().replace("\r\n", " ").replace("\r", " ").replace("\n", " ").trim().equals("")) {
							righeNew.add(righe.get(i));
						}
					}
				}
				
				for (int i = 0; i < righeNew.size(); i++) {
					commentoStringa += righeNew.get(i).text();
					if ((righeNew.size() > 1) && (i != righeNew.size() - 1)) {
						commentoStringa += System.lineSeparator();
					}
				}

				if (!commentoStringa.equals("")) {
					commentoLista.add(commentoStringa);
				}

			}

		}

		return commentoLista;

	}

}