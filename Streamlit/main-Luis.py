import streamlit as st
from PIL import Image
import pandas as pd
#Grafica barras
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px 

import base64
from io import BytesIO


st.set_page_config(page_title = "Empleos Extraccion", page_icon= "https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", layout ="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #a9a9a9
;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def pagina_principal():
    st.title("Bienvenido a la página de búsqueda de empleos de Hackaboss")
    st.subheader("Explora ofertas de empleo IT en España")
    st.write("En este proyecto podrás ver un análisis sobre ofertas de empleo IT publicados recientemente")


def muestra_datos():
    st.title("Datos y graficas")
    st.write("Aquí podras observar patrones en las ofertas de empleo seleccionadas")

    with st.expander(label = "DataFrame - Ofertas", expanded = False):
         df = pd.read_csv(filepath_or_buffer = "/home/bosser/PFB-Empleo/CSV/CSV_finales/ofertas_final.csv")
         st.dataframe(df) 

     # Ruta al archivo HTML generado por folium
    ruta_html_provincias = "/home/bosser/PFB-Empleo/mapa_cloropletico_espana.html"
    ruta_html_calor = "/home/bosser/PFB-Empleo/mapa_calor_ciudades.html"
    ruta_html_comunidades = "/home/bosser/PFB-Empleo/mapa_comunidades.html"


    mapa_seleccionado = st.selectbox(
    "Mapas:",
    ("Ofertas de empleo por provincia", "Ofertas de empleo por ciudad", "Ofertas de empleo por comunidad autónoma")
)

#    Leer el contenido de los archivos HTML
    if mapa_seleccionado == "Ofertas de empleo por provincia":
        with open(ruta_html_provincias, "r", encoding="utf-8") as f:
            html_content = f.read()
    elif mapa_seleccionado == "Ofertas de empleo por ciudad":
        with open(ruta_html_calor, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:  # Mapa de comunidades
        with open(ruta_html_comunidades, "r", encoding="utf-8") as f:
            html_content = f.read()

    # Mostrar el mapa seleccionado
    st.components.v1.html(html_content, width=1200, height=600)

    ####################################################
    #Primera grafica


    # Conexión a la base de datos MySQL
    db_config = st.secrets["database"]
    db = mysql.connector.connect(
         host=db_config["host"],
         user=db_config["user"],
         password=db_config["password"],
         database=db_config["database"])

    # Consulta SQL
    query = """
    SELECT 
        o.titulo, 
        tr.tec_id AS tecnologia, 
        COUNT(*) AS frecuencia,
        t.tecnologia AS nombre_tecnologia
    FROM 
        ofertas o
    JOIN 
        tecnologias_relacion tr ON o.id_oferta = tr.id_oferta
    JOIN 
        tecnologias t ON tr.tec_id = t.tec_id
    GROUP BY 
        o.titulo, tr.tec_id, t.tecnologia
    ORDER BY 
        o.titulo, frecuencia DESC;
    """

    # Leer datos desde la base de datos
    df = pd.read_sql(query, con=db)

    # Filtrar los 10 puestos con más frecuencias de tecnologías
    top_titulos = df.groupby("titulo")["frecuencia"].sum().sort_values(ascending=False).head(10).index
    df_filtered = df[df["titulo"].isin(top_titulos)]

    # Limitar a las 5 tecnologías más frecuentes por puesto de trabajo
    df_filtered = df_filtered.groupby("titulo").apply(lambda x: x.nlargest(5, "frecuencia")).reset_index(drop=True)

    # Configuración de la página Streamlit
    st.title('Frecuencia de Tecnologías por Puesto de Trabajo')

    # Mostrar la tabla filtrada
    st.write("Tabla de tecnologías más solicitadas por puesto de trabajo:")
    st.dataframe(df_filtered)

    # Graficar los resultados
    st.write("Gráfico de Tecnologías más solicitadas por puesto de trabajo:")

    fig, ax = plt.subplots(figsize=(12, 6))
    for titulo in df_filtered["titulo"].unique():
        df_titulo = df_filtered[df_filtered["titulo"] == titulo]
        ax.bar(df_titulo["nombre_tecnologia"], df_titulo["frecuencia"], label=titulo)

    ax.set_ylabel("Frecuencia de tecnologías")
    ax.set_xlabel("Tecnología")
    ax.set_title("Frecuencia de tecnologías más solicitadas por puesto de trabajo")
    ax.tick_params(axis='x', rotation=90)
    ax.legend(title="Puestos de trabajo", bbox_to_anchor=(1.05, 1), loc="upper left")

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)


    ######################################### Mira  aver si cambias color negro (transparente o gris)


    db = mysql.connector.connect(
         host=db_config["host"],
         user=db_config["user"],
         password=db_config["password"],
         database=db_config["database"])

    # Consulta SQL
    consulta_sql = """
        SELECT 
            o.salario_desde, 
            o.salario_hasta, 
            c.ciudad,
            o.experiencia
        FROM 
            ofertas o
        JOIN 
            ciudades c ON o.id_oferta = c.id_oferta
        JOIN 
            ciudades_coordenadas cc ON c.ciudad = cc.ciudad
        WHERE 
            cc.pais = 'España';
    """

    # Ejecutamos la consulta y leemos los datos
    df_graficas = pd.read_sql(consulta_sql, db)

    # Calculamos la media de las dos columnas con información de salario:
    df_graficas["Salario medio"] = df_graficas[["salario_desde", "salario_hasta"]].mean(axis=1)

    # Detectamos outliers con el método de Tukey:
    Q1 = df_graficas["Salario medio"].quantile(0.25)
    Q3 = df_graficas["Salario medio"].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    df_graficas["Outlier Tukey"] = (df_graficas["Salario medio"] < limite_inferior) | (df_graficas["Salario medio"] > limite_superior)

    # Graficamos con fondo transparente
    plt.figure(figsize=(10, 6))

    # Separamos los salarios normales y los outliers
    salarios_normales = df_graficas[df_graficas["Outlier Tukey"] == False]["Salario medio"]
    salarios_outliers = df_graficas[df_graficas["Outlier Tukey"] == True]["Salario medio"]

    # Histograma de salarios normales y outliers
    plt.hist(salarios_normales, bins=50, alpha=0.7, label="Normales", color="green")
    plt.hist(salarios_outliers, bins=50, alpha=0.7, label="Outliers", color="yellow")

    # Línea de la media
    media_salario = np.mean(df_graficas["Salario medio"])
    plt.axvline(media_salario, color="red", linestyle="--", linewidth=2, label=f"Media: {media_salario:.2f} Bruto/año")

    # Etiquetas y título
    plt.xlabel("Salario", fontsize=14, color='black')
    plt.ylabel("Frecuencia", fontsize=14, color='black')
    plt.title("Distribución de Salarios y Outliers", fontsize=16, color='black')
    plt.legend()

    # Hacer el fondo transparente al guardar la figura
    plt.tight_layout()
    st.pyplot(plt, use_container_width=True)

###################################################

    # Creamos el gráfico de caja (box plot)
    fig = px.box(df_graficas,
                x="ciudad",
                y="Salario medio",
                title="Distribución de Salarios por Ciudad",
                labels={"ciudad": "Ciudad", "Salario medio": "Salario Medio"},
                color="ciudad",  # Se usa la columna 'ciudad' para colorear
                boxmode="group"
                )

    # Actualizamos el diseño del gráfico
    fig.update_layout(
        xaxis_title="Comunidad Autónoma",
        yaxis_title="Salario Medio",
        xaxis_tickangle=-45  # Rotamos las etiquetas de las comunidades o ciudades
    )

    # Mostrar el gráfico en Streamlit
    st.title("Análisis de Salarios por Ciudad")
    st.plotly_chart(fig)  # Muestra el gráfico interactivo de Plotly

#################################################

    fig = px.scatter(df_graficas, 
                    x="experiencia", 
                    y="Salario medio", 
                    color="experiencia",  
                    title="Relación entre Salario y Experiencia por Puesto de Trabajo",
                    labels={"experiencia": "Experiencia (años)", "Salario medio": "Salario Medio (€)"},
                    color_continuous_scale="Set1",  
                    template="plotly",  
                    )


    fig.update_layout(
        xaxis_title="Experiencia (años)",
        yaxis_title="Salario Medio (€)",
        title="Relación entre Salario y Experiencia por Puesto de Trabajo",
        legend_title="Puesto de Trabajo",  
    )


    st.title("Relación entre Salario y Experiencia por Puesto de Trabajo")
    st.plotly_chart(fig)

   
@st.cache_data
def load_data():
    return pd.read_csv("/home/bosser/PFB-Empleo/CSV/CSV_finales/ofertas_final.csv")

df = load_data()

def busqueda():
    st.title("Buscar y comparar empleos")
    st.write("Aqui puedes hacer una busqueda y comparativa de los empleos extraidos")

    df_filtrado = pd.DataFrame()

    # Formulario de búsqueda
    with st.form(key='search_form'):
        job_title = st.text_input("Título del trabajo", "").strip().lower()
        location = st.text_input("Ubicación", "").strip().lower()
        company = st.text_input("Empresa", "").strip().lower()
        submit_button = st.form_submit_button("Buscar")
    
       
    if submit_button:
    # Filtrar los resultados según la búsquedaaa
        df_filtrado = df[
            (df["titulo"].str.lower().str.contains(job_title, na=False)) &
            (df["ciudad"].str.lower().str.contains(location, na=False)) &
            (df["empresa"].str.lower().str.contains(company, na=False))
        ]

    # Mostrar resultados
        st.write(f"Resultados para: {job_title}, {location}, {company}")
    if not df_filtrado.empty:
        st.dataframe(df_filtrado)
    elif submit_button:
        st.write("No se encontraron resultados.")


# Inyectar CSS para cambiar el color del sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #b8b8b8 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Inicializar el estado de la página
if 'page' not in st.session_state:
    st.session_state.page = "🏠"

pages = {
    "🏠" : pagina_principal,
    "Muestra de datos" : muestra_datos,
    "Busqueda empleos" : busqueda
}


manfredimg = Image.open("/home/bosser/PFB-Empleo/Streamlit_test/imagenes/manfred.png")
tecnoempleoimg = Image.open("/home/bosser/PFB-Empleo/Streamlit_test/imagenes/tecnoempleo.png")

st.sidebar.image("https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", use_container_width=True)

# Función para convertir imagen a base64
def img_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# URLs para las imágenes
manfred_url = "https://www.getmanfred.com/ofertas-empleo?onlyActive=false&currency=%E2%82%AC"
tecnoempleo_url = "https://www.tecnoempleo.com/ofertas-trabajo/"

# Mostrar imágenes dentro de columnas con enlaces
col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown(f'<a href="{manfred_url}" target="_blank"><img src="data:image/png;base64,{img_to_base64(manfredimg)}" width="100%"></a>', unsafe_allow_html=True)

# Enlace y mostrar imagen para la columna 2 (Tecnoempleo)
with col2:
    st.markdown(f'<a href="{tecnoempleo_url}" target="_blank"><img src="data:image/png;base64,{img_to_base64(tecnoempleoimg)}" width="100%"></a>', unsafe_allow_html=True)


st.sidebar.markdown(
    "<h1 style='color: black;'>Navegación</h1>",
    unsafe_allow_html=True
)


if st.sidebar.button("🏠"):
    st.session_state.page = "🏠"

st.sidebar.markdown(
    """
    <style>
    /* Cambiar color del título "Selecciona una vista" */
    .stSelectbox label {
        color: black !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Selector para navegar entre las demás páginas
st.session_state.page = st.sidebar.selectbox("Selecciona una vista", list(pages.keys()), index=list(pages.keys()).index(st.session_state.page))

pages[st.session_state.page]()