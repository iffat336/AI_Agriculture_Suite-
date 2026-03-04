"""Seed science computations: Ellis-Roberts viability, degradation curves.

References:
    - Ellis & Roberts (1980). Improved Equations for the Prediction of Seed Longevity.
      Annals of Botany 45(1):13-30.
    - Harrington (1972). Seed Storage and Longevity. In: Kozlowski (Ed.) Seed Biology Vol 3.
    - FAO (1994). Seed Storage Guidelines. Chapter 7.
"""
import numpy as np
from scipy.stats import norm

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SEED_TYPES


def ellis_roberts_sigma(seed_type, moisture_content, temperature):
    """
    Compute sigma (std dev of seed deaths in time, in days) using Ellis & Roberts.

    log10(sigma) = KE - CW * log10(m) - CH * t - CQ * t^2

    Args:
        seed_type: key into SEED_TYPES
        moisture_content: seed moisture content (% fresh weight)
        temperature: storage temperature in Celsius
    Returns:
        sigma in days
    """
    vc = SEED_TYPES[seed_type]["viability_constants"]
    mc_safe = np.clip(moisture_content, 1.0, 50.0)
    log_sigma = (
        vc["KE"]
        - vc["CW"] * np.log10(mc_safe)
        - vc["CH"] * temperature
        - vc["CQ"] * temperature ** 2
    )
    return 10.0 ** log_sigma


def viability_curve(seed_type, moisture_content, temperature, ki=3.0, max_days=3650):
    """
    Compute viability (%) over time using the probit model.

    v = Ki - p / sigma
    viability_pct = norm.cdf(v) * 100

    Args:
        seed_type: key into SEED_TYPES
        moisture_content: seed moisture content (%)
        temperature: storage temperature (C)
        ki: initial probit viability (default 3.0 ~ 99.87% initial viability)
        max_days: maximum storage period to compute
    Returns:
        (days_array, viability_pct_array)
    """
    sigma = ellis_roberts_sigma(seed_type, moisture_content, temperature)
    days = np.linspace(0, max_days, 500)
    v = ki - days / max(float(sigma), 0.01)
    viability_pct = norm.cdf(v) * 100
    return days, viability_pct


def compute_stability(rh, temp, load, duration_days, initial_moisture, seed_type):
    """
    Physics-informed stability computation with seed-type-specific parameters.

    Combines humidity, thermal, mechanical, and duration degradation factors
    weighted by seed-type-specific coefficients.

    Returns:
        stability value clipped to [0, 1]
    """
    seed_config = SEED_TYPES[seed_type]
    w = seed_config["degradation_weights"]

    # Humidity factor: non-linear saturation
    humidity_factor = (rh / 100.0) ** 2.3

    # Thermal factor: Arrhenius-inspired acceleration
    thermal_factor = np.exp(0.025 * (temp - 20.0)) / np.exp(0.025 * 25.0)

    # Mechanical factor: normalized with elastic-plastic transition
    mech_factor = (load / 500.0) ** 1.2

    # Duration factor: exponential decay using Ellis-Roberts sigma
    sigma = ellis_roberts_sigma(seed_type, initial_moisture, temp)
    sigma_float = float(sigma) if np.isscalar(sigma) else sigma
    duration_factor = 1.0 - np.exp(-np.asarray(duration_days) / np.maximum(sigma_float, 1.0))

    stability = 1.0 - (
        w["humidity"] * humidity_factor
        + w["thermal"] * thermal_factor
        + w["mechanical"] * mech_factor
        + w["duration"] * duration_factor
    )

    # Initial moisture interaction: higher initial moisture accelerates degradation
    moisture_penalty = 0.05 * np.maximum(0.0, (initial_moisture - 12.0) / 13.0)
    stability = stability - moisture_penalty

    return np.clip(stability, 0.0, 1.0)


def harrington_hundred_rule(temp_celsius, rh_pct):
    """
    Harrington's Hundred Rule: temp(F) + RH(%) should be < 100 for safe storage.

    Returns:
        (sum_value, is_safe)
    """
    temp_f = temp_celsius * 9.0 / 5.0 + 32.0
    total = temp_f + rh_pct
    return total, total < 100.0


def estimate_shelf_life_multiplier(mc_reduction=0.0, temp_reduction_c=0.0):
    """
    Harrington's rules of thumb:
    - Each 1% decrease in MC doubles storage life (valid 5-14% MC range)
    - Each 5.6C decrease in temperature doubles storage life (valid 0-50C range)

    Returns:
        multiplier (e.g., 4.0 means 4x longer storage life)
    """
    mc_mult = 2.0 ** mc_reduction
    temp_mult = 2.0 ** (temp_reduction_c / 5.6)
    return mc_mult * temp_mult
