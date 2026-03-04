"""Seed Database - Real-world reference data and viability curves."""
import streamlit as st
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SEED_TYPES, DATA_DIR, COLOR_PRIMARY, COLOR_WARNING, COLOR_DANGER
from src.seed_science import viability_curve, harrington_hundred_rule, estimate_shelf_life_multiplier
from src.utils import make_transparent_plotly_layout

# ── Load reference data ──────────────────────────────────────────
@st.cache_data
def load_reference_data():
    with open(str(DATA_DIR / "seed_reference_data.json")) as f:
        return json.load(f)

ref_data = load_reference_data()

st.title("🌾 Seed Storage Database")
st.markdown("Real-world reference data curated from FAO, USDA, and peer-reviewed literature.")

# ── Interactive Reference Table ───────────────────────────────────
st.subheader("Optimal Storage Conditions by Seed Type")

table_rows = []
for key, info in ref_data["seed_types"].items():
    table_rows.append({
        "Seed Type": info["common_name"],
        "Scientific Name": info["scientific_name"],
        "Classification": info["classification"],
        "Optimal Temp (°C)": f"{info['optimal_storage_temp_c'][0]} to {info['optimal_storage_temp_c'][1]}",
        "Optimal MC (%)": f"{info['optimal_moisture_content_pct'][0]} - {info['optimal_moisture_content_pct'][1]}",
        "Optimal RH (%)": f"{info['optimal_rh_pct'][0]} - {info['optimal_rh_pct'][1]}",
        "Critical MC (%)": info["critical_moisture_pct"],
        "Max Storage (years)": info["max_storage_years_ideal"],
        "Rupture Force (N)": f"{info['rupture_force_n'][0]} - {info['rupture_force_n'][1]}",
    })

st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

# ── Seed Detail Cards ─────────────────────────────────────────────
st.divider()
st.subheader("Seed Type Details")

selected = st.selectbox(
    "Select seed type for details",
    list(SEED_TYPES.keys()),
    format_func=lambda x: SEED_TYPES[x]["name"],
)

seed_ref = ref_data["seed_types"][selected]
seed_cfg = SEED_TYPES[selected]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Max Storage", f"{seed_ref['max_storage_years_ideal']} years")
    st.metric("Critical MC", f"{seed_ref['critical_moisture_pct']}%")
with c2:
    vc = seed_cfg["viability_constants"]
    st.metric("KE", f"{vc['KE']:.3f}")
    st.metric("CW", f"{vc['CW']:.3f}")
with c3:
    st.metric("CH", f"{vc['CH']:.4f}")
    st.metric("CQ", f"{vc['CQ']:.6f}")

st.info(seed_ref["notes"])

# ── Viability Curves Comparison ───────────────────────────────────
st.divider()
st.subheader("Viability Curves (Ellis-Roberts Equation)")

with st.expander("What is the Ellis-Roberts Equation?"):
    st.markdown("""
The seed viability equation (Ellis & Roberts, 1980) predicts seed longevity:

```
log10(sigma) = KE - CW * log10(m) - CH * t - CQ * t^2
```

Where **sigma** is the standard deviation of seed deaths in time (days),
**m** is moisture content (%), and **t** is temperature (°C).

Viability at time **p**: `v = Ki - p / sigma` (probit scale)

Species-specific constants (KE, CW, CH, CQ) were determined from controlled
aging experiments across multiple seed lots and conditions.
""")

col_ctrl, col_chart = st.columns([1, 2])

with col_ctrl:
    compare_types = st.multiselect(
        "Seed types to compare",
        list(SEED_TYPES.keys()),
        default=["wheat", "soybean", "corn"],
        format_func=lambda x: SEED_TYPES[x]["name"],
    )
    mc_input = st.slider("Moisture Content (%)", 5.0, 25.0, 12.0, key="viab_mc")
    temp_input = st.slider("Storage Temperature (°C)", -5.0, 45.0, 20.0, key="viab_temp")
    max_years = st.slider("Time Horizon (years)", 1, 20, 10, key="viab_years")

with col_chart:
    layout = make_transparent_plotly_layout()
    fig = go.Figure()
    colors = ["#00ff87", "#f1c40f", "#ff4b2b", "#3498db", "#e74c3c", "#9b59b6"]

    for i, st_key in enumerate(compare_types):
        days, viab = viability_curve(st_key, mc_input, temp_input, max_days=max_years * 365)
        fig.add_trace(go.Scatter(
            x=days / 365, y=viab,
            mode="lines", name=SEED_TYPES[st_key]["name"],
            line=dict(color=colors[i % len(colors)], width=3),
        ))

    fig.add_hline(y=50, line_dash="dot", line_color="#b2bec3",
                  annotation_text="50% viability threshold")
    fig.update_layout(
        **layout, height=450,
        xaxis_title="Storage Time (years)",
        yaxis_title="Viability (%)",
        yaxis_range=[0, 105],
        title=f"Predicted Viability at {mc_input}% MC, {temp_input}°C",
        legend=dict(bgcolor="rgba(0,0,0,0.3)"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Allowable Storage Time Table ──────────────────────────────────
st.divider()
st.subheader("Allowable Storage Time — Cereal Grains")
st.caption("Source: NDSU Extension. Values in days before significant quality loss. 999 = >300 days.")

ast_data = ref_data["allowable_storage_days_cereals"]
mc_vals = ast_data["moisture_content_pct"]
temps = ast_data["temperatures"]

ast_df = pd.DataFrame({"MC (%)": mc_vals})
for temp_label, days_list in temps.items():
    ast_df[temp_label] = days_list

st.dataframe(
    ast_df.style.background_gradient(cmap="RdYlGn", subset=list(temps.keys()), vmin=0, vmax=300),
    use_container_width=True,
    hide_index=True,
)

# ── CO2 Monitoring Thresholds ─────────────────────────────────────
st.divider()
st.subheader("CO2 Monitoring Thresholds for Grain Storage")
st.caption("Source: World Grain, OPI Systems, Centaur AG.")

co2_data = ref_data["co2_monitoring_thresholds"]["levels"]
co2_df = pd.DataFrame([{
    "CO2 Range (ppm)": f"{lev['range_ppm'][0]} - {lev['range_ppm'][1]}",
    "Status": lev["status"],
    "Interpretation": lev["interpretation"],
} for lev in co2_data])
st.dataframe(co2_df, use_container_width=True, hide_index=True)

# ── Harrington's Hundred Rule Calculator ──────────────────────────
st.divider()
st.subheader("Harrington's Hundred Rule Calculator")
st.write("**Rule**: Temperature (°F) + Relative Humidity (%) should be < 100 for safe storage.")

hr_c1, hr_c2, hr_c3 = st.columns(3)
with hr_c1:
    hr_temp = st.number_input("Temperature (°C)", value=20.0, min_value=-20.0, max_value=50.0, key="hr_temp")
with hr_c2:
    hr_rh = st.number_input("Relative Humidity (%)", value=50.0, min_value=0.0, max_value=100.0, key="hr_rh")
with hr_c3:
    total, safe = harrington_hundred_rule(hr_temp, hr_rh)
    temp_f = hr_temp * 9 / 5 + 32
    st.metric("Sum (°F + RH%)", f"{total:.1f}")
    if safe:
        st.success(f"{temp_f:.1f}°F + {hr_rh:.0f}% = {total:.1f} < 100 — **SAFE**")
    else:
        st.error(f"{temp_f:.1f}°F + {hr_rh:.0f}% = {total:.1f} >= 100 — **UNSAFE**")

# ── Shelf Life Multiplier ─────────────────────────────────────────
st.divider()
st.subheader("Shelf Life Multiplier (Harrington's Rules)")
st.write("Estimate how much longer seeds will last by reducing moisture or temperature.")

sl_c1, sl_c2, sl_c3 = st.columns(3)
with sl_c1:
    mc_red = st.number_input("MC Reduction (%)", value=2.0, min_value=0.0, max_value=10.0, step=0.5, key="mc_red")
with sl_c2:
    temp_red = st.number_input("Temp Reduction (°C)", value=5.6, min_value=0.0, max_value=30.0, step=0.5, key="temp_red")
with sl_c3:
    mult = estimate_shelf_life_multiplier(mc_red, temp_red)
    st.metric("Storage Life Multiplier", f"{mult:.1f}x")

st.divider()
st.caption("Data sourced from FAO, USDA ARS, NDSU Extension, Ellis & Roberts (1980).")
