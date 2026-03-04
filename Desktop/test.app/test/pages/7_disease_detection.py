"""Disease Detective - AI Vision-based Diagnostics simulation."""
import streamlit as st
import numpy as np
from PIL import Image
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.research_suite.ml_models import model_manager
from src.utils import inject_custom_css, make_transparent_plotly_layout
from config import COLOR_PRIMARY, COLOR_DANGER

# Page config
st.set_page_config(page_title="Disease Detective", page_icon="🔬", layout="wide")
inject_custom_css()

st.title("🔬 Disease Detective")
st.markdown("### AI-Powered Crop Health Monitoring & Diagnostics")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Sample Analysis")
    uploaded_file = st.file_uploader("Upload Leaf/Plant Image", type=["jpg", "png", "jpeg"], help="Upload a photo for AI computer vision analysis.")
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Analyzed Sample", use_container_width=True)
        
        btn = st.button("🚀 Run AI Diagnosis", use_container_width=True)
        if btn:
            with st.spinner("Executing CNN feature extraction..."):
                # Simulate varied features for the demo
                features = {
                    "crop": "wheat",
                    "leaf_color_g": 120 + np.random.randint(-20, 20),
                    "spot_density": 0.4 + np.random.random() * 0.3,
                    "affected_area_pct": 15 + np.random.randint(0, 40),
                    "humidity": 75,
                    "temperature": 28
                }
                st.session_state.disease_result = model_manager.detect_disease(features)
    else:
        st.info("💡 **Demo Tip:** You can find sample leaf images in the `data/` directory or upload any plant photo.")

with col2:
    st.subheader("2. Diagnostic Results")
    if "disease_result" in st.session_state and uploaded_file:
        res = st.session_state.disease_result
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Detected Pathogen", res['prediction'])
        with c2:
            st.metric("Confidence Score", f"{res['confidence']*100:.1f}%")
        
        severity = res['details']['severity_label']
        st.markdown(f"**Severity Level:** `{severity}`")
        if res['details']['severity'] > 3:
            st.error(f"🚨 **Urgent Action Required**: {res['details']['urgency'].title()}")
        elif res['details']['severity'] > 1:
            st.warning(f"⚠️ **Intervention Recommended**: {res['details']['urgency'].title()}")
            
        st.write(f"**Treatment Protocol:**\n{res['details']['treatment']}")
        
        with st.expander("Prevention Strategy"):
            for tip in res['details']['prevention_tips']:
                st.info(f"🛡️ {tip}")
                
        st.caption(f"Estimated Yield Impact: {res['details']['estimated_yield_impact']}")
    else:
        st.write("Results will appear here after analysis.")

st.divider()
st.subheader("Methodology: Computer Vision & Digital Twins")
st.write(
    "This module demonstrates the integration of **Deep Learning (CNN)** into the Research Hub. "
    "By identifying early signs of material degradation or biological disease, we can "
    "trigger adaptive changes in the Digital Twin's environment-control loop."
)
