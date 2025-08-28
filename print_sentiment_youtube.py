import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import os
import numpy

# Leggi il file XML dalla stessa directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTIMENT_FILE = os.path.join(BASE_DIR, "sentiment_totali.xml")
NOMI_FILE = os.path.join(BASE_DIR, "nomi.xml")

# --- Leggi sentiment_totali.xml ---
tree_sent = ET.parse(SENTIMENT_FILE)
root_sent = tree_sent.getroot()

# Estrarre nomi e sentiment degli artisti
artists = []
sentiments = []

for artista in root_sent.findall('Artista'):
    nome = artista.get('nome')
    sentiment_str = artista.get('sentiment')
    # Ignora valori non convertibili
    try:
        sentiment = float(sentiment_str)
        artists.append(nome[1:])
        sentiments.append(sentiment)
    except (ValueError, TypeError):
        print(f"Valore sentiment non valido per {nome}: {sentiment_str}")

# --- Leggi nomi.xml e ordina secondo youtube ---
tree_nomi = ET.parse(NOMI_FILE)
root_nomi = tree_nomi.getroot()

artists_ord = []
sentiments_ord = []

for name in root_nomi.findall('name'):
    yt_id = name.get('youtube')
    artists_ord = list(range(1, 101))    
    if yt_id in artists:
        idx = artists.index(yt_id)
        # artists_ord.append(name.text)
        sentiments_ord.append(sentiments[idx])
    else:
        sentiments_ord.append(numpy.nan)


# Creare il grafico
plt.figure(figsize=(12, 5))
bars = plt.bar(artists_ord, [0 if numpy.isnan(v) else v for v in sentiments_ord], color='skyblue')

# Aggiungere "NaN" sopra le barre mancanti
for xi, yi in zip(artists_ord, sentiments_ord):
    if numpy.isnan(yi):
        plt.text(xi, 0.01, 'N\na\nN', ha='center', va='bottom', color='red', fontsize=8, linespacing=0.9)

# Tick sull'asse X ogni 10
tick_positions = list(range(1, 101, 10))
plt.xticks(tick_positions, rotation=45, ha='center', fontsize=8)

plt.xlabel('Artista')
plt.ylabel('Sentiment')
plt.title('Sentiment medio per artista')
plt.tight_layout()
plt.show()