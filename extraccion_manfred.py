import requests 
import bs4

from pprint import pprint
from bs4 import BeautifulSoup
import selenium # Para ver la versión
from selenium import webdriver # es la clase que permite inicializar el navegador e interaccionar con el mismo
from selenium.webdriver.common.by import By # es la clase que permite filtrar elementos del dom

import time
from time import sleep

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

###################################################################################

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Necesitamos identificar el tipo de sistema operativo
import platform
system = platform.system()

# En función del sistema operativo, instanciamos el objeto de webdriver
if system == "Darwin":
    # Mac
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
else:
    #Linux y Windows
    browser = webdriver.Chrome('')

# Ahora ya podemos cargar la página correspondiente y maximizar la ventana
browser.get("https://www.getmanfred.com/ofertas-empleo?onlyActive=true&currency=%E2%82%AC")
browser.maximize_window()


cookies = browser.find_element(By.ID, "CybotCookiebotDialogBodyButtonAccept")  #Aceptamos las cookies
cookies.click()

all_offers = browser.find_element(By.ID, "activeOffers")  #Activar todas ofertas
all_offers.click()
time.sleep(10)

#oferta01-test
oferta = browser.find_element(By.CLASS_NAME, "sc-e56330b0-6")  #Entramos a una oferta
oferta.click()

url_actual = browser.current_url
url_oferta = {"Url oferta": url_actual}
print (url_oferta)

img_element = browser.find_element(By.CSS_SELECTOR, 'img.sc-2f3afe7a-3')
alt_text = img_element.get_attribute('alt')
empresa_nombre = {"Nombre empresa": alt_text}
print(empresa_nombre)

oferta_titulo = browser.find_element(By.CLASS_NAME, "sc-f61a956f-0").text
oferta_titulo_ult = {"Oferta titulo": oferta_titulo}
print(oferta_titulo_ult)

oferta_info_texto = browser.find_elements(By.CLASS_NAME, "sc-6d3685c2-5")
textos = [elem.text for elem in oferta_info_texto]
oferta_lugar = browser.find_elements(By.CLASS_NAME, "sc-6d3685c2-2")
dato = [elem.text for elem in oferta_lugar]
diccionario_oferta01 = dict(zip(textos, dato))
print(diccionario_oferta01)

oferta_info_texto02 = browser.find_elements(By.CLASS_NAME, "sc-c51cd5df-3")
textos02 = [elem.text for elem in oferta_info_texto02]
oferta_lugar02 = browser.find_elements(By.CLASS_NAME, "sc-c51cd5df-4")
dato02 = [elem.text for elem in oferta_lugar02]
diccionario_oferta02 = dict(zip(textos02, dato02))
print(diccionario_oferta02)

tecnologia_inne = browser.find_elements(By.CLASS_NAME, "sc-e4487fe1-2")
tecnologias_info_inne = [elem.text for elem in tecnologia_inne]
nivel_inne = browser.find_elements(By.CLASS_NAME, "sc-e4487fe1-5")
nivel_tecnologia_inne = [elem.text for elem in nivel_inne]
diccionario_tecnologias_inne = dict(zip(tecnologias_info_inne, nivel_tecnologia_inne))
diccionario_tecnologias_ult = {"Tecnologías": diccionario_tecnologias_inne}
print(diccionario_tecnologias_ult)

otras_habilidades = browser.find_elements(By.CLASS_NAME, "sc-22385303-2")
otras_habilidades_info = [elem.text for elem in otras_habilidades]
otras_habilidades_ult = {"Otras habilidades": otras_habilidades_info}
print(otras_habilidades_ult)
