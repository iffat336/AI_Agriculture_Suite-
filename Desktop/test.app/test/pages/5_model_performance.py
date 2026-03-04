"""Model Performance - Diagnostics, metrics, and about section."""
import streamlit as st
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MODEL_DIR, DATA_DIR, SEED_TYPES, NUMERICAL_FEATURES, COLOR_PRIMARY
from src.utils import make_transparent_plotly_layout

st.title("📈 Model Performance & Diagnostics")

# ── Load Metrics ──────────────────────────────────────────────────
metrics_path = MODEL_DIR / "metrics.json"
test_pred_path = MODEL_DIR / "test_predictions.csv"
training_data_path = DATA_DIR / "simulated_fe_data.csv"

if not metrics_path.exists():
    st.error("Model metrics not found. Please train the model first.")
    st.stop()

with open(str(metrics_path)) as f:
    metrics = json.load(f)

# ── Metrics Cards ─────────────────────────────────────────────────
st.subheader("Model Accuracy Metrics")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("R² Score", f"{metrics['r2']:.4f}")
with c2:
    st.metric("RMSE", f"{metrics['rmse']:.4f}")
with c3:
    st.metric("MAE", f"{metrics['mae']:.4f}")
with c4:
    st.metric("Training Samples", f"{metrics['n_train']:,}")
with c5:
    st.metric("Test Samples", f"{metrics['n_test']:,}")

layout = make_transparent_plotly_layout()

# ── Actual vs Predicted ───────────────────────────────────────────
if test_pred_path.exists():
    st.divider()
    st.subheader("Actual vs Predicted")

    test_df = pd.read_csv(str(test_pred_path))

    col_scatter, col_residual = st.columns(2)

    with col_scatter:
        fig = px.scatter(
            test_df, x="y_actual", y="y_predicted",
            color="seed_type", opacity=0.6,
            labels={"y_actual": "Actual Stability", "y_predicted": "Predicted Stability"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        # Perfect prediction line
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1],
            mode="lines", line=dict(dash="dash", color="#b2bec3", width=2),
            name="Perfect Fit", showlegend=True,
        ))
        fig.update_layout(
            **layout, height=450,
            title="Actual vs Predicted Stability",
            legend=dict(bgcolor="rgba(0,0,0,0.3)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Residual Analysis ─────────────────────────────────────────
    with col_residual:
        test_df["residual"] = test_df["y_actual"] - test_df["y_predicted"]

        fig_res = px.histogram(
            test_df, x="residual", nbins=40, color="seed_type",
            labels={"residual": "Residual (Actual - Predicted)"},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_res.add_vline(x=0, line_dash="dash", line_color=COLOR_PRIMARY)
        fig_res.update_layout(
            **layout, height=450,
            title="Residual Distribution",
            legend=dict(bgcolor="rgba(0,0,0,0.3)"),
        )
        st.plotly_chart(fig_res, use_container_width=True)

    # ── Residuals vs Predicted ────────────────────────────────────
    st.subheader("Residuals vs Predicted (Heteroscedasticity Check)")
    fig_rp = px.scatter(
        test_df, x="y_predicted", y="residual",
        color="seed_type", opacity=0.5,
        labels={"y_predicted": "Predicted Stability", "residual": "Residual"},
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_rp.add_hline(y=0, line_dash="dash", line_color=COLOR_PRIMARY)
    fig_rp.update_layout(
        **layout, height=400,
        title="Residuals vs Predicted — should show no pattern",
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
    )
    st.plotly_chart(fig_rp, use_container_width=True)

    # ── Error by Seed Type ────────────────────────────────────────
    st.subheader("Error Metrics by Seed Type")
    error_by_type = []
    for stype in test_df["seed_type"].unique():
        mask = test_df["seed_type"] == stype
        sub = test_df[mask]
        error_by_type.append({
            "Seed Type": SEED_TYPES.get(stype, {}).get("name", stype),
            "Count": int(mask.sum()),
            "MAE": f"{(sub['y_actual'] - sub['y_predicted']).abs().mean():.4f}",
            "RMSE": f"{np.sqrt(((sub['y_actual'] - sub['y_predicted']) ** 2).mean()):.4f}",
            "Mean Residual": f"{sub['residual'].mean():.4f}",
        })
    st.dataframe(pd.DataFrame(error_by_type), use_container_width=True, hide_index=True)

# ── Training Data Distribution ────────────────────────────────────
if training_data_path.exists():
    st.divider()
    st.subheader("Training Data Distribution")

    train_df = pd.read_csv(str(training_data_path))

    # Feature histograms
    cols = st.columns(3)
    feature_labels = {
        "relative_humidity_pct": "Relative Humidity (%)",
        "temperature_c": "Temperature (°C)",
        "mechanical_loading_kpa": "Mechanical Load (kPa)",
        "storage_duration_days": "Storage Duration (days)",
        "initial_moisture_pct": "Initial Moisture (%)",
        "structural_stability": "Structural Stability",
    }

    for i, feat in enumerate(NUMERICAL_FEATURES + ["structural_stability"]):
        fig_hist = px.histogram(
            train_df, x=feat, nbins=40, color="seed_type",
            labels={feat: feature_labels.get(feat, feat)},
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_hist.update_layout(**make_transparent_plotly_layout(
            height=280, showlegend=(i == 0),
            margin=dict(l=30, r=10, t=30, b=30),
        ))
        with cols[i % 3]:
            st.plotly_chart(fig_hist, use_container_width=True)

    # Seed type distribution
    st.subheader("Samples per Seed Type")
    type_counts = train_df["seed_type"].value_counts()
    fig_pie = px.pie(
        values=type_counts.values,
        names=[SEED_TYPES.get(n, {}).get("name", n) for n in type_counts.index],
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_pie.update_layout(**layout, height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Model Architecture ───────────────────────────────────────────
st.divider()
st.subheader("Model Architecture")

arch_c1, arch_c2 = st.columns(2)
with arch_c1:
    st.markdown("""
**Pipeline Structure:**
1. **ColumnTransformer**
   - Numerical features (5): `StandardScaler`
   - Categorical features (1): `OneHotEncoder(drop='first')`
2. **MLPRegressor** (Artificial Neural Network)
   - Hidden layers: (64, 32, 16)
   - Activation: ReLU
   - Solver: Adam
   - Early stopping: Yes (15% validation)
   - Learning rate: Adaptive
""")

with arch_c2:
    st.markdown(f"""
**Training Configuration:**
- Max iterations: 2,000
- Random state: 42
- Train/test split: 80/20
- Total samples: {metrics.get('n_train', 0) + metrics.get('n_test', 0):,}

**Input Features:**
- `relative_humidity_pct` (30-95%)
- `temperature_c` (5-45°C)
- `mechanical_loading_kpa` (50-500 kPa)
- `storage_duration_days` (0-3650 days)
- `initial_moisture_pct` (5-25%)
- `seed_type` (6 categories)
""")

# ── About Section ─────────────────────────────────────────────────
st.divider()
st.subheader("About This Project")

st.markdown("""
This **Seed Digital Twin** is a proof-of-concept application that bridges
**Plant Genetics** and **Computational Mechanics** through surrogate modeling.

### Scientific Foundation
- **Ellis & Roberts (1980)**: Improved seed viability equations
- **Harrington (1972)**: Rules of thumb for seed storage longevity
- **Szymczak-Graczyk**: Moisture permeability and diffusion modeling
- **Garbowski**: FEM structural homogenization and surrogate modeling

### Key References
- FAO. Chapter 7: Seed Storage. https://www.fao.org/4/ad232e/AD232E07.htm
- USDA ARS. Storage Conditions for Plant Germplasm.
- NDSU Extension. Allowable Storage Time for Cereal Grains.
- Ellis & Hong (2007). Seed Science & Technology 35(2):381-390.

### Technology Stack
- **Frontend**: Streamlit with custom dark theme
- **ML Pipeline**: scikit-learn (MLPRegressor + ColumnTransformer)
- **Visualization**: Plotly (3D surfaces, gauges, contours)
- **Science**: scipy (probit viability curves)
""")

st.caption("Developed for PhD Interview Preparation — Poznan University of Life Sciences")
