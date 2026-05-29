# 📦 Container Showcase: Docker to Kubernetes Migration Suite

Welcome to the **Container Showcase**. This repository is a progressive, hands-on guide designed to walk developers and administrators from basic local container configurations using **Docker** into production-grade orchestration using **Kubernetes (with Rancher Desktop)**.

By contrasting these two suites, beginners can clearly see how Docker concepts (like volumes, bind mounts, user-defined networks, and health checks) translate to native, declarative Kubernetes objects (like PVCs, ConfigMaps, ClusterIP/NodePort Services, Probes, Init Containers, and Helm).

---

## 📂 Progressive Roadmap & Concept Mapping

| Step | Capability | 🐳 Docker (Local Development) | ☸️ Kubernetes (Production Orchestration) | Difficulty |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **Basics & Security** | [docker-showcase/01-single-container-basics](docker-showcase/01-single-container-basics)<br>• Dockerfile syntax<br>• Layer caching<br>• Running as non-root UID/GID | [kubernetes-showcase/01-pod-basics-security](kubernetes-showcase/01-pod-basics-security)<br>• K8s Pod object<br>• `SecurityContext`<br>• Enforced non-root execution | Beginner |
| **02** | **Configurations** | [docker-showcase/02-bind-mounts-development](docker-showcase/02-bind-mounts-development)<br>• Bind Mounts (source sync)<br>• Live hot-reloading | [kubernetes-showcase/02-configmaps-secrets](kubernetes-showcase/02-configmaps-secrets)<br>• ConfigMaps (settings)<br>• Secrets (Base64 data)<br>• Zero-recompile env injection | Beginner |
| **03** | **Persistence & Networking** | [docker-showcase/03-manual-multi-container](docker-showcase/03-manual-multi-container)<br>• Named volumes<br>• User-defined bridge networks<br>• Container DNS resolution | [kubernetes-showcase/03-multi-container-storage](kubernetes-showcase/03-multi-container-storage)<br>• PersistentVolumeClaims (PVC)<br>• ClusterIP Service DNS<br>• NodePort Service exposure | Intermediate |
| **04** | **Startup Ordering & Probes** | [docker-showcase/04-compose-healthcheck-config](docker-showcase/04-compose-healthcheck-config)<br>• Docker Compose<br>• Healthchecks<br>• Sequential dependency startup (`depends_on`) | [kubernetes-showcase/04-probes-init-containers](kubernetes-showcase/04-probes-init-containers)<br>• `initContainers` blocking script<br>• `livenessProbe` (restart trigger)<br>• `readinessProbe` (traffic block) | Intermediate |
| **05** | **Scaling & Load Balancing** | [docker-showcase/05-scaling-load-balancing](docker-showcase/05-scaling-load-balancing)<br>• CLI scale `--scale`<br>• Nginx configuration as LB | [kubernetes-showcase/05-scaling-load-balancing](kubernetes-showcase/05-scaling-load-balancing)<br>• Horizontal replica counts (`replicas`)<br>• LoadBalancer Service type<br>• Ingress Controller (Traefik) | Advanced |
| **06** | **Package Management** | [docker-showcase/06-multi-stage-builds](docker-showcase/06-multi-stage-builds)<br>• Multi-stage builds<br>• Compilation vs Run environments<br>• Image footprint optimization | [kubernetes-showcase/06-helm-chart](kubernetes-showcase/06-helm-chart)<br>• **Helm Charts** packaging<br>• `values.yaml` environment separation<br>• Release upgrades & rollbacks | Advanced |

---

## ⚙️ Prerequisites

To run all steps in this suite, ensure you have the following installed:
1. **Docker Desktop** (for Docker demos)
2. **Rancher Desktop** (with Kubernetes enabled, using either the `dockerd` or `containerd` container engine)
3. **Kubectl** (pointed to your local Rancher Desktop cluster context)
4. **Helm** (version 3.0+)
5. A terminal shell (Bash or Zsh) and web browser.

### Configure Kubectl Context
Verify `kubectl` is pointed to your local Rancher Desktop cluster before starting the Kubernetes presentations:
```bash
# Switch to Rancher Desktop context
kubectl config use-context rancher-desktop

# Verify cluster connection
kubectl get nodes
```
*(Note: If the default Rancher Desktop kubectl wrapper fails due to automatic downloads, use Homebrew's kubectl at `/opt/homebrew/bin/kubectl` instead.)*

---

## 🧹 Quick Reset Scripts (Run before starting demos)

To ensure a clean environment with no resource conflicts, run these commands before each presentation:

### For Docker Suite
```bash
# Stop and remove any active containers that might conflict
docker stop $(docker ps -a -q) 2>/dev/null
docker rm $(docker ps -a -q) 2>/dev/null

# Clean up presentation networks & volumes
docker network rm manual-net 2>/dev/null
docker volume rm postgres-volume 2>/dev/null

# Clean build caches
docker builder prune -f
```

### For Kubernetes Suite
```bash
# Delete all active deployments, services, pods, PVCs, and ingresses in default namespace
kubectl delete all --all --grace-period=0 --force 2>/dev/null
kubectl delete pvc --all --grace-period=0 --force 2>/dev/null
kubectl delete ingress --all --grace-period=0 --force 2>/dev/null
kubectl delete configmaps app-config 2>/dev/null
kubectl delete secrets app-secret 2>/dev/null

# Clean up any leftover Helm releases
helm uninstall demo-app 2>/dev/null
```

---

## 📺 Presentation Tips

### 🐳 Docker Demos
* **Demo 01**: Show the process UID/GID on the page to demonstrate that running containers as `root` user by default leaves container runtimes vulnerable.
* **Demo 02**: Arrange VS Code and your browser side-by-side. Save a simple styling change in `app.py` and refresh the page to highlight hot-reloading.
* **Demo 03**: Delete the `db-node` container and show the page fail. Recreate the container with the same named volume, and show the hit counter pick up where it left off.
* **Demo 04**: Run `docker compose ps` in a loop during startup to show the database status transitioning from `starting` to `healthy` before the web container boots.
* **Demo 05**: Scale the containers up and down using `--scale` and watch the Nginx load balancer route traffic to different nodes.

### ☸️ Kubernetes Demos
* **Demo 01 (Security)**: Explain that Kubernetes namespaces and clusters can restrict root users globally, forcing containers to use a secure `securityContext` setup.
* **Demo 02 (Dynamic Configs)**: Modify `configmap.yaml` values, reapply it, recreate the pod, and watch the background color change in the web app without rebuilding the container image.
* **Demo 03 (PVC Persistence)**: Delete the PostgreSQL pod using `kubectl delete pod -l app=postgres`. Reload the page to show that the hit count does not reset, proving Kubernetes instantly re-attached the PVC to the rescheduled Pod.
* **Demo 04 (Startup Probes)**: Observe the Flask pod in `Init:0/1` status while the database finishes booting up, proving that the web container only starts when the database is ready.
* **Demo 05 (Load Balancing)**: Scale the deployment using `kubectl scale deployment flask-deployment --replicas=5` and refresh your browser on port `8082` to show the round-robin distribution among the hostnames.
* **Demo 06 (Helm Chart)**: Show the templates folder and default values. Run `helm template` first to show how dry-runs work, followed by a live `helm upgrade` and `helm rollback` to show release history management.
