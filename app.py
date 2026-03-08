import streamlit as st
import joblib
import numpy as np

# Load models and encoder
binary_model = joblib.load("binary_model.pkl")
multi_model = joblib.load("best_nids_model.pkl")
label_encoder = joblib.load("new_label_encoder.pkl")

def get_user_input():
    st.subheader("🔧 Input Network Features (40 values)")
    features = []
    for i in range(1, 41):
        val = st.number_input(f"Feature {i}", min_value=0.0, value=0.0, step=0.1, key=f"f{i}")
        features.append(val)
    return np.array(features).reshape(1, -1)

st.set_page_config(page_title="NIDS App", layout="centered")
st.title("🛡️ Network Intrusion Detection System (NIDS)")
st.markdown("This model predicts whether network traffic is **Benign**, or a specific type of **Attack**.")

# Mode selection
mode = st.radio("🔍 Choose Detection Mode", ["Binary (Benign vs Malicious)", "Multi-Class (Attack Type)"])

input_data = get_user_input()

if st.button("🔎 Predict"):
    if input_data.shape != (1, 40):
        st.error("❌ Please ensure exactly 40 features are entered.")
    else:
        if mode == "Binary (Benign vs Malicious)":
            prediction = binary_model.predict(input_data)[0]
            result = "Benign" if prediction == 0 else "Malicious"
            st.success(f"🔒 Prediction: **{result}**")
        else:
            prediction = multi_model.predict(input_data)[0]
            attack_type = label_encoder.inverse_transform([prediction])[0]
            st.success(f"🚨 Attack Type Detected: **{attack_type}**")
