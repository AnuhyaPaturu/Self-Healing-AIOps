import time
from src.brain import fetch_cpu_metrics, analyze_health
from src.healer import trigger_healing

def run_platform():
    print("🚀 Self-Healing AIOps Platform Started...")
    cpu_history = []
    
    while True:
        try:
            # 1. SENSE: Get current metrics
            current_cpu = fetch_cpu_metrics()
            cpu_history.append(current_cpu)
            
            if len(cpu_history) > 50:
                cpu_history.pop(0)

            # 2. THINK: Ask the AI if this is an anomaly
            is_anomaly = analyze_health(cpu_history)
            
            # 3. ACT: If the AI is worried, heal the system
            if is_anomaly:
                print(f"⚠️ Warning: Abnormal CPU detected ({current_cpu:.2f}%)")
                trigger_healing()
                # Clear history after healing so the AI 'resets' its expectation
                cpu_history = [] 
            else:
                print(f"🟢 System Healthy: CPU at {current_cpu:.2f}%")

            time.sleep(5) # Wait 5 seconds before next check
            
        except Exception as e:
            print(f"❌ Error in loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run_platform()