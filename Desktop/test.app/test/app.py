"""Seed Digital Twin - Multi-page Streamlit Application."""
import streamlit as st

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils import inject_custom_css, init_session_state

st.set_page_config(
    page_title="Seed Digital Twin | Agriculture 4.0",
    page_icon="🌱",
    layout="wide",
)

inject_custom_css()
init_session_state()

# --- Research Productivity ---
agribot = st.Page("pages/6_agribot.py", title="AgriBot Assistant", icon="🤖")
disease = st.Page("pages/7_disease_detection.py", title="Disease Detective", icon="🔬")

# --- Crop Logistics ---
logistics = st.Page("pages/8_crop_logistics.py", title="Crop Logistics", icon="🚜")

# --- Urban Dynamics ---
urban = st.Page("pages/9_urban_planning.py", title="Urban Digital Twin", icon="🏙️")

pg = st.navigation(
    {
        "Material Mechanics (Flagship)": [dashboard, batch, sensitivity],
        "Research Productivity": [agribot, disease],
        "Urban Dynamics": [urban],
        "Crop Logistics": [logistics],
        "Reference": [seed_db, model_perf],
    }
)
pg.run()
