import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.io.IOException;

public class getNomi {
    public static void main(String[] args) {
        try {
            File input = new File("Hot 100 Artists.htm");
            Document doc = Jsoup.parse(input, "UTF-8");

            Elements artists = doc.select("h3.c-title");

            // Crea documento XML
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            org.w3c.dom.Document xmlDoc = dBuilder.newDocument();

            // Root element <names>
            org.w3c.dom.Element rootElement = xmlDoc.createElement("names");
            xmlDoc.appendChild(rootElement);

            int count = 0;
            int skip = 2;
            for (Element artist : artists) {
                if (skip > 0) {
                    skip--;
                    continue;
                }
                String name = artist.text().trim();
                if (!name.isEmpty()) {
                    // Crea elemento <name>
                    org.w3c.dom.Element nameElement = xmlDoc.createElement("name");
                    nameElement.setTextContent(name);
                    rootElement.appendChild(nameElement);

                    count++;
                    if (count >= 100) break;
                }
            }

            // Scrivi il documento XML su file
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
            Transformer transformer = transformerFactory.newTransformer();
            transformer.setOutputProperty(OutputKeys.INDENT, "yes");
            transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
            DOMSource source = new DOMSource(xmlDoc);
            StreamResult result = new StreamResult(new File("artists.xml"));
            transformer.transform(source, result);

            System.out.println("XML creato con successo!");

        } catch (IOException | ParserConfigurationException | TransformerException e) {
            e.printStackTrace();
        }
    }
}
