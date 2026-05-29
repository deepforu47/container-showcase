# ☸️ Step 02: ConfigMaps & Secrets

This step demonstrates how to decouple configuration settings and sensitive data from your container images using Kubernetes **ConfigMaps** and **Secrets**. This is a beginner-to-intermediate best practice, ensuring you don't bake passwords or environment-specific values directly into your code or Dockerfiles.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **ConfigMap**: A Kubernetes object used to store non-confidential key-value pairs (e.g. settings, ports, environment names).
2. **Secret**: A Kubernetes object designed to store sensitive data (e.g. API keys, DB passwords, certificates), encoded in Base64.
3. **Decoupled Configuration**: Injecting variables into the container environment at launch time, allowing the same container image to run unchanged in Dev, Staging, and Prod.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Build the Configuration Demo Image
First, build and register the new image containing the configuration-aware code.

#### Option A: if using `containerd` (nerdctl)
```bash
nerdctl --namespace k8s.io build -t flask-config:latest ./app
```

#### Option B: if using `dockerd` (moby/docker)
```bash
docker build -t flask-config:latest ./app
```

---

### 2. Inspect the Manifests

Show the audience the separate configuration resources:

- **[configmap.yaml](file:///Users/kulsharm2/Demo/28052026/02-configmaps-secrets/configmap.yaml)**: Stores the theme color (`#e0f2fe`) and environment label (`Staging-Cluster`).
- **[secret.yaml](file:///Users/kulsharm2/Demo/28052026/02-configmaps-secrets/secret.yaml)**: Stores the base64-encoded secret message. Point out that Secrets in K8s are base64-encoded to handle binary data but are not encrypted by default—highlighting the need for role-based access control (RBAC) or integration with external secret providers (like HashiCorp Vault or Azure Key Vault) in production.

---

### 3. Deploy Configuration Resources
Deploy the ConfigMap, Secret, Service, and the Pod to Rancher Desktop:
```bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f service.yaml
kubectl apply -f pod.yaml
```

Verify that they are running:
```bash
kubectl get configmaps,secrets,services,pods
```

---

### 4. Access the Service & Test

Since we created a `Service` of type `NodePort`, the application is automatically accessible at:
[http://localhost:30082](http://localhost:30082)

* Show how the background color of the web app matches the color specified in the ConfigMap (`#e0f2fe`).
* Show the decrypted secret message displayed inside the warning box.

Alternatively, you can port-forward directly to the Pod:
```bash
kubectl port-forward pod/flask-config-pod 8080:5000
```
Then visit [http://localhost:8080](http://localhost:8080).

---

### 5. Modify Configuration Live (Dynamic Updates)
Explain that we can modify variables without building a new image!

1. Edit [configmap.yaml](file:///Users/kulsharm2/Demo/28052026/02-configmaps-secrets/configmap.yaml) and change `APP_COLOR` to a different color (e.g. `#fef08a` for yellow).
2. Re-apply the ConfigMap:
   ```bash
   kubectl apply -f configmap.yaml
   ```
3. Recreate the Pod to pick up the new environment variables (since env vars are injected on container start):
   ```bash
   kubectl delete pod flask-config-pod
   kubectl apply -f pod.yaml
   ```
4. Start port forwarding again and reload the page. The background color has updated, demonstrating dynamic configuration injection!

---

### 🧼 Clean Up
Once done, clean up the resources:
```bash
kubectl delete -f pod.yaml -f service.yaml -f configmap.yaml -f secret.yaml
```
