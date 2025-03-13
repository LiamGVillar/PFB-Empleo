from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar sin interfaz gráfica

# Iniciar el navegador
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.getmanfred.com/ofertas-empleo?onlyActive=false&currency=%E2%82%AC"
browser.get(url)

browser.implicitly_wait(10)

# Obtener URLs de ofertas
ofertas = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/ofertas-empleo/"]')
urls_ofertas = ["" + oferta.get_attribute("href") for oferta in ofertas]

max_ofertas = 3
todas_ofertas_info = []

# Bucle para recorrer ofertas
for i in range(min(max_ofertas, len(urls_ofertas))):
    try:
        browser.get(urls_ofertas[i])
        time.sleep(1)  

        url_actual = browser.current_url

        # Obtener fecha de estraccion
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: año-mes-día hora:minuto:segundo
        except:
            timestamp = "No disponible"

        # Obtener titulo de la oferta
        try:
            oferta_titulo = browser.find_element(By.CLASS_NAME, "sc-f61a956f-0").text
        except:
            oferta_titulo = "No disponible"

        # Extraer detalles 
        try:
            oferta_info_texto = browser.find_elements(By.CLASS_NAME, "sc-6d3685c2-5")
            textos = [elem.text for elem in oferta_info_texto]

            oferta_lugar = browser.find_elements(By.CLASS_NAME, "sc-6d3685c2-2")
            datos = [elem.text for elem in oferta_lugar]

            diccionario_oferta01 = dict(zip(textos, datos))
        except:
            diccionario_oferta01 = {}

        # Extraer otros detalles
        try:
            oferta_info_texto02 = browser.find_elements(By.CLASS_NAME, "sc-c51cd5df-3")
            textos02 = [elem.text for elem in oferta_info_texto02]

            oferta_lugar02 = browser.find_elements(By.CLASS_NAME, "sc-c51cd5df-4")
            datos02 = [elem.text for elem in oferta_lugar02]

            diccionario_oferta02 = dict(zip(textos02, datos02))
        except:
            diccionario_oferta02 = {}

        # Extraer las tecnologías que se piden
        try:
            tecnologias = browser.find_elements(By.CLASS_NAME, "sc-e4487fe1-2")
            tecnologias_info = [elem.text for elem in tecnologias]

            niveles = browser.find_elements(By.CLASS_NAME, "sc-e4487fe1-5")
            niveles_tecnologia = [elem.text for elem in niveles]

            diccionario_tecnologias = dict(zip(tecnologias_info, niveles_tecnologia))
        except:
            diccionario_tecnologias = {}

        # Otras habilidades requeridas
        try:
            otras_habilidades = browser.find_elements(By.CLASS_NAME, "sc-22385303-2")
            otras_habilidades_info = [elem.text for elem in otras_habilidades]
        except:
            otras_habilidades_info = []

        # Esta operativa la oferta o no
        try:
            oferta_activa = browser.find_element(By.CLASS_NAME, "sc-81fb91b0-11").text
        except:
            oferta_activa = "Activa"

        # Diccionario con toda la información de la oferta
        oferta_info = {
            "url": url_actual,
            "fecha_extraccion": timestamp,
            "titulo": oferta_titulo,
            "detalles_1": diccionario_oferta01,
            "detalles_2": diccionario_oferta02,
            "oferta_activada" : oferta_activa,
            "tecnologias": {"Tecnologías": diccionario_tecnologias},
            "habilidades": {"Otras habilidades": otras_habilidades_info}
        }

        # Guardamos la oferta en la lista
        todas_ofertas_info.append(oferta_info)
        print(f"Oferta {i+1} guardada correctamente.")

    except Exception as e:
        print(f"Error con la oferta {i+1}: {e}")


browser.quit()

print(todas_ofertas_info)