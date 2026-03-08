
import streamlit as st
import joblib
import numpy as np

# Load models and label encoder
binary_model = joblib.load("binary_model.pkl")
multi_model = joblib.load("best_nids_model.pkl")
label_encoder = joblib.load("new_label_encoder.pkl")

# Function to get user input
def get_user_input():
    st.subheader("Input 40 Feature Values")
    features = []
    for i in range(1, 41):
        val = st.number_input(f"Feature {i}", min_value=0.0, value=0.0, step=0.1)
        features.append(val)
    return np.array(features).reshape(1, -1)

# Title
st.title("🛡️ Network Intrusion Detection System (NIDS)")
st.markdown("Predicts whether network traffic is malicious, and if so, identifies the type of attack.")

# Mode Selection
mode = st.radio("Choose Classification Type", ["Binary (Benign vs Attack)", "Multi-Class (Attack Type)"])

# Input
input_data = get_user_input()

# Prediction
if st.button("Predict"):
    if mode == "Binary (Benign vs Attack)":
        prediction = binary_model.predict(input_data)[0]
        result = "Benign" if prediction == 0 else "Malicious"
        st.success(f"🚨 Prediction: **{result}**")
    else:
        prediction = multi_model.predict(input_data)[0]
        attack_type = label_encoder.inverse_transform([prediction])[0]
        st.success(f"🚨 Attack Type Detected: **{attack_type}**")
