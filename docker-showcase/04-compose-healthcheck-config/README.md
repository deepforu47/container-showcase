# Demo 04: Compose Orchestration, Configurations, & Healthchecks

This demo shows how to automate and orchestrate a multi-container stack using **Docker Compose**. We will demonstrate how to separate database credentials from code using a `.env` file, and how to sequence container startup using **healthchecks** to ensure the web application doesn't boot until the database is ready to accept connections.

---

## 💡 Key Concept: Why Healthchecks Matter
In basic Docker Compose setups, the `depends_on` property only waits for the dependency container to **start** (i.e., the container process is running). However, database servers (like PostgreSQL) usually take several seconds to boot up, initialize schemas, and begin listening for connections.

If the web app starts immediately, it will attempt to connect, fail, and crash. 
By adding a **`healthcheck`** using the `pg_isready` utility and setting `depends_on.condition: service_healthy`, Docker Compose holds back the web app container until the database server is verified to be fully operational.

---

## 📂 Files Overview
- `app/`: Web application node (simpler connection logic due to orchestrated startup sequencing).
- `db/`: Bare Postgres alpine Dockerfile, dynamic variables shifted to environment config.
- `docker-compose.yml`: Declarative file configuring networks, volumes, services, and healthcheck dependencies.
- `.env`: Environment variables (credentials) isolated from the codebase.
- `README.md`: Detailed commands and presentation script.

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Fire Up the Stack
Run Docker Compose in detached mode. This command automatically parses `.env`, builds the custom images, creates a private network, initializes the named volume, and starts the services in the correct sequence.

```bash
docker compose up -d
```

*Presenter Note to Audience:*
> "Notice how Compose handles the build, network creation, and volume creation automatically in one command. If you look at the terminal output, you will see it starts the `db` container, waits, and only then starts the `web` container."

---

### Step 2: Monitor Startup Status
Immediately run this command to watch the status:
```bash
docker compose ps
```
You will initially see the database container in a `(health: starting)` status. After a few seconds, run it again:
```bash
docker compose ps
```
You should see:
- `db` status: `Up 5 seconds (healthy)`
- `web` status: `Up 2 seconds` (started only after `db` transitioned to healthy).

---

### Step 3: View Consolidated Container Logs
To see logs from both containers merged chronologically:
```bash
docker compose logs -f
```
*(Press `Ctrl+C` to stop following logs)*

---

### Step 4: Verify the Web App
Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

Refresh a few times. You will see a teal card showing the orchestrated database hit counter incrementing.

---

### Step 5: Tear Down the Stack
Show how easily Compose cleans up your entire workspace:
```bash
docker compose down
```
Explain: *"This stops and removes all containers and networks created by Compose. However, our volume `pgdata_storage` remains intact on the host machine. If we run `docker compose up -d` again, our hit counter will continue from where we left it."*

To delete the volume along with the containers (performing a complete clean reset):
```bash
docker compose down -v
```
*(The `-v` flag tells Docker to purge named volumes).*
