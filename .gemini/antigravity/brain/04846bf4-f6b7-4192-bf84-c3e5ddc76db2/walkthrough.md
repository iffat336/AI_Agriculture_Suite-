# PhytoScout: Project Walkthrough

**PhytoScout** is a Streamlit application designed to bridge fundamental plant genetics research with field applications.

## 🚀 Deployed App
**URL:** [https://phytoscout-mp8mkyfqbvegphi4qrvkfk.streamlit.app/](https://phytoscout-mp8mkyfqbvegphi4qrvkfk.streamlit.app/)

## ✨ Features Implemented

### 1. Phytoremediation Tracker
*   **Goal:** Visualize soil cleanup using *Noccaea caerulescens*.
*   **Status:** ✅ Working. Sliders correctly update the graphs for soil depletion and plant accumulation.

### 2. Biomass Predictor (NPEC-Lite)
*   **Goal:** Estimate biomass from images.
*   **Status:** ✅ Working. Uploading an image triggers the "Greenness Index" calculation and displays a masked result.

### 3. Deficiency Detective
*   **Goal:** Diagnose nutrient deficiencies.
*   **Status:** ✅ Working. Logic correctly identifies Iron, Zinc, and other deficiencies based on user inputs.

## 📂 Project Structure

*   `app.py`: Main entry point.
*   `modules/`: Contains the three core feature pages.
*   `utils/`: Helper functions for image processing and data generation.
*   `DEPLOYMENT.md`: Step-by-step guide for deploying to Streamlit Cloud.

## ✅ Verification
The app has been deployed and manually verified to be fully functional on Streamlit Community Cloud.
