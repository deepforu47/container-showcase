# ☸️ Advanced Kubernetes Migration & Showcase Suite

Welcome to the Advanced Kubernetes Showcase. This suite is a progressive, hands-on demonstration designed to walk developers and administrators from basic Docker configurations into production-grade Kubernetes architectures using **local Rancher Desktop**.

This project serves as a migration of the `advanced-container-showcase` Docker suite to Kubernetes, showing how equivalent features (isolation, persistent volumes, scaling, load balancing, health checks, and package management) are handled natively in Kubernetes.

---

## 📂 Progressive Roadmap & Directory Structure

| Step | Directory | Docker Capability (Reference) | K8s Capability Showcased | Difficulty |
| :--- | :--- | :--- | :--- | :--- |
| **01** | **[01-pod-basics-security](file:///Users/kulsharm2/Demo/28052026/01-pod-basics-security)** | Dockerfile syntax, non-root user | **Pod Basics**, **SecurityContext** (unprivileged UID/GID enforcement) | Beginner |
| **02** | **[02-configmaps-secrets](file:///Users/kulsharm2/Demo/28052026/02-configmaps-secrets)** | Bind Mounts / Env Vars | **ConfigMaps**, **Secrets** (Opaque Base64), and zero-recompile env injection | Beginner |
| **03** | **[03-multi-container-storage](file:///Users/kulsharm2/Demo/28052026/03-multi-container-storage)** | User-defined networks & volumes | **ClusterIP/NodePort Services** (internal DNS resolution), **PersistentVolumeClaims** (`local-path`) | Intermediate |
| **04** | **[04-probes-init-containers](file:///Users/kulsharm2/Demo/28052026/04-probes-init-containers)** | Compose Healthchecks & depends_on | **Init Containers** (sequential startup block), **Liveness/Readiness Probes** | Intermediate |
| **05** | **[05-scaling-load-balancing](file:///Users/kulsharm2/Demo/28052026/05-scaling-load-balancing)** | `--scale`, Nginx Load Balancer | **Replica Scaling**, **Service Type LoadBalancer**, **K8s Ingress Controller** (Traefik) | Advanced |
| **06** | **[06-helm-chart](file:///Users/kulsharm2/Demo/28052026/06-helm-chart)** | Multi-stage builds / compose files | **Helm Package Management**, template variables, dry-runs, upgrades, and rollbacks | Advanced |

---

## ⚙️ Prerequisites

Ensure you have the following installed on your machine:
1. **Rancher Desktop** (with Kubernetes enabled)
2. **Kubectl** (configured to use the `rancher-desktop` context)
3. **Helm** (version 3.0+)
4. A terminal shell (Bash or Zsh) and web browser.

### Configure Kubectl Context
Before starting the presentation, verify that `kubectl` is pointed to your local Rancher Desktop cluster:
```bash
# Switch to Rancher Desktop context
kubectl config use-context rancher-desktop

# Verify cluster connection
kubectl get nodes
```
*(Note: If you run into issues with the default Rancher Desktop kubectl wrapper downloading versions, you can use homebrew's kubectl by typing `/opt/homebrew/bin/kubectl`)*

---

## 🧹 Quick Reset Script (Recommended before starting)
To ensure no leftover pods, PVCs, services, or namespaces conflict during your presentation, run this reset script:

```bash
# Delete all active deployments, services, pods, PVCs, and ingresses in the default namespace
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

- **Demo 01 (Security)**: Explain that while Docker allows running as root by default, Kubernetes' `SecurityContext` can be enforced at the cluster/namespace level to reject any container trying to run as root, which is critical for enterprise environments.
- **Demo 02 (Decoupled Configs)**: Show the audience that the pod YAML loads values from ConfigMaps and Secrets. Change `configmap.yaml` color values live, apply it, recreate the pod, and show the updated color without rebuilding the container.
- **Demo 03 (Persistence)**: Delete the database pod live using `kubectl delete pod -l app=postgres` and keep reloading the Flask UI. Show that the hit count doesn't reset, proving that K8s rebinds the PersistentVolumeClaim to the newly rescheduled Pod instantly.
- **Demo 04 (Startup Probes)**: Run `kubectl get pods -w` during deployment. Point out how Flask blocks in the `Init:0/1` phase while Postgres is preparing, then transitions cleanly once Postgres is ready.
- **Demo 05 (Load Balancing)**: Run `kubectl scale deployment flask-deployment --replicas=5` and watch the pods spin up. Refresh your browser rapidly on port `8082` to show traffic round-robining among all 5 pod hostnames.
- **Demo 06 (Helm Chart)**: Run `helm template` first to show how templates work. Then run `helm upgrade` and `helm rollback` to show how easily complex multi-tier configurations are updated and reverted in a single command.
