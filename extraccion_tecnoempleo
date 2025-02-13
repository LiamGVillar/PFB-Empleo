import requests
from bs4 import BeautifulSoup
from datetime import datetime

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


    