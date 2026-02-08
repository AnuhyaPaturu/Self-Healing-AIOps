import psutil
import sqlite3
from datetime import datetime

DB_PATH = "sentinel_ops.db"

def init_db():
    """Initializes the SQLite database for permanent log storage."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            process_name TEXT,
            pid INTEGER,
            cpu_load TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_incident(name, pid, cpu):
    """Saves remediation details to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO incidents (timestamp, process_name, pid, cpu_load, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), name, pid, f"{cpu}%", "Terminated"))
    conn.commit()
    conn.close()

def trigger_healing(target_process_name="yes", cpu_threshold=80.0):
    init_db()
    healed_items = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            p_info = proc.info
            # Target specific process or any process exceeding threshold
            if p_info['name'] == target_process_name or (p_info['cpu_percent'] or 0) > cpu_threshold:
                save_incident(p_info['name'], p_info['pid'], p_info['cpu_percent'])
                proc.terminate()
                healed_items.append({"pid": p_info['pid'], "name": p_info['name'], "cpu": p_info['cpu_percent']})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return healed_items