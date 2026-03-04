"""Batch Prediction - Upload CSV and get bulk stability predictions."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SEED_TYPES, NUMERICAL_FEATURES
from src.utils import check_model_available, get_status_label, make_transparent_plotly_layout

model = check_model_available()

st.title("📁 Batch Prediction")
st.markdown("Upload a CSV file to predict structural stability for multiple conditions at once.")

# ── Template Download ─────────────────────────────────────────────
st.subheader("1. Download Template")
st.write("Use this template CSV as a starting point. Fill in your data and upload below.")

template_df = pd.DataFrame({
    "seed_type": ["wheat", "rice", "corn", "soybean"],
    "relative_humidity_pct": [55.0, 70.0, 80.0, 60.0],
    "temperature_c": [15.0, 25.0, 35.0, 20.0],
    "mechanical_loading_kpa": [100.0, 200.0, 350.0, 150.0],
    "storage_duration_days": [180.0, 365.0, 730.0, 90.0],
    "initial_moisture_pct": [11.0, 13.0, 18.0, 10.0],
})

csv_template = template_df.to_csv(index=False)
st.download_button(
    "Download Template CSV",
    data=csv_template,
    file_name="batch_prediction_template.csv",
    mime="text/csv",
)

with st.expander("Column Descriptions"):
    st.markdown("""
| Column | Type | Range | Required |
|--------|------|-------|----------|
| `seed_type` | text | wheat, rice, corn, soybean, sunflower, barley | Yes |
| `relative_humidity_pct` | float | 30 - 95 | Yes |
| `temperature_c` | float | 5 - 45 | Yes |
| `mechanical_loading_kpa` | float | 50 - 500 | Yes |
| `storage_duration_days` | float | 0 - 3650 | Optional (default: 180) |
| `initial_moisture_pct` | float | 5 - 25 | Optional (default: 12) |
""")

# ── File Upload ───────────────────────────────────────────────────
st.divider()
st.subheader("2. Upload Your Data")
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded is not None:
    try:
        df = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
        st.stop()

    # Validate required columns
    required = ["seed_type", "relative_humidity_pct", "temperature_c", "mechanical_loading_kpa"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()

    # Fill optional columns
    if "storage_duration_days" not in df.columns:
        df["storage_duration_days"] = 180.0
    if "initial_moisture_pct" not in df.columns:
        df["initial_moisture_pct"] = 12.0

    # Validate seed types
    valid_types = set(SEED_TYPES.keys())
    invalid = set(df["seed_type"].unique()) - valid_types
    if invalid:
        st.error(f"Invalid seed types: {invalid}. Valid types: {valid_types}")
        st.stop()

    st.success(f"Loaded {len(df)} rows successfully.")

    # ── Run Predictions ───────────────────────────────────────────
    st.divider()
    st.subheader("3. Results")

    with st.spinner(f"Predicting {len(df)} samples..."):
        feature_cols = NUMERICAL_FEATURES + ["seed_type"]
        preds = model.predict(df[feature_cols])
        preds = np.clip(preds, 0, 1)
        df["predicted_stability"] = preds
        df["stability_pct"] = (preds * 100).round(2)
        df["status"] = df.apply(
            lambda r: get_status_label(r["predicted_stability"], r["seed_type"])[0], axis=1
        )

    # Summary metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Mean Stability", f"{preds.mean():.1%}")
    with c2:
        st.metric("Min Stability", f"{preds.min():.1%}")
    with c3:
        st.metric("Max Stability", f"{preds.max():.1%}")
    with c4:
        critical_count = (df["status"] == "CRITICAL").sum()
        st.metric("Critical Samples", f"{critical_count}")

    # Results table
    st.dataframe(
        df.style.background_gradient(subset=["stability_pct"], cmap="RdYlGn", vmin=0, vmax=100),
        use_container_width=True,
        hide_index=True,
    )

    # Distribution chart
    col_hist, col_box = st.columns(2)
    layout = make_transparent_plotly_layout()

    with col_hist:
        fig = px.histogram(
            df, x="stability_pct", color="seed_type", nbins=30,
            title="Stability Distribution",
            labels={"stability_pct": "Stability (%)"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig.update_layout(**layout, height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_box:
        fig_box = px.box(
            df, x="seed_type", y="stability_pct", color="seed_type",
            title="Stability by Seed Type",
            labels={"stability_pct": "Stability (%)", "seed_type": "Seed Type"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_box.update_layout(**layout, height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    # Download results
    st.divider()
    result_csv = df.to_csv(index=False)
    st.download_button(
        "Download Results CSV",
        data=result_csv,
        file_name="batch_predictions_results.csv",
        mime="text/csv",
    )
