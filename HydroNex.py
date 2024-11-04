import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process

# Inicializar claves en session_state
def init_session_state():
    session_defaults = {
        "reports": [],
        "water_quality": [],
        "water_supply": [],
        "hydronex_status": "en proceso de llenado",  # Estado por defecto
        "hydronex_condition": "apto"  # Estado por defecto
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
menu_opciones = ["Monitoreo", "Hydro-Bot", "Reportes", "Conciencia Comunitaria"]
choice = st.sidebar.selectbox("Menú", menu_opciones)

# Cargar datos de calidad del agua y suministro (ejemplo de URLs)
water_quality_url = "https://example.com/water_quality.csv"
water_supply_url = "https://example.com/water_supply.csv"

water_quality_data = load_from_url(water_quality_url)
water_supply_data = load_from_url(water_supply_url)

# Ejemplo de datos (reemplazar con datos reales)
water_quality_data = pd.DataFrame({
    "Fecha": ["2024-11-01", "2024-11-02", "2024-11-03"],
    "pH": [7.2, 7.1, 7.3],
    "Contaminantes (mg/L)": [10, 15, 12]
})

water_supply_data = pd.DataFrame({
    "Fecha": ["2024-11-01", "2024-11-02", "2024-11-03"],
    "Litros Distribuidos": [1200, 1100, 1300],
    "Zonas Abastecidas": ["Zona 1, Zona 2", "Zona 1", "Zona 2, Zona 3"]
})

# Monitoreo de Agua en María del Triunfo
if choice == "Monitoreo":
    
    st.title("Monitoreo de Agua en María del Triunfo")
    
    # Calidad del Agua
    st.subheader("Calidad del Agua")
    if not water_quality_data.empty:
        st.write("Los datos actuales de calidad del agua son:")
        st.dataframe(water_quality_data)
        
        # Gráfico de pH y Contaminantes
        fig, ax1 = plt.subplots()
        
        ax1.set_xlabel("Fecha")
        ax1.set_ylabel("pH", color="tab:blue")
        ax1.plot(water_quality_data["Fecha"], water_quality_data["pH"], color="tab:blue", label="pH")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("Contaminantes (mg/L)", color="tab:red")
        ax2.plot(water_quality_data["Fecha"], water_quality_data["Contaminantes (mg/L)"], color="tab:red", label="Contaminantes")
        ax2.tick_params(axis="y", labelcolor="tab:red")
        
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No hay datos disponibles sobre la calidad del agua.")
    
    # Suministro de Agua
    st.subheader("Suministro de Agua")
    if not water_supply_data.empty:
        st.write("Los datos actuales de suministro de agua son:")
        st.dataframe(water_supply_data)
        
        # Gráfico de Litros Distribuidos
        plt.figure(figsize=(10, 5))
        plt.plot(water_supply_data["Fecha"], water_supply_data["Litros Distribuidos"], marker='o', color='green')
        plt.title("Distribución de Agua en Litros")
        plt.xlabel("Fecha")
        plt.ylabel("Litros Distribuidos")
        st.pyplot(plt)
    else:
        st.write("No hay datos disponibles sobre el suministro de agua.")

# Definir estado y condición de ejemplo del dispositivo HydroNex
st.session_state['hydronex_status'] = "lleno"
st.session_state['hydronex_condition'] = "apto"
st.session_state['hydronex_history'] = [80, 90, 85, 100]

# Hydro-Bot
st.title("Hydro-Bot")
st.write("¡Hola! Bienvenido a tu chat bot 'Hydro-Bot'. Aquí podrás consultar sobre el estado de tu dispositivo HydroNex.")

# Tabla de temas sugeridos
st.subheader("Temas sugeridos para preguntar:")
st.markdown("""
| Tema                         | Ejemplo de pregunta                                  |
|------------------------------|------------------------------------------------------|
| Condiciones del dispositivo  | "¿Está el dispositivo en condiciones óptimas?"       |
| Estado del llenado           | "¿Cuál es el estado actual del llenado?"             |
| Historial de llenado         | "¿Cuál es el historial de llenado del dispositivo?"  |
| Cantidad de litros           | "¿Cuántos litros tiene acumulados?"                  |
""")

# Entrada del usuario para Hydro-Bot
user_query = st.text_input("¿Qué deseas saber sobre tu HydroNex?", "")

# Respuesta según la consulta del usuario
if user_query:
    # Estado de llenado
    if "lleno" in user_query.lower():
        st.write(f"Asistente: Actualmente, el dispositivo se encuentra {st.session_state['hydronex_status']}.")
    
    # Condiciones del dispositivo
    elif "apto" in user_query.lower():
        if st.session_state["hydronex_condition"] == "apto":
            st.write("Asistente: El dispositivo se encuentra en condiciones óptimas para su uso.")
        else:
            st.write("Asistente: El dispositivo se encuentra en malas condiciones. Se sugiere reportar este acontecimiento.")
    
    # Cantidad de litros
    elif "cantidad" in user_query.lower() or "litros" in user_query.lower():
        st.write("Asistente: Actualmente, el dispositivo está en proceso de llenado y la cantidad de litros acumulados está en monitoreo.")
    
    # Historial de llenado
    elif "historial" in user_query.lower():
        st.write("Asistente: El historial de llenado del dispositivo es el siguiente:")
        st.write(st.session_state["hydronex_history"])
    
    # Respuesta predeterminada
    else:
        st.write("Asistente: Lo siento, no puedo ayudarte con esa consulta. Intenta preguntar sobre las condiciones del dispositivo, el estado del llenado o el historial de llenado.")

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
    st.write("""\
        El agua es un recurso vital. Aquí hay algunas prácticas recomendadas:
        - Repara fugas en grifos y tuberías.
        - Usa recipientes para regar las plantas.
        - Toma duchas cortas.
        - Recoge agua de lluvia para riego.
    """)
    
    st.subheader("Educación y Recursos")
    st.write("""\
        - **Talleres sobre conservación del agua**: Participa en nuestros talleres para aprender más sobre cómo conservar el agua en tu hogar.
        - **Charlas informativas**: Asiste a nuestras charlas para conocer más sobre la situación del agua en nuestra comunidad.
    """)

st.sidebar.markdown("### Contacto")
st.sidebar.write("Si tienes preguntas o comentarios, no dudes en contactarnos.")
