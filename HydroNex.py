import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process

# Helper function to initialize session state
def init_session_state():
    session_defaults = {
        "informes": [],
        "calidad del agua": [],
        "suministro de agua": [],
        "estado de hydronex": "desconectado",  # Cambio a "desconectado"
        "condición de hydronex": "desconocida",  # Cambio a "desconocida"
        "historial de Hydronex": [],
        "litros acumulados": 0,  # Litros acumulados iniciales
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Configure the page
st.set_page_config(page_title="HydroNex", page_icon="💧")

# Initialize session state
init_session_state()

# Menu options in the sidebar
menu_options = ["Hydro-Bot", "Monitoreo", "Reportes", "Conciencia Comunitaria"]
Choice = st.sidebar.selectbox("Menú", menu_options)

# Sample Data (Replace with real URLs for actual data)
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

# Hydronex Bot interaction
if Choice == "Hydro-Bot":
    st.title("Hydro-Bot")
    st.write("¡Hola! Bienvenido al chatbot 'Hydro-Bot'. Puedes consultar el estado de tu dispositivo HydroNex aquí.")
    st.subheader("Temas sugeridos para preguntar:")
    st.markdown("""
        - **Estado del dispositivo**: "¿Cuál es el estado de llenado actual?"
        - **Historial de llenado**: "¿Cuál es el historial de llenado del dispositivo?"
        - **Litros acumulados**: "¿Cuántos litros hay acumulados?"
    """)

    user_query = st.text_input("¿Qué te gustaría saber acerca de tu HydroNex?")
    
    if user_query:
        # Verificar el estado de conexión
        if st.session_state["estado de hydronex"] == "desconectado":
            st.write("Asistente: El dispositivo está desconectado. No puedo proporcionar información en este momento.")
        else:
            # Si el dispositivo está conectado, procesar las consultas como antes
            if "llenado" in user_query.lower():
                st.write(f"Asistente: El dispositivo actualmente está en {st.session_state['estado de hydronex']}.")
                # Simulate filling state change
                estados_llenado = ["en proceso de llenado", "a la mitad de la capacidad", "completamente lleno"]
                estado_actual = estados_llenado.index(st.session_state["estado de hydronex"])
                st.session_state["estado de hydronex"] = estados_llenado[(estado_actual + 1) % len(estados_llenado)]
            elif "condición" in user_query.lower():
                condicion = "óptimas" if st.session_state["condición de hydronex"] == "apto" else "malas"
                st.write(f"Asistente: El dispositivo está en condiciones {condicion}.")
            elif "historial" in user_query.lower():
                st.write("Asistente: El historial de llenado es el siguiente:")
                st.write(st.session_state["historial de Hydronex"])
            elif "litros acumulados" in user_query.lower():
                if st.session_state["litros acumulados"] == 0:
                    st.write("Asistente: Actualmente no tenemos litros acumulados. Por favor, espera un momento y vuelve a preguntar.")
                    st.session_state["litros acumulados"] = 150  # Simulate accumulation
                else:
                    st.write(f"Asistente: El dispositivo tiene {st.session_state['litros acumulados']} litros acumulados.")
            else:
                st.write("Asistente: Lo siento, no puedo responder esa pregunta. Intente preguntar sobre el estado, la condición o el historial del dispositivo.")

# Water Monitoring
elif Choice == "Monitoreo":
    st.title("Monitoreo del Agua en María del Triunfo")

    # Water Quality Monitoring
    st.subheader("Calidad del Agua")
    if not water_quality_data.empty:
        st.write("Datos actuales de calidad del agua:")
        st.dataframe(water_quality_data)

        # Plot pH and contaminants graph
        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Fecha")
        ax1.set_ylabel("pH", color="blue")
        ax1.plot(water_quality_data["Fecha"], water_quality_data["pH"], marker='o', color="blue", label="pH")
        ax1.tick_params(axis="y", labelcolor="blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("Contaminantes (mg/L)", color="red")
        ax2.plot(water_quality_data["Fecha"], water_quality_data["Contaminantes (mg/L)"], marker='o', color="red", label="Contaminantes")
        ax2.tick_params(axis="y", labelcolor="red")

        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.write("No hay datos disponibles sobre la calidad del agua.")

    # Water Supply Monitoring
    st.subheader("Suministro de Agua")
    if not water_supply_data.empty:
        st.write("Datos actuales del suministro de agua:")
        st.dataframe(water_supply_data)

        # Plot distribution graph
        plt.figure(figsize=(10, 5))
        plt.plot(water_supply_data["Fecha"], water_supply_data["Litros Distribuidos"], marker='o', color="green")
        plt.title("Distribución de Agua en Litros")
        plt.xlabel("Fecha")
        plt.ylabel("Litros Distribuidos")
        st.pyplot(plt)
    else:
        st.write("No hay datos disponibles sobre el suministro de agua.")

# Report Issues
elif Choice == "Reportes":
    st.title("Reportes de Problemas de Agua")
    report_type = st.selectbox("Tipo de reporte", ["Contaminación", "Falta de suministro", "Otro"])
    descripcion = st.text_area("Descripción del problema")
    
    if st.button("Enviar reporte"):
        if descripcion:
            st.session_state["informes"].append((report_type, descripcion))
            st.success("Su informe ha sido enviado.")
        else:
            st.error("Por favor, proporcione una descripción del problema.")
    
    if st.session_state["informes"]:
        st.subheader("Reportes enviados")
        for report in st.session_state["informes"]:
            st.write(f"- **{report[0]}**: {report[1]}")

# Community Awareness
elif Choice == "Conciencia Comunitaria":
    st.title("Conciencia del Agua")
    st.subheader("Consejos para el Uso Eficiente del Agua")
    st.write("""
        - Reparar fugas en grifos y tuberías.
        - Utilizar recipientes para regar las plantas.
        - Tomar duchas breves.
        - Recoger agua de lluvia para riego.
    """)

    st.subheader("Educación y Recursos")
    st.write("""
        - **Talleres de Conservación de Agua**: Aprende cómo conservar agua en tu hogar.
        - **Sesiones Informativas**: Participa en sesiones para conocer más sobre la situación del agua en la comunidad.
    """)
