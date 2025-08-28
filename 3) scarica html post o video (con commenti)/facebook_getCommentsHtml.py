from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException

path = os.path.dirname(os.path.abspath(__file__))

primo_link = True

def openLink(name, myDriver):

    cartella_artista = path + "\\facebook\\commenti\\html\\" + name

    if not os.path.exists(cartella_artista):
        os.makedirs(cartella_artista)

    file_post_link = path + "\\20 posts\\" + name + ".txt"

    with open(file_post_link, 'r') as file:
        n = 0
        global primo_link
        for link in file:
            link = link[:-1]
            n = n + 1
            file_html = cartella_artista + "\\" + str(n) + ".html"
            #file_senza_altro_html = cartella_artista + "\\" + str(n) + "_senza_altro.html"
            if not os.path.exists(file_html): #and os.path.exists(file_senza_altro_html):
                try:
                    funzione(myDriver, link, file_html)
                    saveHtml(myDriver, file_html)
                except (StaleElementReferenceException, ElementNotInteractableException, ElementClickInterceptedException):
                    _ = 0
                primo_link = False

def funzione(myDriver, link, file_html):

    myDriver.implicitly_wait(100)

    myDriver.get(link)

    time.sleep(10)

    if primo_link:
        cookie_div = myDriver.find_element(By.XPATH, '//div/div/div/div/span/span[text()="Rifiuta cookie facoltativi"]')
        cookie_div.click()
        time.sleep(1)

        #lorenzoficchioni@outlook.it giuseppecazzilli@outlook.it rosariopuzzillo@outlook.it mariellospazi@outlook.it luigigronda@outlook.it

        email_input = myDriver.find_elements(By.XPATH, '//input[@name="email"]')[1]
        email_input.send_keys("bavevaj708@wikfee.com")
        time.sleep(1)


        password_input = myDriver.find_elements(By.XPATH, '//input[@name="pass"]')[1]
        password_input.send_keys("ydu$YQi!\"$2N*w:")
        time.sleep(1)

        accedi_span = myDriver.find_elements(By.XPATH, '//span[text()="Accedi"]')[2]
        accedi_div = accedi_span.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
        accedi_div.click()
        time.sleep(10)

        try:
            myDriver.implicitly_wait(5)
            myDriver.find_element(By.XPATH, '//div/div/div/div/span/span[text()="Rifiuta cookie facoltativi"]')
            return
        except NoSuchElementException:
            _ = 0
        finally:
            myDriver.implicitly_wait(100)
        
    time.sleep(2)

    #account_div = myDriver.find_element(By.XPATH, '//div[@aria-label="Chiudi"]')

    #account_div.click()

    #accedi_o_registrati_div = myDriver.find_element(By.XPATH, '//span[text() = "Accedi o iscriviti a Facebook per connetterti con amici, familiari e persone che conosci."]')
    #accedi_o_registrati_div = accedi_o_registrati_div.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, "..")
    #myDriver.execute_script("arguments[0].remove();", accedi_o_registrati_div)

    if "/photos/" in link:
        parent = (myDriver.find_element(By.XPATH, "//span[contains(text(),'Visualizza altri commenti')]")).find_element(By.XPATH, "../../../../../..")
        size = len(parent.find_elements(By.XPATH, "*"))
        element = parent.find_elements(By.XPATH, "*")[size-1]
        myDriver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)

    k = 0
    counter = 0
    myDriver.implicitly_wait(10)
    start = time.time()
    end = time.time()
    while ((end - start) < 90) and (counter < 1000) and not (((end - start) > 50) and (counter <= 500)) and not (((end - start) > 40) and (counter <= 400)) and not (((end - start) > 30) and (counter <= 300)):
        print("tempo: " + str(end - start) + " counter: " + str(counter))
        end = time.time()
        try:
            for i in range(100):
                scroll_script = "window.scrollTo(" + str((k*100+i)*100) + ", +" + str(((k*100+i)+1)*100) + ");"
                myDriver.execute_script(scroll_script)
            visualizza_altri_commenti = (myDriver.find_element(By.XPATH, "//span[contains(text(),'Visualizza altri commenti')]")).find_element(By.XPATH, "..").find_element(By.XPATH, "..")
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(visualizza_altri_commenti)
            )
            visualizza_altri_commenti.click()
            conteggio = visualizza_altri_commenti.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(By.XPATH, 'following-sibling::*').find_element(By.XPATH, './*')
            counter = int(conteggio.text.split()[0])
            k = k + 1
        except NoSuchElementException:
            _ = 0

    #html_content = myDriver.page_source

    #with open(file_senza_altro_html, "w", encoding="utf-8") as file:
    #    file.write(html_content)

    altro_divs = myDriver.find_elements(By.XPATH, '//div[text() = "Altro..." and @role="button"]')
    for div in altro_divs:
        print(div.find_element(By.XPATH, ".."))
        div.click()

    myDriver.implicitly_wait(100)

def saveHtml(myDriver, file_html):
    html_content = myDriver.page_source
    with open(file_html, "w", encoding="utf-8") as file:
        file.write(html_content)



names = []
for filename in os.listdir(path + "\\20 posts\\"):
    names.append(filename[:-4])

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

for n in names:
    openLink(n, driver)

driver.quit()