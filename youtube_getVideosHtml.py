from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
import os
import xml.etree.ElementTree as ET

path = os.path.dirname(os.path.abspath(__file__))
htmlPath = path + "\\youtube\\channel\\html\\"

if not os.path.exists(htmlPath):
    os.makedirs(htmlPath)

max_threads = 4
semaphore = threading.Semaphore(max_threads)

def funzione(nome):

    file_html = htmlPath + nome + ".html"

    if os.path.exists(file_html):
        return

    options = webdriver.FirefoxOptions()
    options.set_preference("media.volume_scale", "0.0")
    driver = webdriver.Firefox(options=options)

    driver.implicitly_wait(100)

    driver.get("https://www.youtube.com/@" + nome + "/")

    cookie_div = driver.find_element(By.XPATH, '//button/span[text()="Rifiuta tutto"]')

    cookie_div.click()

    account_div = driver.find_element(By.XPATH, '//yt-tab-shape/div[text()="Video"]')

    account_div.click()

    for i in range(500):
        scroll_script = "window.scrollTo(" + str(i*100) + ", +" + str((i+1)*100) + ");"
        driver.execute_script(scroll_script)
        time.sleep(0.1)

    time.sleep(10)

    html_content = driver.page_source

    with open(file_html, "w", encoding="utf-8") as file:
        file.write(html_content)

    driver.quit()

def worker(name):
    with semaphore:
        funzione(name)

file_nomi = path + '\\nomi.txt'
albero_nomi = ET.parse(file_nomi)
radice_nomi = albero_nomi.getroot()

threads = []

for name_element in radice_nomi.findall('name'):
    name = name_element.get('youtube')
    if name != "":
        thread = threading.Thread(target=worker, args=(name,))
        thread.start()
        threads.append(thread)

for thread in threads:
    thread.join()