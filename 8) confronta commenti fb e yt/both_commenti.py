import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import numpy as np

def main():
    folder = os.path.dirname(os.path.abspath(__file__))

    # Carica file medie Facebook e YouTube
    fb_tree = ET.parse(os.path.join(folder, "medie_facebook.xml"))
    fb_root = fb_tree.getroot()
    fb_dict = {a.attrib['name']: int(a.attrib['media']) for a in fb_root.findall("Artista")}

    yt_tree = ET.parse(os.path.join(folder, "medie_youtube.xml"))
    yt_root = yt_tree.getroot()
    yt_dict = {a.attrib['name']: int(a.attrib['media']) for a in yt_root.findall("Artista")}

    # Carica file nomi
    names_tree = ET.parse(os.path.join(folder, "nomi.xml"))
    names_root = names_tree.getroot()

    # Liste finali
    nomi_comuni = []
    valori_facebook = []
    valori_youtube = []

    for elem in names_root.findall("name"):
        fb_name = "_" + elem.attrib.get("facebook")   # aggiunge underscore
        yt_name = "_" + elem.attrib.get("youtube")   # aggiunge underscore

        if fb_name in fb_dict and yt_name in yt_dict:
            nomi_comuni.append(elem.text)           # nome leggibile
            valori_facebook.append(fb_dict[fb_name])
            valori_youtube.append(yt_dict[yt_name])

    print("Nomi comuni:", nomi_comuni)
    print("Valori Facebook:", valori_facebook)
    print("Valori YouTube:", valori_youtube)
    print(f"Totale artisti comuni: {len(nomi_comuni)}")

    # Grafico 1
    x = np.arange(len(nomi_comuni))
    width = 0.35

    plt.figure(figsize=(14, 6))
    plt.bar(x - width/2, valori_facebook, width, label='Facebook', color='skyblue')
    plt.bar(x + width/2, valori_youtube, width, label='YouTube', color='salmon')
    plt.xticks(x, nomi_comuni, rotation=45, ha='right', fontsize=8)
    plt.xlabel('Artista')
    plt.ylabel('Numero di commenti')
    plt.title('Commenti Facebook vs YouTube')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

    # Grafico 2 - medie
    mean_fb = np.mean(valori_facebook)
    mean_yt = np.mean(valori_youtube)

    plt.figure(figsize=(3, 4))
    plt.bar(['Facebook', 'YouTube'], [mean_fb, mean_yt], color=['skyblue', 'salmon'], width=0.5)
    plt.ylabel('Numero di commenti')
    plt.title('Numero di commenti medio')
    plt.ylim(0, 1500)
    plt.xlim(-0.5, 1.5)
    plt.tight_layout()
    plt.show()

    print("Media Facebook:", mean_fb)
    print("Media YouTube:", mean_yt)

if __name__ == "__main__":
    main()
