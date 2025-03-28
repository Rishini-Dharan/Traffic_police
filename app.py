import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load dataset
@st.cache_data
def load_data():
    file_path = "data/chennai_traffic_data_final.csv"  # Ensure correct file path
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Streamlit App
st.title("🚦 Traffic & Weather Monitoring System")
st.sidebar.header("Filter Options")

# User selects filtering options
traffic_filter = st.sidebar.multiselect("Select Traffic Density:", df["Traffic Density"].unique(), default=df["Traffic Density"].unique())
weather_filter = st.sidebar.multiselect("Select Weather Condition:", df["Weather Condition"].unique(), default=df["Weather Condition"].unique())

# Filter data
df_filtered = df[df["Traffic Density"].isin(traffic_filter) & df["Weather Condition"].isin(weather_filter)]

# Create Folium Map
chennai_map = folium.Map(location=[13.0827, 80.2707], zoom_start=12)
marker_cluster = MarkerCluster().add_to(chennai_map)

# Define traffic color mapping
traffic_colors = {"Low": "green", "Medium": "orange", "High": "red"}

for _, row in df_filtered.iterrows():
    location = row["Location"]
    traffic_status = row["Traffic Density"]
    weather = row["Weather Condition"]
    temperature = row["Temperature (°C)"]
    delay = row["Estimated Delay (Minutes)"]
    lat, lon = row["Latitude"], row["Longitude"]
    
    popup_info = f"""
    <b>Location:</b> {location}<br>
    <b>Traffic:</b> {traffic_status}<br>
    <b>Weather:</b> {weather}<br>
    <b>Temperature:</b> {temperature}°C<br>
    <b>Delay:</b> {delay} mins
    """
    
    folium.Marker(
        location=[lat, lon],
        popup=popup_info,
        tooltip=location,
        icon=folium.Icon(color=traffic_colors.get(traffic_status, "gray"), icon="info-sign")
    ).add_to(marker_cluster)

st.subheader("📍 Traffic & Weather Map")
folium_static(chennai_map)

# Display filtered data
st.subheader("📊 Traffic Data Table")
st.dataframe(df_filtered)
