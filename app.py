import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, time as dt_time
import time
import sys
import os
import sqlite3

# --- SYSTEM PATCHES ---
try:
    import imghdr
except ImportError:
    import types
    m = types.ModuleType("imghdr"); m.what = lambda x, h=None: None
    sys.modules["imghdr"] = m

sys.path.append(os.path.dirname(__file__))
from src.brain import fetch_cpu_metrics, analyze_health
from src.healer import trigger_healing, init_db

# Ensure DB exists on startup
init_db()

# --- UI CONFIG ---
st.set_page_config(
    page_title="Sentinel AIOps | Mission Control", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED PROFESSIONAL STYLING (CSS) ---
st.markdown("""
    <style>
        /* Base Background */
        .stApp { background: linear-gradient(135deg, #0d1117 0%, #010409 100%); color: #c9d1d9; }
        
        /* Metric Card Styling */
        [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #58a6ff !important; }
        [data-testid="stMetricLabel"] { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.1rem; color: #8b949e; }
        
        /* Glassmorphism Containers */
        .main-card {
            background: rgba(22, 27, 34, 0.7);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] { background-color: #0d1117 !important; border-right: 1px solid #30363d; }
        
        /* Dataframe Styling */
        .stDataFrame { border: 1px solid #30363d; border-radius: 8px; }
        
        /* Custom Header Gradient */
        .header-text {
            background: -webkit-linear-gradient(#58a6ff, #1f6feb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 2.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# --- DB UTILS ---
DB_PATH = "sentinel_ops.db"
def get_historical_logs(filter_dt):
    if not os.path.exists(DB_PATH): return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT timestamp, process_name, pid, cpu_load, status FROM incidents WHERE timestamp >= ?"
    df = pd.read_sql_query(query, conn, params=(filter_dt.strftime('%Y-%m-%d %H:%M:%S'),))
    conn.close()
    return df

# --- DATA PROCESSING (Observe) ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Time", "CPU"])
if 'heal_logs' not in st.session_state:
    st.session_state.heal_logs = []

current_cpu = fetch_cpu_metrics()
now = datetime.now()
new_row = pd.DataFrame([{"Time": now, "CPU": current_cpu}])
st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True).tail(40)

# --- AI ANALYSIS (Orient) ---
cpu_list = st.session_state.history["CPU"].tolist()
is_anomaly, confidence = analyze_health(cpu_list)

is_learning = len(cpu_list) < 15
if is_learning:
    status_label = "LEARNING"
    status_color = "#8b949e"
    is_anomaly = False
else:
    status_label = "ANOMALY" if is_anomaly else "HEALTHY"
    status_color = "#f85149" if is_anomaly else "#3fb950"

# Fail-safe Trigger (Decide)
if current_cpu > 90.0 and not is_learning:
    is_anomaly, confidence = True, 100.0
    status_label, status_color = "CRITICAL", "#f85149"

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.markdown("<h2 style='color:#58a6ff;'>🛡️ Sentinel Control</h2>", unsafe_allow_html=True)
    st.divider()
    st.write("### AI Engine Status")
    st.info(f"OODA Cycle: Active\nFrequency: 2.0s")
    
    st.divider()
    st.write("### Operational Overrides")
    auto_heal = st.toggle("Autonomous Remediation", value=True)
    if st.button("🗑️ Purge Local Session Logs"):
        st.session_state.heal_logs = []
        st.rerun()

# --- MAIN DASHBOARD ---
st.markdown(f'<p class="header-text">SENTINEL AIOPS ENGINE</p>', unsafe_allow_html=True)
st.caption(f"Hardware Telemetry Feed • Active Session: {now.strftime('%H:%M:%S')}")

# KPI Row
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("System Load", f"{current_cpu}%")
with m2:
    st.markdown(f"**Status** \n<span style='color:{status_color}; font-size:24px; font-weight:bold;'>{status_label}</span>", unsafe_allow_html=True)
with m3:
    st.metric("Detection Confidence", f"{confidence}%" if not is_learning else "LEARNING...")
with m4:
    st.metric("Remediations", len(st.session_state.heal_logs))

st.divider()

# Central Telemetry and Pipeline
col_graph, col_pipeline = st.columns([2, 1])

with col_graph:
    st.subheader("🛰️ Real-time Hardware Telemetry")
    fig = px.area(st.session_state.history, x="Time", y="CPU", color_discrete_sequence=['#1f6feb'])
    fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(
        showgrid=False, 
        tickfont=dict(color="#8b949e")  # Fixed from 'font' to 'tickfont'
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor="#30363d", 
        range=[0, 105], 
        tickfont=dict(color="#8b949e")  # Fixed from 'font' to 'tickfont'
    )
)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_pipeline:
    st.subheader("🩹 Remediation Log")
    if is_learning:
        st.warning(f"AI Brain Training: {len(cpu_list)}/15 points")
    elif is_anomaly:
        st.error(f"Anomaly Detected: Triggering Act Phase...")
        if auto_heal:
            with st.spinner("Surgical termination in progress..."):
                killed = trigger_healing()
                if killed:
                    for k in killed:
                        st.session_state.heal_logs.append({"Timestamp": now.strftime("%H:%M:%S"), "Process": k['name']})
                    st.toast("System Stabilized", icon="✅")
    else:
        st.success("System Healthy: Nominal CPU patterns.")

# --- HISTORICAL AUDIT ---
st.divider()
st.subheader("📋 Historical Incident Archive (SQLite)")
expander = st.expander("Filter Archive Parameters")
with expander:
    f_c1, f_c2 = st.columns(2)
    f_date = f_c1.date_input("Audit Date", value=now.date())
    f_time = f_c2.time_input("Start Threshold", value=dt_time(0, 0))
    filter_dt = datetime.combine(f_date, f_time)

history_df = get_historical_logs(filter_dt)
if not history_df.empty:
    st.dataframe(history_df.iloc[::-1], use_container_width=True, hide_index=True)
    csv = history_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export CSV Audit Report", data=csv, file_name=f"sentinel_report_{now.date()}.csv", mime="text/csv")
else:
    st.info("No historical records detected for the selected window.")

time.sleep(2)
st.rerun()