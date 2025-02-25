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
        background-color: black
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

    with st.expander(label = "DataFrame - Ofertas", expanded = False):
         df = pd.read_csv(filepath_or_buffer = "CSV/CSV_finales/ofertas_final.csv")
         st.dataframe(df)


def muestra_datos():
    st.title("Datos y graficas")
    st.write("Aquí podras observar patrones en las ofertas de empleo seleccionadas")

     

     # Ruta al archivo HTML generado por folium
    ruta_html_provincias = "mapa_cloropletico_espana.html"
    ruta_html_calor = "mapa_calor_ciudades.html"
    ruta_html_comunidades = "mapa_comunidades.html"


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
    #Primera grafica/dividida


    # Conexión a la base de datos MySQL
    db_config = st.secrets["database"]
    db = mysql.connector.connect(
         host=db_config["host"],
         user=db_config["user"],
         password=db_config["password"],
         database=db_config["database"])

    # Consulta SQL para Tecnologías
    query_tech = """
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

    # Consulta SQL para Habilidades
    query_skills = """
    SELECT 
        o.titulo, 
        hr.hab_id AS habilidad, 
        COUNT(*) AS frecuencia,
        h.habilidad AS nombre_habilidad
    FROM 
        ofertas o
    JOIN 
        habilidades_relacion hr ON o.id_oferta = hr.id_oferta
    JOIN 
        habilidades h ON hr.hab_id = h.hab_id
    GROUP BY 
        o.titulo, hr.hab_id, h.habilidad
    ORDER BY 
        o.titulo, frecuencia DESC;
    """

    # Leer datos desde la base de datos
    df_tech = pd.read_sql(query_tech, con=db)
    df_skills = pd.read_sql(query_skills, con=db)

    # Filtrar los 10 puestos con más frecuencias
    top_titulos_tech = df_tech.groupby("titulo")["frecuencia"].sum().sort_values(ascending=False).head(10).index
    df_tech_filtered = df_tech[df_tech["titulo"].isin(top_titulos_tech)].groupby("titulo").apply(lambda x: x.nlargest(5, "frecuencia")).reset_index(drop=True)

    top_titulos_skills = df_skills.groupby("titulo")["frecuencia"].sum().sort_values(ascending=False).head(10).index
    df_skills_filtered = df_skills[df_skills["titulo"].isin(top_titulos_skills)].groupby("titulo").apply(lambda x: x.nlargest(5, "frecuencia")).reset_index(drop=True)

    # Configuración de la página Streamlit
    st.title('Frecuencia de Tecnologías y Habilidades por Puesto de Trabajo')

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tecnologías más solicitadas")
        with st.expander("Ver datos"):
            st.dataframe(df_tech_filtered)
        fig_tech = px.sunburst(df_tech_filtered, 
                        path=["titulo", "nombre_tecnologia"], 
                        values="frecuencia",
                        title="Frecuencia de Tecnologías por Puesto de Trabajo",
                        color="frecuencia",
                        color_continuous_scale=px.colors.sequential.Turbo)
        st.plotly_chart(fig_tech)

    with col2:
        st.subheader("Habilidades más solicitadas")
        with st.expander("Ver datos"):
            st.dataframe(df_skills_filtered)
        fig_skills = px.sunburst(df_skills_filtered, 
                        path=["titulo", "nombre_habilidad"], 
                        values="frecuencia",
                        title="Frecuencia de Habilidades por Puesto de Trabajo",
                        color="frecuencia",
                        color_continuous_scale=px.colors.sequential.Turbo)
        st.plotly_chart(fig_skills)


    ######################################### Segunda grafica


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

    # Calculamos la media de los salarios
    df_graficas["Salario medio"] = df_graficas[["salario_desde", "salario_hasta"]].mean(axis=1)

    # Detectamos outliers con el método de Tukey
    Q1 = df_graficas["Salario medio"].quantile(0.25)
    Q3 = df_graficas["Salario medio"].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    df_graficas["Outlier Tukey"] = (df_graficas["Salario medio"] < limite_inferior) | (df_graficas["Salario medio"] > limite_superior)

    # Creamos el histograma interactivo
    fig = px.histogram(df_graficas, x="Salario medio", color="Outlier Tukey",
                    nbins=50, labels={"Salario medio": "Salario Bruto/Año"},
                    title="Distribución de Salarios y Outliers",
                    color_discrete_map={False: "green", True: "yellow"})

    # Línea de la media salarial
    media_salario = df_graficas["Salario medio"].mean()
    fig.add_vline(x=media_salario, line_dash="dash", line_color="blue", annotation_text=f"Media: {media_salario:.2f}")

    # Mostramos en Streamlit
    st.plotly_chart(fig, use_container_width= True)

################################################### Tercera Grafica

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
    st.plotly_chart(fig, use_container_width= True)  # Muestra el gráfico interactivo de Plotly

################################################# Cuarta grafica

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
    st.plotly_chart(fig, use_container_width= True)

   
@st.cache_data
def load_data():
    return pd.read_csv("CSV/CSV_finales/ofertas_final.csv")

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


manfredimg = Image.open("Streamlit_test/imagenes/manfred.png")
tecnoempleoimg = Image.open("Streamlit_test/imagenes/tecnoempleo.png")

st.sidebar.image("https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", use_column_width=True)

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
    st.rerun()

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


# Selector para navegar entre páginas
selected_page = st.sidebar.selectbox("Selecciona una vista", list(pages.keys()), index=list(pages.keys()).index(st.session_state.page))

# Actualizar solo si el usuario cambia la selección en el selectbox
if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

pages[st.session_state.page]()