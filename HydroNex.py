import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time  # Para medir el tiempo de ejecución

# Token de Ubidots
UBIDOTS_TOKEN = "BBUS-2uhNhBDqzsn7DaMmvLAHb18bNt8yFe"

# IDs de variables de Ubidots (reemplaza con tus IDs reales)
VARIABLES = {
    "pH": "ID_VARIABLE_PH",  # Reemplaza con el ID de tu variable pH
    "Turbidez": "ID_VARIABLE_TURBIDEZ",  # Reemplaza con el ID de turbidez
    "Conductividad": "ID_VARIABLE_CONDUCTIVIDAD"  # Reemplaza con el ID de conductividad
}

# Función para extraer datos desde Ubidots
@st.cache_data(ttl=300)
def fetch_ubidots_data(variable_id, token):
    """Extrae datos desde Ubidots y devuelve un DataFrame."""
    url = f"https://industrial.api.ubidots.com/api/v1.6/variables/{variable_id}/values"
    headers = {"X-Auth-Token": token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()["results"]
        return pd.DataFrame([{
            "Fecha": pd.to_datetime(item["timestamp"], unit='ms'),
            "Valor": item["value"]
        } for item in data])
    except Exception as e:
        st.error(f"Error al obtener datos de Ubidots: {e}")
        return pd.DataFrame()

# Función para calibrar datos
def calibrate_data(df, slope, intercept):
    """Calibra los datos aplicando pendiente y offset."""
    return df["Valor"] * slope + intercept

# Configuración de Streamlit
st.set_page_config(page_title="Monitoreo HydroNex", page_icon="💧", layout="wide")

# Título de la aplicación
st.title("📊 Monitoreo y Calibración de Sensores - HydroNex")
st.write("Aplicación para monitorear y calibrar sensores de calidad del agua.")

# Cargar datos desde Ubidots
with st.spinner("Cargando datos desde Ubidots..."):
    ph_data = fetch_ubidots_data(VARIABLES["pH"], UBIDOTS_TOKEN)
    turbidez_data = fetch_ubidots_data(VARIABLES["Turbidez"], UBIDOTS_TOKEN)
    conductividad_data = fetch_ubidots_data(VARIABLES["Conductividad"], UBIDOTS_TOKEN)

# Verificar si los datos fueron cargados
if ph_data.empty or turbidez_data.empty or conductividad_data.empty:
    st.error("No se pudieron cargar los datos. Revisa las IDs de las variables y el token.")
else:
    st.success("✅ Datos cargados exitosamente.")

    # Parámetros dinámicos para calibración
    with st.sidebar:
        st.header("Ajustes de Calibración")
        slope_ph = st.number_input("Pendiente (pH)", min_value=0.0, max_value=5.0, value=1.02, step=0.01)
        intercept_ph = st.number_input("Offset (pH)", min_value=-5.0, max_value=5.0, value=-0.05, step=0.01)
        
        slope_turbidez = st.number_input("Pendiente (Turbidez)", min_value=0.0, max_value=5.0, value=0.98, step=0.01)
        intercept_turbidez = st.number_input("Offset (Turbidez)", min_value=-5.0, max_value=5.0, value=1.2, step=0.01)
        
        slope_conductividad = st.number_input("Pendiente (Conductividad)", min_value=0.0, max_value=5.0, value=1.05, step=0.01)
        intercept_conductividad = st.number_input("Offset (Conductividad)", min_value=-5.0, max_value=5.0, value=-0.3, step=0.01)

    # Calibrar los datos
    ph_data["Calibrado"] = calibrate_data(ph_data, slope_ph, intercept_ph)
    turbidez_data["Calibrado"] = calibrate_data(turbidez_data, slope_turbidez, intercept_turbidez)
    conductividad_data["Calibrado"] = calibrate_data(conductividad_data, slope_conductividad, intercept_conductividad)

    # Mostrar los datos calibrados en un expander
    with st.expander("📄 Ver Datos Calibrados"):
        st.subheader("Datos Calibrados de pH")
        st.dataframe(ph_data)
        
        st.subheader("Datos Calibrados de Turbidez")
        st.dataframe(turbidez_data)
        
        st.subheader("Datos Calibrados de Conductividad")
        st.dataframe(conductividad_data)

    # Gráficas interactivas
    st.subheader("📈 Gráficas de Sensores Calibrados")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### pH")
        st.line_chart(ph_data.set_index("Fecha")["Calibrado"])

    with col2:
        st.write("### Turbidez")
        st.line_chart(turbidez_data.set_index("Fecha")["Calibrado"])

    with col3:
        st.write("### Conductividad")
        st.line_chart(conductividad_data.set_index("Fecha")["Calibrado"])

    # Exportar datos calibrados
    st.download_button(
        label="📥 Descargar datos calibrados (CSV)",
        data=pd.concat([ph_data, turbidez_data, conductividad_data], axis=0).to_csv(index=False),
        file_name="calibrated_data.csv",
        mime="text/csv"
    )
