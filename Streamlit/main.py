import streamlit as st
from PIL import Image
import pandas as pd
#Grafica barras
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px 


st.set_page_config(page_title = "Empleos Extraccion", page_icon= "https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", layout ="wide")

def pagina_principal():
    st.title("Bienvenido a la pagina de empleos de Hackaboss")
    st.subheader("Explora ofertas de empleo en España")
    st.write("Este es un proyecto donde podras hacer una busqueda de empleos publicados recientemente")


def muestra_datos():
    st.title("Datos y graficas")
    st.write("Aquí podras observar patrones en las ofertas de empleo seleccionadas")

    with st.expander(label = "DataFrame - Ofertas", expanded = False):
         df = pd.read_csv(filepath_or_buffer = "/home/bosser/Documentos/PROYECTOFINAL/CSV/CSV_finales/ofertas_final.csv")
         st.dataframe(df) 

     # Ruta al archivo HTML generado por folium
    ruta_html = "/home/bosser/Documentos/PROYECTOFINAL/mapa_cloropletico_espana.html"

    # Leer el contenido del archivo HTML
    with open(ruta_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Mostrar el mapa en Streamlit
    st.components.v1.html(html_content, width=1200, height=600)

    ####################################################
    #Primera grafica


    # Conexión a la base de datos MySQL
    database = "ofertas_de_empleo"
    db = mysql.connector.connect(host="localhost",
                                user="root",
                                password="Madrenero10+",
                                database=database)

    # Consulta SQL
    query = """
    SELECT 
        o.titulo, 
        tr.tec_id AS tecnologia, 
        COUNT(*) AS frecuencia,
        t.tecnologia AS nombre_tecnologia  -- Seleccionamos el nombre de la tecnología desde la tabla "tecnologias"
    FROM 
        ofertas o
    JOIN 
        tecnologias_relacion tr ON o.id_oferta = tr.id_oferta  -- Unimos "ofertas" y "tecnologias_relacion" por "id_oferta"
    JOIN 
        tecnologias t ON tr.tec_id = t.tec_id  -- Unimos "tecnologias_relacion" y "tecnologias" por "tec_id"
    GROUP BY 
        o.titulo, tr.tec_id, t.tecnologia  -- Agrupamos por puesto de trabajo, tecnología y nombre de la tecnología
    ORDER BY 
        o.titulo, frecuencia DESC;  -- Ordenamos por puesto de trabajo y frecuencia
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


    database = "ofertas_de_empleo"
    db = mysql.connector.connect(host="localhost",
                                user="root",
                                password="Madrenero10+",
                                database=database)

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
    return pd.read_csv("/home/bosser/Documentos/PROYECTOFINAL/CSV/CSV_manfred/general_limpio.csv")

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
            (df["Presencial"].str.lower().str.contains(location, na=False)) &
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
            background-color: lightblue !important;  /* Cambia este color */
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

manfredimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit_test/imagenes/manfred.png")
tecnoempleoimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit_test/imagenes/tecnoempleo.png")

st.sidebar.image("https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", use_container_width=True)

# Crear dos columnas en el sidebar
col1, col2 = st.sidebar.columns(2)

# Mostrar las imágenes en las columnas
with col1:
    st.image(manfredimg, use_container_width=True)
with col2:
    st.image(tecnoempleoimg, use_container_width=True)

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