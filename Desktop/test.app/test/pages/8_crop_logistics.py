"""Crop Logistics - Yield Prediction & Smart Irrigation Advisor."""
import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.research_suite.ml_models import model_manager
from src.utils import inject_custom_css
from config import COLOR_PRIMARY, COLOR_WARNING

# Page config
st.set_page_config(page_title="Crop Logistics", page_icon="🚜", layout="wide")
inject_custom_css()

st.title("🚜 Crop Logistics Hub")
st.markdown("### Decision Support for Yield Optimization & Resource Management")
st.divider()

tab_yield, tab_irrigation = st.tabs(["🌾 Yield Prediction", "💧 Smart Irrigation"])

with tab_yield:
    st.subheader("Yield Optimization Analysis")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        crop = st.selectbox("Select Crop Type", ["Wheat", "Rice", "Maize", "Cotton", "Soybean", "Sugarcane", "Potato", "Tomato"])
        c1, c2 = st.columns(2)
        with c1:
            temp = st.slider("Target Temperature (°C)", 10.0, 45.0, 25.0, key="yield_temp")
            rain = st.slider("Expected Rainfall (mm)", 0.0, 1000.0, 450.0)
        with c2:
            ph = st.slider("Soil pH Level", 4.0, 10.0, 6.5)
            nitro = st.number_input("Nitrogen (N) kg/ha", 0, 500, 150)
            
        irr_type = st.radio("Irrigation Strategy", ["Flood", "Sprinkler", "Drip", "Rainfed"], horizontal=True)
        area = st.number_input("Cultivation Area (Hectares)", 0.1, 1000.0, 1.0)
        
        predict_btn = st.button("📊 Calculate Expected Yield", use_container_width=True)
        
    with col2:
        if predict_btn:
            with st.spinner("Analyzing multi-factor growth vectors..."):
                features = {
                    "crop": crop,
                    "temperature": temp,
                    "rainfall": rain,
                    "soil_ph": ph,
                    "nitrogen": nitro,
                    "irrigation_type": irr_type,
                    "farm_area_ha": area
                }
                res = model_manager.predict_yield(features)
                
                st.success("Analysis Complete")
                m1, m2 = st.columns(2)
                m1.metric("Predicted Yield", f"{res['prediction']} t/ha")
                m2.metric("Total Harvest", f"{res['details']['yield_per_hectare_tons'] * area:.1f} tons")
                
                st.write("**Operational Recommendations:**")
                for rec in res['details']['recommendations']:
                    st.info(f"👉 {rec}")
                    
                with st.expander("Physics-Informed Factors"):
                    st.json(res['details']['factors'])
        else:
            st.info("Adjust parameters and click 'Calculate' to see yield projections.")

with tab_irrigation:
    st.subheader("Smart Irrigation Advisor")
    col_i1, col_i2 = st.columns([1, 1])
    
    with col_i1:
        irr_crop = st.selectbox("Target Crop", ["Vegetables", "Rice", "Wheat", "Maize", "Cotton"], key="irr_crop_sel")
        moisture = st.slider("Current Soil Moisture (%)", 0, 100, 45)
        last_hours = st.number_input("Hours since last irrigation", 0, 168, 24)
        
        irr_btn = st.button("💧 Get Irrigation Advice", use_container_width=True)
        
    with col_i2:
        if irr_btn:
            i_features = {
                "crop": irr_crop,
                "soil_moisture": moisture,
                "temperature": 28.0, # Using standard temp for advisory
                "humidity": 60,
                "irrigation_type": "drip",
                "last_irrigation_hours": last_hours
            }
            i_res = model_manager.recommend_irrigation(i_features)
            
            st.markdown(f"### Strategy: **{i_res['prediction']}**")
            im1, im2 = st.columns(2)
            im1.metric("Water Budget", f"{i_res['details']['water_amount_mm']} mm")
            im2.metric("Optimal Timing", i_res['details']['best_time'])
            
            st.write("**Water Efficiency Protocol:**")
            for tip in i_res['details']['water_saving_tips']:
                st.success(f"✔️ {tip}")
        else:
            st.info("Input current soil moisture to generate a water management plan.")

st.divider()
st.subheader("Integration Note")
st.write(
    "The **Crop Logistics** module uses a rule-based inference engine to translate "
    "environmental data into actionable agricultural decisions. This complements the "
    "**Material Mechanics** lab by providing the 'Applied' perspective of the PhD project."
)
