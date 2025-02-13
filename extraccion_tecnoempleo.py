import requests
from bs4 import BeautifulSoup
from datetime import datetime
#Extracción primera página
url = "https://www.tecnoempleo.com/ofertas-trabajo/?pagina=1"  

response = requests.get(url)
if response.status_code != 200:
    print("Error al acceder a la página principal")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

enlaces = soup.find_all("a", class_="font-weight-bold text-cyan-700")
urls = [enlace.get("href") for enlace in enlaces if enlace.get("href")]

for link in urls:

    response_link = requests.get(link)
    if response_link.status_code != 200:
        print(f"Error al acceder a {link}")
        continue

    soup_link = BeautifulSoup(response_link.text, "html.parser")

    titulo = soup_link.find("h1").get_text(strip=True) if soup_link.find("h1") else "Sin título"
    fecha = soup_link.find("span", class_= "ml-4").get_text(strip=True) if soup_link.find("span", class_= "ml-4").get_text else "Sin fecha"    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: año-mes-día hora:minuto:segund
    # Tecnologías:
    div = soup_link.find("div", class_="pl--12 pr--12")
    tecnologias = [a["title"] for a in div.find_all("a") if div and a.has_attr("title")]
    
    #Todos los datos principales
    todos_textos_enunciados = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="d-inline-block px-2")]
    todos_textos = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="float-end")]

    #Otros detalles de la oferta
    todos_detalles = soup_link.find_all("p", class_="m-0")[1:]
    todos_textos_detalles = [p.get_text(strip=True) for p in soup_link.find_all("p", class_="m-0")] 

    
    print(f"Título: {titulo}")
    print(todos_textos_enunciados)
    print (todos_textos)
    print (tecnologias)
    print(fecha)

    print("-" * 40)


# Extracción primeras 3 páginas
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def extraer_ofertas_tecnoempleo(num_paginas=None):
    base_url = "https://www.tecnoempleo.com/ofertas-trabajo/?pagina={}"
    todas_las_ofertas = []
    pagina = 1

    # Set tecnologías únicas
    todas_las_tecnologias = set()

    while True:
        url = base_url.format(pagina)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error al acceder a la página {pagina}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        enlaces = soup.find_all("a", class_="font-weight-bold text-cyan-700")
        urls = [enlace.get("href") for enlace in enlaces if enlace.get("href")]

        if not urls:
            print(f"No se encontraron más ofertas en la página {pagina}. Finalizando.")
            break

        for link in urls:
            response_link = requests.get(link)
            if response_link.status_code != 200:
                print(f"Error al acceder a {link}")
                continue

            soup_link = BeautifulSoup(response_link.text, "html.parser")
            # Título, fecha de publicación y timestamp
            titulo = soup_link.find("h1").get_text(strip=True) if soup_link.find("h1") else "Sin título"
            fecha = soup_link.find("span", class_="ml-4").get_text(strip=True) if soup_link.find("span", class_="ml-4") else "Sin fecha"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato: año-mes-día hora:minuto:segundo
            # Datos principales
            todos_textos_enunciados = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="d-inline-block px-2")]
            todos_textos = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="float-end")]
            diccionario_principales = dict(zip(todos_textos_enunciados, todos_textos))

            # Otros detalles
            todos_textos_detalles = [p.get_text(strip=True) for p in soup_link.find_all("p", class_="m-0")[1:]]
            diccionario_detalles = {}

            for item in todos_textos_detalles:
                if ":" in item:
                    clave, valor = item.split(":", 1)
                    diccionario_detalles[clave.strip()] = valor.strip()
                else:
                    diccionario_detalles[item.strip()] = None

            # Tecnologías
            div = soup_link.find("div", class_="pl--12 pr--12")
            tecnologias = [a["title"].replace("Ofertas de Empleo de ", "") for a in div.find_all("a") if div and a.has_attr("title")]

            # Actualizar el set de todas las tecnologías
            todas_las_tecnologias.update(tecnologias)

            # Diccionario total ofertas
            oferta = {
                "Título": titulo,
                "URL": link,
                "Tecnologías": tecnologias,
                "Time Stamp": timestamp,
                "Fecha publicacion": fecha,
            }

            for clave, valor in diccionario_principales.items():
                oferta[clave] = valor if valor else "No especificado"

            for clave, valor in diccionario_detalles.items():
                oferta[clave] = valor if valor else "No especificado"

            todas_las_ofertas.append(oferta)

        # Para cuando especifiquemos número de páginas
        if num_paginas and pagina >= num_paginas:
            break

        pagina += 1

    # DataFrames ofertas
    df_ofertas = pd.DataFrame(todas_las_ofertas)

    # Crear columnas binarias para cada tecnología
    for tecnologia in todas_las_tecnologias:
        df_ofertas[tecnologia] = df_ofertas["Tecnologías"].apply(lambda x: 1 if tecnologia in x else 0)
    df_ofertas.drop(columns=["Tecnologías"], inplace=True)

    # CSV
    df_ofertas.to_csv("ofertas_tecnoempleo.csv", index=False, encoding="utf-8-sig")
    return df_ofertas

# Llamar a función
df_ofertas = extraer_ofertas_tecnoempleo(3)
df_ofertas