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
    st.markdown("""\
    | Topic                        | Example Question                                |
    |------------------------------|-------------------------------------------------|
    | Device Condition             | "Is the device in optimal condition?"          |
    | Filling Status               | "What is the current filling status?"         
