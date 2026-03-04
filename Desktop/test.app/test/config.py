"""Central configuration for the Seed Digital Twin application."""
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
MODEL_PATH = MODEL_DIR / "surrogate_model.pkl"
TRAINING_DATA_PATH = DATA_DIR / "simulated_fe_data.csv"

# --- Seed Type Definitions ---
# Ellis-Roberts viability constants sourced from:
#   - Ellis & Roberts (1980), Annals of Botany 45(1):13-30
#   - Ellis & Hong (2007), Seed Science & Technology 35(2):381-390
#   - viabilitymetrics R package (Aravind J.)
# Optimal storage conditions from FAO and USDA ARS guidelines.
SEED_TYPES = {
    "wheat": {
        "name": "Wheat (Triticum aestivum)",
        "optimal_temp_c": (-18, 15),
        "optimal_moisture_pct": (10, 14),
        "optimal_rh_pct": (30, 50),
        "critical_moisture_pct": 14.5,
        "max_storage_years": 10,
        "classification": "Orthodox",
        "viability_constants": {"KE": 9.04, "CW": 5.18, "CH": 0.0351, "CQ": 0.000475},
        "stability_thresholds": {"optimal": 0.75, "degraded": 0.45},
        "degradation_weights": {"humidity": 0.35, "thermal": 0.10, "mechanical": 0.25, "duration": 0.15},
    },
    "rice": {
        "name": "Rice (Oryza sativa)",
        "optimal_temp_c": (-18, 15),
        "optimal_moisture_pct": (11, 13),
        "optimal_rh_pct": (35, 55),
        "critical_moisture_pct": 13.0,
        "max_storage_years": 8,
        "classification": "Orthodox",
        "viability_constants": {"KE": 8.24, "CW": 4.34, "CH": 0.0307, "CQ": 0.000501},
        "stability_thresholds": {"optimal": 0.72, "degraded": 0.42},
        "degradation_weights": {"humidity": 0.40, "thermal": 0.12, "mechanical": 0.20, "duration": 0.18},
    },
    "corn": {
        "name": "Corn/Maize (Zea mays)",
        "optimal_temp_c": (-18, 10),
        "optimal_moisture_pct": (11, 13),
        "optimal_rh_pct": (35, 55),
        "critical_moisture_pct": 13.5,
        "max_storage_years": 10,
        "classification": "Orthodox",
        "viability_constants": {"KE": 9.993, "CW": 5.993, "CH": 0.0329, "CQ": 0.000478},
        "stability_thresholds": {"optimal": 0.70, "degraded": 0.40},
        "degradation_weights": {"humidity": 0.38, "thermal": 0.11, "mechanical": 0.28, "duration": 0.13},
    },
    "soybean": {
        "name": "Soybean (Glycine max)",
        "optimal_temp_c": (-18, 10),
        "optimal_moisture_pct": (9, 11),
        "optimal_rh_pct": (30, 40),
        "critical_moisture_pct": 12.0,
        "max_storage_years": 3,
        "classification": "Orthodox",
        "viability_constants": {"KE": 7.52, "CW": 4.09, "CH": 0.0329, "CQ": 0.000478},
        "stability_thresholds": {"optimal": 0.68, "degraded": 0.38},
        "degradation_weights": {"humidity": 0.42, "thermal": 0.13, "mechanical": 0.22, "duration": 0.20},
    },
    "sunflower": {
        "name": "Sunflower (Helianthus annuus)",
        "optimal_temp_c": (-18, 10),
        "optimal_moisture_pct": (6, 9),
        "optimal_rh_pct": (20, 40),
        "critical_moisture_pct": 9.5,
        "max_storage_years": 5,
        "classification": "Orthodox",
        "viability_constants": {"KE": 8.10, "CW": 4.60, "CH": 0.0329, "CQ": 0.000478},
        "stability_thresholds": {"optimal": 0.70, "degraded": 0.40},
        "degradation_weights": {"humidity": 0.36, "thermal": 0.09, "mechanical": 0.30, "duration": 0.15},
    },
    "barley": {
        "name": "Barley (Hordeum vulgare)",
        "optimal_temp_c": (-18, 15),
        "optimal_moisture_pct": (10, 13),
        "optimal_rh_pct": (30, 50),
        "critical_moisture_pct": 13.5,
        "max_storage_years": 8,
        "classification": "Orthodox",
        "viability_constants": {"KE": 9.983, "CW": 5.896, "CH": 0.040, "CQ": 0.000428},
        "stability_thresholds": {"optimal": 0.73, "degraded": 0.43},
        "degradation_weights": {"humidity": 0.35, "thermal": 0.10, "mechanical": 0.27, "duration": 0.15},
    },
}

# --- UI Constants ---
COLOR_PRIMARY = "#00ff87"
COLOR_WARNING = "#f1c40f"
COLOR_DANGER = "#ff4b2b"
COLOR_TEXT_SECONDARY = "#b2bec3"

# --- Feature Ranges (min, max, default) ---
FEATURE_RANGES = {
    "relative_humidity_pct": (30.0, 95.0, 60.0),
    "temperature_c": (5.0, 45.0, 22.0),
    "mechanical_loading_kpa": (50.0, 500.0, 150.0),
    "storage_duration_days": (0.0, 3650.0, 180.0),
    "initial_moisture_pct": (5.0, 25.0, 12.0),
}

NUMERICAL_FEATURES = [
    "relative_humidity_pct",
    "temperature_c",
    "mechanical_loading_kpa",
    "storage_duration_days",
    "initial_moisture_pct",
]

CATEGORICAL_FEATURES = ["seed_type"]
