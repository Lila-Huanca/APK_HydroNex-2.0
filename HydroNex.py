import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process

# Initialize session state
def init_session_state():
    session_defaults = {
        "reports": [],
        "water_quality": [],
        "water_supply": [],
        "hydronex_status": "en proceso de llenado",  # Default status
        "hydronex_condition": "apto",               # Default condition
        "hydronex_history": [80, 90, 85, 100]       # Sample history of filling status
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Load data from URL
def load_from_url(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading data from {url}: {e}")
        return pd.DataFrame()

# Page configuration
st.set_page_config(page_title="HydroNex", page_icon="💧")
init_session_state()

# Sidebar menu
menu_options = ["Hydro-Bot", "Monitoreo", "Reportes", "Conciencia Comunitaria"]
choice = st.sidebar.selectbox("Menu", menu_options)

# Load sample data (replace URLs with actual data URLs)
water_quality_url = "https://example.com/water_quality.csv"
water_supply_url = "https://example.com/water_supply.csv"

water_quality_data = load_from_url(water_quality_url)
water_supply_data = load_from_url(water_supply_url)

# Sample data (for demonstration purposes; replace with real data)
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

# Water Supply Section
st.subheader("Water Supply")
if not water_supply_data.empty:
    st.write("Current water supply data:")
    st.dataframe(water_supply_data)
    
    # Plotting Distributed Water
    plt.figure(figsize=(10, 5))
    plt.plot(water_supply_data["Fecha"], water_supply_data["Litros Distribuidos"], marker='o', color='green')
    plt.title("Water Distribution in Liters")
    plt.xlabel("Fecha")
    plt.ylabel("Litros Distribuidos")
    st.pyplot(plt)
else:
    st.write("No data available on water supply.")

# Hydro-Bot
if choice == "Hydro-Bot":
    st.title("Hydro-Bot")
    st.write("Hello! Welcome to your chatbot 'Hydro-Bot'. You can check the status of your HydroNex device here.")

    # Suggested topics
    st.subheader("Suggested Topics to Ask:")
    st.markdown("""
    | Topic                        | Example Question                                |
    |------------------------------|-------------------------------------------------|
    | Device Condition             | "Is the device in optimal condition?"          |
    | Filling Status               | "What is the current filling status?"          |
    | Filling History              | "What is the filling history of the device?"   |
    | Accumulated Liters           | "How many liters are accumulated?"             |
    """)

    user_query = st.text_input("What would you like to know about your HydroNex?", "")

    if user_query:
        if "filling" in user_query.lower():
            st.write(f"Assistant: The device is currently {st.session_state['hydronex_status']}.")
        elif "condition" in user_query.lower():
            st.write("Assistant: The device is in optimal condition." if st.session_state["hydronex_condition"] == "apto" else "The device is in poor condition; consider reporting.")
        elif "liters" in user_query.lower():
            st.write("Assistant: The device is being monitored, and the accumulated liters are under observation.")
        elif "history" in user_query.lower():
            st.write("Assistant: The filling history is as follows:")
            st.write(st.session_state["hydronex_history"])
        else:
            st.write("Assistant: Sorry, I can't help with that question. Try asking about the device's condition, filling status, or filling history.")

# Monitoring page
if choice == "Monitoreo":
    st.title("Water Monitoring in María del Triunfo")

    # Water Quality Section
    st.subheader("Water Quality")
    if not water_quality_data.empty:
        st.write("Current water quality data:")
        st.dataframe(water_quality_data)
        
        # Plotting pH and Contaminants
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
        st.write("No data available on water quality.")

# Reports
if choice == "Reportes":
    st.title("Water Issue Reports")
    report_type = st.selectbox("Type of report", ["Contamination", "Lack of supply", "Other"])
    description = st.text_area("Problem description")
    
    if st.button("Submit Report"):
        if description:
            st.session_state["reports"].append((report_type, description))
            st.success("Your report has been submitted.")
        else:
            st.error("Please provide a description of the problem.")

    if st.session_state["reports"]:
        st.subheader("Submitted Reports")
        for report in st.session_state["reports"]:
            st.write(f"- {report[0]}: {report[1]}")

# Community Awareness
if choice == "Conciencia Comunitaria":
    st.title("Conciencia del agua")

    st.subheader("Efficient Water Usage Tips")
    st.write("""
        El agua es un recurso vital. A continuación, se indican algunas prácticas recomendadas:
        - Reparar fugas en grifos y tuberías.
        - Utilizar recipientes para regar las plantas.
        - Tomar duchas breves.
        - Recoger agua de lluvia para riego.
    """)

    st.subheader("Educación y recursos")
    st.write("""
        - **Talleres de conservación de agua**: Participe en nuestros talleres para aprender más sobre cómo conservar el agua en su hogar.
        - **Sesiones informativas**: Asista a nuestras sesiones para aprender más sobre la situación del agua en nuestra comunidad.
    """)

st.sidebar.markdown("### Contacto")
st.sidebar.write("Si tienes preguntas o comentarios, no dudes en contactarnos..")
