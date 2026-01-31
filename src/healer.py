import subprocess
import os

def trigger_healing():
    """Executes the shell script to fix the system"""
    print("🩹 Healer: Attempting to resolve the anomaly...")
    
    # Get the path to the script
    script_path = os.path.join(os.getcwd(), "scripts", "fix_cpu.sh")
    
    try:
        # Run the shell script
        result = subprocess.run([script_path], capture_output=True, text=True)
        
        # Log the output of the script to the console
        print(result.stdout)
        return True
    except Exception as e:
        print(f"❌ Healer Failed: {e}")
        return False

# Quick Test
if __name__ == "__main__":
    print("Testing Healer independently...")
    trigger_healing()