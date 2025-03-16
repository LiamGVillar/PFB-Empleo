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
import time
import joblib
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pickle
import dill
import toml
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
    
    st.image("Streamlit/Data/portada.jpg", width=1850)

    st.write("---------------------------------------------------------------------------------------------------------------")

    # Crear 2 columnas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h1 style='color: orange;'>Datos y gráficas</h1>", unsafe_allow_html=True)
        st.write("""
            En este apartado se presentan las gráficas y los datos relevantes que permiten visualizar
            y analizar de manera clara y concisa la información recopilada.
        """)

    with col2:
        st.markdown("<h1 style='color: white;'>Búsqueda y comparador de empleos</h1>", unsafe_allow_html=True)
        st.write("""
            En este apartado se presenta una herramienta diseñada para facilitar la búsqueda y comparación de empleos,
            permitiendo a los usuarios explorar diversas opciones laborales disponibles en el mercado. 
        """)

    with col1:
        st.markdown("<h1 style='color: white;'>Información PBI</h1>", unsafe_allow_html=True)
        st.write("""
            Utilizando Power BI, este comparador presenta visualizaciones dinámicas que te ayudarán a analizar las ofertas según diferentes criterios
                  como ubicación, salario, tipo de contrato y requisitos.
        """)

    with col2:
        st.markdown("<h1 style='color: orange;'>Clústering y Clasificación</h1>", unsafe_allow_html=True)
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
            <p>"La mejor app de empleo de toda la historia."</p>
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
    unsafe_allow_html=True)

     # Ruta al archivo HTML generado por folium
    ruta_html_provincias = "Streamlit/Data/mapa_cloropletico_espana.html"
    ruta_html_calor = "Streamlit/Data/mapa_calor_ciudades.html"
    ruta_html_comunidades = "Streamlit/Data/mapa_comunidades.html"


    mapa_seleccionado = st.selectbox(
    "Mapas:",
    ("Ofertas de empleo por provincia", "Ofertas de empleo por ciudad", "Ofertas de empleo por comunidad autónoma"))

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
    st.components.v1.html(html_content, width=1400, height=600)

    ####################################################
    #Primera grafica/dividida


    # Conexión a la base de datos MySQL
    config = toml.load(".streamlit/secrets.toml")
    db_config = config["database"]

    db = mysql.connector.connect(host=db_config["host"],
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
    st.title("Frecuencia de Tecnologías y Habilidades por Puesto de Trabajo")

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


    st.write("Esta es una gráfica comparativa que muestra la frecuencia de tecnología, a la izquierda y habilidades a la derecha,"
    " asociadas a distintos puestos de trabajo. En la parte de la leyenda podemos ver los colores de la frecuencia relativa que va desde 10 a 30  para poder visualizar qué tecnologías y habilidades sin más recurrentes en ofertas laborales. su claridad.")

    ####################################################Primeragrafica B

    import plotly.graph_objects as go
    consulta_habilidades = """
    SELECT 
        h.habilidad,
        COUNT(hr.id_oferta) AS demanda,
        AVG((o.salario_desde + o.salario_hasta)/2) AS salario_promedio
    FROM habilidades_relacion hr
    JOIN habilidades h ON hr.hab_id = h.hab_id
    JOIN ofertas o ON hr.id_oferta = o.id_oferta
    WHERE o.salario_desde IS NOT NULL 
    AND o.salario_hasta IS NOT NULL
    GROUP BY h.habilidad
    ORDER BY demanda DESC
    LIMIT 10;
    """

    consulta_tecnologias = """
    SELECT 
        t.tecnologia,
        COUNT(tr.id_oferta) AS demanda,
        AVG((o.salario_desde + o.salario_hasta)/2) AS salario_promedio
    FROM tecnologias_relacion tr
    JOIN tecnologias t ON tr.tec_id = t.tec_id
    JOIN ofertas o ON tr.id_oferta = o.id_oferta
    GROUP BY t.tecnologia
    ORDER BY demanda DESC
    LIMIT 10;
    """

    # Cargar datos
    df_tech = pd.read_sql(consulta_tecnologias, db)
    df_hab = pd.read_sql(consulta_habilidades, db)

    # Crear subplots
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=("Top 10 Tecnologías Demandadas", "Top 10 Habilidades Demandadas"),
                        horizontal_spacing=0.2)

    # Gráfico de Tecnologías
    fig.add_trace(go.Bar(
        x=df_tech["tecnologia"],
        y=df_tech["demanda"],
        marker=dict(color=df_tech["salario_promedio"], coloraxis="coloraxis"),
        name="Tecnologías",
    ), row=1, col=1)

    # Gráfico de Habilidades
    fig.add_trace(go.Bar(
        x=df_hab["habilidad"],
        y=df_hab["demanda"],
        marker=dict(color=df_hab["salario_promedio"], coloraxis="coloraxis"),
        name="Habilidades",
    ), row=1, col=2)

    # Configuración de color y leyenda
    fig.update_layout(
        coloraxis=dict(colorscale="Viridis", colorbar=dict(
            title="Salario Promedio (€)",  
            title_side="top",
            ticksuffix=" €")),
        showlegend=False)

    # Mostrar el gráfico en Streamlit
    st.title("Comparativa de Tecnologías y Habilidades Demandadas")
    st.plotly_chart(fig)

    st.write("Estos gráficos de barras comparan las 10 tecnologías y habilidades más demandadas en el mercado laboral,"
    " mostrando tanto la cantidad de ofertas disponibles como el salario asociado a cada una. En el apartado de tecnologías,"
    " **Python** se posiciona como la más solicitada, mientras que **AWS** destaca por ofrecer los salarios más altos."
    " En cuanto a habilidades, la **proactividad** es la más demandada junto con trabajo en equipo, mientras que **programador**,"
    " es la menos solicitada y con menor remuneración. ")

    ######################################### Segunda grafica

    consulta_top_niveles = """
    WITH top_niveles AS (
        SELECT 
            nivel_profesional,
            COUNT(id_oferta) AS total_ofertas
        FROM ofertas
        WHERE nivel_profesional IS NOT NULL
        GROUP BY nivel_profesional
        ORDER BY total_ofertas DESC
        LIMIT 2
    )
    SELECT 
        o.salario_desde,
        o.salario_hasta,
        o.nivel_profesional,
        CASE
            WHEN o.experiencia IN ("Más de 10 años", "Más de 5 años") THEN "Más de 5 años"
            WHEN o.experiencia IN ("3-5 años", "3 años", "2 años") THEN "2-5 años"
            ELSE "Menos de 2 años"
        END AS experiencia_agrupada
    FROM ofertas o
    JOIN top_niveles tn ON o.nivel_profesional = tn.nivel_profesional
    WHERE o.salario_desde IS NOT NULL
    AND o.salario_hasta IS NOT NULL
    AND o.experiencia IS NOT NULL;
    """

    # Cargar datos
    df = pd.read_sql(consulta_top_niveles, db)

    # Calcular salario bruto anual
    df["Salario bruto anual"] = df[["salario_desde", "salario_hasta"]].mean(axis=1)

    # Crear el gráfico con leyenda mejorada
    fig = px.histogram(
        df,
        x="Salario bruto anual",
        facet_row="nivel_profesional",
        color="experiencia_agrupada",
        nbins=30,
        labels={
            "Salario bruto anual": "Salario Bruto Anual (en miles de €)",
            "count": "Número de ofertas",
            "experiencia_agrupada": "Años de experiencia requeridos"
        },
        title="Distribución Salarial por Nivel Profesional y Experiencia",
        category_orders={
            "nivel_profesional": df["nivel_profesional"].value_counts().index.tolist(),
            "experiencia_agrupada": ["Menos de 2 años", "2-5 años", "Más de 5 años"]
        },
        color_discrete_map={
            "Menos de 2 años": "#1f77b4",
            "2-5 años": "#ff7f0e",
            "Más de 5 años": "#2ca02c"
        },
        barmode="group",
        opacity=0.9,
        height=800
    )

    # Personalizar la leyenda
    fig.update_layout(
        legend=dict(
        title=dict(
            text="Años de experiencia:",  
            font=dict(color="black")  
        ),
            orientation="v",
            yanchor="top",
            xanchor="right",
            y=1.02,
            x=1.15,
            bgcolor="rgba(255,255,255,0.9)",
            font=dict(color="black")
        ),
        hovermode="x unified",
        bargap=0.15,
        xaxis_title="Salario Bruto Anual (€)",
        yaxis_title="Número de ofertas"
    )

    # Ajustes adicionales
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.update_traces(
        hovertemplate="<b>Rango salarial:</b> %{x}€<br><b>Ofertas:</b> %{y}"
    )

    # Mostrar el gráfico en Streamlit
    st.title("Distribución Salarial por Nivel Profesional y Experiencia")
    st.plotly_chart(fig)
    
    st.write("La mayor concentración de ofertas laborales corresponde a perfiles de Empleado con experiencia media (2-5 años) y rangos salariales de 30.000-39.000€ anuales. Para posiciones junior (sin experiencia requerida), el grueso de oportunidades se concentra en la franja de 20.000-29.000€, evidenciando una correlación directa entre años de experiencia y nivel retributivo en el mercado laboral analizado.")

################################################### Tercera Grafica

    # Creamos el gráfico de caja (box plot)
    import plotly.graph_objects as go
    consulta_sql = """
    SELECT 
        c.ciudad,
        (o.salario_desde + o.salario_hasta) / 2 AS salario_promedio
    FROM ofertas o
    INNER JOIN ciudades c ON o.id_oferta = c.id_oferta
    INNER JOIN ciudades_coordenadas cc ON c.ciudad = cc.ciudad
    WHERE cc.pais = "España"
    AND o.salario_desde IS NOT NULL 
    AND o.salario_hasta IS NOT NULL
    AND c.ciudad IN (
        SELECT c2.ciudad
        FROM ciudades c2
        INNER JOIN ofertas o2 ON c2.id_oferta = o2.id_oferta
        GROUP BY c2.ciudad
        HAVING COUNT(*) > 3
    );
    """

    df = pd.read_sql(consulta_sql, db)
    ciudades = df["ciudad"].unique().tolist()

    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=df["ciudad"],
            y=df["salario_promedio"],
            visible=True,
            name="Todas"
        )
    )

    for ciudad in ciudades:
        df_ciudad = df[df["ciudad"] == ciudad]
        fig.add_trace(
            go.Box(
                x=df_ciudad["ciudad"],
                y=df_ciudad["salario_promedio"],
                visible=False,
                name=ciudad
            )
        )

    botones = []
    botones.append({
        "label": "Todas las ciudades",
        "method": "update",
        "args": [{"visible": [True] + [False]*len(ciudades)}]
    })

    for i, ciudad in enumerate(ciudades):
        visibilidad = [False]*(len(ciudades)+1)
        visibilidad[i+1] = True
        
        botones.append({
            "label": ciudad,
            "method": "update",
            "args": [{"visible": visibilidad}]
        })

    fig.update_layout(
        updatemenus=[{
            "buttons": botones,
            "direction": "down",
            "showactive": True,
            "x": 0.5,
            "xanchor": "center",
            "y": 1.15,
            "yanchor": "top"
        }],
        title="Distribución de salarios por ciudad",
        showlegend=False,
        xaxis_title="Ciudad",
        yaxis_title="Salario Promedio (€)"
    )

    st.title("Análisis de Salarios por Ciudad")
    st.plotly_chart(fig)

    
    st.write("En esta gráfica con desplegable, podemos ver con detalle la distribución de salarios por ciudad. Destacan algunas ciudades como Álava y Bizkaia con una gran cantidad de ofertas. Madrid y Barcelona se caracterizan por tener ofertas con salarios con unos sueldos mayores, fuera de los datos normales.")
    

################################################# Cuarta grafica

    st.title("Análisis de Salarios por tecnología y experiencia")
    query = """
    WITH top_tecnologias AS (
        SELECT 
            t.tecnologia,
            COUNT(*) AS num_ofertas
        FROM tecnologias_relacion tr
        JOIN tecnologias t ON tr.tec_id = t.tec_id
        JOIN ofertas o ON tr.id_oferta = o.id_oferta
        WHERE o.salario_desde IS NOT NULL 
        AND o.salario_hasta IS NOT NULL
        AND o.experiencia IS NOT NULL
        GROUP BY t.tecnologia
        ORDER BY num_ofertas DESC
        LIMIT 5
    )
    SELECT 
        t.tecnologia AS Tecnologia,
        (o.salario_desde + o.salario_hasta) / 2 AS Salario,
        CASE
            WHEN o.experiencia IN ("Más de 10 años", "Más de 5 años") THEN "Más de 5 años"
            WHEN o.experiencia IN ("3-5 años", "3 años", "2 años") THEN "Entre 2 y 5 años"
            WHEN o.experiencia IN ("1 año", "Menos de un año", "Sin Experiencia") THEN "Menos de 2 años"
            ELSE "Otros"
        END AS Experiencia_agrupada
    FROM tecnologias_relacion tr
    JOIN tecnologias t ON tr.tec_id = t.tec_id
    JOIN ofertas o ON tr.id_oferta = o.id_oferta
    JOIN top_tecnologias tt ON t.tecnologia = tt.tecnologia
    WHERE o.salario_desde IS NOT NULL 
    AND o.salario_hasta IS NOT NULL
    AND o.experiencia IS NOT NULL;
    """

    # Ejecutar la consulta y obtener los resultados en un DataFrame de pandas
    df_boxplot = pd.read_sql(query, db)

    # Definir el orden de las categorías agrupadas
    orden_experiencia = ["Más de 5 años", "Entre 2 y 5 años", "Menos de 2 años"]

    # Crear el gráfico de boxplot con Plotly
    fig = px.box(
        df_boxplot,
        x="Experiencia_agrupada",
        y="Salario",
        color="Tecnologia",
        title="Distribución de Salarios por Tecnología y Experiencia",
        labels={"Salario": "Salario (€)", "Experiencia_agrupada": "Años de Experiencia"},
        category_orders={"Experiencia_agrupada": orden_experiencia}
    )

    # Personalizar el layout del gráfico
    fig.update_layout(
        xaxis_title="Años de experiencia",
        yaxis_title="Salario (en miles de €)",
        legend_title="Tecnología",
        boxmode="group"  # Agrupar los boxplots por categoría de experiencia
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)


    st.write("El diagrama de caja muestra la relación entre tecnologías clave (Azure, Python, SQL, SAP EWM, Peoplesoft), niveles de experiencia (eje x) y distribución salarial (eje y). Peoplesoft, software de gestión empresarial y recursos humanos, presenta los salarios más altos en roles senior (+5 años), mientras que Azure destaca en posiciones junior (<2 años). Los rangos salariales son homogéneos en experiencia media,evidenciando una correlación directa entre años de experiencia exigidos y remuneración ofertada.")


################################################################################GRAFICO QUINTO

    consulta = """
    SELECT 
        empresa,
        COUNT(id_oferta) AS numero_puestos,
        SUM(cvs_inscritos) AS total_candidatos,
        SUM(cvs_inscritos) AS candidatos_por_puesto
    FROM ofertas
    GROUP BY empresa
    ORDER BY numero_puestos DESC
    LIMIT 10;
    """

    df = pd.read_sql(consulta, db)
    df = df[df["empresa"] != "nuestra política al respecto"]

    st.title("Relación entre Candidatos y Puestos por Empresa")

    fig = px.bar(df,
                x="total_candidatos",
                y="empresa",
                orientation="h",
                color="numero_puestos",
                title="Relación entre candidatos y puestos por empresa",
                labels={
                    "total_candidatos": "Total candidatos inscritos",
                    "empresa": "",
                    "numero_puestos": "Número de puestos"
                })

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        coloraxis_colorbar=dict(
            title="Puestos ofertados", 
            title_side="top"
        )
    )

    st.plotly_chart(fig)

    st.write("El análisis de competitividad laboral revela una marcada disparidad en las oportunidades de acceso: "
    "Michel Page, líder en oferta con 620 vacantes, presenta un ratio de 1,4% de éxito (44.285 candidatos),"
    " mientras que en el extremo inferior (168 vacantes/4.058 candidatos) la probabilidad alcanza el 4,14%, cuadruplicando las opciones."
    " Estos datos evidencian mayor presión selectiva en empresas con amplia oferta frente a mercados nicho con menor competencia,"
    " subrayando la necesidad de estrategias diferenciadoras para candidatos y políticas de contratación basadas en datos.")

    st.write("-------------------------------------------------------------------------------------------------------------------------------------")
    config = toml.load(".streamlit/secrets.toml")
    db_config = config["database"]

    db = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"])

    # Crear un cursor
    cursor = db.cursor()

    # Consulta SQL
    query = "SELECT * FROM ofertas"

    # Cargar datos en un DataFrame usando el cursor
    df = pd.read_sql(query, db)

    # Cerrar la conexión
    cursor.close()
    db.close()

    with st.expander(label = "Despliega todas las ofertas", expanded = False):
        st.dataframe(df)
   
@st.cache_data
def load_data():
    config = toml.load(".streamlit/secrets.toml")
    db_config = config["database"]

    db = mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"])

    # Consulta SQL
    query = "SELECT * FROM ofertas"

    # Cargar los datos en un DataFrame
    df = pd.read_sql(query, db)

    # Cerrar la conexión a la base de datos
    db.close()

    # Almacenar el DataFrame en session_state para que sea accesible en toda la aplicación
    st.session_state.df = df

# Llamar a la función load_data() para cargar los datos en session_state cuando se inicia la app
if "df" not in st.session_state:
    load_data()

# Ahora puedes acceder a st.session_state.df en cualquier parte de tu app, por ejemplo:
def busqueda():
    # Asegurarse de que df_filtrado y selected_jobs estén inicializados
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

    # Cuando se envía el formulario, filtrar los resultados
    if submit_button:
        # Asegurarse de que df está cargado
        if "df" not in st.session_state or st.session_state.df.empty:
            st.write("No hay datos disponibles para filtrar.")
            return
        
        # Filtrar df según la búsqueda
        st.session_state.df_filtrado = st.session_state.df[
            (st.session_state.df["titulo"].str.lower().str.contains(job_title, na=False)) &
            (st.session_state.df["ciudad"].str.lower().str.contains(location, na=False)) &
            (st.session_state.df["empresa"].str.lower().str.contains(company, na=False)) &
            (st.session_state.df["salario_desde"] >= salario_desde) &
            (st.session_state.df["salario_hasta"] <= salario_hasta)
        ]

        # Mostrar resultados
        st.write(f"Resultados para: {job_title} {location} {company} entre {salario_desde}K y {salario_hasta}K/€")
        
        if not st.session_state.df_filtrado.empty:
            st.dataframe(st.session_state.df_filtrado)
        else:
            st.write("No se encontraron resultados.")

    # Aquí puedes continuar con la lógica de trabajo seleccionados y gráficos (como antes)
    if "titulo" not in st.session_state.df_filtrado.columns:
        st.write("")  # Evita error si no hay datos filtrados
    else:
        selected_jobs = [
            job for job in st.session_state.selected_jobs if job in st.session_state.df_filtrado["titulo"].tolist()
        ]

        # Selección múltiple para comparar trabajos
        selected_jobs = st.multiselect(
            "Selecciona trabajos para comparar", 
            st.session_state.df_filtrado["titulo"].tolist(), 
            default=selected_jobs, 
            format_func=lambda x: f"💼 {x}"
        )

        # Actualizar trabajos seleccionados
        if selected_jobs != st.session_state.selected_jobs:
            st.session_state.selected_jobs = selected_jobs

        # Filtrar los trabajos seleccionados y mostrar gráficos
        if selected_jobs:
            df_selected = st.session_state.df_filtrado[st.session_state.df_filtrado["titulo"].isin(selected_jobs)]

            # Comparación de salarios con Plotly
            import plotly.express as px
            custom_colors = ["#FFA500", "#FFFFFF"]
            fig = px.bar(df_selected, 
                        x="titulo", 
                        y=["salario_desde", "salario_hasta"], 
                        title="Comparación de Salarios de los Trabajos Seleccionados",
                        labels={"titulo": "Trabajo", "salario_desde": "Salario Mínimo", "salario_hasta": "Salario Máximo"},
                        barmode="group",
                        color_discrete_sequence=custom_colors)
            st.plotly_chart(fig, use_container_width=True)

    


def informacion_pbi():
    ##Titulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>INFORMACION ADICIONAL CON PBI 📊</h1>
        <h3>Conoce mejor tu futuro empleo</h3>
        <p style="font-size: 18px;">
            - Navega comodamente en la interfaz y encuentra el empleo mas adecuado para tí -
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    powerbi_width = 600
    powerbi_height = 373.5
    st.markdown(
        body=f"""
        <iframe title="Proyecto Final" width="1400" height="850" 
        src="https://app.powerbi.com/view?r=eyJrIjoiOWQ5NzJkZWEtZjAwZS00MDY4LThhMmUtNDg3ZDJhODFkYTI0IiwidCI6IjVlNzNkZTM1LWU4MjUtNGVkNS1iZTIyLTg4NTYzNTI3MDkxZSIsImMiOjl9&pageName=2c80c0101e4ee066730c" 
        frameborder="0" allowFullScreen="true"></iframe>
        """,
        unsafe_allow_html=True
    )
def clustering_clasificacion():
    ##Titulos
    st.markdown(
    """
    <div style="text-align: center;">
        <h1>CLUSTERING Y CLASIFICACIÓN 🌐</h1>
        <h3>Conoce mejor tu futuro empleo</h3>
        <p style="font-size: 18px;">
            - Navega comodamente en la interfaz y encuentra el empleo mas adecuado para tí -
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    # Cargar los DataFrames
    df_general_cluster = pd.read_csv("Streamlit/Data/df_imputado_final_clusterizado.csv")
    df_cluster = pd.read_csv("Streamlit/Data/df_clusters.csv")
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
        df_general_cluster["Cluster"] = df_general_cluster["Cluster"].astype("category")
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
    if st.button("Mostrar comparación de medidas por Cluster"):
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
        <h1>ARQUITECTURA SQL ⛁</h1>
        <h3>Así se ha estructurado nuestros datos</h3>
        <p style="font-size: 18px;">
            - Conoce la relación de nuestros datos para la extracción de información -
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    
    st.write("---------------------------------------------")
    
    st.image("Streamlit/Data/DIAGRAMA_SQL.png", width=900)

    st.write("-----------------------------------------------")

    st.write("En nuestra base de datos SQL, las relaciones conectan tablas entre sí. Las relaciones más comunes son: uno a uno, uno a muchos y muchos a muchos. Las claves primarias identifican de manera única los registros, mientras que las claves foráneas vinculan tablas relacionadas. Las relaciones permiten realizar consultas complejas usando JOIN para combinar datos de varias tablas. Este enfoque garantiza la integridad y eficiencia de la base de datos.")
    

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
            <img src="https://i.imgur.com/eLBwCXj.jpeg" class="circle-img">
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
                font-size: 50px;
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
                <p class="main-title">Luis Martínez de la Riva Doallo</p>
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
            <img src="https://media.licdn.com/dms/image/v2/D5603AQEK5WIc8prgEQ/profile-displayphoto-shrink_200_200/B56ZV_TsohHoAY-/0/1741597625372?e=1747267200&v=beta&t=1EHrFoRLCBGPFJ2I3P_n3JYhXf9wDBs1LAfTYzuXUrQ" class="circle-img">
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

    st.write("----------------------------------------------")


    # URL del repositorio
    repo_url = "https://github.com/LiamGVillar/PFB-Empleo"

    # URL de la imagen del logo de GitHub
    github_logo_url = "https://pngimg.com/d/github_PNG71.png"

    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
            <a href="{}" target="_blank">
                <button style="border: none; background: transparent; cursor: pointer;">
                    <img src="{}" alt="GitHub Logo" style="width: 100px; height: 100px;"/>
                </button>
            </a>
            <p style="text-align: center; font-size: 16px; color: #440;">Visita nuestro repositorio de GitHub</p>
        </div>
    """.format(repo_url, github_logo_url), unsafe_allow_html=True)



    st.write("---------------------------------------------------")
    st.write("Somos un equipo apasionado por la innovación y el análisis de datos, comprometido con ofrecer soluciones tecnológicas que faciliten la toma de decisiones informadas. Nuestra misión es proporcionar herramientas intuitivas y poderosas que permitan a nuestros usuarios explorar, comprender y utilizar los datos de manera eficiente. Con un enfoque en la simplicidad y la eficacia, nos esforzamos por crear experiencias que transformen la forma en que las personas interactúan con la información, impulsando el éxito tanto en el ámbito profesional como personal.")


def predictor ():
    
    st.title("Calculadora de Salario para Creación de Ofertas de Empleo")

    # Agregamos un identificador a la caja de contraseña
    password = st.text_input("Introduce la contraseña:", type="password", key="password_input_1")
    correct_password = "faltalogaritmo_siu"

    if password != correct_password:
        if password:  # Solo muestra el error si el usuario ha intentado introducir una contraseña
            st.error(":x: Acceso restringido a usuarios registrados. Contacta con soporte para crear tu cuenta profesional.")
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

    df_general = pd.read_csv("Streamlit/Data/df_imputado.csv")
    objects_loaded = joblib.load("Streamlit/Data/transformadores_y_modelo_regresion_salario.pkl")
    encoder, scaler, imputer, model = objects_loaded["encoder"], objects_loaded["scaler"], objects_loaded["imputer"], objects_loaded["model"]

    # Subtítulo de la sección
    st.subheader("Introduce los datos de la oferta que deseas publicar para comprobar el salario estimado según nuestra base de datos.")

    # Dividimos la página en tres columnas
    col1, col2, col3 = st.columns(3)

    with col1:
        ciudad = st.selectbox(
            "Ciudad",
            ["Madrid", "100% Remoto", "Barcelona", "Valencia", "Málaga", "Bizkaia", "Zaragoza", "A Coruña", "Sevilla", "Gipuzkoa", "No Especificado", "Alicante", "Valladolid", "Pontevedra", "Navarra", "Asturias", "Castellón", "Álava", "Girona", "Baleares", "Cantabria", "La Rioja", "Córdoba"],
            key="ciudad_selectbox"
        )
        jornada_tipo = st.selectbox(
            "Tipo de jornada laboral",
            ["Jornada Completa", "Media Jornada", "Flexible", "Intensiva Mañana", "Turno Rotatorio"],
            key="jornada_tipo_selectbox"
        )
        experiencia = st.slider(
            "Experiencia requerida (años)",
            0, 10, 1,
            key="experiencia_slider"
        )

    with col2:
        funciones = st.selectbox(
            "Funciones:",
            ["Programador", "Consultor", "Analista Programador", "Ingenieros/Industria", "Big Data", "Jefe de Proyecto", "Ciberseguridad", "Analista", "Técnico de Sistemas", "Arquitecto TIC", "Desarrollador Web", "Marketing", "DevOps", "Administrador", "Soporte Técnico", "Tester", "Redes", "Jefe de Equipo", "Electrónica", "Helpdesk", "Desarrollador Móvil", "Base de Datos/DBA", "Inteligencia Artificial/Machine Learning", "Diseño gráfico", "Sistemas de Calidad", "Técnico de Gestión", "Responsable de Producto", "Comercial", "Auditor", "I+D"],
            key="funciones_selectbox"
        )
        contrato_tipo = st.selectbox(
            "Tipo de contrato",
            ["Indefinido", "Temporal", "Prácticas", "Freelance/Autónomo"],
            key="contrato_tipo_selectbox"
        )
        nivel_profesional = st.selectbox(
            "Nivel profesional",
            ["Empleado", "Especialista", "Mando Intermedio", "Director"],
            key="nivel_profesional_selectbox"
        )

    with col3:
        formacion_minima = st.selectbox(
            "Formación mínima requerida:",
            ["FP2/Grado Superior", "Grado Medio", "Ingeniero Técnico", "Sin estudios", "Grado EEES (Bolonia)", "E.S.O. (Educación Secundaria Obligatoria)", "Ingeniero Superior", "FP1", "Licenciado", "Bachillerato/COU", "Postgrado EEES (Máster)", "Diplomado", "Otros títulos, certificaciones y carnets", "Certificado de Profesionalidad", "Otra Formación Tecnológica", "Doctorado"],
            key="formacion_minima_selectbox"
        )
        idioma = st.selectbox(
            "Idiomas requeridos:",
            ["--","Inglés", "Español", "Catalán", "Francés", "Alemán", "Italiano", "Euskera", "Noruego"],
            key="idioma_selectbox"
        )
        teletrabajo = st.selectbox(
            "Teletrabajo",
            ["Presencial", "Híbrido", "Remoto"],
            key="teletrabajo_selectbox"
        )

    # Añadir tecnología y habilidades en la parte de abajo
    tecnologias = st.multiselect(
        "Tecnologías requeridas:",
        ["sap ewm", "python", "sql", "AWS", "JavaScript", "Python", "peoplesoft", "Docker", "aws", "React"],
        key="tecnologias_multiselect"
    )
    habilidades = st.multiselect(
        "Habilidades requeridas:",
        ["Programador", "Proactividad", "Trabajo en equipo", "Aprendizaje Continuo", "Capacidad de autogestión"],
        key="habilidades_multiselect"
    )

    # Continuar con la lógica para predecir el salario y demás funcionalidades
    vacaciones_moda = df_general["vacaciones"].mode()[0]
    # Crear el dataframe de entrada del usuario
    user_input = pd.DataFrame({
        "variable": [0],
        "vacaciones": [vacaciones_moda],
        "teletrabajo": [teletrabajo],
        "jornada_tipo": [jornada_tipo],
        "funciones": [funciones],
        "contrato_tipo": [contrato_tipo],
        "nivel_profesional": [nivel_profesional],
        "formacion_minima": [formacion_minima],
        "personas_a_cargo": [0],
        "experiencia": [experiencia],
        "idioma": [-1 if idioma == "Ningún idioma" else idioma],  # Asignar -1 si no se selecciona ningún idioma
        "ciudad": [ciudad]
    }, index=[0])
    # Añadimos tecnologías y habilidades
    for tech in ["sap ewm", "python", "sql", "AWS", "JavaScript", "Python", "peoplesoft", "Docker", "aws", "React"]:
        user_input[tech] = 1 if tech in tecnologias else 0
    for habilidad in ["Programador", "Proactividad", "Trabajo en equipo", "Aprendizaje Continuo", "Capacidad de autogestión"]:
        user_input[habilidad] = 1 if habilidad in habilidades else 0
    #encoder
    for column in encoder.keys():
        if column in user_input.columns:
            if isinstance(encoder[column], dict):  # Si es un mapeo de categorías
                user_input[column] = user_input[column].map(encoder[column])
            elif encoder[column] is not None:  # Si hay un valor específico (como la moda de "vacaciones")
                user_input[column] = encoder[column]
    expected_columns = scaler.feature_names_in_
    missing_columns = [col for col in expected_columns if col not in user_input.columns]
    for col in missing_columns:
        user_input[col] = 0  # Añadir columnas faltantes con valores por defecto
    user_input = user_input[expected_columns]
    #scaler
    user_input_scaled = scaler.transform(user_input)
    #imputer
    user_input_imputed = imputer.transform(user_input_scaled)
    user_input_imputed = np.delete(user_input_imputed, 0, axis=1) #eliminamos la columna salario, generada aleatoriamente, para poder usar el modelo.
    # Predicción
    if st.button("Predecir Salario"):
        salario_predicho = model.predict(user_input_imputed)
        # Desescalar salario
        salario_min = scaler.data_min_[0]  # Valor mínimo del scaler para la primera característica
        salario_max = scaler.data_max_[0]  # Valor máximo del scaler para la primera característica
        salario_range = salario_max - salario_min
        # Escala inversa:
        # Desescalamos usando la fórmula inversa de MinMaxScaler
        salario_predicho_desescalado = salario_predicho * salario_range + salario_min
        mensaje_placeholder = st.empty()  # Espacio reservado para el mensaje
        for i in range(5):  # Repite 4 veces la animación (puedes ajustar)
            puntos = "." * i
            mensaje_placeholder.write(f"⌛: Calculando el salario adecuado según los parámetros{puntos}")
            time.sleep(1)  # Pequeña pausa para el efecto
        # Mostrar el resultado final
        mensaje_placeholder.write(f"✅: La estimación del salario para una oferta con las características introducidas es: {salario_predicho_desescalado[0] * 1000:,.0f} €")



with open("Streamlit/Data/dbscan_model.pkl", "rb") as f:
    dbscan = pickle.load(f)

def predecir_cluster():

    st.markdown("<h1 style='text-align: center;'>Calculadora de Cluster para Creación de Ofertas de Empleo</h1>", unsafe_allow_html=True)
    # Agregamos un identificador a la caja de contraseña
    password = st.text_input("Introduce la contraseña:", type="password", key="password_input")
    correct_password = "faltalogaritmo_siu"
    if password != correct_password:
        if password:  # Solo muestra el error si el usuario ha intentado introducir una contraseña
            st.error(":x: Acceso restringido a usuarios registrados. Contacta con soporte para crear tu cuenta profesional.")
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
    df_general = pd.read_csv("Streamlit/Data/df_imputado_final.csv")
    with open("Streamlit/Data/encoder_clustering.pkl", "rb") as f:
        encoder = dill.load(f)
    with open("Streamlit/Data/scaler_clustering.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("Streamlit/Data/imputer_clustering.pkl", "rb") as f:
        imputer = pickle.load(f)
    with open("Streamlit/Data/modelo_regresion_clustering.pkl", "rb") as f:
        model = pickle.load(f)
    st.markdown(
    "<h1 style='text-align: center; font-size: 22px;'>Introduce los datos de la oferta que deseas publicar para saber a qué cluster pertenece</h1>", 
    unsafe_allow_html=True)
    # Crear columnas para los sliders
    col1, col2 = st.columns(2)
    with col1:
        salario_media = st.slider(
            "Salario anual",
            0, 154000, 40000,  # Rango de 0 a 154000, valor inicial 40000
            key="salario_media_slider"
        )
    with col2:
        experiencia = st.slider(
            "Experiencia requerida (años)",
            0, 10, 1,  # Rango de 0 a 10, valor inicial 1
            key="experiencia_slider"
        )
    # Crear columnas para los select boxes y multiselects
    col3, col4, col5 = st.columns(3)
    with col3:
        teletrabajo = st.selectbox(
            "Teletrabajo",
            ["Presencial", "Híbrido", "Remoto"],
            key="teletrabajo_selectbox"
        )
        ciudad = st.selectbox(
            "Ciudad",
            ["Madrid", "100% Remoto", "Barcelona", "Valencia", "Málaga", "Bizkaia", "Zaragoza", "A Coruña", "Sevilla", "Gipuzkoa", "No Especificado", "Alicante", "Valladolid", "Pontevedra", "Navarra", "Asturias", "Castellón", "Álava", "Girona", "Baleares", "Cantabria", "La Rioja", "Córdoba"],
            key="ciudad_selectbox"
        )
        tecnologias = st.multiselect(
            "Tecnologías requeridas:",
            ["sap ewm", "python", "sql", "AWS", "JavaScript", "Python", "peoplesoft", "Docker", "aws", "React"],
            key="tecnologias_multiselect"
        )
    with col4:
        jornada_tipo = st.selectbox(
            "Tipo de jornada laboral",
            ["Jornada Completa", "Media Jornada", "Flexible", "Intensiva Mañana", "Turno Rotatorio"],
            key="jornada_tipo_selectbox"
        )
        funciones = st.selectbox(
            "Funciones:",
            ["Programador", "Consultor", "Analista Programador", "Ingenieros/Industria", "Big Data", "Jefe de Proyecto", "Ciberseguridad", "Analista", "Técnico de Sistemas", "Arquitecto TIC", "Desarrollador Web", "Marketing", "DevOps", "Administrador", "Soporte Técnico", "Tester", "Redes", "Jefe de Equipo", "Electrónica", "Helpdesk", "Desarrollador Móvil", "Base de Datos/DBA", "Inteligencia Artificial/Machine Learning", "Diseño gráfico", "Sistemas de Calidad", "Técnico de Gestión", "Responsable de Producto", "Comercial", "Auditor", "I+D"],
            key="funciones_selectbox"
        )
        habilidades = st.multiselect(
            "Habilidades requeridas:",
            ["Programador", "Proactividad", "Trabajo en equipo", "Aprendizaje Continuo", "Capacidad de autogestión"],
            key="habilidades_multiselect"
        )
    with col5:
        contrato_tipo = st.selectbox(
            "Tipo de contrato",
            ["Indefinido", "Temporal", "Prácticas", "Freelance/Autónomo"],
            key="contrato_tipo_selectbox"
        )
        nivel_profesional = st.selectbox(
            "Nivel profesional",
            ["Empleado", "Especialista", "Mando Intermedio", "Director"],
            key="nivel_profesional_selectbox"
        )
        formacion_minima = st.selectbox(
            "Formación mínima requerida:",
            ["FP2/Grado Superior", "Grado Medio", "Ingeniero Técnico", "Sin estudios", "Grado EEES (Bolonia)", "E.S.O. (Educación Secundaria Obligatoria)", "Ingeniero Superior", "FP1", "Licenciado", "Bachillerato/COU", "Postgrado EEES (Máster)", "Diplomado", "Otros títulos, certificaciones y carnets", "Certificado de Profesionalidad", "Otra Formación Tecnológica", "Doctorado"],
            key="formacion_minima_selectbox"
        )
    # Crear el dataframe de entrada del usuario
    user_input = pd.DataFrame({
        "salario_media": [salario_media // 1000],
        "experiencia": [experiencia],
        "teletrabajo": [teletrabajo],
        "ciudad": [ciudad],
        "jornada_tipo": [jornada_tipo],
        "funciones": [funciones],
        "contrato_tipo": [contrato_tipo],
        "nivel_profesional": [nivel_profesional],
        "formacion_minima": [formacion_minima],
        "num_tecnologias": [len(tecnologias)],  # Contar el número de tecnologías seleccionadas
        "num_habilidades": [len(habilidades)]   # Contar el número de habilidades seleccionadas
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
    if st.button("Predecir Cluster"):
        cluster_predicho = model.predict(user_input_imputed)
        st.success(f"El cluster predicho es: {cluster_predicho[0]}")
        if cluster_predicho[0] == 0:
            st.write("Representa la mayor parte del mercado laboral IT, con roles técnicos operativos y de soporte, generalmente a jornada completa y con salarios más bajos. Es el punto de entrada ideal para profesionales junior o aquellos que buscan estabilidad en funciones generales de IT.")
        elif cluster_predicho[0] == 1:
            st.write("Se enfoca en perfiles altamente especializados con salarios más altos y una fuerte presencia del teletrabajo. Es el más atractivo para profesionales con experiencia en desarrollo de software, ciberseguridad o consultoría IT.")
        elif cluster_predicho[0] == 2:
            st.write("Comprende roles críticos de infraestructura IT con disponibilidad 24/7, demandando experiencia avanzada. Aunque menos frecuente, es esencial en sectores que requieren supervisión constante, como telecomunicaciones, finanzas y salud.")





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
if "page" not in st.session_state:
    st.session_state.page = "🏠"


pages = {
    "🏠" : pagina_principal,
    "Muestra de datos" : muestra_datos,
    "Busqueda empleos" : busqueda,
    "Informacion PBI" : informacion_pbi,
    "Clustering y Clasificación" : clustering_clasificacion,
    "Arquitectura de SQL" : arquitectura_sql,
    "About us" : about_us,
    "Calculadora de salario 💎" : predictor,
    "Calculadora de cluster 💎" : predecir_cluster
}

if st.session_state.page not in pages.keys():
    st.session_state.page = "🏠"


manfredimg = Image.open("Streamlit/Data/manfred.png")
tecnoempleoimg = Image.open("Streamlit/Data/tecnoempleo.png")

st.sidebar.image("https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", use_container_width=True)

# Función para convertir imagen a base64
def img_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Mostrar imágenes dentro de columnas con enlaces
col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown(
    f'<a href="{manfred_url}" target="_blank">'
    f'<img src="data:image/png;base64,{img_to_base64(manfredimg)}" width="100%"></a>',
    unsafe_allow_html=True
)

# Enlace y mostrar imagen para la columna 2 (Tecnoempleo)
with col2:
    st.markdown(
        f'<a href="{tecnoempleo_url}" target="_blank">'
        f'<img src="data:image/png;base64,{img_to_base64(tecnoempleoimg)}" width="100%"></a>',
        unsafe_allow_html=True)


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

# Botón "Predecir" (Calculadora de salario)
st.sidebar.markdown("<p style='color: black;'>Opción disponible para usuarios Premium</p>", unsafe_allow_html=True)
if st.sidebar.button("Calculadora de salario 💎"):
    st.session_state.page = "Calculadora de salario 💎"  # Actualiza la página para mostrar la predicción
    st.rerun()  # Refresca la app para que se actualicen los cambios

# Botón "Predecir" (Calculadora de cluster)
if st.sidebar.button("Calculadora de cluster 💎"):
    st.session_state.page = "Calculadora de cluster 💎"  # Actualiza la página para mostrar la predicción
    st.rerun()  # Refresca la app para que se actualicen los cambios



st.sidebar.markdown("<br>" * 9, unsafe_allow_html=True)
st.sidebar.markdown(
    "<p style='color: black;'>App en versión de pruebas</p>",
    unsafe_allow_html=True
)