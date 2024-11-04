import pandas as pd
import streamlit as st
from fuzzywuzzy import fuzz, process

# Inicializar claves en session_state
def init_session_state():
    session_defaults = {
        "reports": [],
        "water_quality": [],
        "water_supply": []
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Función para cargar datos desde URL de CSV
def load_from_url(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error al cargar los datos desde {url}: {e}")
        return pd.DataFrame()

# Configuración de la página
st.set_page_config(page_title="HydroNex", page_icon="💧")
init_session_state()

# Menú lateral
menu_opciones = ["Monitoreo", "Reportes", "Conciencia Comunitaria"]
choice = st.sidebar.selectbox("Menú", menu_opciones)

# Cargar datos de calidad del agua y suministro (ejemplo de URLs)
water_quality_url = "https://example.com/water_quality.csv"
water_supply_url = "https://example.com/water_supply.csv"

water_quality_data = load_from_url(water_quality_url)
water_supply_data = load_from_url(water_supply_url)

if choice == "Monitoreo":
    st.title("Monitoreo de Agua en María del Triunfo")
    
    # Visualizar calidad del agua
    st.subheader("Calidad del Agua")
    if not water_quality_data.empty:
        st.dataframe(water_quality_data)
    else:
        st.write("No hay datos disponibles sobre la calidad del agua.")
    
    # Visualizar suministro de agua
    st.subheader("Suministro de Agua")
    if not water_supply_data.empty:
        st.dataframe(water_supply_data)
    else:
        st.write("No hay datos disponibles sobre el suministro de agua.")

elif choice == "Reportes":
    st.title("Reportes de Problemas de Agua")
    
    report_type = st.selectbox("Tipo de reporte", ["Contaminación", "Falta de suministro", "Otro"])
    description = st.text_area("Descripción del problema")
    
    if st.button("Enviar Reporte"):
        if description:
            st.session_state["reports"].append((report_type, description))
            st.success("Tu reporte ha sido enviado.")
        else:
            st.error("Por favor, proporciona una descripción del problema.")

    if st.session_state["reports"]:
        st.subheader("Reportes Enviados")
        for report in st.session_state["reports"]:
            st.write(f"- {report[0]}: {report[1]}")

elif choice == "Conciencia Comunitaria":
    st.title("Conciencia sobre el Agua")
    
    st.subheader("Información sobre el uso eficiente del agua")
    st.write("""
        El agua es un recurso vital. Aquí hay algunas prácticas recomendadas:
        - Repara fugas en grifos y tuberías.
        - Usa recipientes para regar las plantas.
        - Toma duchas cortas.
        - Recoge agua de lluvia para riego.
    """)
    
    st.subheader("Educación y Recursos")
    st.write("""
        - **Talleres sobre conservación del agua**: Participa en nuestros talleres para aprender más sobre cómo conservar el agua en tu hogar.
        - **Charlas informativas**: Asiste a nuestras charlas para conocer más sobre la situación del agua en nuestra comunidad.
    """)

st.sidebar.markdown("### Contacto")
st.sidebar.write("Si tienes preguntas o comentarios, no dudes en contactarnos.")
