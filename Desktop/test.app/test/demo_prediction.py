"""CLI demo: run Digital Twin predictions using the trained pipeline model."""
import joblib
import pandas as pd
import time

from config import MODEL_PATH, SEED_TYPES


def run_prediction(seed_type="wheat", rh=60.0, temp=22.0, load=150.0,
                   duration=180.0, moisture=12.0):
    """Run a single prediction and print results."""
    try:
        model = joblib.load(str(MODEL_PATH))
    except FileNotFoundError:
        print("Error: Model not found. Run the training pipeline first:")
        print('  python -c "from src.data_simulator import generate_scientific_data; generate_scientific_data()"')
        print('  python -c "from src.surrogate_model import train_surrogate; train_surrogate()"')
        return

    input_df = pd.DataFrame([{
        "relative_humidity_pct": rh,
        "temperature_c": temp,
        "mechanical_loading_kpa": load,
        "storage_duration_days": duration,
        "initial_moisture_pct": moisture,
        "seed_type": seed_type,
    }])

    start = time.time()
    prediction = max(0.0, min(1.0, float(model.predict(input_df)[0])))
    latency = (time.time() - start) * 1000

    print("-" * 50)
    print(f"Digital Twin Response — {SEED_TYPES[seed_type]['name']}")
    print(f"  RH: {rh}% | Temp: {temp}C | Load: {load} kPa")
    print(f"  Duration: {duration} days | Moisture: {moisture}%")
    print(f"  Predicted Stability: {prediction:.2%}")
    print(f"  Latency: {latency:.4f} ms")

    if prediction < 0.4:
        print("  Status: CRITICAL — High risk of structural failure!")
    elif prediction < 0.7:
        print("  Status: DEGRADED — Monitor closely.")
    else:
        print("  Status: OPTIMAL — Seed is stable.")
    print("-" * 50)


if __name__ == "__main__":
    # Harsh conditions
    run_prediction(seed_type="soybean", rh=85.0, temp=35.0, load=400.0,
                   duration=365.0, moisture=18.0)
    # Safe conditions
    run_prediction(seed_type="wheat", rh=45.0, temp=10.0, load=100.0,
                   duration=90.0, moisture=10.0)
    # Moderate conditions
    run_prediction(seed_type="corn", rh=65.0, temp=25.0, load=200.0,
                   duration=180.0, moisture=13.0)
