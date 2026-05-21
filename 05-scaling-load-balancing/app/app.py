from flask import Flask
from datetime import datetime
import os
import socket
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "analytics_db")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "supersecurepassword")

def get_db_connection():
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
        
        # Retrieve logs grouped by container ID to show traffic distribution
        cur.execute("SELECT container_id, COUNT(*) FROM visit_logs GROUP BY container_id ORDER BY COUNT(*) DESC;")
        node_stats = cur.fetchall()
        
        cur.close()
        conn.close()
    except Exception as e:
        return f"""
        <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #fee2e2; border: 1px solid #fca5a5;">
            <h1 style="color: #dc2626; margin-top: 0;">❌ Database Connection Error</h1>
            <pre style="background: #f87171; color: white; padding: 15px; border-radius: 6px; overflow-x: auto;">{str(e)}</pre>
        </div>
        """
    
    stats_html = "".join([
        f"<li style='display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #ddd6fe;'><span>Node Hostname: <code style='background: #f3e8ff; padding: 2px 6px; border-radius: 4px;'>{stat[0]}</code></span><span style='background: #8b5cf6; color: white; padding: 2px 8px; border-radius: 12px; font-weight: bold; font-size: 13px;'>{stat[1]} requests</span></li>"
        for stat in node_stats
    ])
    
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #faf5ff; border: 1px solid #e9d5ff;">
        <h1 style="color: #6d28d9; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            ⚖️ Scaling & Load Balancing Demo
        </h1>
        <p style="font-size: 15px; color: #4b5563;"><b>Current Server Time:</b> <code>{current_time}</code></p>
        
        <div style="background-color: #ffffff; border: 2px solid #a78bfa; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);">
            <h3 style="color: #5b21b6; margin-top: 0; margin-bottom: 10px; font-size: 16px;">
                ⚡ Active Web Node Hostname
            </h3>
            <code style="background: #ede9fe; color: #6d28d9; padding: 10px 15px; border-radius: 6px; font-size: 20px; font-weight: bold; display: block; text-align: center; border: 1px dashed #8b5cf6;">
                {container_id}
            </code>
            <p style="font-size: 13px; color: #7c3aed; margin-top: 10px; margin-bottom: 0; text-align: center; font-weight: 500;">
                🔄 Refresh the page! Nginx will route your request to a different container replica.
            </p>
        </div>

        <div style="background-color: #f5f3ff; border-radius: 8px; padding: 20px; margin: 20px 0; border: 1px solid #ddd6fe;">
            <h4 style="margin-top: 0; margin-bottom: 15px; color: #5b21b6; font-size: 14px; text-transform: uppercase; letter-spacing: 0.05em;">
                📊 Cluster Traffic Distribution
            </h4>
            <ul style="list-style: none; padding: 0; margin: 0;">
                {stats_html}
            </ul>
            <hr style="border: 0; border-top: 1px solid #ddd6fe; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #6b7280; font-size: 14px;">Total hits logged in shared Postgres volume:</span>
                <span style="font-size: 18px; color: #6d28d9; font-weight: bold;"><code>{total_hits}</code> hits</span>
            </div>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #e9d5ff; margin: 20px 0;">
        <p style="color: #7c3aed; font-style: italic; font-size: 13px; text-align: center;">
            Security Note: Web containers are isolated. Traffic is public only through Nginx port 80.
        </p>
    </div>
    """

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
