import streamlit as st
import pandas as pd

st.set_page_config(page_title='vise',  layout='wide')

t1, t2 = st.columns((0.15,1)) 

t1.image('images/viselab_logo.jpeg', width = 140)
t2.title("Recomendador de productos para tu local")
t2.markdown("**| website:** https://viselab.io/")

col1, col2 = st.columns(2)

# Cargar CSV de productos y ventas
with col1:
    st.subheader("Sube tu CSV de productos y ventas")
    products_file = st.file_uploader("Selecciona un archivo CSV de productos y ventas", type=["csv"])

# Cargar CSV de calendario de fechas señaladas
with col2:
    st.subheader("Sube tu CSV de fechas señaladas")
    calendar_file = st.file_uploader("Selecciona un archivo CSV de fechas señaladas", type=["csv"])

# Crear una nueva fila para mostrar los datos cargados
st.subheader("Datos cargados")


col3, col4 = st.columns(2)

# Mostrar los datos cargados si existen
if products_file is not None:
    col3.write("Datos de productos y ventas:")
    products_data = pd.read_csv(products_file)
    col3.dataframe(products_data)

if calendar_file is not None:
    col4.write("Datos del calendario de fechas señaladas:")
    calendar_data = pd.read_csv(calendar_file)
    col4.dataframe(calendar_data)
