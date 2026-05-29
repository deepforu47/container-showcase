# Demo 03: Manual Multi-Container Setup

This demo shows how multiple containers communicate and persist data without an orchestrator wrapper. We will manually establish an isolated bridge network for name-based container communication and a managed volume to persist database records independently of the database container's lifecycle.

---

## 📂 Files Overview
- `app/`: Web node folder containing Python code, dependencies, and web container Dockerfile.
- `db/`: Database folder containing a PostgreSQL configuration Dockerfile.
- `README.md`: Detailed commands and presentation script.

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Initialize the Isolated Network Environment
Explain to the audience: *"By default, containers can only resolve each other by IP address. We create a user-defined bridge network. This network enables automatic DNS name resolution so containers can address each other by name."*

```bash
docker network create manual-net
```

---

### Step 2: Initialize the Storage Volume
Explain: *"Containers are ephemeral and their writeable layer is destroyed when they are removed. We create a managed named volume on the host filesystem to persist database records."*

```bash
docker volume create postgres-volume
```

---

### Step 3: Build Both Images
Build the web application blueprint:
```bash
docker build -t manual-web-app:1.0 ./app
```

Build the custom database blueprint:
```bash
docker build -t manual-db-image:1.0 ./db
```

---

### Step 4: Launch the PostgreSQL Database Container
- We attach the container to the custom network using `--network manual-net`.
- We assign a host identifier name using `--name db-node`.
- We map our volume to the Postgres storage directory inside the container: `-v postgres-volume:/var/lib/postgresql/data`.
- **Note**: We do *not* map ports (no `-p 5432:5432`). The database remains securely hidden inside our network, unreachable from outside the host.

```bash
docker run -d \
  --name db-node \
  --network manual-net \
  -v postgres-volume:/var/lib/postgresql/data \
  manual-db-image:1.0
```

---

### Step 5: Launch the Web Application Container
- We run the web server on the same network.
- We map port 8080 to the host: `-p 8080:5000`.
- We use `-e DB_HOST=db-node` to inject the database hostname. Docker DNS resolves `db-node` to the IP address of the database container we launched in Step 4.

```bash
docker run -d \
  --name web-node \
  --network manual-net \
  -p 8080:5000 \
  -e DB_HOST=db-node \
  manual-web-app:1.0
```

---

### Step 6: Verify Connections in the Web Browser
Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

Refresh the page a few times. You should see the purple card displaying the **"Database Tracked Visits"** counter incrementing.

---

### Step 7: Demonstrate Network Discovery (Optional)
Show how Docker maps containers on the network:
```bash
docker network inspect manual-net
```
In the terminal output, point out the `Containers` object. You will see both `db-node` and `web-node` on the same subnet (e.g., `172.19.0.2` and `172.19.0.3`), explaining how they can resolve each other by name.

---

### Step 8: The Data Survival Test (Key Demo Moment)
Show the audience that containers are ephemeral but volumes preserve data.

1. Stop and remove the database container:
   ```bash
   docker stop db-node && docker rm db-node
   ```
2. Refresh the web browser at **[http://localhost:8080](http://localhost:8080)**. It will show a connection error because the database container is gone.
3. Launch a brand new database container using the exact same command from Step 4:
   ```bash
   docker run -d \
     --name db-node \
     --network manual-net \
     -v postgres-volume:/var/lib/postgresql/data \
     manual-db-image:1.0
   ```
4. Wait 3 seconds, then refresh the web browser at **[http://localhost:8080](http://localhost:8080)**.
5. Point out that the count **did not reset to 1**; it continued from where it left off (e.g., if it was at 5, it is now 6). This proves that the data was safely stored inside the volume and survived the destruction of the database container.

---

## 🧹 Housekeeping & Cleanup

```bash
docker stop web-node db-node
docker rm web-node db-node
docker network rm manual-net
docker volume rm postgres-volume
docker rmi manual-web-app:1.0 manual-db-image:1.0
```
