import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import numpy as np

# Directory dei file
base_dir = os.path.dirname(os.path.abspath(__file__))

# Percorsi completi
file_fb = os.path.join(base_dir, "sentiment_totali_facebook.xml")
file_yt = os.path.join(base_dir, "sentiment_totali_youtube.xml")
file_names = os.path.join(base_dir, "nomi.xml")

def load_sentiments(path):
    root = ET.parse(path).getroot()
    sentiments = {}
    for artista in root.findall("Artista"):
        nome = artista.attrib.get("nome")
        val = artista.attrib.get("sentiment")
        try:
            sentiments[nome.lower()] = float(val)
        except (TypeError, ValueError):
            continue
    return sentiments

# Carica dizionari sentiment
sentiments_fb = load_sentiments(file_fb)
sentiments_yt = load_sentiments(file_yt)

# Liste finali
artisti = []
facebook = []
youtube = []

# Cicla sui 100 artisti in nomi.xml
root_names = ET.parse(file_names).getroot()
for name_tag in root_names.findall("name"):
    nome_leggibile = name_tag.text.strip()
    nome_fb = name_tag.attrib.get("facebook", "").strip()
    nome_yt = name_tag.attrib.get("youtube", "").strip()

    if not nome_fb or not nome_yt:
        continue

    key_fb = ("_" + nome_fb).lower()
    key_yt = ("_" + nome_yt).lower()

    if key_fb in sentiments_fb and key_yt in sentiments_yt:
        artisti.append(nome_leggibile)
        facebook.append(sentiments_fb[key_fb])
        youtube.append(sentiments_yt[key_yt])

# --- Grafico 1: barre per artista ---
x = np.arange(len(artisti))
width = 0.35

plt.figure(figsize=(14, 6))
plt.bar(x - width/2, facebook, width, label='Facebook', color='skyblue')
plt.bar(x + width/2, youtube, width, label='YouTube', color='salmon')
plt.xticks(x, artisti, rotation=45, ha='right', fontsize=8)
plt.xlabel('Artista')
plt.ylabel('Sentiment')
plt.title('Sentiment Facebook vs YouTube')
plt.legend()
plt.tight_layout()
plt.show()

# --- Grafico 2: barre medie ---
mean_fb = np.mean(facebook)
mean_yt = np.mean(youtube)

plt.figure(figsize=(3, 4))
plt.bar(['Facebook', 'YouTube'], [mean_fb, mean_yt], color=['skyblue', 'salmon'], width=0.5)
plt.ylabel('Sentiment')
plt.title('Sentiment medio')
plt.ylim(0, 0.5)
plt.xlim(-0.5, 1.5)
plt.tight_layout()
plt.show()

# Stampa valori
print("Artisti trovati:", len(artisti))
print("Media Facebook:", mean_fb)
print("Media YouTube:", mean_yt)
