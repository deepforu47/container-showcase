# ☸️ Step 06: Production-Grade Helm Chart Deployment

This step demonstrates the peak of the Kubernetes migration: packaging the entire multi-tier stack as a single, version-controlled, highly configurable package using **Helm** (the package manager for Kubernetes).

This shows how to avoid writing raw, environment-specific YAML files by templating configuration parameters and deploying the stack in a single command.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **Helm Chart**: A collection of files that describe a related set of Kubernetes resources.
2. **Values.yaml**: A file containing default configuration parameters that can be overridden at install/upgrade time.
3. **Dry Run / Template Rendering**: Testing chart configurations and validating manifests before applying them.
4. **Releases and Rollbacks**: Single-command upgrades and rollbacks of the entire application deployment version history.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Build & Ensure the Base Image Exists
Ensure you have built the Flask app image from Step 03/04:
* Docker tag: `flask-db:latest`

---

### 2. Inspect the Helm Structure
Show the audience the Helm chart files:
- **[Chart.yaml](file:///Users/kulsharm2/Demo/28052026/06-helm-chart/charts/advanced-showcase/Chart.yaml)**: Holds chart metadata.
- **[values.yaml](file:///Users/kulsharm2/Demo/28052026/06-helm-chart/charts/advanced-showcase/values.yaml)**: Lists default variables (replicaCount, image name, DB credentials, background color).
- **[templates/](file:///Users/kulsharm2/Demo/28052026/06-helm-chart/charts/advanced-showcase/templates/)**: Contains templates for Deployments, Services, ConfigMaps, Secrets, PVCs, and Ingresses. Point out how `{{ .Release.Name }}` and `{{ .Values.config.appColor }}` are injected dynamically.

---

### 3. Dry-Run & Manifest Verification
Show the audience how Helm compiles variables into raw YAML files without deploying them:
```bash
helm template my-demo ./charts/advanced-showcase --debug
```
*Scroll through the output to show how variables like `APP_COLOR` and `DB_PASSWORD` (automatically Base64 encoded!) were replaced.*

---

### 4. Deploy the Helm Chart
Deploy the stack with a default release name `demo-app`:
```bash
helm install demo-app ./charts/advanced-showcase
```

Check the resources created:
```bash
kubectl get all,pvc,configmaps,secrets -l release=demo-app
```
*(Notice that all resource names have the prefix `demo-app-`, preventing naming collisions with other deployments!)*

---

### 5. Verify the Default App
Access the application on the default NodePort:
[http://localhost:30086](http://localhost:30086)
* Observe the background color is the default light green (`#f0fdf4`) from `values.yaml`.

---

### 6. Overriding Configuration on the Fly (The "Helm Upgrade" Demo)
Upgrade the release to change the background color, scale up pods, and change environment tags, all in one command:
```bash
helm upgrade demo-app ./charts/advanced-showcase \
  --set replicaCount=5 \
  --set config.appColor="#fee2e2" \
  --set config.appEnv="Helm-Configured-Prod"
```

Observe the changes:
1. Run `kubectl get pods` to see 5 pods active.
2. Reload [http://localhost:30086](http://localhost:30086) in your browser:
   * Background color immediately updates to light red (`#fee2e2`).
   * Environment tag displays `Helm-Configured-Prod`.
   * Hostnames rotate among 5 pods.

---

### 7. View History and Rollback
Show how Helm tracks version history:
1. List releases and view history:
   ```bash
   helm history demo-app
   ```
2. Rollback to Revision 1 (the default configuration):
   ```bash
   helm rollback demo-app 1
   ```
3. Reload [http://localhost:30086](http://localhost:30086). It reverts back to the original 3 replicas and light green background, showing instant rollback safety!

---

### 🧼 Uninstall
Clean up the entire stack in one command:
```bash
helm uninstall demo-app
```
*(This automatically deletes Deployments, Services, ConfigMaps, Secrets, PVCs, and Ingresses, leaving nothing behind!)*


/opt/homebrew/bin/helm upgrade -i demo-app ./charts/advanced-showcase -f charts/advanced-showcase/values-tst.yaml -n tst --create-namespace