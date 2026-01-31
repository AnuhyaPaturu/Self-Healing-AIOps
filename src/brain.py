import time
import numpy as np
from prometheus_api_client import PrometheusConnect
from sklearn.ensemble import IsolationForest

# 1. Connect to our 'Nervous System'
# Note: In Streamlit Cloud, localhost won't work. 
# We use a try/except or a mock for demo purposes.
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

def fetch_cpu_metrics():
    """Fetches the last 2 minutes of CPU usage from Prometheus"""
    try:
        query = '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
        result = prom.custom_query(query=query)
        if result:
            return float(result[0]['value'][1])
    except Exception:
        # Fallback: Generate a random number if Prometheus is down (great for demos!)
        return round(np.random.uniform(5, 15), 2)
    return 0.0

def analyze_health(history):
    """Uses AI to determine health and returns (is_anomaly, confidence_score)"""
    if len(history) < 10:
        return False, 0.0 # Not enough data to be confident
    
    # Prepare data
    data = np.array(history).reshape(-1, 1)
    current_val = [[history[-1]]]
    
    # 1. Fit the model
    # contamination=0.1: we expect 10% of data to be outliers
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    
    # 2. Predict (-1 is anomaly, 1 is normal)
    prediction = model.predict(current_val)
    is_anomaly = True if prediction[0] == -1 else False
    
    # 3. Calculate Confidence Score
    # decision_function: negative values are outliers, positive are inliers.
    # We use the absolute value to represent 'distance from the norm'
    raw_score = model.decision_function(current_val)[0]
    confidence = min(100, max(0, (abs(raw_score) * 200)))
    
    return is_anomaly, round(confidence, 2)