import streamlit as st
import pandas as pd
from openai import OpenAI
from pydantic import BaseModel


client = OpenAI(api_key=st.secrets["openai_api_key"])

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


class Recommendations(BaseModel):
    product: str
    reasons: list[str]

class RecommendationList(BaseModel):
    recommendationList: list[Recommendations]

    
def generate_response(products_data, calendar_data):
    # Convertir los DataFrames a string
    products_data_str = products_data.to_string(index=False)
    calendar_data_str = calendar_data.to_string(index=False)

    # Crear el prompt usando los datos de los CSV
    prompt = f"""
    Tengo los siguientes productos con sus ventas mensuales:
    {products_data_str}

    También tengo las siguientes fechas señaladas:
    {calendar_data_str}

    Por favor, dame 3 recomendaciones de productos para vender en estas fechas a partir de los datos proporcionados:
    """

    # Llamada a la API de OpenAI usando el modelo GPT
    response = client.beta.chat.completions.parse(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], response_format=RecommendationList)
    return response.choices[0].message.parsed



if products_file is not None and calendar_file is not None:
    if st.button("¡Recomiéndame!"):
        with st.spinner('Generando recomendaciones...'):  # Añade el spinner de carga
            recommendation_response = generate_response(products_data, calendar_data)
        st.subheader("Productos recomendados")
    

        cols = st.columns(len(recommendation_response.recommendationList))  # Crear columnas dinámicamente

        for i, rec in enumerate(recommendation_response.recommendationList):
            with cols[i]:
                st.markdown(f"""
                    <div style="
                        border: 2px solid #8B0000; 
                        padding: 15px; 
                        border-radius: 10px; 
                        margin-bottom: 20px; 
                        text-align: left;
                        min-height: 300px;  /* Altura mínima para los cuadros */
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;">
                        <h4>{rec.product}</h4>
                        <ul>
                            <li>{rec.reasons[0]}</li>
                            <li>{rec.reasons[1]}</li>
                            <li>{rec.reasons[2]}</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
