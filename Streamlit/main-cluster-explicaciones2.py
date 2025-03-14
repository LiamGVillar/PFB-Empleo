import streamlit as st
from PIL import Image
import pandas as pd
#Grafica barras
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px 
import seaborn as sns
import joblib
import time
import dill
import pickle
import plotly.graph_objects as go


import base64
from io import BytesIO

# URLs para las imágenes
manfred_url = "https://www.getmanfred.com/ofertas-empleo?onlyActive=false&currency=%E2%82%AC"
tecnoempleo_url = "https://www.tecnoempleo.com/ofertas-trabajo/"


st.set_page_config(page_title = "Empleos Extraccion", page_icon= "https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg",
                    layout ="wide",
                    initial_sidebar_state="collapsed" )

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
    #Imagen superior
    # Crear una fila con tres columnas para centrar la imagen
    col1, col2, col3 = st.columns([1, 2, 1]) 

    with col2:  # Solo usamos la columna central
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <img src="https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/620e82ff8680cd26532fff29_Logotipo%20HACK%20A%20BOSS_white%20100%20px.svg" 
                    width="200">
            </div>
            """,
            unsafe_allow_html=True
        )

    ##Titulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>¡Bienvenido a la página de búsqueda de empleos de Hackaboss!</h1>
        <h3>Explora ofertas de empleo IT en España</h3>
        <p style="font-size: 18px;">
            -En este proyecto podrás ver un análisis sobre ofertas de empleo IT publicados recientemente-
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    st.write("---------------------------------------------------------------------------------------------------------------")

    # Crear 2 columnas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h1 style='color: orange;'>Datos y graficas</h1>", unsafe_allow_html=True)
        st.write("""
            En este apartado se presentan las gráficas y los datos relevantes que permiten visualizar
            y analizar de manera clara y concisa la información recopilada.
        """)

    with col2:
        st.markdown("<h1 style='color: white;'>Busqueda y comparador de empleos</h1>", unsafe_allow_html=True)
        st.write("""
            En este apartado se presenta una herramienta diseñada para facilitar la búsqueda y comparación de empleos,
            permitiendo a los usuarios explorar diversas opciones laborales disponibles en el mercado. 
        """)

    with col1:
        st.markdown("<h1 style='color: white;'>Informacion PBI</h1>", unsafe_allow_html=True)
        st.write("""
            Utilizando Power BI, este comparador presenta visualizaciones dinámicas que te ayudarán a analizar las ofertas según diferentes criterios
                  como ubicación, salario, tipo de contrato y requisitos.
        """)

    with col2:
        st.markdown("<h1 style='color: orange;'>Clustering y Clasificación</h1>", unsafe_allow_html=True)
        st.write("""
            En este apartado se exploran las técnicas de Clustering y Clasificación, dos enfoques clave en el análisis de datos y aprendizaje automático. 
        """)

    with col1:
        st.markdown("<h1 style='color: orange;'>Arquitectura SQL</h1>", unsafe_allow_html=True)
        st.write("""
            Aquí se aborda la Arquitectura SQL, que es la estructura fundamental que soporta el almacenamiento, recuperación y gestión de datos en sistemas de bases de datos. 
        """)

    with col2:
        st.markdown("<h1 style='color: white;'>About Us</h1>", unsafe_allow_html=True)
        st.write("""
            Conoce el equipo encargado de que conozcas mejor el mercado laboral que nos rodea actualmente. 
        """)

    st.write("---------------------------------------")

    # Título principal
    st.title("Opiniones de Usuarios")

    # Texto introductorio
    st.markdown("""
        Aquí tienes algunas opiniones de nuestros usuarios. 
        ¡Descubre lo que dicen sobre nuestra app!
    """)

    # Cuadrados de opiniones con estrellas
    st.markdown("""
        <style>
            .opinion-box {
                width: 300px;
                height: 150px;
                background-color: gray;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
                display: inline-block;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            .opinion-box h3 {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .stars {
                color: gold;
                font-size: 20px;
            }
        </style>
        
        <div class="opinion-box">
            <h3>Liam Gonzalez</h3>
            <p>"Me llego el pedido frio no lo recomiendo"</p>
            <div class="stars">⭐</div>
        </div>
        <div class="opinion-box">
            <h3>Luis Martinez</h3>
            <p>"Muy útil para analizar datos de manera rápida y efectiva."</p>
            <div class="stars">⭐⭐⭐⭐</div>
        </div>
        <div class="opinion-box">
            <h3>Raquel </h3>
            <p>"Gran experiencia, la interfaz es muy amigable y eficiente."</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
        </div>
        <div class="opinion-box">
            <h3>Joshua Metcalf</h3>
            <p>"La mejor app de empleo de la historia"</p>
            <div class="stars">⭐⭐⭐⭐⭐</div>
        </div>
    """, unsafe_allow_html=True)



def muestra_datos():
    st.markdown(
    """
    <h1 style="text-align: center;">DATOS Y GRÁFICAS 📊</h1>
    <p style="text-align: center; font-size: 20px;">
        -Aquí podrás observar patrones en las ofertas de empleo seleccionadas-
    </p>
    """,
    unsafe_allow_html=True
)

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


    st.write("Esto es una grafica de habilidades y de tecnologias")


    ######################################### Segunda grafica

    st.title("Distribucion de salarios")
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

    st.write("""
Este gráfico analiza cómo el salario medio varía según los años de experiencia laboral. Los datos se han organizado para reflejar una secuencia lógica, 
desde los niveles iniciales hasta los más avanzados, facilitando la identificación de tendencias clave.

Eje X (horizontal):  
Vemos el nivel de experiencia requerido en las ofertas de trabajo.  

Eje Y (vertical):  
Salario medio asociado a cada nivel, expresado en euros y dividido por 1000. Se ha realizado el cálculo de la media entre el salario más bajo y el salario más alto ofrecido en cada vacante.

Se observa una correlación positiva entre experiencia y salario. Por ejemplo, quienes tienen más de 10 años de experiencia perciben un salario mayor que aquellos sin experiencia.

El valor que más datos tiene es - 3 años, con 1295 muestras, y "Menos de un año" con tan solo 28, por lo que no veo una tendencia tan clara, aunque sí queda constancia.

Las categorías como 3 años y 3-5 años, aunque parecidas en resultados, se representan por separado para diferenciar las ofertas de empleo que solicitan 3 años de experiencia o más de 3 años de experiencia.

Después de investigar, hay ofertas en las que se piden skills más específicos y de ahí podemos apreciar la mayoría de los outliers que se muestran en la gráfica.

En resumen, el gráfico confirma que la experiencia es un determinante crítico del salario, pero también destaca oportunidades para optimizar estrategias de compensación y desarrollo.
""")


    st.write("-------------------------------------------------------------------------------------------------------------------------------------")

    with st.expander(label = "Despliega todas las ofertas", expanded = False):
        df = pd.read_csv(filepath_or_buffer = "../CSV/CSV_finales/ofertas_final.csv")
        st.dataframe(df)
   
@st.cache_data
def load_data():
    return pd.read_csv("../CSV/CSV_finales/ofertas_final.csv")

df = load_data()

def busqueda():
    # Solucion primera al error de refresco
    if "selected_jobs" not in st.session_state:
        st.session_state.selected_jobs = []  
    
    if "df_filtrado" not in st.session_state:
        st.session_state.df_filtrado = pd.DataFrame() 

    # Títulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>BUSCA Y COMPARA EMPLEOS 🔎</h1>
        <h3>Explora ofertas de empleo IT en España</h3>
        <p style="font-size: 18px;">
            - Realiza un filtrado en la interfaz inferior para encontrar tu empleo -
        </p>
    </div>
    """,
    unsafe_allow_html=True
    )

    # Formulario de búsqueda
    with st.form(key="search_form"):
        job_title = st.text_input("Título del trabajo", "").strip().lower()
        location = st.text_input("Ubicación", "").strip().lower()
        company = st.text_input("Empresa", "").strip().lower()
        salario_desde, salario_hasta = st.slider(
            "Rango de salario",
            min_value=0,
            max_value=200,
            value=(0, 100),
            step=5
        )
        
        submit_button = st.form_submit_button("Buscar")

    if submit_button:
        # Filtrar los resultados 
        st.session_state.df_filtrado = df[
            (df["titulo"].str.lower().str.contains(job_title, na=False)) &
            (df["ciudad"].str.lower().str.contains(location, na=False)) &
            (df["empresa"].str.lower().str.contains(company, na=False)) &
            (df["salario_desde"] >= salario_desde) &
            (df["salario_hasta"] <= salario_hasta)
        ]

        # Mostrar los resultados
        st.write(f"Resultados para: {job_title} {location} {company} entre {salario_desde}K y {salario_hasta}K/€")
        
        if not st.session_state.df_filtrado.empty:
            st.dataframe(st.session_state.df_filtrado)
        else:
            st.write("No se encontraron resultados.")

    # Aseguramos datos
    if 'titulo' not in st.session_state.df_filtrado.columns:
        st.write("") #Aseguramos que no da error al principio
    else:
        # Filtramos los trabajos seleccionados para que coincidan con los que están disponibles en df_filtrado
        selected_jobs = [
            job for job in st.session_state.selected_jobs if job in st.session_state.df_filtrado["titulo"].tolist()
        ]

        # Selección múltiple
        selected_jobs = st.multiselect(
            "Selecciona trabajos para comparar", 
            st.session_state.df_filtrado["titulo"].tolist(), 
            default=selected_jobs, 
            format_func=lambda x: f"💼 {x}"
        )

        # Solución buscada para el error de refrescar página
        if selected_jobs != st.session_state.selected_jobs:
            st.session_state.selected_jobs = selected_jobs

        # Filtramos de nuevo el df
        if selected_jobs:
            df_selected = st.session_state.df_filtrado[st.session_state.df_filtrado["titulo"].isin(selected_jobs)]

            # GRafica01
            custom_colors = ["#FFA500", "#FFFFFF"]

            fig = px.bar(df_selected, 
                        x="titulo", 
                        y=["salario_desde", "salario_hasta"], 
                        title="Comparación de Salarios de los Trabajos Seleccionados",
                        labels={"titulo": "Trabajo", "salario_desde": "Salario Mínimo", "salario_hasta": "Salario Máximo"},
                        barmode='group',
                        color_discrete_sequence=custom_colors)

            st.plotly_chart(fig, use_container_width=True)

    


import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer

import pandas as pd
import numpy as np
import joblib
import streamlit as st

import pandas as pd
import numpy as np
import streamlit as st
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer

import pandas as pd
import numpy as np
import joblib
import streamlit as st

import pandas as pd
import numpy as np
import joblib
import streamlit as st

import pandas as pd
import numpy as np
import joblib
import streamlit as st

def informacion_pbi():

    st.markdown("<h1 style='text-align: center;'>Calculadora de Cluster para Creación de Ofertas de Empleo</h1>", unsafe_allow_html=True)
    
    # Agregamos un identificador a la caja de contraseña
    password = st.text_input("Introduce la contraseña:", type="password", key="password_input")
    correct_password = "f"

    if password != correct_password:
        if password:  # Solo muestra el error si el usuario ha intentado introducir una contraseña
            st.error("❌ Acceso restringido a usuarios registrados. Contacta con soporte para crear tu cuenta profesional.")

            # CSS vibración si contraseña es incorrecta.
            st.markdown(
                """
                <style>
                @keyframes shake {
                    0% { transform: translateX(0); }
                    25% { transform: translateX(-5px); }
                    50% { transform: translateX(5px); }
                    75% { transform: translateX(-5px); }
                    100% { transform: translateX(0); }
                }
                .stTextInput input {
                    animation: shake 0.3s ease-in-out;
                    border: 2px solid red !important;
                }
                </style>
                """, 
                unsafe_allow_html=True
            )
        return  # Salir de la función si la contraseña es incorrecta
    
    # Si la contraseña es correcta, ejecutar el resto del código
    df_general = pd.read_csv("/home/bosser/Escritorio/proyectofinal/clustering/df_imputado_final.csv")
        
    with open("/home/bosser/Escritorio/proyectofinal/clustering/encoder.pkl", "rb") as f:
        encoder = dill.load(f)
    with open("/home/bosser/Escritorio/proyectofinal/clustering/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("/home/bosser/Escritorio/proyectofinal/clustering/imputer.pkl", "rb") as f:
        imputer = pickle.load(f)
    with open("/home/bosser/Escritorio/proyectofinal/clustering/modelo_regresion.pkl", "rb") as f:
        model = pickle.load(f)

    st.markdown("<h1 style='text-align: center; font-size: 22px;'>Introduce los datos de la oferta que deseas publicar para saber a qué cluster pertenece</h1>", unsafe_allow_html=True)


    # Nuevos inputs
    salario_media = st.slider(
        'Salario anual', 
        0, 154000, 40000,  # Rango de 0 a 154000, valor inicial 40000
        key="salario_media_slider"
    )

    experiencia = st.slider(
        'Experiencia requerida (años)', 
        0, 10, 1,  # Rango de 0 a 10, valor inicial 1
        key="experiencia_slider"
    )

    teletrabajo = st.selectbox(
        'Teletrabajo', 
        ['Presencial', 'Híbrido', 'Remoto'],
        key="teletrabajo_selectbox"
    )

    ciudad = st.selectbox(
        'Ciudad', 
        ['Madrid', '100% Remoto', 'Barcelona', 'Valencia', 'Málaga', 'Bizkaia', 'Zaragoza', 'A Coruña', 'Sevilla', 'Gipuzkoa', 'No Especificado', 'Alicante', 'Valladolid', 'Pontevedra', 'Navarra', 'Asturias', 'Castellón', 'Álava', 'Girona', 'Baleares', 'Cantabria', 'La Rioja', 'Córdoba'],
        key="ciudad_selectbox"
    )

    jornada_tipo = st.selectbox(
        'Tipo de jornada laboral', 
        ['Jornada Completa', 'Media Jornada', 'Flexible', 'Intensiva Mañana', 'Turno Rotatorio'],
        key="jornada_tipo_selectbox"
    )

    funciones = st.selectbox(
        'Funciones:', 
        ['Programador', 'Consultor', 'Analista Programador', 'Ingenieros/Industria', 'Big Data', 'Jefe de Proyecto', 'Ciberseguridad', 'Analista', 'Técnico de Sistemas', 'Arquitecto TIC', 'Desarrollador Web', 'Marketing', 'DevOps', 'Administrador', 'Soporte Técnico', 'Tester', 'Redes', 'Jefe de Equipo', 'Electrónica', 'Helpdesk', 'Desarrollador Móvil', 'Base de Datos/DBA', 'Inteligencia Artificial/Machine Learning', 'Diseño gráfico', 'Sistemas de Calidad', 'Técnico de Gestión', 'Responsable de Producto', 'Comercial', 'Auditor', 'I+D'],
        key="funciones_selectbox"
    )

    contrato_tipo = st.selectbox(
        'Tipo de contrato', 
        ['Indefinido', 'Temporal', 'Prácticas', 'Freelance/Autónomo'],
        key="contrato_tipo_selectbox"
    )

    nivel_profesional = st.selectbox(
        'Nivel profesional', 
        ['Empleado', 'Especialista', 'Mando Intermedio', 'Director'],
        key="nivel_profesional_selectbox"
    )

    formacion_minima = st.selectbox(
        'Formación mínima requerida:', 
        ['FP2/Grado Superior', 'Grado Medio', 'Ingeniero Técnico', 'Sin estudios', 'Grado EEES (Bolonia)', 'E.S.O. (Educación Secundaria Obligatoria)', 'Ingeniero Superior', 'FP1', 'Licenciado', 'Bachillerato/COU', 'Postgrado EEES (Máster)', 'Diplomado', 'Otros títulos, certificaciones y carnets', 'Certificado de Profesionalidad', 'Otra Formación Tecnológica', 'Doctorado'],
        key="formacion_minima_selectbox"
    )

    # Inputs de tecnologías y habilidades
    tecnologias = st.multiselect(
        'Tecnologías requeridas:', 
        ['sap ewm', 'python', 'sql', 'AWS', 'JavaScript', 'Python', 'peoplesoft', 'Docker', 'aws', 'React'],
        key="tecnologias_multiselect"
    )

    habilidades = st.multiselect(
        'Habilidades requeridas:', 
        ['Programador', 'Proactividad', 'Trabajo en equipo', 'Aprendizaje Continuo', 'Capacidad de autogestión'],
        key="habilidades_multiselect"
    )

    # Crear el dataframe de entrada del usuario
    user_input = pd.DataFrame({
        'salario_media': [salario_media // 1000],
        'experiencia': [experiencia],
        'teletrabajo': [teletrabajo],
        'ciudad': [ciudad],
        'jornada_tipo': [jornada_tipo],
        'funciones': [funciones],
        'contrato_tipo': [contrato_tipo],
        'nivel_profesional': [nivel_profesional],
        'formacion_minima': [formacion_minima],
        'num_tecnologias': [len(tecnologias)],  # Contar el número de tecnologías seleccionadas
        'num_habilidades': [len(habilidades)]   # Contar el número de habilidades seleccionadas
    }, index=[0])

    # Aplicar el encoder
    for column in encoder.keys():
        if column in user_input.columns:
            if isinstance(encoder[column], dict):  # Si es un mapeo de categorías
                user_input[column] = user_input[column].map(encoder[column])
            elif callable(encoder[column]):  # Si es una función lambda
                user_input[column] = encoder[column](user_input)
            elif encoder[column] is not None:  # Si hay un valor específico
                user_input[column] = encoder[column]


    # Asegurar que las columnas estén en el orden correcto
    expected_columns = scaler.feature_names_in_
    missing_columns = [col for col in expected_columns if col not in user_input.columns]
    for col in missing_columns:
        user_input[col] = 0  # Añadir columnas faltantes con valores por defecto

    user_input = user_input[expected_columns]

    # Aplicar el scaler
    user_input_scaled = scaler.transform(user_input)

    # Aplicar el imputer
    user_input_imputed = imputer.transform(user_input_scaled)

    # Predicción del cluster
    if st.button('Predecir Cluster'):
        cluster_predicho = model.predict(user_input_imputed)
        st.success(f'El cluster predicho es: {cluster_predicho[0]}')

        if cluster_predicho[0] == 0:
            st.write('El clúster más grande, dominado por roles más básicos o de entrada, pero con cierta especialización. Caracterizado por ofertas para profesionales para roles técnicos operativos y de soporte, además de  ofertas junior.')
        elif cluster_predicho[0] == 1:
            st.write('Ofertas en el mercado de roles especializados, con un mayor salario y opciones de teletrabajo. Dominado por profesionales experimentados.')
        elif cluster_predicho[0] == 2:
            st.write('Este grupo representa la categoría más crítica y especializada. Roles vitales dentro del sector.')


import pandas as pd
import streamlit as st

def clustering_clasificacion():
    # Cargar los DataFrames
    df_general_cluster = pd.read_csv("/home/bosser/Escritorio/proyectofinal/clustering/df_imputado_final_clusterizado.csv")
    df_cluster = pd.read_csv("/home/bosser/Escritorio/proyectofinal/clustering/df_clusters.csv")
    
    colores = {
        0: "rgba(46, 139, 87, 0.5)",
        1: "rgba(191, 0, 255, 1)",
        2: "rgba(255, 100, 0, 1)"
    }
    
    st.markdown(
        """
        <h1 style="text-align: center;">CLASIFICACIÓN DE OFERTAS ☁️</h1>
        <p style="text-align: center; font-size: 20px;">
            -Echa un vistazo a nuestro estudio de clustering sobre las ofertas de empleo en nuestra base de datos-
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Inicializar el estado de sesión si no existe
    if "show_original" not in st.session_state:
        st.session_state.show_original = True  # Mostrar el DataFrame original al inicio
    if "df_to_show" not in st.session_state:
        st.session_state.df_to_show = df_cluster  # DataFrame a mostrar (original o ordenado)
    if "show_cluster_counts" not in st.session_state:
        st.session_state.show_cluster_counts = False  # Controlar si se muestran los conteos de clusters
    if "show_dbscan_plot" not in st.session_state:
        st.session_state.show_dbscan_plot = False  # Controlar si se muestra la gráfica de DBSCAN
    if "show_mean_comparison" not in st.session_state:
        st.session_state.show_mean_comparison = False  # Controlar si se muestra la comparación de medias
    
    # Mostrar el DataFrame original solo si show_original es True
    if st.session_state.show_original:
        st.write("Comprobación con diferentes EPS para obtención del mejor cluster")
        st.dataframe(df_cluster)
    
    # Botón para ordenar el DataFrame por el Silhouette Score de mayor a menor
    if st.button("Obtener mejores EPS"):
        df_ordenado = df_cluster.sort_values(by="silhouette_score", ascending=False)
        st.session_state.df_to_show = df_ordenado
        st.session_state.show_original = False
        st.session_state.show_cluster_counts = True
    
    # Mostrar el DataFrame ordenado y la gráfica de conteo de clusters
    if not st.session_state.show_original and st.session_state.show_cluster_counts:
        
        col1, col2 = st.columns([2, 2])
        
        with col1:
            st.markdown("<h3 style='text-align: center;'>Revisión del EPS más adecuado para clasificación</h3>", unsafe_allow_html=True)
            st.dataframe(st.session_state.df_to_show)
        
        with col2:
            st.markdown("<h3 style='text-align: center;'>Clusters resultantes tras escoger el mejor EPS", unsafe_allow_html=True)
            cluster_counts = df_general_cluster["Cluster"].value_counts()
            fig = go.Figure()
            for cluster, count in cluster_counts.items():
                fig.add_trace(go.Bar(
                    x=[cluster],
                    y=[count],
                    name=f"Cluster {cluster}",
                    marker_color=colores.get(cluster, "rgba(128, 128, 128, 1)")
                ))
            fig.update_layout(title="Conteo de Clusters", xaxis_title="Cluster")
            st.plotly_chart(fig)
    
    # Botón para mostrar la gráfica de DBSCAN
    if st.button("Clasificación con DBSCAN"):
        st.session_state.show_dbscan_plot = True
    
    # Mostrar la gráfica de DBSCAN
    if st.session_state.get("show_dbscan_plot", False):
        st.markdown("<h3 style='text-align: center;'>Visualización de los clusters generados por DBSCAN:</h3>", unsafe_allow_html=True)
        df_general_cluster['Cluster'] = df_general_cluster['Cluster'].astype('category')
        fig_dbscan = px.scatter(
            df_general_cluster,  
            x="ciudad",  
            y="salario_media", 
            color="Cluster", 
            color_discrete_map=colores,
            title="Clustering con DBSCAN", 
            labels={"ciudad": "Ciudad", "salario_media": "Salario Medio"}
        )
        st.plotly_chart(fig_dbscan)
    
    # Botón para mostrar la comparación de medias por cluster
    if st.button("Mostrar comparación de medias por Cluster"):
        st.session_state.show_mean_comparison = True
    # Mostrar la comparación de medias por cluster
    if st.session_state.show_mean_comparison:
        st.markdown("<h3 style='text-align: center;'>Comparación de valores medios por Cluster:</h3>", unsafe_allow_html=True)
        df_grouped = df_general_cluster.groupby(by="Cluster").mean().T
        df_long = df_grouped.reset_index().melt(id_vars="index", var_name="Cluster", value_name="Valor")
        
        fig_mean = px.bar(
            df_long,
            x="index",
            y="Valor",
            color="Cluster",
            color_discrete_sequence=list(colores.values()),
            barmode="group",
            labels={"index": "Características", "Valor": "Valor Medio"},
            title="Comparación de valores medios por Cluster"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(fig_mean, use_container_width=True)
        with col2:
            st.dataframe(df_grouped)



def arquitectura_sql():
    ##Titulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>ARQUITECTURA SQL<h1>
        <h3>Así se ha estructurado nuestros datos</h3>
        <p style="font-size: 18px;">
            - Conoce la relación de nuestros datos para la extracción de información -
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    st.write("---------------------------------------------")
    
    st.image("../DIAGRAMA_SQL.drawio.png", width=900)
    

def about_us():
    ##Titulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>ABOUT US ❤️
        <h3>¡Conócenos!</h3>
        <p style="font-size: 18px;">
            - Este es el equipo encargado de que puedas disfrutar de los mejores datos -
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    st.write("-------------------------------------------------------------------------")
    
    col1, col2, col3, col4 = st.columns(4)

    # Persona 1
    with col1:
        st.markdown(
        f"""
        <style>
            .circle-container {{
                text-align: center;  /* Centra todo el contenido */
            }}
            .circle-img {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                object-fit: cover;
                display: block;
                margin: 0 auto; /* Centrar imagen */
            }}
            .linkedin-link {{
                display: block;
                margin-top: 10px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                color: #0077b5; /* Color LinkedIn */
            }}
        </style>
        <div class="circle-container">
            <img src="https://media.licdn.com/dms/image/v2/D4D03AQHAUDedAyCf1A/profile-displayphoto-shrink_800_800/B4DZVYJI61GcAc-/0/1740940546315?e=1746662400&v=beta&t=lEhQ0eNa2gJfx0QuuKkr6Bk1mG8VIKR7IjLETdyfKQg" class="circle-img">
            <br>
            <a href="https://www.linkedin.com/in/liam-gonzalez-villar-2994aa248" class="linkedin-link" target="_blank">-LinkedIn-</a>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
            """
            <style>
                .title-container {
                    text-align: center;
                }
                .main-title {
                    font-size: 40px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color : orange;
                }
                .subtitle {
                    font-size: 24px;
                    color: gray;
                }
            </style>
            <div class="title-container">
                <p class="main-title">Liam Gonzalez Villar</p>
                <p class="subtitle">Data Analyst</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Persona 2
    with col2:
        st.markdown(
        f"""
        <style>
            .circle-container {{
                text-align: center;  /* Centra todo el contenido */
            }}
            .circle-img {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                object-fit: cover;
                display: block;
                margin: 0 auto; /* Centrar imagen */
            }}
            .linkedin-link {{
                display: block;
                margin-top: 10px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                color: #0077b5; /* Color LinkedIn */
            }}
        </style>
        <div class="circle-container">
            <img src="https://media.licdn.com/dms/image/v2/D4D35AQG5hLgxvtx7SA/profile-framedphoto-shrink_200_200/B4DZVYJJPyG8AY-/0/1740940547326?e=1741629600&v=beta&t=QAM6NUInIxCpraohRVAWjQE9gbK9W_6Kpm3IUQ6SZrM" class="circle-img">
            <br>
            <a href="https://www.linkedin.com/in/liam-gonzalez-villar-2994aa248" class="linkedin-link" target="_blank">-LinkedIn-</a>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
            """
            <style>
                .title-container {
                    text-align: center;
                }
                .main-title-white {{
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 5px;
                color: white; /* Solo para este título */
                }
                .subtitle {
                    font-size: 24px;
                    color: gray;
                }
            </style>
            <div class="title-container">
                <p class="main-title">Luis Martínez de la Riva</p>
                <p class="subtitle">Data Analyst</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Persona 3
    with col3:
        st.markdown(
        f"""
        <style>
            .circle-container {{
                text-align: center;  /* Centra todo el contenido */
            }}
            .circle-img {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                object-fit: cover;
                display: block;
                margin: 0 auto; /* Centrar imagen */
            }}
            .linkedin-link {{
                display: block;
                margin-top: 10px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                color: #0077b5; /* Color LinkedIn */
            }}
        </style>
        <div class="circle-container">
            <img src="https://media.licdn.com/dms/image/v2/D4D35AQG5hLgxvtx7SA/profile-framedphoto-shrink_200_200/B4DZVYJJPyG8AY-/0/1740940547326?e=1741629600&v=beta&t=QAM6NUInIxCpraohRVAWjQE9gbK9W_6Kpm3IUQ6SZrM" class="circle-img">
            <br>
            <a href="https://www.linkedin.com/in/raquel-barbeito-garcia-783497319/" class="linkedin-link" target="_blank">-LinkedIn-</a>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
            """
            <style>
                .title-container {
                    text-align: center;
                }
                .main-title {
                    font-size: 40px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color : orange;
                }
                .subtitle {
                    font-size: 24px;
                    color: gray;
                }
            </style>
            <div class="title-container">
                <p class="main-title">Raquel Barbeito Garcia</p>
                <p class="subtitle">Data Analyst</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Persona 4
    with col4:
        st.markdown(
        f"""
        <style>
            .circle-container {{
                text-align: center;  /* Centra todo el contenido */
            }}
            .circle-img {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                object-fit: cover;
                display: block;
                margin: 0 auto; /* Centrar imagen */
            }}
            .linkedin-link {{
                display: block;
                margin-top: 10px;
                font-size: 16px;
                font-weight: bold;
                text-decoration: none;
                color: #0077b5; /* Color LinkedIn */
            }}
        </style>
        <div class="circle-container">
            <img src="https://media.licdn.com/dms/image/v2/D4E03AQHHCjJEhF6yTg/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1714734604277?e=1746662400&v=beta&t=UGM21u5Qnhs4G__Ih8m0nyeP15r7tP-CH54MGHFKIGI" class="circle-img">
            <br>
            <a href="https://www.linkedin.com/in/joshua-metcalf/" class="linkedin-link" target="_blank">-LinkedIn-</a>
        </div>
        """,
        unsafe_allow_html=True
    )

        st.markdown(
            """
            <style>
                .title-container {
                    text-align: center;
                }
                .main-title {
                    font-size: 40px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    color : orange;
                }
                .subtitle {
                    font-size: 24px;
                    color: gray;
                }
            </style>
            <div class="title-container">
                <p class="main-title">Joshua Metcalf</p>
                <p class="subtitle">Data Analyst</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("---------------------------------------------------")
    st.write("Somos un equipo apasionado por la innovación y el análisis de datos, comprometido con ofrecer soluciones tecnológicas que faciliten la toma de decisiones informadas. Nuestra misión es proporcionar herramientas intuitivas y poderosas que permitan a nuestros usuarios explorar, comprender y utilizar los datos de manera eficiente. Con un enfoque en la simplicidad y la eficacia, nos esforzamos por crear experiencias que transformen la forma en que las personas interactúan con la información, impulsando el éxito tanto en el ámbito profesional como personal.")











# Inyectar CSS para cambiar el color del sidebar
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: white !important;
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
    "Busqueda empleos" : busqueda,
    "Informacion PBI" : informacion_pbi,
    "Clustering y Clasificación" : clustering_clasificacion,
    "Arquitectura de SQL" : arquitectura_sql,
    "About us" : about_us
}


manfredimg = Image.open("/home/bosser/PFB-Empleo/Streamlit_test/imagenes/manfred.png")
tecnoempleoimg = Image.open("/home/bosser/PFB-Empleo/Streamlit_test/imagenes/tecnoempleo.png")

st.sidebar.image("https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", use_column_width=True)

# Función para convertir imagen a base64
def img_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


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


st.sidebar.markdown("<br>" * 12, unsafe_allow_html=True)
st.sidebar.markdown(
    '<p style="color: black;">App en versión de pruebas</p>',
    unsafe_allow_html=True
)