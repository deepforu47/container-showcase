from flask import Flask
from datetime import datetime
import socket
import os
import sys

app = Flask(__name__)

# Fetch environment variables injected by ConfigMap and Secret
app_color = os.environ.get("APP_COLOR", "#f8fafc")
app_env = os.environ.get("APP_ENV", "Unknown")
secret_message = os.environ.get("SECRET_MESSAGE", "No secret loaded")

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container_id = socket.gethostname()
    
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: {app_color}; transition: background-color 0.5s ease;">
        <h1 style="color: #326ce5; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            ☸️ ConfigMaps & Secrets
        </h1>
        <p style="font-size: 16px;"><b>Environment:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{app_env}</code></p>
        <p style="font-size: 16px;"><b>Pod Hostname:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        <p style="font-size: 16px;"><b>Current Time:</b> <code style="background: rgba(0,0,0,0.05); padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        
        <div style="background-color: rgba(255,255,255,0.7); border: 1px solid rgba(0,0,0,0.1); border-radius: 8px; padding: 15px; margin: 20px 0;">
            <h3 style="color: #0f172a; margin-top: 0; margin-bottom: 10px;">⚙️ Decoupled Configurations</h3>
            <p style="font-size: 14px; margin: 5px 0;"><b>App Color Theme:</b> <code>{app_color}</code></p>
            <p style="font-size: 14px; margin: 5px 0;">(This background color was dynamically injected from a ConfigMap!)</p>
        </div>

        <div style="background-color: #fffbeb; border: 1px solid #fef08a; border-radius: 8px; padding: 15px; margin: 20px 0;">
            <h3 style="color: #854d0e; margin-top: 0; margin-bottom: 10px;">🔒 Injected Secret</h3>
            <p style="font-size: 14px; margin: 5px 0; font-family: monospace; background: #fef9c3; padding: 8px; border-radius: 4px;"><b>Decrypted Secret Message:</b> {secret_message}</p>
            <p style="font-size: 12px; margin: 5px 0; color: #854d0e;">Stored as base64 in a K8s Secret, injected securely at runtime!</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid rgba(0,0,0,0.1); margin: 20px 0;">
        <p style="color: #64748b; font-style: italic; font-size: 14px;">Demonstrating zero-recompile configuration injection.</p>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
