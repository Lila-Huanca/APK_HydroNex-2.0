import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Initialize session state
def init_session_state():
    session_defaults = {
        "informes": [],
        "calidad del agua": [],
        "suministro de agua": [],
        "estado de hydronex": "en proceso de llenado",  # Default status
        "condición de hydronex": "apto",               # Default condition
        "historial de Hydronex": [80, 90, 85, 100]     # Sample history of filling status
    }
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Load data from URL with fallback
def load_from_url(url, fallback_data=None):
    try:
        return pd.read_csv(url)
    except Exception as e:
        if fallback_data is not None:
            return fallback_data
        return pd.DataFrame()

# Page configuration
st.set_page_config(page_title="HydroNex", page_icon="💧")
init_session_state()

# Sidebar menu
menu_options = ["Hydro-Bot", "Monitoreo", "Reportes", "Conciencia Comunitaria"]
choice = st.sidebar.selectbox("Menu", menu_options)

# Fallback data for demo purposes
fallback_water_quality = pd.DataFrame({
    "Fecha": ["2024-11-01", "2024-11-02", "2024-11-03"],
    "pH": [7.2, 7.1, 7.3],
    "Contaminantes (mg/L)": [10, 15, 12]
})

fallback_water_supply = pd.DataFrame({
    "Fecha": ["2024-11-01", "2024-11-02", "2024-11-03"],
    "Litros Distribuidos": [1200, 1100, 1300],
    "Zonas Abastecidas": ["Zona 1, Zona 2", "Zona 1", "Zona 2, Zona 3"]
})

# Load data only when needed
if choice == "Monitoreo":
    # Load water quality data
    water_quality_url = "https://example.com/water_quality.csv"
    water_quality_data = load_from_url(water_quality_url, fallback_water_quality)

    # Load water supply data
    water_supply_url = "https://example.com/water_supply.csv"
    water_supply_data = load_from_url(water_supply_url, fallback_water_supply)

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

# Other menu options
if choice == "Hydro-Bot":
    st.title("Hydro-Bot")
    st.write("Hola! Te damos la bienvenida a tu chatbot 'Hydro-Bot'. Puedes consultar el estado de tu dispositivo HydroNex aquí.")

if choice == "Reportes":
    st.title("Water Issue Reports")
    report_type = st.selectbox("Type of report", ["Contamination", "Lack of supply", "Other"])
    description = st.text_area("Problem description")
    
    if st.button("Submit Report"):
        if description:
            st.session_state["informes"].append((report_type, description))
            st.success("Your report has been submitted.")
        else:
            st.error("Please provide a description of the problem.")

    if st.session_state["informes"]:
        st.subheader("Submitted Reports")
        for report in st.session_state["informes"]:
            st.write(f"- {report[0]}: {report[1]}")

if choice == "Conciencia Comunitaria":
    st.title("Conciencia del agua")
    st.write("Promoviendo el uso eficiente del agua en María del Triunfo.")
