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

if products_file is not None and calendar_file is not None:
    if st.button("¡Recomiéndame!"):
        st.subheader("Productos recomendados")

        # Lógica simple de recomendación (esto puede mejorarse con un algoritmo más sofisticado)
        recommendations = []
        
        # Ejemplo: recomendación basada en las ventas más altas en los últimos meses
        best_selling_products = products_data.iloc[:, -1].sort_values(ascending=False).head(3).index.tolist()
        for product in best_selling_products:
            reason = [
                "Es uno de los productos más vendidos en los últimos meses.",
                "Su margen de ganancia es alto.",
                "Tiene alta demanda en fechas específicas."
            ]
            product_name = products_data.iloc[product, 0]
            recommendations.append({"product": product_name, "reasons": reason})

        # Ejemplo: recomendación basada en fechas señaladas (si hay alguna festividad cercana)
        for _, row in calendar_data.iterrows():
            if 'Navidad' in row['Evento']:
                recommendations.append({
                    "product": "Productos navideños",
                    "reasons": [
                        f"Se acerca **{row['Evento']}** ({row['Fecha']}).",
                        "Los productos navideños suelen incrementar las ventas.",
                        "Los clientes buscan productos temáticos."
                    ]
                })

        # Mostrar las recomendaciones estilizadas
        cols = st.columns(len(recommendations))  # Crear columnas dinámicamente

        for i, rec in enumerate(recommendations):
            with cols[i]:
                st.markdown(f"""
                    <div style="border: 2px solid #8B0000; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: left;">
                        <h4>{rec['product']}</h4>
                        <ul>
                            <li>{rec['reasons'][0]}</li>
                            <li>{rec['reasons'][1]}</li>
                            <li>{rec['reasons'][2]}</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
