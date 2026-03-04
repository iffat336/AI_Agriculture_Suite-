"""Enhanced data simulator for the Seed Digital Twin.

Generates physics-informed training data with 5 numerical features + seed type.
Uses Ellis-Roberts viability equation structure for duration-related degradation.
"""
import pandas as pd
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SEED_TYPES, DATA_DIR, FEATURE_RANGES
from src.seed_science import compute_stability


def generate_scientific_data(n_samples_per_type=800):
    """
    Generate training data for the surrogate model.

    Creates n_samples_per_type samples for each seed type in SEED_TYPES,
    totaling n_samples_per_type * len(SEED_TYPES) samples.
    """
    np.random.seed(42)
    all_rows = []

    for seed_type in SEED_TYPES:
        n = n_samples_per_type

        rh = np.random.uniform(*FEATURE_RANGES["relative_humidity_pct"][:2], n)
        temp = np.random.uniform(*FEATURE_RANGES["temperature_c"][:2], n)
        load = np.random.uniform(*FEATURE_RANGES["mechanical_loading_kpa"][:2], n)
        duration = np.random.uniform(*FEATURE_RANGES["storage_duration_days"][:2], n)
        moisture = np.random.uniform(*FEATURE_RANGES["initial_moisture_pct"][:2], n)

        stability = compute_stability(rh, temp, load, duration, moisture, seed_type)

        # Add realistic noise
        noise = np.random.normal(0, 0.025, n)
        stability = np.clip(stability + noise, 0.0, 1.0)

        df = pd.DataFrame({
            "seed_type": seed_type,
            "relative_humidity_pct": rh,
            "temperature_c": temp,
            "mechanical_loading_kpa": load,
            "storage_duration_days": duration,
            "initial_moisture_pct": moisture,
            "structural_stability": stability,
        })
        all_rows.append(df)

    result = pd.concat(all_rows, ignore_index=True)

    # Shuffle
    result = result.sample(frac=1, random_state=42).reset_index(drop=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(str(DATA_DIR / "simulated_fe_data.csv"), index=False)
    print(f"Generated {len(result)} samples across {len(SEED_TYPES)} seed types.")
    print(f"Saved to {DATA_DIR / 'simulated_fe_data.csv'}")
    return result


if __name__ == "__main__":
    generate_scientific_data()
