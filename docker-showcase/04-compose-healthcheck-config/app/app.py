from flask import Flask
from datetime import datetime
import os
import socket
import psycopg2

app = Flask(__name__)

# Fetch configuration variables injected by Docker Compose
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "analytics_db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "supersecurepassword")

def get_db_connection():
    # Because Compose holds this app back until PostgreSQL is healthy,
    # we don't need a heavy sleep/retry connection loop in our code!
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return conn

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
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #f0fdfa;">
        <h1 style="color: #0d9488; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            🐳 Compose Orchestration & Healthchecks
        </h1>
        <p style="font-size: 16px;"><b>Current Server Time:</b> <code style="background: #ccfbf1; padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        <p style="font-size: 16px;"><b>Web Node Hostname:</b> <code style="background: #ccfbf1; padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        
        <div style="background-color: #e0f2fe; border: 1px solid #bae6fd; border-radius: 8px; padding: 20px; margin: 20px 0; text-align: center;">
            <span style="font-size: 14px; color: #0369a1; font-weight: bold; text-transform: uppercase;">Orchestrated Database Hits</span>
            <h2 style="font-size: 48px; color: #0284c7; margin: 10px 0;">{total_hits}</h2>
            <p style="font-size: 13px; color: #0284c7; margin: 0;">This container did not start until the DB was fully healthy!</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #ccfbf1; margin: 20px 0;">
        <p style="color: #0f766e; font-style: italic; font-size: 14px;">Automated deployment using Docker Compose, dotenv config, and native service healthchecks.</p>
    </div>
    """

if __name__ == '__main__':
    # Initialize schema on startup
    init_db()
    app.run(host='0.0.0.0', port=5000)
