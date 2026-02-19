"""
Agricultural Data Generation Script
Generates realistic datasets for AI Agriculture Suite
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# =============================================================================
# 1. CROP YIELD DATASET
# =============================================================================

def generate_crop_yield_data(n_samples=5000):
    """
    Generate crop yield dataset with climate and soil features
    """
    print("Generating Crop Yield Dataset...")

    crops = ['Wheat', 'Rice', 'Maize', 'Soybean', 'Cotton', 'Sugarcane', 'Potato', 'Tomato']
    regions = ['North', 'South', 'East', 'West', 'Central']
    soil_types = ['Clay', 'Sandy', 'Loamy', 'Silt', 'Peat']
    seasons = ['Kharif', 'Rabi', 'Zaid']

    data = []

    for i in range(n_samples):
        crop = random.choice(crops)
        region = random.choice(regions)
        soil_type = random.choice(soil_types)
        season = random.choice(seasons)
        year = random.randint(2015, 2024)

        # Climate features
        avg_temperature = np.random.normal(25, 8)  # Celsius
        avg_rainfall = np.random.exponential(100) + 20  # mm
        humidity = np.random.uniform(40, 90)  # %
        sunlight_hours = np.random.uniform(4, 12)  # hours/day

        # Soil features
        soil_ph = np.random.uniform(5.5, 8.5)
        nitrogen_content = np.random.uniform(100, 400)  # kg/ha
        phosphorus_content = np.random.uniform(10, 80)  # kg/ha
        potassium_content = np.random.uniform(50, 300)  # kg/ha
        organic_matter = np.random.uniform(0.5, 5)  # %

        # Farm features
        farm_area = np.random.exponential(5) + 0.5  # hectares
        irrigation_type = random.choice(['Drip', 'Sprinkler', 'Flood', 'Rainfed'])
        fertilizer_used = np.random.uniform(50, 300)  # kg/ha
        pesticide_used = np.random.uniform(0, 10)  # liters/ha

        # Calculate yield based on features (with realistic relationships)
        base_yield = {
            'Wheat': 3.5, 'Rice': 4.0, 'Maize': 5.5, 'Soybean': 2.5,
            'Cotton': 2.0, 'Sugarcane': 70.0, 'Potato': 25.0, 'Tomato': 30.0
        }

        yield_per_ha = base_yield[crop]

        # Temperature effect (optimal range varies by crop)
        temp_effect = 1 - abs(avg_temperature - 25) * 0.02

        # Rainfall effect
        rain_effect = min(1, avg_rainfall / 150) if avg_rainfall < 200 else max(0.5, 1 - (avg_rainfall - 200) / 500)

        # Soil effect
        ph_effect = 1 - abs(soil_ph - 6.5) * 0.1
        nutrient_effect = min(1, (nitrogen_content + phosphorus_content + potassium_content) / 500)

        # Irrigation effect
        irrigation_multiplier = {'Drip': 1.2, 'Sprinkler': 1.1, 'Flood': 1.0, 'Rainfed': 0.8}

        # Calculate final yield
        yield_per_ha *= temp_effect * rain_effect * ph_effect * nutrient_effect
        yield_per_ha *= irrigation_multiplier[irrigation_type]
        yield_per_ha *= np.random.uniform(0.85, 1.15)  # Random variation
        yield_per_ha = max(0.5, yield_per_ha)  # Minimum yield

        total_yield = yield_per_ha * farm_area

        data.append({
            'crop': crop,
            'region': region,
            'soil_type': soil_type,
            'season': season,
            'year': year,
            'avg_temperature': round(avg_temperature, 2),
            'avg_rainfall': round(avg_rainfall, 2),
            'humidity': round(humidity, 2),
            'sunlight_hours': round(sunlight_hours, 2),
            'soil_ph': round(soil_ph, 2),
            'nitrogen_content': round(nitrogen_content, 2),
            'phosphorus_content': round(phosphorus_content, 2),
            'potassium_content': round(potassium_content, 2),
            'organic_matter': round(organic_matter, 2),
            'farm_area_ha': round(farm_area, 2),
            'irrigation_type': irrigation_type,
            'fertilizer_kg_ha': round(fertilizer_used, 2),
            'pesticide_l_ha': round(pesticide_used, 2),
            'yield_per_ha': round(yield_per_ha, 2),
            'total_yield_tons': round(total_yield, 2)
        })

    df = pd.DataFrame(data)
    df.to_csv('crop_yield_data.csv', index=False)
    print(f"  Created crop_yield_data.csv with {len(df)} records")
    return df


# =============================================================================
# 2. CROP DISEASE DATASET
# =============================================================================

def generate_crop_disease_data(n_samples=3000):
    """
    Generate crop disease dataset for classification
    """
    print("Generating Crop Disease Dataset...")

    diseases = {
        'Healthy': {'severity': 0, 'treatment_cost': 0},
        'Leaf_Blight': {'severity': 3, 'treatment_cost': 150},
        'Powdery_Mildew': {'severity': 2, 'treatment_cost': 100},
        'Rust': {'severity': 4, 'treatment_cost': 200},
        'Bacterial_Spot': {'severity': 3, 'treatment_cost': 180},
        'Mosaic_Virus': {'severity': 5, 'treatment_cost': 250},
        'Root_Rot': {'severity': 4, 'treatment_cost': 220},
        'Anthracnose': {'severity': 3, 'treatment_cost': 160},
        'Downy_Mildew': {'severity': 2, 'treatment_cost': 120},
        'Fusarium_Wilt': {'severity': 5, 'treatment_cost': 280}
    }

    crops = ['Tomato', 'Potato', 'Corn', 'Wheat', 'Rice', 'Apple', 'Grape', 'Pepper']

    data = []

    for i in range(n_samples):
        disease = random.choice(list(diseases.keys()))
        crop = random.choice(crops)

        # Environmental factors that affect disease
        temperature = np.random.normal(25, 8)
        humidity = np.random.uniform(40, 95)
        rainfall_last_week = np.random.exponential(30)

        # Disease is more likely in certain conditions
        if disease != 'Healthy':
            # Diseases more common in high humidity
            humidity = np.random.uniform(60, 95)

        # Leaf features (simulated image features)
        leaf_color_r = np.random.randint(50, 200)
        leaf_color_g = np.random.randint(80, 220) if disease == 'Healthy' else np.random.randint(40, 150)
        leaf_color_b = np.random.randint(20, 100)

        # Texture features
        leaf_texture_variance = np.random.uniform(0.1, 0.9)
        spot_density = 0 if disease == 'Healthy' else np.random.uniform(0.1, 0.8)
        affected_area_pct = 0 if disease == 'Healthy' else np.random.uniform(5, 80)

        # Detection confidence
        confidence = np.random.uniform(0.7, 0.99)

        data.append({
            'crop': crop,
            'disease': disease,
            'severity': diseases[disease]['severity'],
            'treatment_cost_usd': diseases[disease]['treatment_cost'],
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'rainfall_last_week_mm': round(rainfall_last_week, 2),
            'leaf_color_r': leaf_color_r,
            'leaf_color_g': leaf_color_g,
            'leaf_color_b': leaf_color_b,
            'leaf_texture_variance': round(leaf_texture_variance, 3),
            'spot_density': round(spot_density, 3),
            'affected_area_pct': round(affected_area_pct, 2),
            'detection_confidence': round(confidence, 3),
            'image_id': f"img_{i:05d}.jpg",
            'detected_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        })

    df = pd.DataFrame(data)
    df.to_csv('crop_disease_data.csv', index=False)
    print(f"  Created crop_disease_data.csv with {len(df)} records")
    return df


# =============================================================================
# 3. SOIL & IRRIGATION DATA
# =============================================================================

def generate_soil_irrigation_data(n_samples=4000):
    """
    Generate soil and irrigation monitoring data
    """
    print("Generating Soil & Irrigation Dataset...")

    data = []

    for i in range(n_samples):
        timestamp = datetime.now() - timedelta(hours=random.randint(0, 8760))

        # Soil sensors
        soil_moisture = np.random.uniform(10, 80)  # %
        soil_temperature = np.random.normal(22, 8)  # Celsius
        soil_ph = np.random.uniform(5.5, 8.5)
        soil_ec = np.random.uniform(0.5, 4.0)  # Electrical conductivity dS/m

        # Nutrient levels
        nitrogen = np.random.uniform(50, 400)
        phosphorus = np.random.uniform(10, 100)
        potassium = np.random.uniform(50, 350)

        # Weather data
        air_temperature = np.random.normal(25, 10)
        air_humidity = np.random.uniform(30, 90)
        wind_speed = np.random.exponential(5)
        solar_radiation = np.random.uniform(100, 1000)  # W/m²

        # Irrigation system
        irrigation_zone = random.choice(['Zone_A', 'Zone_B', 'Zone_C', 'Zone_D'])
        irrigation_type = random.choice(['Drip', 'Sprinkler', 'Center_Pivot'])

        # Calculate irrigation need
        evapotranspiration = (0.0023 * (air_temperature + 17.8) *
                             (solar_radiation / 2.45) * 0.5)

        water_deficit = max(0, 60 - soil_moisture)  # Target 60% moisture
        irrigation_needed = water_deficit > 15
        recommended_water_mm = water_deficit * 0.5 if irrigation_needed else 0

        # Water usage
        actual_water_used = recommended_water_mm * np.random.uniform(0.8, 1.2) if irrigation_needed else 0

        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'irrigation_zone': irrigation_zone,
            'irrigation_type': irrigation_type,
            'soil_moisture_pct': round(soil_moisture, 2),
            'soil_temperature_c': round(soil_temperature, 2),
            'soil_ph': round(soil_ph, 2),
            'soil_ec_ds_m': round(soil_ec, 2),
            'nitrogen_ppm': round(nitrogen, 2),
            'phosphorus_ppm': round(phosphorus, 2),
            'potassium_ppm': round(potassium, 2),
            'air_temperature_c': round(air_temperature, 2),
            'air_humidity_pct': round(air_humidity, 2),
            'wind_speed_kmh': round(wind_speed, 2),
            'solar_radiation_wm2': round(solar_radiation, 2),
            'evapotranspiration_mm': round(evapotranspiration, 2),
            'irrigation_needed': irrigation_needed,
            'recommended_water_mm': round(recommended_water_mm, 2),
            'actual_water_used_mm': round(actual_water_used, 2)
        })

    df = pd.DataFrame(data)
    df.to_csv('soil_irrigation_data.csv', index=False)
    print(f"  Created soil_irrigation_data.csv with {len(df)} records")
    return df


# =============================================================================
# 4. PEST MONITORING DATA
# =============================================================================

def generate_pest_data(n_samples=2500):
    """
    Generate pest monitoring and prediction data
    """
    print("Generating Pest Monitoring Dataset...")

    pests = {
        'Aphids': {'damage_level': 3, 'treatment': 'Neem oil spray'},
        'Whiteflies': {'damage_level': 2, 'treatment': 'Yellow sticky traps'},
        'Locusts': {'damage_level': 5, 'treatment': 'Chemical pesticide'},
        'Caterpillars': {'damage_level': 4, 'treatment': 'Bt spray'},
        'Thrips': {'damage_level': 2, 'treatment': 'Spinosad'},
        'Beetles': {'damage_level': 3, 'treatment': 'Manual removal'},
        'Mites': {'damage_level': 2, 'treatment': 'Miticide spray'},
        'Borers': {'damage_level': 4, 'treatment': 'Systemic insecticide'},
        'None': {'damage_level': 0, 'treatment': 'No action needed'}
    }

    crops = ['Wheat', 'Rice', 'Maize', 'Cotton', 'Vegetables', 'Fruits']

    data = []

    for i in range(n_samples):
        date = datetime.now() - timedelta(days=random.randint(0, 730))
        pest = random.choice(list(pests.keys()))
        crop = random.choice(crops)

        # Environmental factors
        temperature = np.random.normal(28, 7)
        humidity = np.random.uniform(40, 90)
        rainfall_last_month = np.random.exponential(80)

        # Pest counts
        pest_count_per_plant = 0 if pest == 'None' else np.random.exponential(5)
        affected_plants_pct = 0 if pest == 'None' else np.random.uniform(5, 60)

        # Economic impact
        crop_loss_pct = affected_plants_pct * pests[pest]['damage_level'] * 0.05
        economic_loss_usd_ha = crop_loss_pct * np.random.uniform(30, 80)

        # Prediction features
        pest_risk_score = (humidity / 100 * 0.3 +
                         min(1, temperature / 35) * 0.3 +
                         min(1, rainfall_last_month / 150) * 0.2 +
                         np.random.uniform(0, 0.2))

        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'crop': crop,
            'pest_type': pest,
            'damage_level': pests[pest]['damage_level'],
            'recommended_treatment': pests[pest]['treatment'],
            'temperature_c': round(temperature, 2),
            'humidity_pct': round(humidity, 2),
            'rainfall_last_month_mm': round(rainfall_last_month, 2),
            'pest_count_per_plant': round(pest_count_per_plant, 1),
            'affected_plants_pct': round(affected_plants_pct, 2),
            'crop_loss_pct': round(crop_loss_pct, 2),
            'economic_loss_usd_ha': round(economic_loss_usd_ha, 2),
            'pest_risk_score': round(pest_risk_score, 3),
            'field_id': f"FIELD_{random.randint(1, 100):03d}",
            'region': random.choice(['North', 'South', 'East', 'West', 'Central'])
        })

    df = pd.DataFrame(data)
    df.to_csv('pest_monitoring_data.csv', index=False)
    print(f"  Created pest_monitoring_data.csv with {len(df)} records")
    return df


# =============================================================================
# 5. FARMER CHATBOT KNOWLEDGE BASE
# =============================================================================

def generate_chatbot_knowledge():
    """
    Generate knowledge base for agricultural chatbot
    """
    print("Generating Chatbot Knowledge Base...")

    knowledge_base = {
        "crop_info": {
            "wheat": {
                "growing_season": "October to April (Rabi)",
                "optimal_temperature": "15-25°C",
                "water_requirement": "450-650 mm",
                "soil_type": "Well-drained loamy soil",
                "ph_range": "6.0-7.5",
                "major_diseases": ["Rust", "Powdery Mildew", "Leaf Blight"],
                "fertilizer_npk": "120:60:40 kg/ha",
                "yield_potential": "4-6 tons/ha"
            },
            "rice": {
                "growing_season": "June to November (Kharif)",
                "optimal_temperature": "20-35°C",
                "water_requirement": "1200-1400 mm",
                "soil_type": "Clay or clay loam",
                "ph_range": "5.5-6.5",
                "major_diseases": ["Blast", "Bacterial Leaf Blight", "Sheath Rot"],
                "fertilizer_npk": "100:50:50 kg/ha",
                "yield_potential": "5-8 tons/ha"
            },
            "maize": {
                "growing_season": "June to September",
                "optimal_temperature": "21-30°C",
                "water_requirement": "500-800 mm",
                "soil_type": "Well-drained sandy loam",
                "ph_range": "5.8-7.0",
                "major_diseases": ["Leaf Blight", "Downy Mildew", "Stalk Rot"],
                "fertilizer_npk": "150:75:40 kg/ha",
                "yield_potential": "6-10 tons/ha"
            },
            "cotton": {
                "growing_season": "April to December",
                "optimal_temperature": "21-30°C",
                "water_requirement": "700-1200 mm",
                "soil_type": "Black cotton soil",
                "ph_range": "6.0-8.0",
                "major_diseases": ["Bacterial Blight", "Fusarium Wilt", "Root Rot"],
                "fertilizer_npk": "80:40:40 kg/ha",
                "yield_potential": "2-3 tons/ha"
            },
            "tomato": {
                "growing_season": "Year-round (varies by region)",
                "optimal_temperature": "20-27°C",
                "water_requirement": "400-600 mm",
                "soil_type": "Well-drained sandy loam",
                "ph_range": "6.0-7.0",
                "major_diseases": ["Early Blight", "Late Blight", "Mosaic Virus"],
                "fertilizer_npk": "100:50:50 kg/ha",
                "yield_potential": "30-50 tons/ha"
            },
            "potato": {
                "growing_season": "October to March",
                "optimal_temperature": "15-20°C",
                "water_requirement": "500-700 mm",
                "soil_type": "Light sandy loam",
                "ph_range": "5.5-6.5",
                "major_diseases": ["Late Blight", "Early Blight", "Black Scurf"],
                "fertilizer_npk": "150:100:100 kg/ha",
                "yield_potential": "25-40 tons/ha"
            }
        },
        "disease_treatments": {
            "rust": {
                "symptoms": "Orange-brown pustules on leaves",
                "prevention": "Use resistant varieties, proper spacing",
                "treatment": "Propiconazole or Tebuconazole spray",
                "dosage": "1ml per liter of water"
            },
            "powdery_mildew": {
                "symptoms": "White powdery growth on leaves",
                "prevention": "Avoid overhead irrigation, ensure air circulation",
                "treatment": "Sulfur dust or Karathane spray",
                "dosage": "2g per liter of water"
            },
            "leaf_blight": {
                "symptoms": "Brown lesions on leaves",
                "prevention": "Crop rotation, remove infected debris",
                "treatment": "Mancozeb or Copper oxychloride",
                "dosage": "2.5g per liter of water"
            },
            "bacterial_blight": {
                "symptoms": "Water-soaked lesions, wilting",
                "prevention": "Use disease-free seeds, avoid waterlogging",
                "treatment": "Streptomycin + Copper spray",
                "dosage": "0.5g + 3g per liter"
            }
        },
        "fertilizer_guide": {
            "nitrogen_deficiency": {
                "symptoms": "Yellowing of older leaves, stunted growth",
                "solution": "Apply urea (46% N) at 50-100 kg/ha",
                "timing": "Split application recommended"
            },
            "phosphorus_deficiency": {
                "symptoms": "Purple coloration, poor root development",
                "solution": "Apply DAP or SSP at 50-75 kg/ha",
                "timing": "At sowing time"
            },
            "potassium_deficiency": {
                "symptoms": "Leaf edge browning, weak stems",
                "solution": "Apply MOP at 40-60 kg/ha",
                "timing": "At sowing or first irrigation"
            }
        },
        "pest_control": {
            "aphids": {
                "identification": "Small soft-bodied insects, often green or black",
                "damage": "Suck plant sap, transmit viruses",
                "organic_control": "Neem oil spray (5ml/L), ladybug release",
                "chemical_control": "Imidacloprid (0.5ml/L)"
            },
            "whiteflies": {
                "identification": "Tiny white flying insects",
                "damage": "Suck sap, transmit viruses, honeydew excretion",
                "organic_control": "Yellow sticky traps, neem spray",
                "chemical_control": "Thiamethoxam (0.3g/L)"
            },
            "caterpillars": {
                "identification": "Larvae of moths/butterflies",
                "damage": "Chew leaves and fruits",
                "organic_control": "Bt spray, hand picking",
                "chemical_control": "Chlorantraniliprole (0.3ml/L)"
            }
        },
        "irrigation_tips": {
            "drip_irrigation": {
                "benefits": "50% water savings, precise application",
                "suitable_crops": "Vegetables, fruits, cotton",
                "maintenance": "Clean filters weekly, check emitters"
            },
            "sprinkler_irrigation": {
                "benefits": "Uniform distribution, frost protection",
                "suitable_crops": "Field crops, lawns",
                "maintenance": "Check nozzles, avoid wind drift"
            },
            "flood_irrigation": {
                "benefits": "Low initial cost, simple operation",
                "suitable_crops": "Rice, sugarcane",
                "efficiency": "40-50% (improve with laser leveling)"
            }
        },
        "weather_advice": {
            "heat_wave": "Increase irrigation frequency, apply mulch, provide shade for sensitive crops",
            "frost": "Cover plants, irrigate before frost, use windbreaks",
            "heavy_rain": "Ensure drainage, apply fungicide preventively, stake tall plants",
            "drought": "Mulching, reduce planting density, use drought-tolerant varieties"
        }
    }

    import json
    with open('chatbot_knowledge.json', 'w') as f:
        json.dump(knowledge_base, f, indent=2)
    print("  Created chatbot_knowledge.json")

    return knowledge_base


# =============================================================================
# 6. MARKET PRICE DATA
# =============================================================================

def generate_market_price_data(n_samples=2000):
    """
    Generate agricultural commodity price data
    """
    print("Generating Market Price Dataset...")

    commodities = ['Wheat', 'Rice', 'Maize', 'Soybean', 'Cotton', 'Sugarcane', 'Potato', 'Tomato', 'Onion']
    markets = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore', 'Hyderabad']

    data = []

    base_prices = {
        'Wheat': 2200, 'Rice': 3500, 'Maize': 1800, 'Soybean': 4500,
        'Cotton': 6000, 'Sugarcane': 350, 'Potato': 1500, 'Tomato': 2500, 'Onion': 2000
    }

    for i in range(n_samples):
        date = datetime.now() - timedelta(days=random.randint(0, 365))
        commodity = random.choice(commodities)
        market = random.choice(markets)

        # Price with seasonal and random variation
        base = base_prices[commodity]
        seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * date.timetuple().tm_yday / 365)
        random_factor = np.random.uniform(0.85, 1.15)

        price_per_quintal = base * seasonal_factor * random_factor

        # Volume traded
        volume_quintals = np.random.exponential(500)

        # Quality grade
        grade = random.choice(['A', 'B', 'C'])
        grade_multiplier = {'A': 1.1, 'B': 1.0, 'C': 0.9}
        price_per_quintal *= grade_multiplier[grade]

        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'commodity': commodity,
            'market': market,
            'grade': grade,
            'price_per_quintal': round(price_per_quintal, 2),
            'volume_quintals': round(volume_quintals, 2),
            'total_value': round(price_per_quintal * volume_quintals, 2),
            'price_change_pct': round(np.random.uniform(-5, 5), 2)
        })

    df = pd.DataFrame(data)
    df.to_csv('market_price_data.csv', index=False)
    print(f"  Created market_price_data.csv with {len(df)} records")
    return df


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI Agriculture Suite - Data Generation")
    print("="*60 + "\n")

    # Generate all datasets
    generate_crop_yield_data()
    generate_crop_disease_data()
    generate_soil_irrigation_data()
    generate_pest_data()
    generate_chatbot_knowledge()
    generate_market_price_data()

    print("\n" + "="*60)
    print("All datasets generated successfully!")
    print("="*60)
