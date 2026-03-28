import streamlit as st
import requests

# ---------------- CONFIG ----------------
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="💳",
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
    <style>
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💳 Real-Time Fraud Detection System")
st.markdown("### Production-Grade ML Deployment Interface")
st.divider()

# ---------------- INPUT SECTION ----------------
st.subheader("🔢 Transaction Features Input")

# 1. Create Top Row for Time and Amount (The Scaler needs these!)
top_col1, top_col2 = st.columns(2)
with top_col1:
    time_val = st.number_input("Time (Seconds from first transaction)", value=0.0, help="Order Position 1")
with top_col2:
    amount_val = st.number_input("Transaction Amount ($)", value=0.0, format="%.2f", help="Order Position 30")

st.markdown("---")
st.write("**PCA Components (V1 to V28)**")

# 2. Create Grid for V1 to V28
v_features = []
v_cols = st.columns(4) # 4 columns for a cleaner look

for i in range(1, 29):
    with v_cols[(i-1) % 4]:
        val = st.number_input(f"V{i}", value=0.0, format="%.5f")
        v_features.append(val)

st.divider()

# ---------------- PREDICT BUTTON ----------------
if st.button("🚀 Analyze Transaction"):
    
    # --- CRITICAL FIX: RECONSTRUCT THE LIST IN SCALER ORDER ---
    # According to your check: 1. Time, 2-29. V1-V28, 30. Amount
    ordered_features = [time_val] + v_features + [amount_val]
    
    with st.spinner("Processing transaction..."):
        try:
            response = requests.post(
                API_URL,
                json={"features": ordered_features}, # Send the ordered list
                timeout=5
            )

            if response.status_code != 200:
                st.error(f"API Error: {response.text}")
            else:
                data = response.json()
                result = data["result"]
                
                prediction = result["prediction"]
                prob = result["probability"]
                confidence = result["confidence_level"]

                # ---------------- RESULTS DISPLAY ----------------
                st.subheader("📊 Prediction Result")
                col1, col2, col3 = st.columns(3)

                with col1:
                    if prediction == "FRAUD":
                        st.error(f"🚨 ALERT: {prediction}")
                    else:
                        st.success(f"✅ CLEAN: {prediction}")

                with col2:
                    st.metric("Fraud Probability", f"{prob:.4f}")

                with col3:
                    st.metric("Confidence Level", confidence)

                st.progress(min(max(prob, 0.0), 1.0))

        except requests.exceptions.RequestException as e:
            st.error(f"Connection Error: Could not reach FastAPI server at {API_URL}. Ensure uvicorn is running!")