import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process

# Inicializar el estado de la sesión
def init_session_state():
    session_defaults = {
        "reports": [],
        "water_quality": [],
        "water_supply": [],
        "hydronex_status": "en proceso de llenado",  # Estado predeterminado
        "hydronex_condition": "apto",                 # Condición predeterminada
        "hydronex_history": [80, 90, 85, 100]         # Historial de llenado de muestra
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Cargar datos desde una URL
def load_from_url(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error al cargar datos desde {url}: {e}")
        return pd.DataFrame()

# Configuración de la página
st.set_page_config(page_title="HydroNex", page_icon="💧")
init_session_state()

# Menú lateral
menu_options = ["Hydro-Bot", "Monitoreo", "Reportes", "Conciencia Comunitaria"]
choice = st.sidebar.selectbox("Menú", menu_options)

# Cargar datos de ejemplo (reemplazar las URLs con las reales)
water_quality_url = "https://example.com/water_quality.csv"
water_supply_url = "https://example.com/water_supply.csv"

water_quality_data = load_from_url(water_quality_url)
water_supply_data = load_from_url(water_supply_url)

# Datos de muestra (para fines de demostración; reemplazar con datos reales)
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

# Sección de Suministro de Agua
if choice == "Monitoreo":
    st.title("Monitoreo de Agua en María del Triunfo")

    # Sección de Calidad del Agua
    st.subheader("Calidad del Agua")
    if not water_quality_data.empty:
        st.write("Datos actuales de calidad del agua:")
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

# Hydro-Bot
if choice == "Hydro-Bot":
    st.title("Hydro-Bot")
    st.write("¡Hola! Bienvenido a tu chatbot 'Hydro-Bot'. Aquí puedes verificar el estado de tu dispositivo HydroNex.")

    # Temas sugeridos
    st.subheader("Temas Sugeridos para Preguntar:")
    st.markdown("""\
    | Tema                        | Ejemplo de Pregunta                                |
    |-----------------------------|-----------------------------------------------------|
    | Condición del Dispositivo   | "¿Está el dispositivo en condiciones óptimas?"      |
    | Estado de Llenado           | "¿Cuál es el estado actual de llenado?"            |
    | Historial de Llenado        | "¿Cuál es el historial de llenado del dispositivo?" |
    | Litros Acumulados           | "¿Cuántos litros están acumulados?"                |
    """)

    user_query = st.text_input("¿Qué te gustaría saber sobre tu HydroNex?", "")

    if user_query:
        query = user_query.lower()
        if "llenado" in query:
            st.write(f"Asistente: El dispositivo está actualmente {st.session_state['hydronex_status']}.")
        elif "condición" in query:
            condition_response = "en condiciones óptimas." if st.session_state["hydronex_condition"] == "apto" else "en malas condiciones; considera reportarlo."
            st.write(f"Asistente: El dispositivo está {condition_response}")
        elif "litros" in query:
            st.write("Asistente: El dispositivo está siendo monitoreado y los litros acumulados están bajo observación.")
        elif "historial" in query:
            st.write("Asistente: El historial de llenado es el siguiente:")
            st.write(st.session_state["hydronex_history"])
        else:
            st.write("Asistente: Lo siento, no puedo ayudar con esa pregunta. Intenta preguntar sobre la condición del dispositivo, el estado de llenado o el historial de llenado.")

# Reportes
if choice == "Reportes":
    st.title("Reportes de Problemas de Agua")
    report_type = st.selectbox("Tipo de reporte", ["Contaminación", "Falta de suministro", "Otro"])
    description = st.text_area("Descripción del problema")
    
    if st.button("Enviar Reporte"):
        if description:
            st.session_state["reports"].append((report_type, description))
            st.success("Tu reporte ha sido enviado.")
        else:
            st.error("Por favor proporciona una descripción del problema.")

    if st.session_state["reports"]:
        st.subheader("Reportes Enviados")
        for report in st.session_state["reports"]:
            st.write(f"- {report[0]}: {report[1]}")

# Conciencia Comunitaria
if choice == "Conciencia Comunitaria":
    st.title("Conciencia sobre el Agua")

    st.subheader("Consejos para el Uso Eficiente del Agua")
    st.write("""\
        El agua es un recurso vital. Aquí hay algunas prácticas recomendadas:
        - Repara las fugas en grifos y tuberías.
        - Usa recipientes para regar las plantas.
        - Toma duchas cortas.
        - Recoge agua de lluvia para el riego.
    """)

    st.subheader("Educación y Recursos")
    st.write("""\
        - **Talleres de Conservación de Agua**: Participa en nuestros talleres para aprender más sobre cómo conservar agua en tu hogar.
        - **Sesiones Informativas**: Asiste a nuestras sesiones para aprender más sobre la situación del agua en nuestra comunidad.
    """)

st.sidebar.markdown("### Contacto")
st.sidebar.write("Si tienes preguntas o comentarios, no dudes en contactarnos.")

    """)

st.sidebar.markdown("### Contact")
st.sidebar.write("If you have questions or comments, feel free to contact us.")
