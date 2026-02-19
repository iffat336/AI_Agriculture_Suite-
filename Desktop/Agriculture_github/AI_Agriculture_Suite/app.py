import streamlit as st
import os
import sys
import pandas as pd
import numpy as np
from PIL import Image

# Add backend and models to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'models'))

from ml_models import model_manager
from chatbot import chatbot

# Set page config
st.set_page_config(
    page_title="AI Agriculture Suite",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4CAF50;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .metrics-container {
        display: flex;
        justify-content: space-between;
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/tractor.png", width=80)
    st.title("Admin Controls")
    
    st.info("System Status: Online 🟢")
    
    with st.expander("About"):
        st.write("""
        This AI Agriculture Suite provides tools for modern farming:
        - Yield Prediction
        - Disease Detection
        - Pest Risk Assessment
        - Irrigation Advice
        - Market Analysis
        """)
    
    st.write("---")
    st.caption("v1.0.0 | AI-Powered Farming")

# Main Header
st.markdown('<div class="main-header">🌾 AI Agriculture Suite</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home", 
    "📈 Crop Yield", 
    "🔬 Disease Detective", 
    "🐛 Pest Risk", 
    "💧 Smart Irrigation",
    "🤖 AgriBot"
])

# --- TAB 1: HOME ---
with tab1:
    st.markdown("### Welcome to Smart Farming")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🌡️ Weather Advisory")
        # Dummy weather data for now, could be integrated with API
        st.metric("Temperature", "28°C", "2°C")
        st.metric("Humidity", "65%", "-5%")
        st.caption("Condition: Partly Cloudy")
        
    with col2:
        st.success("### 📊 Market Trends")
        st.metric("Wheat", "₹2,250/q", "+₹50")
        st.metric("Rice", "₹3,400/q", "-₹20")
        st.caption("Updated: Today 09:00 AM")
        
    with col3:
        st.warning("### ⚠️ Alerts")
        st.write("• High pest risk in cotton belt")
        st.write("• Light rain expected tomorrow")
        st.write("• Fertilizer subsidy deadline approaching")

    st.markdown("---")
    st.markdown("### Quick Tips")
    
    tips = [
        "Check soil moisture before irrigating to save water.",
        "Rotate crops to maintain soil health.",
        "Monitor for pests early morning.",
        "Clean farm equipment to prevent disease spread."
    ]
    
    for tip in tips:
        st.info(f"💡 {tip}")

# --- TAB 2: CROP YIELD PREDICTION ---
with tab2:
    st.markdown('<div class="sub-header">📈 Crop Yield Predictor</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Maize", "Cotton", "Soybean", "Sugarcane", "Potato", "Tomato"])
        temperature = st.slider("Temperature (°C)", 0.0, 50.0, 25.0)
        rainfall = st.slider("Rainfall (mm)", 0.0, 1000.0, 150.0)
        soil_ph = st.slider("Soil pH", 4.0, 10.0, 6.5)
        
    with col2:
        nitrogen = st.number_input("Nitrogen (N)", 0.0, 500.0, 120.0)
        phosphorus = st.number_input("Phosphorus (P)", 0.0, 500.0, 60.0)
        potassium = st.number_input("Potassium (K)", 0.0, 500.0, 60.0)
        irrigation_type = st.selectbox("Irrigation Type", ["Flood", "Sprinkler", "Drip", "Rainfed"])
        area = st.number_input("Farm Area (Hectares)", 0.1, 1000.0, 1.0)

    if st.button("Predict Yield 🚜"):
        with st.spinner("Analyzing soil and climate data..."):
            features = {
                "crop": crop,
                "temperature": temperature,
                "rainfall": rainfall,
                "soil_ph": soil_ph,
                "nitrogen": nitrogen,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "irrigation_type": irrigation_type,
                "farm_area_ha": area
            }
            
            result = model_manager.predict_yield(features)
            
            st.success("Analysis Complete!")
            
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.metric("Predicted Yield (per ha)", f"{result['prediction']} tons/ha")
                st.metric("Total Expected Harvest", f"{result['details']['total_expected_yield_tons']} tons")
            
            with res_col2:
                st.write("### Recommendations")
                for rec in result['details']['recommendations']:
                    st.info(f"👉 {rec}")
                    
            with st.expander("View Detailed Factors"):
                st.json(result['details']['factors'])

# --- TAB 3: DISEASE DETECTION ---
with tab3:
    st.markdown('<div class="sub-header">🔬 Disease Detection</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Leaf Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Leaf", use_column_width=True)
            
        with col2:
            st.write("### AI Analysis")
            if st.button("Analyze Disease 🔍"):
                with st.spinner("Scanning for symptoms..."):
                    # Simulate features extract from image (in real app, use CV/CNN)
                    # Here passing dummy values to simulation model
                    features = {
                        "crop": "tomato", # Default/Detected
                        "leaf_color_g": 100, # Simulated
                        "spot_density": 0.6, # Simulated
                        "affected_area_pct": 25, # Simulated
                        "humidity": 75,
                        "temperature": 28
                    }
                    
                    result = model_manager.detect_disease(features)
                    
                    st.error(f"Detected: {result['prediction']}")
                    st.progress(result['confidence'])
                    st.caption(f"Confidence: {result['confidence']*100}%")
                    
                    st.write(f"**Severity:** {result['details']['severity_label']}")
                    st.write(f"**Treatment:** {result['details']['treatment']}")
                    
                    st.write("### Prevention Tips")
                    for tip in result['details']['prevention_tips']:
                        st.info(f"🛡️ {tip}")

# --- TAB 4: PEST RISK ---
with tab4:
    st.markdown('<div class="sub-header">🐛 Pest Risk Prediction</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        pest_crop = st.selectbox("Select Crop", ["General", "Cotton", "Maize", "Vegetables"], key="pest_crop")
        pest_temp = st.slider("Current Temperature (°C)", 10.0, 45.0, 28.0)
    
    with col2:
        pest_humidity = st.slider("Humidity (%)", 0, 100, 65)
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon", "Spring"])
        
    if st.button("Predict Pest Risk 🦟"):
        features = {
            "crop": pest_crop,
            "temperature": pest_temp,
            "humidity": pest_humidity,
            "season": season
        }
        
        result = model_manager.predict_pest(features)
        
        risk_level = result['prediction']
        color = "red" if risk_level == "High" else "orange" if risk_level == "Medium" else "green"
        
        st.markdown(f"<h3 style='color: {color}'>Risk Level: {risk_level}</h3>", unsafe_allow_html=True)
        st.write(f"**Highest Risk Pest:** {result['details']['highest_risk_pest']}")
        
        st.write("### Control Measures")
        for rec in result['details']['recommendations']:
            st.warning(f"⚠️ {rec}")
            
        with st.expander("View Risk Breakdown"):
            st.json(result['details']['all_pest_risks'])

# --- TAB 5: SMART IRRIGATION ---
with tab5:
    st.markdown('<div class="sub-header">💧 Smart Irrigation Advisor</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        irr_crop = st.selectbox("Crop", ["Vegetables", "Rice", "Wheat", "Maize", "Cotton"], key="irr_crop")
        soil_moisture = st.slider("Soil Moisture (%)", 0, 100, 45)
        
    with col2:
        last_irrigation = st.number_input("Hours since last irrigation", 0, 100, 24)
        irr_temp = st.slider("Temp (°C)", 10.0, 45.0, 30.0, key="irr_temp")
        
    if st.button("Get Advice 💧"):
        features = {
            "crop": irr_crop,
            "soil_moisture": soil_moisture,
            "temperature": irr_temp,
            "humidity": 60, # Default
            "irrigation_type": "flood",
            "last_irrigation_hours": last_irrigation
        }
        
        result = model_manager.recommend_irrigation(features)
        
        st.info(f"### Recommendation: {result['prediction']}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Water Needed", f"{result['details']['water_amount_mm']} mm")
        with col2:
            st.metric("Best Time", result['details']['best_time'])
            
        st.write("### Water Saving Tips")
        for tip in result['details']['water_saving_tips']:
            st.success(f"💧 {tip}")

# --- TAB 6: CHATBOT ---
with tab6:
    st.markdown('<div class="sub-header">🤖 AgriBot - AI Assistant</div>', unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me about crops, diseases, or prices..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get response
        with st.spinner("AgriBot is thinking..."):
            response_data = chatbot.chat(prompt)
            response = response_data['response']

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    with st.sidebar:
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            chatbot.clear_history()
            st.rerun()

