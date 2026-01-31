import time
import numpy as np
from prometheus_api_client import PrometheusConnect
from sklearn.ensemble import IsolationForest

# 1. Connect to our 'Nervous System'
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

def fetch_cpu_metrics():
    """Fetches the last 2 minutes of CPU usage from Prometheus"""
    # This PromQL query calculates CPU usage percentage
    query = '100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
    result = prom.custom_query(query=query)
    
    if result:
        # Extract the number from the Prometheus response
        return float(result[0]['value'][1])
    return 0.0

def analyze_health(history):
    """Uses AI to determine if the current CPU is an anomaly"""
    if len(history) < 10:
        return False # Wait until we have enough data to 'learn'
    
    # Reshape data for the AI model
    data = np.array(history).reshape(-1, 1)
    
    # IsolationForest: Contamination 0.1 means we expect 10% of data to be 'weird'
    model = IsolationForest(contamination=0.2)
    model.fit(data)
    
    # Predict (-1 is an anomaly, 1 is normal)
    prediction = model.predict([[history[-1]]])
    return prediction[0] == -1

# Simple Test Loop
if __name__ == "__main__":
    print("🧠 Brain is warming up... collecting data...")
    cpu_history = []
    
    while True:
        current_cpu = fetch_cpu_metrics()
        cpu_history.append(current_cpu)
        
        # Keep only the last 50 data points to save memory
        if len(cpu_history) > 50:
            cpu_history.pop(0)
            
        is_anomaly = analyze_health(cpu_history)
        
        status = "🚨 ANOMALY" if is_anomaly else "✅ NORMAL"
        print(f"Current CPU: {current_cpu:.2f}% | Status: {status}")
        
        time.sleep(5)