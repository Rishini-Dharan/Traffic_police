import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import datetime
import random

# Load Dataset
@st.cache_data
def load_data():
    file_path = "data/chennai_traffic_data_final.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Streamlit Title
st.title("🚦 Chennai Traffic & Weather Live Map")

# Display Data Preview
st.sidebar.header("📂 Dataset Preview")
st.sidebar.write(df.head())

# Get Current Time
current_time = datetime.datetime.now()
next_hour_time = current_time + datetime.timedelta(hours=1)

# Function to Predict Traffic and Weather for Next Hour
def predict_traffic(traffic_now):
    return random.choice(["Low", "Medium", "High"]) if traffic_now == "High" else traffic_now

def predict_weather(weather_now):
    return random.choice(["Sunny", "Cloudy", "Rainy", "Foggy", "Stormy"])

df["Predicted Traffic"] = df["Traffic Density"].apply(predict_traffic)
df["Predicted Weather"] = df["Weather Condition"].apply(predict_weather)

# Initialize Map
chennai_map = folium.Map(location=[13.0827, 80.2707], zoom_start=12, tiles="CartoDB Positron")

# Add Traffic Data to Map
for _, row in df.iterrows():
    risk_level = "🔴 High Risk" if row["Traffic Density"] == "High" else ("🟠 Medium Risk" if row["Traffic Density"] == "Medium" else "🟢 Low Risk")
    alt_route = "✅ Available" if row["Alternate Route Available"] == "Yes" else "❌ Not Available"
    
    popup_text = f"""
    <b>Location:</b> {row['Location']}<br>
    <b>Current Time:</b> {current_time.strftime("%Y-%m-%d %H:%M:%S")}<br>
    <b>Traffic:</b> {row['Traffic Density']}<br>
    <b>Weather:</b> {row['Weather Condition']}<br>
    <b>Temperature:</b> {row['Temperature (°C)']}°C<br>
    <b>Risk Level:</b> {risk_level}<br>
    <b>Estimated Delay:</b> ⏳ {row['Estimated Delay (Minutes)']} min<br>
    <b>📌 Predicted Traffic (Next Hour):</b> {row['Predicted Traffic']}<br>
    <b>📌 Predicted Weather (Next Hour):</b> {row['Predicted Weather']}<br>
    <b>Alternate Route:</b> {alt_route}
    """
    
    marker_color = "red" if row["Traffic Density"] == "High" else ("orange" if row["Traffic Density"] == "Medium" else "green")
    
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_text,
        icon=folium.Icon(color=marker_color)
    ).add_to(chennai_map)

# Display Map
folium_static(chennai_map)

# Summary of High Traffic Areas
high_traffic_summary = df[df["Traffic Density"] == "High"][["Location", "Estimated Delay (Minutes)"]].groupby("Location").mean().reset_index()
st.write("### 🚦 High Traffic Areas & Estimated Delays")
st.write(high_traffic_summary)
