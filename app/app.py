import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px

st.set_page_config(page_title="AI Threat Detection", layout="wide")

st.title("🛡️ AI Cybersecurity Threat Detection")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "threat_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "UNSW_NB15_testing-set.csv")

# Load model safely
@st.cache_resource
def load_assets():
    try:
        model = joblib.load(MODEL_PATH)
        encoders = joblib.load(ENCODER_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, encoders, scaler
    except:
        return None, None, None

model, encoders, scaler = load_assets()

# Load data
try:
    data = pd.read_csv(DATA_PATH).sample(50)
except:
    st.error("Dataset not found!")
    st.stop()

# Button
if st.button("▶ Run Detection"):

    if model is None:
        st.error("Model not loaded properly!")
        st.stop()

    malicious_count = 0
    threat_history = []

    for i, row in data.iterrows():

        features = row.drop(['label', 'attack_cat', 'id'], errors='ignore')

        for col in ['proto', 'service', 'state']:
            if col in features:
                try:
                    features[col] = encoders[col].transform([str(features[col])])[0]
                except:
                    features[col] = -1

        X = pd.DataFrame([features])
        X_scaled = scaler.transform(X)

        pred = model.predict(X_scaled)[0]

        if pred == 1:
            malicious_count += 1

        threat_history.append(malicious_count)

    # -----------------------------
    # SHOW GRAPHS (FINAL)
    # -----------------------------
    st.subheader("📊 Threat Analytics")

    # Pie Chart
    pie_df = pd.DataFrame({
        "Type": ["Normal", "Attack"],
        "Count": [len(data) - malicious_count, malicious_count]
    })

    st.plotly_chart(px.pie(pie_df, names="Type", values="Count"),
                    use_container_width=True)

    # Line Chart
    line_df = pd.DataFrame({
        "Time": list(range(len(threat_history))),
        "Threat Count": threat_history
    })

    st.plotly_chart(px.line(line_df, x="Time", y="Threat Count"),
                    use_container_width=True)

    st.success("✅ Detection Completed + Graphs Displayed!")
    # AI Cybersecurity Threat Detection Project