"""Enhanced surrogate model training pipeline.

Uses sklearn Pipeline with ColumnTransformer for preprocessing
and MLPRegressor for the surrogate model. Saves metrics and test predictions.
"""
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import MODEL_DIR, TRAINING_DATA_PATH, NUMERICAL_FEATURES, CATEGORICAL_FEATURES


def train_surrogate():
    """Train the surrogate model pipeline and save artifacts."""
    try:
        data = pd.read_csv(str(TRAINING_DATA_PATH))
    except FileNotFoundError:
        print(f"Error: {TRAINING_DATA_PATH} not found. Run data_simulator.py first.")
        return

    X = data[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = data["structural_stability"]

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), NUMERICAL_FEATURES),
        ("cat", OneHotEncoder(drop="first", sparse_output=False), CATEGORICAL_FEATURES),
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", MLPRegressor(
            hidden_layer_sizes=(64, 32, 16),
            max_iter=2000,
            early_stopping=True,
            validation_fraction=0.15,
            learning_rate="adaptive",
            random_state=42,
        )),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training surrogate model (MLP Pipeline)...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    mae = float(mean_absolute_error(y_test, y_pred))

    metrics = {
        "r2": round(r2, 6),
        "rmse": round(rmse, 6),
        "mae": round(mae, 6),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "architecture": "MLPRegressor(64, 32, 16)",
        "features_numerical": NUMERICAL_FEATURES,
        "features_categorical": CATEGORICAL_FEATURES,
    }

    print(f"R2: {r2:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")

    # Save
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, str(MODEL_DIR / "surrogate_model.pkl"))

    with open(str(MODEL_DIR / "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    test_results = X_test.copy()
    test_results["y_actual"] = y_test.values
    test_results["y_predicted"] = y_pred
    test_results.to_csv(str(MODEL_DIR / "test_predictions.csv"), index=False)

    print(f"Saved model and metrics to {MODEL_DIR}/")


if __name__ == "__main__":
    train_surrogate()
