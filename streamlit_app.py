import numpy as np
import streamlit as st
import pandas as pd
import joblib

# 📁 Load the trained models
benzoate_model = joblib.load("models/regression/benzoate_model.pkl")
sorbate_model = joblib.load("models/regression/sorbate_model.pkl")

# 🧪 Page setup
st.set_page_config(page_title="Preservative Predictor", layout="centered")
st.title("🧪 Benzoate & Sorbate Estimator")

# 🎛️ Manual Input Section
st.subheader("🔬 Manual UV Absorbance Input")
st.write("Enter UV absorbance readings to predict preservative concentrations (ppm)")

abs_280 = st.number_input("Absorbance at 280 nm", value=0.42, step=0.01)
abs_320 = st.number_input("Absorbance at 320 nm", value=0.35, step=0.01)
abs_400 = st.number_input("Absorbance at 400 nm", value=0.28, step=0.01)

abs_280_320_ratio = abs_280 / abs_320 if abs_320 != 0 else 0.0

if st.button("🔮 Predict Benzoate & Sorbate"):
    sample = pd.DataFrame([{
        "abs_280": abs_280,
        "abs_320": abs_320,
        "abs_400": abs_400,
        "abs_280_320_ratio": abs_280_320_ratio
    }])
    
    benzoate_pred = benzoate_model.predict(sample)[0]
    sorbate_pred = sorbate_model.predict(sample)[0]

    st.success(f"✅ Benzoate: **{benzoate_pred:.2f} ppm**")
    st.success(f"✅ Sorbate: **{sorbate_pred:.2f} ppm**")
    
    
# 📂 File Upload Section
st.subheader("📂 Upload Sensor Data (CSV)")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        expected = {"abs_280", "abs_320", "abs_400"}
        if not expected.issubset(df.columns):
            st.error(f"CSV must contain: {', '.join(expected)}")
        else:
            df["abs_280_320_ratio"] = df["abs_280"] / df["abs_320"].replace(0, np.nan)
            df = df.dropna()

            X = df[["abs_280", "abs_320", "abs_400", "abs_280_320_ratio"]]
            df["benzoate_ppm"] = benzoate_model.predict(X)
            df["sorbate_ppm"] = sorbate_model.predict(X)

            # ✅ Highlight unsafe rows
            def highlight_unsafe(row):
                benzoate_flag = row["benzoate_ppm"] > 150
                sorbate_flag = row["sorbate_ppm"] > 250
                if benzoate_flag or sorbate_flag:
                    return ["background-color: #ffcccc"] * len(row)
                return [""] * len(row)

            styled_df = df.style.apply(highlight_unsafe, axis=1)
            st.success("✅ Batch predictions completed")
            st.dataframe(styled_df, use_container_width=True)

            # ✅ Bar chart
            st.subheader("📊 Preservative Levels Comparison")
            st.bar_chart(df[["benzoate_ppm", "sorbate_ppm"]])

            # ✅ Download button
            st.download_button(
                label="📥 Download Predictions",
                data=df.to_csv(index=False),
                file_name="predicted_preservatives.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")

