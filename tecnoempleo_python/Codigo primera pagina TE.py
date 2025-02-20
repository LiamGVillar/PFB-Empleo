# Después accedemos a la información dentro de los enlaces de cada página:

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
    if response_link.status_code != 200: #En caso de que la solicitud no se procese correctamente, pedimos que nos lo comunique y que continue. 
        print(f"Error al acceder a {link}")
        continue

    soup_link = BeautifulSoup(response_link.text, "html.parser")
    # Sacamos título, fecha, habilidades, nombre de la empresa y añadimos el timestamp para que se indique la fecha en la que se han solicitado los datos. 
    titulo = soup_link.find("h1").get_text(strip=True) if soup_link.find("h1") else "Sin título"
    fecha = soup_link.find("span", class_= "ml-4").get_text(strip=True) if soup_link.find("span", class_= "ml-4").get_text else "Sin fecha" 
    nombre_empresa = [x.text.strip() for x in soup_link.find("div", class_ = "col-12 col-md-12 col-lg-8").find("a")][1]
    nombre_empresas = soup.find_all("a", class_="text-primary link-muted")
    for empresa in nombre_empresas:
        print(f"Nombre de empresa", empresa.text.strip())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    
    # Tecnologías. En el caso de tecnologías, limpiamos ya la información que sacamos para que nos muestre solola tecnología sin el texto que no es necesario: "Ofertas de Empleo de":
    div = soup_link.find("div", class_="pl--12 pr--12")
    tecnologias = [a["title"].replace("Ofertas de Empleo de ", "") for a in div.find_all("a") if div and a.has_attr("title")] 
    
    #Todos los datos principales
    todos_textos_enunciados = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="d-inline-block px-2")]
    todos_textos = [span.get_text(strip=True) for span in soup_link.find_all("span", class_="float-end")]

    #Otros detalles de la oferta
    todos_detalles = soup_link.find_all("p", class_="m-0")
    todos_textos_detalles = [x.text.strip() for x in todos_detalles if len(x["class"]) == 1] 

    # Printeamos toda la información que hemos sacado:
    print(f"Título: {titulo}")
    print(f"Fecha: {fecha}")
    print(f"Habilidades: {habilidades}")
    print(f"Time Stamp: {timestamp}")
    print(f"Tecnologías: {tecnologias}")
    print(f"Todos los textos de los datos principales: {todos_textos}")
    print(f"Todos los textos de detales: {todos_textos_detalles}")
    print("-" * 40) # Printeamos varios caracteres para diferenciar mejor a nivel visual una oferta de otra. 