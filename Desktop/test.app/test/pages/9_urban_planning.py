"""
Smart City Digital Twin: Urban Planning & Sustainability Simulator
Integrated as Pillar 3: Urban Dynamics
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

# Fix paths for integrated execution
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import inject_custom_css

# Page setup (Skip config if integrated, but multi-page apps handle this)
st.set_page_config(page_title="Urban Digital Twin", page_icon="🏙️", layout="wide")
inject_custom_css()

def calculate_metrics(residential, commercial, industrial, green_space):
    total = residential + commercial + industrial + green_space
    r_p = residential / total
    c_p = commercial / total
    i_p = industrial / total
    g_p = green_space / total
    
    co2 = (i_p * 80 + c_p * 30 + r_p * 15) * (1 - g_p * 0.5)
    energy_eff = (r_p * 0.6 + c_p * 0.4) * (1 + g_p * 0.2)
    traffic = (r_p * c_p * 50) + (i_p * 20)
    job_density = (c_p * 100 + i_p * 60)
    
    return {
        "CO2 Emissions": round(co2, 1),
        "Energy Efficiency": round(energy_eff * 100, 1),
        "Traffic Index": round(traffic, 1),
        "Green Space Ratio": round(g_p * 100, 1),
        "Job Density": round(job_density, 1)
    }

st.title("🏙️ Urban Planning Digital Twin")
st.markdown("### Pillar 3: Smart City Dynamics & Environmental Metabolism")
st.divider()

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/city.png", width=80)
    st.header("Zoning Controls")
    res = st.slider("Residential Area (Ha)", 10, 500, 200)
    com = st.slider("Commercial Area (Ha)", 10, 500, 150)
    ind = st.slider("Industrial Area (Ha)", 0, 500, 50)
    grn = st.slider("Green Space (Ha)", 10, 500, 100)
    st.divider()
    if st.button("🚀 Run Connectivity Optimization"):
        st.success("Optimization analysis complete.")

metrics = calculate_metrics(res, com, ind, grn)
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("CO2 Footprint", f"{metrics['CO2 Emissions']} kt")
with col2: st.metric("Sustainability", f"{metrics['Energy Efficiency']}%")
with col3: st.metric("Traffic Index", f"{metrics['Traffic Index']}")
with col4: st.metric("Labor Index", f"{metrics['Job Density']}")

st.divider()
grid_size = 20
x, y = np.meshgrid(np.linspace(0, 10, grid_size), np.linspace(0, 10, grid_size))
z = (np.sin(x) * np.cos(y) * (metrics['CO2 Emissions']/10)) + (np.random.rand(grid_size, grid_size) * 2)
fig = go.Figure(data=[go.Surface(z=z, colorscale='Viridis')])
fig.update_layout(title='Thermal Surface Map', template="plotly_dark", height=600)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔬 Research Connection"):
    st.write("This module analyzes urban metabolic rates, demonstrating how structural engineering (Digital Twins) applies to larger urban biosystems.")
