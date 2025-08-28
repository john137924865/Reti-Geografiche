from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import threading
import os
import xml.etree.ElementTree as ET
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.keys import Keys

path = os.path.dirname(os.path.abspath(__file__))
channelLinkPath = path + "\\youtube\\channel\\link\\"
videoHtmlPath = path + "\\youtube\\video\\html\\"

if not os.path.exists(videoHtmlPath):
    os.makedirs(videoHtmlPath)

def scroll_function(driver, k_var):
    k_var[0] = 0
    while k_var[0] < 100:
        for i in range(100):
            scroll_script = "window.scrollTo(" + str((k_var[0]*100+i)*100) + ", +" + str(((k_var[0]*100+i)+1)*100) + ");"
            driver.execute_script(scroll_script)
        k_var[0] = k_var[0] + 1
        print(f'\r{("-" * k_var[0]) + str(k_var[0]) + "%"}', end='')

def funzione(name, link, n):

    dict = {}
    
    num_videos = 32
    
    if name in dict:
        num_videos = dict.get(name) + 100

    if n > num_videos:
        return
    
    name_path = videoHtmlPath + name
    file_html = name_path + "\\" + str(n) + ".html"

    print(file_html)

    if not os.path.exists(name_path):
        os.makedirs(name_path)

    if os.path.exists(file_html):
        return

    options = webdriver.FirefoxOptions()
    options.set_preference("media.volume_scale", "0.0")
    driver = webdriver.Firefox(options=options)
        
    driver.implicitly_wait(100)

    #driver.set_window_size(3840, 2160)

    driver.get("https://www.youtube.com/")
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[@aria-label="Rifiuta l\'utilizzo dei cookie e di altri dati per le finalità descritte"]').click()
    time.sleep(1)

    driver.get(link)

    time.sleep(5)
    scroll_script = "window.scrollTo(" + str((20)*20) + ", +" + str(((20)+1)*20) + ");"
    driver.execute_script(scroll_script)
    time.sleep(5)
    try:
        ordina_per = driver.find_element(By.XPATH, '//tp-yt-paper-menu-button/div/tp-yt-paper-button/div[text()="Ordina per"]')
    except NoSuchElementException:
        driver.quit()
        print("NoSuchElementException " + name + " " + str(n))
        return
    ordina_per.click()
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, '//a/tp-yt-paper-item/tp-yt-paper-item-body/div/div[starts-with(text(), "Dal più recente")]').click()
    except ElementClickInterceptedException:
        driver.quit()
        print("ElementClickInterceptedException " + name + " " + str(n))
        return
    except ElementNotInteractableException:
        driver.quit()
        print("ElementNotInteractableException " + name + " " + str(n))
        return
    time.sleep(5)

    start = time.time()
    curr = time.time()
    k_var = [0]
    scroll_thread = threading.Thread(target=scroll_function, args=(driver, k_var,))
    scroll_thread.start()

    while (True):
        curr = time.time()
        if (curr - start >= 1000):
            print("\nTimeout: " + name + " " + str(n))
            break
        if (k_var[0] >= 100):
            print("\nK 100: " + name + " " + str(n))
            break

    html_content = driver.page_source

    with open(file_html, "w", encoding="utf-8") as file:
        file.write(html_content)

    time.sleep(2)

    driver.quit()



names = []

for filename in os.listdir(channelLinkPath):
    names.append(filename[:-4])

#https://addons.mozilla.org/firefox/downloads/file/4328681/ublock_origin-1.59.0.xpi


for name in names:
    link_file = channelLinkPath + name + ".txt"
    with open(link_file, 'r') as file:
        n = 0
        for link in file:
            link = link[:-1]
            n = n + 1
            funzione(name, link, n)