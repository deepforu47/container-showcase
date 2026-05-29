from flask import Flask
from datetime import datetime
import socket
import os
import sys

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    container_id = socket.gethostname()
    python_ver = sys.version
    user_id = os.getuid() if hasattr(os, 'getuid') else 'N/A'
    group_id = os.getgid() if hasattr(os, 'getgid') else 'N/A'
    
    return f"""
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 600px; margin: 50px auto; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background-color: #f8fafc;">
        <h1 style="color: #326ce5; margin-top: 0; display: flex; align-items: center; gap: 10px;">
            ☸️ Kubernetes Basics: Single Pod
        </h1>
        <p style="font-size: 16px;"><b>Current Server Time:</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{current_time}</code></p>
        <p style="font-size: 16px;"><b>Pod Hostname (Name):</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{container_id}</code></p>
        <p style="font-size: 16px;"><b>Python Version:</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{python_ver.split()[0]}</code></p>
        
        <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 15px; margin: 20px 0;">
            <h3 style="color: #166534; margin-top: 0; margin-bottom: 10px;">🛡️ Security Best Practice: Kubernetes SecurityContext</h3>
            <p style="font-size: 14px; margin: 5px 0;"><b>Process UID/GID:</b> <code>{user_id} / {group_id}</code></p>
            <p style="font-size: 14px; margin: 5px 0; color: #166534;">Running securely as an unprivileged user inside the Pod, enforced by K8s SecurityContext!</p>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 20px 0;">
        <p style="color: #64748b; font-style: italic; font-size: 14px;">Hello from inside your completely isolated Kubernetes Pod!</p>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
