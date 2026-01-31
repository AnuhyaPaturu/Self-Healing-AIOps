# --- EMERGENCY PATCH FOR PYTHON 3.13 ---
import sys
try:
    import imghdr
except ImportError:
    import types
    m = types.ModuleType("imghdr")
    m.what = lambda x, h=None: None
    sys.modules["imghdr"] = m
# ---------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os

# Ensure the 'src' folder can be found
sys.path.append(os.path.dirname(__file__))

# Import your custom logic
from src.brain import fetch_cpu_metrics, analyze_health, get_confidence_score
from src.healer import trigger_healing

# 1. Page Setup
st.set_page_config(page_title="AIOps Control Center", layout="wide")
st.title("🤖 AIOps Self-Healing Dashboard")

# 2. Sidebar & Session State Initialization
st.sidebar.header("Platform Settings")
check_interval = st.sidebar.slider("Scan Frequency (seconds)", 2, 10, 5)
heal_threshold = st.sidebar.slider("AI Confidence Threshold (%)", 50, 95, 85)

if 'history' not in st.session_state:
    st.session_state.history = []
if 'heal_logs' not in st.session_state:
    st.session_state.heal_logs = []

# 3. Layout Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 System Vitals")
    chart_placeholder = st.empty()

with col2:
    st.subheader("🧠 AI Diagnosis")
    status_placeholder = st.empty()
    confidence_placeholder = st.empty() # New placeholder for confidence

# 4. Live Data Fetching
current_cpu = fetch_cpu_metrics()
st.session_state.history.append({"Time": pd.Timestamp.now(), "CPU": current_cpu})

if len(st.session_state.history) > 30:
    st.session_state.history.pop(0)

df = pd.DataFrame(st.session_state.history)

# Update Graph
fig = px.line(df, x="Time", y="CPU", range_y=[0, 100], template="plotly_dark")
chart_placeholder.plotly_chart(fig, use_container_width=True)

# 5. AI Logic & Confidence Scoring
cpu_values = [item["CPU"] for item in st.session_state.history]

# analyze_health now returns (is_anomaly, confidence_score)
is_anomaly, confidence = analyze_health(cpu_values)

with status_placeholder.container():
    if is_anomaly:
        st.error(f"🚨 ANOMALY DETECTED ({current_cpu}%)")
        st.metric("AI Confidence Score", f"{confidence}%")
        
        # Automatic Healing Logic with Confidence Gate
        if confidence >= heal_threshold:
            trigger_healing()
            st.session_state.heal_logs.append({
                "Timestamp": pd.Timestamp.now().strftime("%H:%M:%S"),
                "Event": f"AI Auto-Heal (Conf: {confidence}%)",
                "Result": "Success"
            })
            st.success("✅ Confidence high: Remediation executed.")
        else:
            st.warning("⚠️ Confidence low: Remediation paused.")
    else:
        st.success(f"✅ SYSTEM HEALTHY ({current_cpu}%)")
        st.metric("AI Confidence Score", f"{confidence}%")

# 6. Healing History Table
st.markdown("---")
st.subheader("📋 Healing Audit Trail")
if st.session_state.heal_logs:
    log_df = pd.DataFrame(st.session_state.heal_logs[::-1])
    st.table(log_df)
else:
    st.info("No healing events recorded yet.")

# 7. Wait and Rerun
time.sleep(check_interval)
st.rerun()