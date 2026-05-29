from flask import Flask
from datetime import datetime
import os
import socket
import time
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres-service")
DB_NAME = os.environ.get("DB_NAME", "analytics_db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "supersecurepassword")
APP_COLOR = os.environ.get("APP_COLOR", "#f8fafc")
APP_ENV = os.environ.get("APP_ENV", "Production-Release")
SECRET_MESSAGE = os.environ.get("SECRET_MESSAGE", "No secret loaded")

def get_db_connection():
    retries = 10
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            print(f"Database not ready yet ({e}). Retrying in 2s... ({10 - retries}/10)")
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
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: {APP_COLOR}; transition: background-color 0.5s ease;">
        <h1 style="color: #326ce5; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            ☸️ K8s Multi-Container & Storage
        </h1>
        <p style="font-size: 16px;"><b>Environment:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{APP_ENV}</code></p>
        <p style="font-size: 16px;"><b>Current Server Time:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        <p style="font-size: 16px;"><b>Web Pod Name:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        
        <div style="background-color: #f3e8ff; border: 1px solid #e9d5ff; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
            <span style="font-size: 14px; color: #6b21a8; font-weight: bold; text-transform: uppercase;">Database Tracked Visits</span>
            <h2 style="font-size: 48px; color: #7c3aed; margin: 10px 0;">{total_hits}</h2>
            <p style="font-size: 13px; color: #7c3aed; margin: 0;">Every visit is recorded in an isolated Postgres Pod!</p>
        </div>

        <div style="background-color: #fffbeb; border: 1px solid #fef08a; border-radius: 8px; padding: 15px; margin: 20px 0;">
            <h3 style="color: #854d0e; margin-top: 0; margin-bottom: 10px;">🔒 Injected Secret</h3>
            <p style="font-size: 14px; margin: 5px 0; font-family: monospace; background: #fef9c3; padding: 8px; border-radius: 4px;"><b>Decrypted Secret Message:</b> {SECRET_MESSAGE}</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 20px 0;">
        <p style="color: #64748b; font-style: italic; font-size: 14px;">Demonstrating ClusterIP Services and PersistentVolumeClaims on Rancher Desktop.</p>
    </div>
    """

if __name__ == '__main__':
    # Initialize schema on startup
    init_db()
    app.run(host='0.0.0.0', port=5000)
