# Demo 02: Developer Workflow & Bind Mounts

This demo showcases how to establish a rapid development environment. By utilizing Docker **Bind Mounts**, we mount the application source code directly from our host machine into the container. This allows us to modify code on the fly and see changes update in real-time (**hot-reloading**) without rebuilding the Docker image.

---

## 📂 Files Overview
- `app.py`: A Flask app running in debug mode with hot reloading enabled.
- `requirements.txt`: Python package requirements.
- `Dockerfile`: Standard blueprint.
- `README.md`: Step-by-step commands and developer notes.

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Build the Docker Image
```bash
docker build -t dev-web-app:1.0 .
```

---

### Step 2: Spin Up the Container with a Bind Mount
We mount the current directory on our laptop directly over the `/app` folder inside the container. 
- `-v "$(pwd):/app"` binds the host's current directory to the container's `/app` folder.
- `-e FLASK_ENV=development` passes an environment variable to indicate development mode.

```bash
docker run -d \
  -p 8080:5000 \
  -v "$(pwd):/app" \
  -e FLASK_ENV=development \
  --name running-dev-app \
  dev-web-app:1.0
```

*(Note: On Windows PowerShell, use `"${PWD}:/app"` instead of `"$(pwd):/app"`)*

---

### Step 3: Verify the App in Web Browser
Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

You should see a yellow card highlighting **"Docker Dev Workflow: Bind Mounts"** and "Environment Mode: development".

---

### Step 4: Perform the "Hot-Reload" Test (Live Action)
Keep your browser open on one side and your text editor on the other.

1. Open `app.py` in your code editor.
2. Search for the text: `Try editing this string now!`.
3. Change it to: `Wow! Code hot-reloading works instantly! 🚀`.
4. Optionally, modify the color in line 12: change `background-color: #fef3c7;` to `background-color: #e0f2fe;` (light blue) or `background-color: #fee2e2;` (light red) and `color: #d97706;` to another hex.
5. Save the file.
6. Refresh your web browser page at **[http://localhost:8080](http://localhost:8080)**.

*Presenter Note to Audience:*
> "Notice how I did NOT run `docker build` or `docker stop` / `docker run`! Because of the bind mount, the container sees the file changes instantly. Since Flask was started in debug mode, it detected the change and automatically restarted the server inside the container in less than a second."

---

### Step 5: Check the Container Logs to See Flask Reloading
To prove that Flask detected the code changes and restarted, view the container logs:
```bash
docker logs running-dev-app
```
You will see output indicating that the files changed and the detector triggered a reload:
```text
 * Detected change in '/app/app.py', reloading
 * Restarting with stat
 * Debugger is active!
```

---

## 🧹 Housekeeping & Cleanup

```bash
docker stop running-dev-app
docker rm running-dev-app
docker rmi dev-web-app:1.0
```

---

## 💡 Key Concept: Bind Mounts vs Volumes

Explain this distinction to your audience:
- **Bind Mounts**: Maps any folder on the host machine to a path in the container. Excellent for **local development** so developers don't have to keep rebuilding images. However, it relies on the host filesystem having a specific structure.
- **Volumes**: Managed entirely by Docker inside its storage directory. Best for **data persistence** (like databases) because they are isolated from host OS configurations, have better write performance on macOS/Windows, and are easy to back up or share.
