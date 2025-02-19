import streamlit as st
from PIL import Image


st.set_page_config(page_title = "ESTUDIO EMPLEOS", page_icon= "💻", layout = "wide")

st.sidebar.title("Empleos")

st.markdown(
    '<h1 style="color: black; background-color: yellow;">PRESENTACION DE EMPLEO</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<span style="color: yellow;">A continuacion podremos ver los datframes con informacion sobre las ofertas de empleo</span>',
    unsafe_allow_html=True
)

st.sidebar.success ("Escoge una sección")

manfredimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit/imagenes/manfred.png")
tecnoempleoimg = Image.open("/home/bosser/Documentos/PROYECTOFINAL/Streamlit/imagenes/tecnoempleo.png")

# Crear dos columnas en el sidebar
col1, col2 = st.sidebar.columns(2)

# Mostrar las imágenes en las columnas
with col1:
    st.image(manfredimg, use_container_width=True)
with col2:
    st.image(tecnoempleoimg, use_container_width=True)