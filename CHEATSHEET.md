# 📑 Container & Orchestration Command Cheat Sheet

This cheat sheet serves as a quick reference guide for running, managing, and troubleshooting the Docker and Kubernetes showcases in this repository.

---

## 🐳 Docker CLI Cheat Sheet

### Image Operations
```bash
# Build an image with a tag
docker build -t <image-name>:<tag> <path-to-dockerfile-dir>

# List local images
docker images

# Remove an image
docker rmi <image-name>:<tag>
```

### Container Operations
```bash
# Run container in background (detached) and publish ports
docker run -d --name <container-name> -p <host-port>:<container-port> <image-name>

# View running containers
docker ps

# View all containers (including stopped ones)
docker ps -a

# Fetch container logs
docker logs <container-name>

# Follow container logs live
docker logs -f <container-name>

# Execute a command inside a running container
docker exec -it <container-name> <command> (e.g. bash, sh, id)

# Stop a container
docker stop <container-name>

# Remove a container
docker rm <container-name>
```

### Volumes & Networks
```bash
# Create a user-defined bridge network
docker network create <network-name>

# Create a named volume
docker volume create <volume-name>

# List volumes
docker volume ls

# Remove a volume
docker volume rm <volume-name>
```

---

## 🐙 Docker Compose Cheat Sheet

```bash
# Start all services defined in compose file in background
docker compose up -d

# Stop and remove containers, networks, and volumes
docker compose down -v

# Scale a specific service
docker compose up -d --scale <service-name>=<replica-count>

# View logs for all services (interleaved)
docker compose logs -f

# Check status of compose services
docker compose ps
```

---

## ☸️ Kubernetes (Kubectl) Cheat Sheet

### Resource Management (Declarative)
```bash
# Deploy or update resources defined in a YAML file
kubectl apply -f <filename.yaml>

# Deploy all YAML resources inside a directory
kubectl apply -f <directory-path>/

# Delete resources defined in a YAML file
kubectl delete -f <filename.yaml>
```

### Inspection & Troubleshooting
```bash
# List resources (pods, services, deployments, ingress)
kubectl get pods
kubectl get services
kubectl get deployments
kubectl get ingress
kubectl get configmaps
kubectl get secrets

# List resources with extended details (IPs, Node name)
kubectl get pods -o wide

# Describe detailed state of a resource (useful for debugging pending/failed states)
kubectl describe pod <pod-name>
kubectl describe deployment <deployment-name>

# Fetch logs from a specific pod
kubectl logs <pod-name>

# Follow pod logs live
kubectl logs -f <pod-name>

# Fetch logs from a multi-container pod
kubectl logs <pod-name> -c <container-name>

# Open an interactive shell inside a running container
kubectl exec -it <pod-name> -- <command> (e.g., sh, bash, env)
```

### Port Forwarding & Access
```bash
# Forward local host port to pod container port (bypasses service exposure)
kubectl port-forward pod/<pod-name> <host-port>:<container-port>

# Forward local host port to service port
kubectl port-forward svc/<service-name> <host-port>:<service-port>
```

### Scaling & Rollouts
```bash
# Manually scale a deployment's replica count
kubectl scale deployment <deployment-name> --replicas=<count>

# Restart all pods in a deployment gracefully (rolling restart)
kubectl rollout restart deployment <deployment-name>

# Check the status of a rolling upgrade
kubectl rollout status deployment <deployment-name>
```

---

## ☸️ Helm (Package Manager) Cheat Sheet

### Chart Lifecycle
```bash
# Render templates locally to verify outputs (dry-run)
helm template <release-name> <chart-directory>

# Validate chart syntax
helm lint <chart-directory>

# Install a chart release
helm install <release-name> <chart-directory>

# List all active releases
helm list
```

### Upgrades & Rollbacks
```bash
# Upgrade a release with new parameter overrides
helm upgrade <release-name> <chart-directory> --set <key>=<value>

# Upgrade using a specific values file override
helm upgrade <release-name> <chart-directory> -f <values-file.yaml>

# View the deployment history of a release (shows revision numbers)
helm history <release-name>

# Rollback a release to a specific historical revision
helm rollback <release-name> <revision-number>
```

### Cleanup
```bash
# Uninstall a release and delete all its Kubernetes components
helm uninstall <release-name>
```
