import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Hacemos una función para extraer todos los URLS y aprovechamos para extraer de estos enlaces los nombres de las empresas:
def extraer_urls(num_paginas=None):
    base_url = "https://www.tecnoempleo.com/ofertas-trabajo/?pagina={}"
    todos_urls = []
    nombres_empresas = []  
    pagina = 1

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

        # Extraemos los nombres de las empresas
        nombre_empresas = soup.find_all("a", class_="text-primary link-muted")
        for empresa in nombre_empresas:
            nombres_empresas.append(empresa.text.strip())

        todos_urls.extend(urls)
        print(f"Página {pagina}: {len(urls)} URLs añadidos.") # Hacemos print para asegurarnos de que está funcionando correctamente.

        # Calculamos el número total de páginas para asegurarnos de que las recorra todas:
        if num_paginas is None:
            total_ofertas = int(soup.find("h1").text.split()[0].replace(".", ""))
            total_paginas = (total_ofertas // 30) + (1 if total_ofertas % 30 != 0 else 0)
            if pagina >= total_paginas:
                break
        elif pagina >= num_paginas:
            break

        pagina += 1

    return todos_urls, nombres_empresas

# Hacemos una función que recorre los urls para extraer los datos:
def extraer_datos_de_urls(urls, nombres_empresas):
    todas_las_ofertas = []
    todas_las_tecnologias = set()

    # Creamos un bucle que recorra las urls:
    for idx, link in enumerate(urls):
        response_link = requests.get(link)
        if response_link.status_code != 200:
            print(f"Error al acceder a {link}")
            continue

        soup_link = BeautifulSoup(response_link.text, "html.parser")

        # Sacamos título, fecha, habilidades y añadimos el timestamp para que se indique la fecha en la que se han solicitado los datos. 
        titulo = soup_link.find("h1").get_text(strip=True) if soup_link.find("h1") else "Sin título"
        fecha = soup_link.find("span", class_="ml-4").get_text(strip=True) if soup_link.find("span", class_="ml-4") else "Sin fecha"
        habilidades = [x.text.strip() for x in soup_link.find_all("div", class_="d-flex py-2")[1].find_all("a")]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Tecnologías. En el caso de tecnologías, limpiamos ya la información que sacamos para que nos muestre solola tecnología sin el texto que no es necesario: "Ofertas de Empleo de":
        div = soup_link.find("div", class_="pl--12 pr--12")
        tecnologias = [a["title"].replace("Ofertas de Empleo de ", "") for a in div.find_all("a") if div and a.has_attr("title")]
        todas_las_tecnologias.update(tecnologias)

        # Extraemos todos los datos principales
        todos_textos_enunciados = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="d-inline-block px-2")]
        todos_textos = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="float-end")]
        diccionario_principales = dict(zip(todos_textos_enunciados, todos_textos))

        # Extraemos otros detalles de la oferta
        todos_detalles = soup_link.find_all("p", class_="m-0")
        todos_textos_detalles = [x.text.strip() for x in todos_detalles if len(x["class"]) == 1][1:]
        diccionario_detalles = {}
        for item in todos_textos_detalles:
            if ":" in item:
                clave, valor = item.split(":", 1)
                diccionario_detalles[clave.strip()] = valor.strip()
            else:
                diccionario_detalles[item.strip()] = None

        # Creamos el diccionario para añadir toda la información
        oferta = {
            "Título": titulo,
            "URL": link,
            "Tecnologías": tecnologias,
            "Time Stamp": timestamp,
            "Fecha publicacion": fecha,
            "Habilidades": habilidades,
            "Nombre de empresa": nombres_empresas[idx] if idx < len(nombres_empresas) else "No encontrado",  # Nos aseguramos de que los nombres de empresas se corresponden con los urls sacados
        }

        # Creamos un bucle para asegurarnos de que añadimos todos los datos y, en el caso de que no haya datos, que se añadan también. 
        for clave, valor in diccionario_principales.items():
            oferta[clave] = valor if valor else "No especificado"

        for clave, valor in diccionario_detalles.items():
            oferta[clave] = valor if valor else "No especificado"

        todas_las_ofertas.append(oferta)
        print(f"Procesada oferta: {titulo}")

    # Creamos el DF
    df_ofertas = pd.DataFrame(todas_las_ofertas)

    # Creamos columnas binarias para cada tecnología. Esto nos facilita hacer un DF para más adelante relacionarlo con el DF principal. 
    for tecnologia in todas_las_tecnologias:
        df_ofertas[tecnologia] = df_ofertas["Tecnologías"].apply(lambda x: 1 if tecnologia in x else 0)
    df_ofertas.drop(columns=["Tecnologías"], inplace=True)

    # Guardamos el CSV
    df_ofertas.to_csv("ofertas_tecnoempleo.csv", index=False, encoding="utf-8-sig") # Usamos el encoding para evitar cualquier error de compatibilidad al abrir el archivo con otros programas. 
    return df_ofertas

# Llamamos a las funciones
urls, nombres_empresas = extraer_urls()
df_ofertas = extraer_datos_de_urls(urls, nombres_empresas)
print(df_ofertas)