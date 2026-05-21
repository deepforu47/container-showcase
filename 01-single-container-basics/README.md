# Demo 01: Single Container Basics

A lightweight, production-ready Flask application designed to demonstrate the fundamentals of containerization. This project serves as a hands-on example for understanding Dockerfiles, image layers, port forwarding, and container lifecycles, while introducing essential security practices like running as a **non-root user**.

---

## 📂 Files Overview
- `app.py`: A simple Flask server displaying server time, container hostname, and runtime user identity details.
- `requirements.txt`: Python package requirements.
- `Dockerfile`: Instructions to build the image (incorporating non-root setup and layer caching optimization).
- `.dockerignore`: Controls what is sent to the Docker build context (keeps build files and environment details out of the image).

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Build the Docker Image
Compile your Dockerfile instructions into a local, read-only image layer stack.
- The `-t` flag assigns a tag/name to the image.
- The `.` specifies the current directory as the build context.

```bash
docker build -t simple-web-app:1.0 .
```

*Presenter Note to Audience:*
> "Notice how Docker executes each step sequentially. If you run this build a second time, it will utilize the cached layers for steps that haven't changed, making the build near-instantaneous. Specifically, copying `requirements.txt` and running `pip install` occurs *before* copying the code, which means changing `app.py` doesn't force a rebuild of the Python environment layer."

---

### Step 2: Spin Up the Container (Detached Mode)
Instantiate the built image into an active, isolated runtime process.
- `-d` runs the container in detached mode (in the background, freeing up the terminal).
- `-p 8080:5000` maps port `8080` on the host to port `5000` inside the container.
- `--name` assigns a recognizable name to this container instance.

```bash
docker run -d -p 8080:5000 --name running-simple-app simple-web-app:1.0
```

---

### Step 3: Verify and Test the Web App
Open your web browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

Point out to your audience:
1. **Container Hostname (ID)**: It displays a random alphanumeric string (e.g., `1a2b3c4d5e6f`). This matches the container's short ID.
2. **Security Best Practice**: The page shows `Process UID/GID: 10001 / 10001`. Explain that the app is executing under the unprivileged `appuser` user rather than `root`, protecting the host OS if the containerized application is ever compromised.

---

### Step 4: Inspect Container Logs
To view output and debug statements streaming from the background process:
```bash
docker logs running-simple-app
```
Add the `-f` flag to follow logs in real-time (like `tail -f`):
```bash
docker logs -f running-simple-app
```
*(Press `Ctrl+C` to stop following)*

---

### Step 5: Access the Container's Internal Terminal
Explore the container's isolated file system or verify security manually:
```bash
docker exec -it running-simple-app bash
```
Run these commands inside the container terminal to demonstrate isolation:
```bash
# Verify the current folder and path
pwd
ls -la

# Verify who you are logged in as
whoami
id
```
*(Type `exit` and press Enter to return to your host terminal)*

---

### Step 6: Verify Security from the Host Machine
To prove to the audience that the process is run by an unprivileged user without accessing the container's terminal:
```bash
docker inspect running-simple-app --format='{{.Config.User}}'
```
*(This returns `10001:10001` or `appuser`, verifying it starts secure.)*

---

## 🧹 Housekeeping & Cleanup

Use these commands to stop processes or free up local disk space:

### Stop the Running Container
```bash
docker stop running-simple-app
```

### Remove the Stopped Container
```bash
docker rm running-simple-app
```

### Remove the Docker Image
```bash
docker rmi simple-web-app:1.0
```
