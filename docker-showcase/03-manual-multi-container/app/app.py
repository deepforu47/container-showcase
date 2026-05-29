from flask import Flask
from datetime import datetime
import os
import socket
import time
import psycopg2

app = Flask(__name__)

# Fetch configuration variables injected at runtime via environment variables
DB_HOST = os.environ.get("DB_HOST", "postgres-db-host")
DB_NAME = os.environ.get("DB_NAME", "analytics_db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "supersecurepassword")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            print(f"Database not ready yet ({e}). Retrying in 2s... ({5 - retries}/5)")
            time.sleep(2)
    raise Exception("Could not connect to the database after multiple retries.")

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visit_logs (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            container_id VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container_id = socket.gethostname()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO visit_logs (timestamp, container_id) VALUES (%s, %s);",
            (datetime.now(), container_id)
        )
        conn.commit()
        
        cur.execute("SELECT COUNT(*) FROM visit_logs;")
        total_hits = cur.fetchone()[0]
        
        cur.close()
        conn.close()
    except Exception as e:
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #fee2e2; border: 1px solid #fca5a5;">
            <h1 style="color: #dc2626; margin-top: 0;">❌ Database Connection Error</h1>
            <p style="font-size: 16px;">The application was unable to query the database.</p>
            <pre style="background: #f87171; color: white; padding: 15px; border-radius: 6px; overflow-x: auto;">{str(e)}</pre>
        </div>
        """
    
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #f8fafc;">
        <h1 style="color: #2496ed; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            🐳 Manual Multi-Container Setup
        </h1>
        <p style="font-size: 16px;"><b>Current Server Time:</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        <p style="font-size: 16px;"><b>Web Node Hostname:</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        
        <div style="background-color: #f3e8ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
            <span style="font-size: 14px; color: #6b21a8; font-weight: bold; text-transform: uppercase;">Database Tracked Visits</span>
            <h2 style="font-size: 48px; color: #7c3aed; margin: 10px 0;">{total_hits}</h2>
            <p style="font-size: 13px; color: #7c3aed; margin: 0;">Every visit is recorded in an isolated Postgres container!</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p style="color: #64748b; font-style: italic; font-size: 14px;">Demonstrating bridge networks and storage persistence across lifecycles.</p>
    </div>
    """

if __name__ == '__main__':
    # Initialize schema on startup
    init_db()
    app.run(host='0.0.0.0', port=5000)
