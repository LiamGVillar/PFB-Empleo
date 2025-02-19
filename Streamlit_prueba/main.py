import streamlit as st
from PIL import Image
import pandas as pd


st.set_page_config(page_title = "Empleos Extraccion", page_icon= "https://cdn.prod.website-files.com/5f3108520188e7588ef687b1/64e7429d8afae2bb6f5acd85_logo-hab-pez.svg", layout ="wide")

def pagina_principal():
    st.title("Bienvenido a la pagina de empleos de Hackaboss")
    st.subheader("Explora ofertas de empleo en España")
    st.write("Este es un proyecto donde podras hacer una busqueda de empleos publicados recientemente")


def muestra_datos():
    st.title("Datos y graficas")
    st.write("Aquí podras observar patrones en las ofertas de empleo seleccionadas")

    with st.expander(label = "DataFrame - Manfred", expanded = False):
         df = pd.read_csv(filepath_or_buffer = "/home/bosser/Documentos/PROYECTOFINAL/CSV/CSV_manfred/general_limpio.csv")
         st.dataframe(df) 

def busqueda():
    st.title("Buscar y comparar empleos")
    st.write("Aqui puedes hacer una busqueda y comparativa de los empleos extraidos")




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

manfredimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit/imagenes/manfred.png")
tecnoempleoimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit/imagenes/tecnoempleo.png")


# Crear dos columnas en el sidebar
col1, col2 = st.sidebar.columns(2)

# Mostrar las imágenes en las columnas
with col1:
    st.image(manfredimg, use_container_width=True)
with col2:
    st.image(tecnoempleoimg, use_container_width=True)

st.sidebar.title("Navegación")

if st.sidebar.button("🏠"):
    st.session_state.page = "🏠"

# Selector para navegar entre las demás páginas
st.session_state.page = st.sidebar.selectbox("Selecciona una vista", list(pages.keys()), index=list(pages.keys()).index(st.session_state.page))

pages[st.session_state.page]()