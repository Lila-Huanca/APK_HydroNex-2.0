import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuración inicial
UBIDOTS_TOKEN = "BBUS-2uhNhBDqzsn7DaMmvLAHb18bNt8yFe"
VARIABLES = {
    "pH": "67375fe260cea2000b34d149",
    "Turbidez": "6737603ddea6c6000c3367c9",
    "Conductividad": "6737603276021b000b240924"
}

@st.cache_data(ttl=300)
def fetch_and_calibrate(variable_name, variable_id, token, slope, intercept):
    """Obtiene y calibra datos de una variable."""
    url = f"https://stem.ubidots.com/app/dashboards/6668d2444d59830886a44331"
    headers = {"X-Auth-Token": token}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()["results"]
        df = pd.DataFrame([{
            "Fecha": pd.to_datetime(item["timestamp"], unit='ms'),
            "Valor": item["value"]
        } for item in data])
        df["Calibrado"] = df["Valor"] * slope + intercept
        return df
    except Exception as e:
        st.error(f"Error al obtener datos de {variable_name}: {e}")
        return pd.DataFrame()

# Configuración de la aplicación
st.set_page_config(page_title="Monitoreo HydroNex", page_icon="💧", layout="wide")
st.title("📊 Monitoreo y Calibración de Sensores - HydroNex")

# Ajustes de calibración
with st.sidebar:
    st.header("Ajustes de Calibración")
    st.write("Configura la pendiente y el offset para cada sensor:")
    
    calibration_params = {
        "pH": {
            "slope": st.number_input("Pendiente (pH)", 0.0, 5.0, 1.02, 0.01),
            "intercept": st.number_input("Offset (pH)", -5.0, 5.0, -0.05, 0.01)
        },
        "Turbidez": {
            "slope": st.number_input("Pendiente (Turbidez)", 0.0, 5.0, 0.98, 0.01),
            "intercept": st.number_input("Offset (Turbidez)", -5.0, 5.0, 1.2, 0.01)
        },
        "Conductividad": {
            "slope": st.number_input("Pendiente (Conductividad)", 0.0, 5.0, 1.05, 0.01),
            "intercept": st.number_input("Offset (Conductividad)", -5.0, 5.0, -0.3, 0.01)
        }
    }

# Cargar y calibrar datos
st.spinner("Cargando y calibrando datos desde Ubidots...")
sensor_data = {}
for sensor, ids in VARIABLES.items():
    params = calibration_params[sensor]
    sensor_data[sensor] = fetch_and_calibrate(sensor, ids, UBIDOTS_TOKEN, params["slope"], params["intercept"])

# Verificar datos cargados
if any(df.empty for df in sensor_data.values()):
    st.error("No se pudieron cargar los datos de todos los sensores. Verifica las configuraciones.")
else:
    st.success("✅ Datos cargados y calibrados exitosamente.")

    # Visualización de datos
    st.subheader("📈 Visualización de Sensores")
    for sensor, df in sensor_data.items():
        st.write(f"### {sensor}")
        if not df.empty:
            st.line_chart(df.set_index("Fecha")["Calibrado"])

    # Exportar datos
    export_data = pd.concat(sensor_data.values(), keys=sensor_data.keys(), names=["Sensor", "Index"]).reset_index()
    st.download_button(
        label="📥 Descargar datos calibrados (CSV)",
        data=export_data.to_csv(index=False),
        file_name="calibrated_data.csv",
        mime="text/csv"
    )
