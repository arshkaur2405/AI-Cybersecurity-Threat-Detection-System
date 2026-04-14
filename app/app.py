import streamlit as st
import pandas as pd
import joblib
import time
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Threat Detection SOC", layout="wide")

st.title("🛡️ AI-Powered Cybersecurity Threat Detection System")

# -----------------------------
# PATH HANDLING (IMPORTANT FIX)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "threat_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "UNSW_NB15_training-set.csv")

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_assets():
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, encoders, scaler

model, encoders, scaler = load_assets()

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("⚙️ Simulation Settings")
sim_speed = st.sidebar.slider("Simulation Speed (seconds)", 0.1, 3.0, 1.0)

# -----------------------------
# LOAD DATA
# -----------------------------
data = pd.read_csv(DATA_PATH).sample(50)

# -----------------------------
# UI METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)
total_packets = col1.empty()
threat_count = col2.empty()
system_status = col3.empty()

# -----------------------------
# LOG DISPLAY
# -----------------------------
st.subheader("📡 Live Network Traffic Logs")
log_placeholder = st.empty()

# -----------------------------
# SIMULATION BUTTON
# -----------------------------
logs = []
malicious_count = 0

if st.button("▶ Start Simulation"):

    for i, row in data.iterrows():

        # -----------------------------
        # PREPROCESS SINGLE ROW
        # -----------------------------
        features = row.drop(['label', 'attack_cat', 'id'], errors='ignore')

        # Encode categorical columns
        for col in ['proto', 'service', 'state']:
            if col in features:
                try:
                    features[col] = encoders[col].transform([str(features[col])])[0]
                except:
                    features[col] = -1  # unknown value

        # Convert to DataFrame
        X_input = pd.DataFrame([features])

        # Scale
        X_scaled = scaler.transform(X_input)

        # -----------------------------
        # PREDICTION
        # -----------------------------
        prediction = model.predict(X_scaled)[0]
        confidence = model.predict_proba(X_scaled).max()

        status = "⚠️ ATTACK" if prediction == 1 else "✅ NORMAL"

        if prediction == 1:
            malicious_count += 1
            st.error("🚨 THREAT DETECTED!")

        # -----------------------------
        # LOG ENTRY
        # -----------------------------
        log_entry = {
            "Time": time.strftime("%H:%M:%S"),
            "Protocol": row.get("proto", "N/A"),
            "Service": row.get("service", "N/A"),
            "Status": status,
            "Confidence": f"{confidence:.2%}"
        }

        logs.insert(0, log_entry)

        # -----------------------------
        # UPDATE METRICS
        # -----------------------------
        total_packets.metric("Total Packets", i + 1)
        threat_count.metric("Threats Detected", malicious_count)
        system_status.metric("System Status", "ACTIVE 🟢")

        # -----------------------------
        # SHOW LOG TABLE
        # -----------------------------
        log_placeholder.dataframe(pd.DataFrame(logs).head(10))

        time.sleep(sim_speed)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.markdown("🔐 Built with AI for Cybersecurity Threat Detection | Student Project")