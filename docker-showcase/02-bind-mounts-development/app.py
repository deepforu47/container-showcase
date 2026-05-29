from flask import Flask
from datetime import datetime
import socket
import os

app = Flask(__name__)

ENV_MODE = os.environ.get("FLASK_ENV", "development")

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container_id = socket.gethostname()
    
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #fef3c7;">
        <h1 style="color: #d97706; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            🛠️ Docker Dev Workflow: Bind Mounts
        </h1>
        <p style="font-size: 16px;"><b>Current Time:</b> <code style="background: #fde68a; padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        <p style="font-size: 16px;"><b>Container Hostname:</b> <code style="background: #fde68a; padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        <p style="font-size: 16px;"><b>Environment Mode after changes:</b> <span style="background: #d97706; color: white; padding: 2px 8px; border-radius: 20px; font-size: 12px; font-weight: bold; text-transform: uppercase;">{ENV_MODE}</span></p>
        
        <div style="background-color: #fffbeb; border: 1px solid #fcd34d; border-radius: 8px; padding: 15px; margin: 20px 0;">
            <h3 style="color: #b45309; margin-top: 0; margin-bottom: 10px;">🔥 Live Hot Reload Demo</h3>
            <p style="font-size: 14px; margin: 5px 0;">Modify the code in <b>app.py</b> on your host machine (e.g. HELLO change this text or the background color) and watch it update instantly without rebuilding the image!</p>
            <p style="font-size: 14px; margin: 5px 0; color: #b45309; font-weight: bold;">Try editing this string now!</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #fcd34d; margin: 20px 0;">
        <p style="color: #78350f; font-style: italic; font-size: 14px;">Running with source code bind-mounted directly from the host filesystem.</p>
    </div>
    """

if __name__ == '__main__':
    # Debug mode is essential for Flask's interactive reloader to monitor source changes
    app.run(host='0.0.0.0', port=5000, debug=True)
