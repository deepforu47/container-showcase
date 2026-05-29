# ☸️ Step 04: Health Checks & Sequential Startup

This step demonstrates how to build resilient, self-healing architectures in Kubernetes using **Liveness Probes**, **Readiness Probes**, and **Init Containers**.

This maps to Docker Compose's `depends_on: { condition: service_healthy }` and healthchecks, showing how Kubernetes provides native, robust primitives for orchestrating sequential startups and recovering from application failures.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **Liveness Probe**: Determines if a container needs to be restarted. If the probe fails, Kubernetes kills the container and triggers its restart policy.
2. **Readiness Probe**: Determines if a container is ready to accept network traffic. If it fails, the Pod is removed from the Service's load balancer endpoints.
3. **Init Container**: A block of code that runs to completion *before* any app containers start. Used here to block Flask startup until Postgres is listening on port `5432`.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Re-use the Step 03 Image
No new build is required. We will reuse the `flask-db:latest` image built in the previous step.

---

### 2. Inspect the Manifests

Show the audience the health and startup orchestrations:
- **[postgres-deployment.yaml](file:///Users/kulsharm2/Demo/28052026/04-probes-init-containers/postgres-deployment.yaml)**: Uses a command-based (`exec`) probe calling `pg_isready` to verify database health.
- **[flask-deployment.yaml](file:///Users/kulsharm2/Demo/28052026/04-probes-init-containers/flask-deployment.yaml)**:
  - Adds an `initContainers` block running `busybox` and checking `nc -z postgres-service 5432`.
  - Adds HTTP-based (`httpGet`) probes for both Liveness and Readiness.

---

### 3. Deploy and Observe Sequential Startup (The "Live Status" Demo)

1. Ensure the previous step's services are clean (they are deployed in the same namespace, so we will just apply the updates).
2. Apply the updated deployments:
   ```bash
   # Ensure PVC and Services are active from Step 03
   # Apply all manifests in the directory (PVC, Services, and Deployments)
   kubectl apply -f .

   ```
3. Immediately run `kubectl get pods -w` to watch the transition:
   - Notice the Flask pod stays in `Init:0/1` status while Postgres is starting.
   - Once Postgres starts and passes its readiness probe, the init container exits successfully.
   - The Flask pod transitions to `PodInitializing`, then `Running` (but `0/1` containers ready).
   - Once Flask passes its readiness check, it transitions to `1/1` ready!
   - This proves that Flask never tries to connect to an offline database during startup, preventing start up errors.

---

### 4. Verify Application Health
Check that the application is fully operational by visiting:
[http://localhost:30084](http://localhost:30084)

---

### 5. Self-Healing Simulation
Explain how Liveness Probes recover from deadlocks or failures:
1. Simulating a failure (e.g., kill the Flask process or force it to hang, or delete the Postgres Pod).
2. If Flask hangs and fails its HTTP Liveness check on `/`, Kubernetes will automatically restart the Flask container in place—which you can verify by checking the `RESTARTS` count in `kubectl get pods`.

---

### 🧼 Clean Up
Once done, clean up:
```bash
kubectl delete -f .
```
