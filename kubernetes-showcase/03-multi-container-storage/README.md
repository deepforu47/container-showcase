# ☸️ Step 03: Multi-Container Setup & Storage Persistence

This step demonstrates how to build a multi-tier application stack in Kubernetes (Flask Web + Postgres Database), connect them using internal DNS resolution, and persist database data across Pod lifecycles using a **PersistentVolumeClaim** (PVC).

This maps to the manual network, named volume, and Postgres setup in the Docker intermediate demo but shows how Kubernetes abstracts networking and storage.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **ClusterIP Service**: An internal-only load-balanced Service that registers a stable DNS name (e.g. `postgres-service`) within CoreDNS, allowing pods to communicate securely.
2. **NodePort Service**: Exposes a Service on a static port of each cluster node, allowing external clients on the host to connect directly (e.g., port `30083` in our setup).
3. **PersistentVolumeClaim (PVC)**: A request for storage that binds to a PersistentVolume (PV). In Rancher Desktop, this uses the built-in `local-path` storage provisioner to map storage to your host filesystem.
4. **Data Persistence**: Demonstrating that stateless containers can be destroyed and recreated, while stateful data survives.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Build the Database-Enabled Web Image

Build the new database-aware Flask application:

#### Option A: if using `containerd` (nerdctl)
```bash
nerdctl --namespace k8s.io build -t flask-db:latest ./app
```

#### Option B: if using `dockerd` (moby/docker)
```bash
docker build -t flask-db:latest ./app
```

---

### 2. Inspect the Manifests

Show the audience the architecture components:
- **[postgres-pvc.yaml](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage/postgres-pvc.yaml)**: Requests 1Gi of persistent storage from Rancher's `local-path` provisioner.
- **[postgres-deployment.yaml](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage/postgres-deployment.yaml)**: Runs Postgres and mounts the PVC to `/var/lib/postgresql/data`.
- **[postgres-service.yaml](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage/postgres-service.yaml)**: Declares a ClusterIP Service. Point out that the metadata name `postgres-service` matches the `DB_HOST` env variable in the Flask deployment!
- **[flask-deployment.yaml](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage/flask-deployment.yaml)**: Runs the Flask app.
- **[flask-service.yaml](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage/flask-service.yaml)**: Declares a NodePort Service exposing port `30083` to your host machine.

---

### 3. Deploy the Stack
Apply the manifests to the cluster:
```bash
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

Wait until all pods are running:
```bash
kubectl get pods
```
*(Note: Because the Flask container starts up immediately and tries to run `init_db()`, it may crash and restart once or twice while waiting for Postgres to bind and start. We will solve this dependency ordering problem in Step 04!)*

---

### 4. Verify Application and Write Data
Open your browser and navigate to:
[http://localhost:30083](http://localhost:30083)

* Note the "Database Tracked Visits" counter starting at 1.
* Refresh the page several times. The count increments on each refresh.

---

### 5. The Data Survival Test (The "Wow" Factor)

Now, prove that storage persistence works in Kubernetes:

1. Look at the running pods:
   ```bash
   kubectl get pods
   ```
2. Delete the active Postgres Pod:
   ```bash
   kubectl delete pod -l app=postgres
   ```
3. Watch Kubernetes instantly reschedule and start a new Postgres Pod:
   ```bash
   kubectl get pods -w
   ```
4. Once the new pod status is `Running`, reload [http://localhost:30083](http://localhost:30083) in your browser.
5. Notice that the count **does not reset to 1**! It picks up exactly where you left off, proving the persistent volume survived the pod's destruction.

---

### 🧼 Clean Up
Once done, clean up the resources:
```bash
kubectl delete -f flask-service.yaml -f flask-deployment.yaml -f postgres-deployment.yaml -f postgres-service.yaml -f postgres-pvc.yaml
```
