"""Shared utilities: CSS injection, model loading, formatting helpers."""
import streamlit as st
import joblib

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MODEL_PATH, SEED_TYPES, COLOR_PRIMARY, COLOR_WARNING, COLOR_DANGER


def inject_custom_css():
    """Inject the dark-theme CSS used across all pages."""
    st.markdown("""<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
    }
    [data-testid="stMetricValue"] {
        font-size: 40px;
        color: #00ff87;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #b2bec3;
        font-size: 18px;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.8);
        border-right: 1px solid #34495e;
    }
    h1, h2, h3 {
        color: #00ff87 !important;
        font-family: 'Inter', sans-serif;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(0, 255, 135, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
    }
    .stAlert {
        background-color: rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(0, 255, 135, 0.3) !important;
        color: #ecf0f1 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        color: #b2bec3;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 255, 135, 0.15) !important;
        color: #00ff87 !important;
    }
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 255, 135, 0.1);
        border-radius: 10px;
    }
    </style>""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained surrogate pipeline model. Returns model or None."""
    try:
        model = joblib.load(str(MODEL_PATH))
        return model
    except FileNotFoundError:
        return None


def get_status_label(stability, seed_type_key="wheat"):
    """Return (status_text, status_color) based on seed-type-specific thresholds."""
    thresholds = SEED_TYPES[seed_type_key]["stability_thresholds"]
    if stability > thresholds["optimal"]:
        return "OPTIMAL", COLOR_PRIMARY
    elif stability > thresholds["degraded"]:
        return "DEGRADED", COLOR_WARNING
    else:
        return "CRITICAL", COLOR_DANGER


def init_session_state():
    """Initialize session state keys used across pages."""
    defaults = {
        "prediction_history": [],
        "selected_seed_type": "wheat",
        "comparison_mode": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def check_model_available():
    """Check if model is loaded, show error and stop if not."""
    model = load_model()
    if model is None:
        st.error("Model not found. Please run the training pipeline first:")
        st.code(
            "python -c \"from src.data_simulator import generate_scientific_data; generate_scientific_data()\"\n"
            "python -c \"from src.surrogate_model import train_surrogate; train_surrogate()\"",
            language="bash",
        )
        st.stop()
    return model


def make_transparent_plotly_layout(**overrides):
    """Return common Plotly layout kwargs for dark transparent backgrounds.

    Any keyword arguments override the defaults (e.g. margin, font, height).
    """
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#b2bec3", family="Inter, Arial, sans-serif"),
        margin=dict(l=40, r=40, t=50, b=30),
    )
    base.update(overrides)
    return base
