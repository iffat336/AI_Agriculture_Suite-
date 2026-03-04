# 🌱 Hygrothermal Digital Twin: Seed Mechanics & Material Stability

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/) 
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture-4.0](https://img.shields.io/badge/Industry-4.0-green)

This project is a professional **Proof-of-Concept Digital Twin** developed for the PhD interview process at the **Poznań University of Life Sciences (Faculty of Environmental and Mechanical Engineering)**. 

The demonstration bridges the gap between **Plant Genetics** and **Computational Mechanics**, specifically aligning with the research of **Prof. Tomasz Garbowski** and **Prof. Anna Maria Szymczak-Graczyk**.

---

## 🔬 Scientific Context: The Research Bridge

This project focuses on the **Hygrothermal Performance** of biological materials. In structural engineering and building diagnostics, understanding moisture diffusion and mechanical homogenization is critical. This tool applies those same engineering principles to **Seed Quality Control**.

### Key Concept: The Surrogate Model
Traditional **Finite Element Method (FEM)** simulations are accurate but computationally expensive (taking hours/days). This project demonstrates the use of **Artificial Neural Networks (ANN)** as "Surrogate Models" that:
1.  Learn the non-linear physics of anisotropic diffusion.
2.  Provide real-time structural stability predictions (<1ms).
3.  Enable immediate intervention in smart agricultural storage systems (Agriculture 4.0).

---

## 🎨 Professional Dashboard Features
The interactive **Streamlit Dashboard** provides a premium, "wow-factor" visualization of the Digital Twin:
- **Premium UI**: Custom "Agriculture 4.0" dark theme with neon accents.
- **Real-Time Sliders**: Control **Relative Humidity (Vapor Diffusion)**, **Temperature**, and **Mechanical Loading (kPa)**.
- **Dynamic Gauges**: Real-time structural integrity indicators powered by a trained MLPRegressor.
- **Latency Tracking**: Displays the speed advantage of Machine Learning over traditional numerical methods.

---

## 📁 Project Architecture
- `app.py`: The premium Streamlit dashboard and main entry point.
- `data_simulator.py`: Logic for generating scientific training data based on non-linear hygrothermal degradation.
- `surrogate_model.py`: Multi-Layer Perceptron (ANN) training pipeline with standardized scaling.
- `requirements.txt`: Exact dependency versions for reproducible research cloud deployment.

---

## 🚀 Installation & Local Execution

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/iffat336/seed-digital-twin-demo.git
   cd seed-digital-twin-demo
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Surrogate Model** (Optional, models are pre-included):
   ```bash
   python data_simulator.py
   python surrogate_model.py
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## 🎓 PhD Candidate Value Proposition
As a researcher, this project demonstrates my readiness to:
*   Deploy **Machine Learning** to solve bottlenecks in **Computational Mechanics**.
*   Process and simulate complex, multi-variable **Material Characterization** data.
*   Communicate sophisticated engineering concepts through **Interactive Data Visualization**.

---
*Developed by **Iffat Nazir** - Bridging Plant Science and Civil Engineering through AI.*
