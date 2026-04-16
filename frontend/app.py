import streamlit as st
import requests
import time

API_BASE = "http://3.110.119.189:8000"

st.set_page_config(page_title="ML Serving Platform", layout="centered")

# ----------------------------
# SESSION STATE
# ----------------------------
if "job_id" not in st.session_state:
    st.session_state.job_id = None

# ----------------------------
# HEADER
# ----------------------------
st.title("🚀 ML Model Serving Platform")
st.markdown("Async ML inference with job tracking")

st.divider()

# ----------------------------
# TABS
# ----------------------------
tab1, tab2, tab3 = st.tabs(["🤖 Inference", "📦 Upload Model", "🩺 Health"])

# ============================
# 🔹 COMMON FUNCTION
# ============================
def fetch_models():
    try:
        res = requests.get(f"{API_BASE}/models/list")
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return []

# ============================
# 🤖 TAB 1: INFERENCE
# ============================
with tab1:

    models_data = fetch_models()
    model_names = list(set([m["name"] for m in models_data])) if models_data else ["iris"]

    col1, col2 = st.columns(2)

    with col1:
        selected_model = st.selectbox("Select Model", model_names)

    with col2:
        versions = [m["version"] for m in models_data if m["name"] == selected_model]
        if not versions:
            versions = ["v1"]

        selected_version = st.selectbox("Select Version", versions)

    st.markdown("### 🔢 Input Features")

    features_input = st.text_input(
        "Enter features (comma separated)",
        placeholder="e.g. 5.1,3.5,1.4,0.2"
    )

    st.caption("Example: 5.1,3.5,1.4,0.2")

    if st.button("🔮 Predict"):

        if not features_input:
            st.error("Please enter features")
            st.stop()

        try:
            features = [float(x.strip()) for x in features_input.split(",")]

            if len(features) != 4:
                st.error("Model requires exactly 4 features")
                st.stop()

        except:
            st.error("Invalid input format")
            st.stop()

        payload = {
            "model_name": selected_model,
            "version": selected_version,
            "features": features
        }

        try:
            with st.spinner("Sending request..."):
                res = requests.post(f"{API_BASE}/inference/predict", json=payload)

            if res.status_code != 200:
                st.error("Failed to create job")
                st.write(res.text)
                st.stop()

            job_id = res.json()["job_id"]
            st.session_state.job_id = job_id

            st.success(f"🆔 Job Created: {job_id}")
            st.divider()

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.stop()

    # ----------------------------
    # POLLING
    # ----------------------------
    if st.session_state.job_id:

        job_id = st.session_state.job_id

        st.markdown("### 📡 Tracking Job Status")

        status_placeholder = st.empty()
        result_placeholder = st.empty()

        status = "pending"

        with st.spinner("Processing..."):
            while status not in ["completed", "failed"]:
                time.sleep(2)

                try:
                    result = requests.get(f"{API_BASE}/results/{job_id}").json()
                except:
                    st.error("Error fetching result")
                    break

                status = result.get("status", "unknown")
                status_placeholder.info(f"⏳ Status: {status.upper()}")

        if status == "completed":
            result_placeholder.success(f"✅ Prediction: {result['prediction']}")
            st.session_state.job_id = None

        elif status == "failed":
            result_placeholder.error(f"❌ Error: {result.get('error', 'Unknown')}")
            st.session_state.job_id = None

# ============================
# 📦 TAB 2: MODEL UPLOAD (FIXED)
# ============================
with tab2:

    from pathlib import Path

    st.header("📦 Register New Model")

    MODEL_DIR = Path("/models")   # 🔥 FIXED PATH

    file = st.file_uploader("Upload .pkl model")
    name = st.text_input("Model Name")
    version = st.text_input("Version")
    accuracy = st.number_input("Accuracy", min_value=0.0, max_value=1.0, step=0.01)
    framework = st.selectbox("Framework", ["sklearn"])

    if st.button("Upload Model"):

        if not file or not name or not version:
            st.error("All fields required")
            st.stop()

        if not file.name.endswith(".pkl"):
            st.error("Only .pkl files allowed")
            st.stop()

        try:
            # ✅ Ensure folder exists
            MODEL_DIR.mkdir(parents=True, exist_ok=True)

            filename = f"{name}_{version}.pkl"
            file_path = MODEL_DIR / filename

            if file_path.exists():
                st.error("Model version already exists")
                st.stop()

            # ✅ Save file to SHARED VOLUME
            with open(file_path, "wb") as f:
                f.write(file.getvalue())

            st.success(f"📁 Model saved: {file_path}")

            # ✅ Register metadata
            payload = {
                "name": name,
                "version": version,
                "framework": framework,
                "accuracy": float(accuracy)
            }

            with st.spinner("Registering model..."):
                res = requests.post(
                    f"{API_BASE}/models/register",
                    json=payload
                )

            st.write("Status:", res.status_code)
            st.write("Response:", res.text)

            if res.status_code == 200:
                st.success("✅ Model registered successfully")
                st.rerun()
            else:
                st.error("❌ Registration failed")

        except Exception as e:
            st.error(f"Upload failed: {str(e)}")

# ============================
# 🩺 TAB 3: HEALTH
# ============================
with tab3:

    st.header("🩺 System Health")

    if st.button("Check Health"):

        try:
            db = requests.get(f"{API_BASE}/health/db").json()
            kafka = requests.get(f"{API_BASE}/health/kafka").json()

            st.subheader("Database")
            if db["status"] == "healthy":
                st.success("DB Healthy")
            else:
                st.error(db)

            st.subheader("Kafka")
            if kafka["status"] == "healthy":
                st.success("Kafka Healthy")
                st.write("Topics:", kafka.get("topics", []))
            else:
                st.error(kafka)

        except Exception as e:
            st.error(f"Health check failed: {str(e)}")