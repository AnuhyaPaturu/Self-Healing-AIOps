# Sentinel AIOps: Autonomous Self-Healing Engine 🤖🛡️

An AI-driven system that observes, detects, and heals infrastructure anomalies in real-time.

## 🌟 Project Overview
This platform is a **Closed-Loop AIOps engine** designed to reduce system downtime and manual intervention. It integrates real-time hardware telemetry with Machine Learning to identify "invisible" system failures and automatically execute remediation scripts to restore system health.

## 🏗️ Technical Architecture (OODA Loop)
The system follows the **Observe-Orient-Decide-Act** framework:
* **Observe**: Real-time metrics are scraped from the Mac host using a native **Node Exporter** and **Prometheus**.
* **Orient**: Data is processed in Python and passed to an **Isolation Forest** (Unsupervised ML) model to establish a behavioral baseline.
* **Decide**: The engine uses hybrid logic—ML anomaly scores plus a **90% CPU fail-safe**—to trigger remediation.
* **Act**: The **Remediation Engine** uses `psutil` to perform surgical process termination.



## 🚀 Key Features
* **Machine Learning Brain**: Uses an Isolation Forest model to detect deviations after a 15-point baseline is established.
* **Professional Dashboard**: A high-performance Streamlit UI featuring **Glassmorphism** styling and real-time Plotly telemetry.
* **Persistent Incident Archive**: Every automated "heal" is logged into a **SQLite3** database for permanent auditing and reporting.
* **Precision Remediation**: Identifies specific high-CPU PIDs and terminates them to ensure minimal system disruption.

## 📂 Project Structure
```plaintext
├── app.py              # Streamlit Dashboard (UI & Logic Orchestrator)
├── docker-compose.yml  # Infrastructure (Prometheus)
├── prometheus.yml      # Scrape configurations for host.docker.internal
├── sentinel_ops.db     # SQLite Database (Persistent Incident Logs)
├── src/
│   ├── brain.py        # ML Logic (Isolation Forest & Telemetry Fetching)
│   ├── healer.py       # Remediation Logic (psutil & SQLite Integration)
└── chaos.sh            # Stress-test script to simulate failures

🛠️ Installation & Setup
1. Prerequisites
Install Node Exporter natively on your Mac: brew install node_exporter.

Start Node Exporter: brew services start node_exporter.

2. Launch Infrastructure
Start the Prometheus container to begin scraping metrics:

Bash
docker-compose up -d

3. Run the Dashboard
Ensure your virtual environment is active and dependencies are installed, then launch the app:

Bash
pip install -r requirements.txt
streamlit run app.py


👨‍💻 Author
Anuhya Paturu Full Stack Engineer | MS in Computer Science


---

### How to Run the Code to See the Dashboard
To see your professional dashboard in action and verify the self-healing logic, follow these steps:

1.  **Start Sensors**: Ensure `node_exporter` is running natively on your Mac (`brew services start node_exporter`) so Prometheus has real data to read.
2.  **Start Prometheus**: Run `docker-compose up -d`.
3.  **Launch App**: Run `streamlit run app.py`. Your browser will open to `http://localhost:8501`.
4.  **Establish Baseline**: Wait for the dashboard to collect **15/15 points** (approx. 30 seconds). The status must change from `🟡 LEARNING` to `🟢 HEALTHY`.
5.  **Trigger Chaos**: In a separate terminal, run `./chaos.sh`.
6.  **Observe the Heal**: Watch the dashboard. The graph will spike, the AI will trigger an **ANOMALY** state, and the "Remediation Log" will show the process being killed.

**Would you like me to help you generate the `requirements.txt` file now to make sure it includes `scikit-learn` and `plotly`?**
