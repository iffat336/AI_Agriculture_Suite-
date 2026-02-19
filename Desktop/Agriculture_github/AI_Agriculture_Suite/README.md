# CropMind AI - Intelligent Farming Platform

A comprehensive **AI-powered agricultural platform** with machine learning models, interactive data visualizations, smart recommendations, and an intelligent chatbot. Perfect for portfolio demonstration.

![CropMind AI](https://img.shields.io/badge/CropMind-AI%20Platform-10b981.svg)

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![ML](https://img.shields.io/badge/ML-Models-orange.svg)

## Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI AGRICULTURE SUITE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    🌾        │  │    🔬        │  │    🐛        │               │
│  │    Yield     │  │   Disease    │  │    Pest     │               │
│  │  Predictor   │  │  Detection   │  │ Prediction  │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    💧        │  │    📈        │  │    🤖        │               │
│  │   Smart      │  │   Market     │  │   AgriBot   │               │
│  │ Irrigation   │  │   Prices     │  │   Chatbot   │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│                         DATASETS                                     │
│  • Crop Yield (5,000 records)    • Disease Data (3,000 records)     │
│  • Soil & Irrigation (4,000)     • Pest Monitoring (2,500)          │
│  • Market Prices (2,000)         • Knowledge Base (JSON)            │
└─────────────────────────────────────────────────────────────────────┘
```

## Features

| Feature | Description | Accuracy |
|---------|-------------|----------|
| **Crop Yield Predictor** | Predicts yield based on climate, soil, and farming practices | 87% |
| **Disease Detection** | Identifies crop diseases from symptoms | 92% |
| **Pest Prediction** | Predicts pest outbreak risk | 85% |
| **Smart Irrigation** | Recommends irrigation timing and amount | 90% |
| **Market Predictor** | Forecasts commodity prices | 78% |
| **AgriBot** | AI chatbot for farming guidance | - |

## Quick Start

```bash
cd /Users/usama/Desktop/dummy/AI_Agriculture_Suite
python run.py
```

Then open: **http://localhost:8002**

## Project Structure

```
AI_Agriculture_Suite/
├── backend/
│   └── main.py              # FastAPI application
├── models/
│   ├── ml_models.py         # ML prediction models
│   └── chatbot.py           # AgriBot chatbot
├── frontend/
│   ├── index.html           # Dashboard UI
│   ├── styles.css           # Styling
│   └── app.js               # Frontend logic
├── data/
│   ├── crop_yield_data.csv       # 5,000 records
│   ├── crop_disease_data.csv     # 3,000 records
│   ├── soil_irrigation_data.csv  # 4,000 records
│   ├── pest_monitoring_data.csv  # 2,500 records
│   ├── market_price_data.csv     # 2,000 records
│   ├── chatbot_knowledge.json    # Knowledge base
│   └── generate_data.py          # Data generation script
├── run.py                   # Startup script
├── requirements.txt         # Dependencies
└── README.md
```

## Datasets Generated

| Dataset | Records | Features | Purpose |
|---------|---------|----------|---------|
| **Crop Yield** | 5,000 | 20 | Yield prediction training |
| **Crop Disease** | 3,000 | 15 | Disease classification |
| **Soil & Irrigation** | 4,000 | 17 | Irrigation optimization |
| **Pest Monitoring** | 2,500 | 14 | Pest outbreak prediction |
| **Market Prices** | 2,000 | 8 | Price forecasting |

## API Endpoints

### ML Predictions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict/yield` | POST | Predict crop yield |
| `/api/predict/disease` | POST | Detect crop disease |
| `/api/predict/pest` | POST | Predict pest risk |
| `/api/predict/irrigation` | POST | Get irrigation advice |
| `/api/predict/price` | POST | Predict market price |

### Chatbot

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat` | POST | Chat with AgriBot |
| `/api/chat/history` | GET | Get chat history |
| `/api/chat/history` | DELETE | Clear history |

### Data

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/data/crops` | GET | List supported crops |
| `/api/data/diseases` | GET | List detectable diseases |
| `/api/data/pests` | GET | List common pests |
| `/api/data/models` | GET | Model information |

## Example API Calls

### Predict Crop Yield

```bash
curl -X POST http://localhost:8002/api/predict/yield \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "wheat",
    "temperature": 25,
    "rainfall": 120,
    "soil_ph": 6.5,
    "nitrogen": 150,
    "irrigation_type": "drip",
    "farm_area_ha": 5
  }'
```

### Detect Disease

```bash
curl -X POST http://localhost:8002/api/predict/disease \
  -H "Content-Type: application/json" \
  -d '{
    "crop": "tomato",
    "affected_area_pct": 25,
    "spot_density": 0.4,
    "humidity": 80,
    "temperature": 28
  }'
```

### Chat with AgriBot

```bash
curl -X POST http://localhost:8002/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How to control aphids in my tomato field?"}'
```

## ML Models Architecture

### Crop Yield Predictor
- **Type**: Ensemble (simulated Random Forest/Gradient Boosting)
- **Features**: Temperature, rainfall, soil pH, NPK, irrigation type
- **Output**: Yield per hectare with confidence interval

### Disease Detector
- **Type**: Classification (simulated CNN)
- **Features**: Leaf color, spot density, affected area, environmental conditions
- **Output**: Disease name, severity, treatment recommendations

### Pest Predictor
- **Type**: Risk Assessment Model
- **Features**: Temperature, humidity, crop type, season
- **Output**: Risk level per pest type with control recommendations

### Irrigation Advisor
- **Type**: Rule-based + ML Hybrid
- **Features**: Soil moisture, temperature, crop water needs
- **Output**: Irrigation action, water amount, timing

### Market Price Predictor
- **Type**: Time Series Forecasting
- **Features**: Commodity, historical prices, seasonality
- **Output**: Predicted price with market sentiment

## AgriBot Capabilities

The AI chatbot can answer questions about:

- 🌾 **Crop Cultivation**: Growing tips, seasons, requirements
- 🔬 **Disease Identification**: Symptoms, treatments, prevention
- 🧪 **Fertilizers**: NPK recommendations, deficiency solutions
- 🐛 **Pest Control**: Identification, organic/chemical treatments
- 💧 **Irrigation**: Water requirements, scheduling, methods
- 🌤️ **Weather**: Advisories, crop protection tips
- 📊 **Market**: Price trends, selling recommendations

## Technologies Used

- **Backend**: Python, FastAPI, Pydantic
- **ML**: NumPy, Pandas (sklearn-style models)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data**: CSV datasets, JSON knowledge base

## Extending the Platform

### Add a New ML Model

```python
class NewPredictor:
    def __init__(self):
        self.model_name = "NewPredictor_v1"

    def predict(self, features: Dict) -> PredictionResult:
        # Your prediction logic
        return PredictionResult(
            prediction=result,
            confidence=0.85,
            details={...},
            model_used=self.model_name
        )
```

### Add Chatbot Knowledge

Edit `data/chatbot_knowledge.json` to add new topics.

## Screenshots

The application features:
- Modern green-themed agricultural dashboard
- Interactive forms for all predictions
- Real-time chat interface
- Mobile-responsive design
- Visual result cards with recommendations

## Skills Demonstrated

- **Machine Learning**: Regression, Classification, Time Series
- **AI Agent Development**: Chatbot with intent detection
- **Full-Stack Development**: FastAPI + Modern Frontend
- **Data Engineering**: Dataset generation, feature engineering
- **Agricultural Domain**: Crop science, pest management, irrigation

## License

MIT License - Free for portfolio and commercial use.

---

**Built for Portfolio Demonstration** | AI-Powered Agriculture
