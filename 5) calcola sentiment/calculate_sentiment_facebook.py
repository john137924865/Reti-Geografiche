import xml.etree.ElementTree as ET
import fasttext
import os
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import statistics

# === CONFIG ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTIMENT_DIR = os.path.join(BASE_DIR, "sentiment")
SCARTI_DIR = os.path.join(BASE_DIR, "scarti")
FASTTEXT_MODEL = os.path.join(BASE_DIR, "lid.176.bin")
SUMMARY_FILE = os.path.join(BASE_DIR, "sentiment_totali.xml")

INPUT_DIR = r"C:\Users\John\Desktop\facebook\commenti\xml"

# Crea cartelle output se non esistono
os.makedirs(SENTIMENT_DIR, exist_ok=True)
os.makedirs(SCARTI_DIR, exist_ok=True)

# === CARICA MODELLI ===
print("Carico modello di lingua...")
lang_model = fasttext.load_model(FASTTEXT_MODEL)
analyzer = SentimentIntensityAnalyzer()

# === FUNZIONI ===
def remove_links(text):
    # rimuove tutti gli URL che iniziano con http o https
    return re.sub(r'https?://\S+', '', text)

def detect_lang(text, top_k=3, min_ratio=0.95):
    text = text.lower().strip()
    labels, probs = lang_model.predict(text.replace("\n", " ")[:500], k=top_k)
    max_prob = probs[0]
    for label, prob in zip(labels, probs):
        language_code = label.replace("__label__", "")
        if language_code == "en" and prob >= min_ratio * max_prob:
            return "en"
    
    # Se non trovi l'inglese con sufficiente probabilità, ritorna la lingua più probabile
    return labels[0].replace("__label__", "")

def vader_sentiment(text):
    return analyzer.polarity_scores(text)["compound"]

# === ROOT DEL FILE SUMMARY ===
summary_root = ET.Element("Artisti")

# === ELABORA TUTTI I FILE ===
for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(".xml"):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    base_name = os.path.splitext(filename)[0]
    output_path = os.path.join(SENTIMENT_DIR, f"{base_name}Sentiment.xml")
    scarti_path = os.path.join(SCARTI_DIR, f"{base_name}Scarti.xml")

    print(f"Analizzo {filename}...")

    # === PARSE XML ===
    tree = ET.parse(input_path)
    root = tree.getroot()

    scarti_root = ET.Element("Scarti")

    artist_scores = []

    # Nodo artista nel summary
    artista_node = ET.SubElement(summary_root, "Artista")
    artista_node.set("nome", base_name)

    for file_node in root.findall("./"):
        if not file_node.tag.startswith("File_"):
            continue

        post_scores = []

        for comment_node in file_node.findall("./"):
            testo = comment_node.attrib.get("testo", "").strip()
            testo = remove_links(testo).strip()
            if not testo:
                continue

            lang = detect_lang(testo)
            if lang == "en":
                score = vader_sentiment(testo)
                comment_node.set("sentiment", f"{score:.3f}")
                post_scores.append(score)
                artist_scores.append(score)
            else:
                # aggiungi ai commenti scartati
                scarti_comment = ET.SubElement(scarti_root, "Commento")
                scarti_comment.set("lingua", lang)
                scarti_comment.text = testo

        if post_scores:
            mean_post = statistics.mean(post_scores)
            file_node.set("sentiment", f"{mean_post:.3f}")
            # aggiungi post al nodo artista del summary
            post_node = ET.SubElement(artista_node, "Post")
            post_node.set("nome", file_node.tag)
            post_node.set("sentiment", f"{mean_post:.3f}")
        else:
            file_node.set("sentiment", "N/A")

    if artist_scores:
        mean_artist = statistics.mean(artist_scores)
        root.set("sentiment", f"{mean_artist:.3f}")
        # aggiungi sentiment artista del summary
        artista_node.set("sentiment", f"{mean_artist:.3f}")
    else:
        root.set("sentiment", "N/A")
        artista_node.set("sentiment", "N/A")

    # === SALVA FILE ===
    ET.ElementTree(root).write(output_path, encoding="utf-8", xml_declaration=True)
    ET.ElementTree(scarti_root).write(scarti_path, encoding="utf-8", xml_declaration=True)

    print(f"→ Salvato {output_path} e {scarti_path}")

# === SALVA SUMMARY ===
ET.ElementTree(summary_root).write(SUMMARY_FILE, encoding="utf-8", xml_declaration=True)
print(f"Creato summary in {SUMMARY_FILE}")