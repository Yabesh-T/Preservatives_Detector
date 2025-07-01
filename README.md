# 🧪 Preservatives Detector – Benzoate & Sorbate Estimation App

This project is an AI-powered Streamlit dashboard designed to estimate the concentration of **benzoate** and **sorbate** preservatives in food and beverage samples using UV-VIS absorbance data.

Built with a focus on real-time monitoring, safety classification, and batch processing, this tool bridges sensor data with machine learning to support chemical quality control in lab and industrial settings.

---

## 🚀 Features

- 📥 Upload CSV sensor data or enter absorbance values manually
- 🔬 Predict benzoate and sorbate concentrations using trained regression models
- ⚠️ Highlight unsafe preservative levels based on safety thresholds
- 📊 Visualize preservative levels with interactive bar charts
- 📤 Download prediction results as a CSV file
- 🌐 Deployed on Streamlit Cloud for easy access

---

## 📁 File Structure


---

## 📄 Sample Input Format (CSV)

Your uploaded CSV should contain the following columns:

```csv
abs_280,abs_320,abs_400
0.42,0.35,0.28
0.50,0.40,0.30
...
