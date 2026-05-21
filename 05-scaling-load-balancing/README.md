# Demo 05: Scaling & Load Balancing

This demo showcases **horizontal scaling** and **reverse-proxy load balancing** using Docker. We will scale our web application container to multiple replicas, then use an Nginx container to distribute web traffic evenly across the active replicas.

---

## 💡 Key Concepts
1. **Horizontal Scaling**: Running multiple identical instances (replicas) of our application to handle more traffic and provide high availability.
2. **Reverse Proxy Load Balancer**: Nginx sits in front on port `80`. It accepts public traffic and routes it to the backend `web` replicas.
3. **Dynamic Service Discovery**: Inside a Docker Compose network, Nginx routes requests to `http://web:5000`. Docker's internal DNS automatically resolves the host `web` to all active replicas in a round-robin rotation.

---

## 📂 Files Overview
- `app/`: Web app code that queries Postgres and displays traffic distribution statistics per node.
- `nginx/`: Nginx reverse-proxy setup and config mapping upstream servers to `web:5000`.
- `db/`: Core database module.
- `docker-compose.yml`: Declares service structures, hiding backend web ports from the public host.
- `.env`: Environment variables.
- `README.md`: Detailed commands and presentation script.

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Start the Initial Stack
Run the services. By default, this spins up 1 database, 1 Nginx load balancer, and 1 web node instance.

```bash
docker compose up -d
```

Check the active containers:
```bash
docker compose ps
```

---

### Step 2: Scale the Web App to 3 Replicas
Explain to the audience: *"Our traffic is growing, so we are horizontally scaling our web app to 3 instances. Docker Compose handles this with a single command without any code or Nginx config modifications."*

```bash
docker compose up -d --scale web=3
```

Check the active containers again:
```bash
docker compose ps
```
*Notice that we now have 3 web nodes running simultaneously (e.g., `web-1`, `web-2`, `web-3`).*

---

### Step 3: Test Load Balancing Live in the Browser
Open your browser and navigate to the Nginx load balancer endpoint:
👉 **[http://localhost](http://localhost)** *(No port number is needed since Nginx listens on port 80).*

1. Observe the **"Active Web Node Hostname"** shown in the dashboard.
2. Refresh the browser page multiple times.
3. Notice that the Hostname ID changes, rotating between the three active containers!
4. Review the **"Node Traffic Distribution"** card. It displays a list of active node hostnames and query counts loaded directly from the database, proving that Nginx is load balancing traffic in a round-robin cycle.

---

### Step 4: Inspect Dynamic Logs
To see the load balancer dispatching traffic and nodes handling requests in real-time:
```bash
docker compose logs -f web
```
*(Press `Ctrl+C` to stop following logs)*

---

### Step 5: Scale Down (Consolidated Clean)
Show how we can dynamically scale down to 2 replicas when traffic subsides:
```bash
docker compose up -d --scale web=2
```
And inspect:
```bash
docker compose ps
```

---

## 🧹 Housekeeping & Cleanup

```bash
docker compose down -v
```
*(The `-v` flag removes the named database storage volume).*
