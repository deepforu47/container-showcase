# ☸️ Step 01: Kubernetes Pod Basics & Security

This step demonstrates the smallest deployable unit in Kubernetes—the **Pod**—and how to secure it using **SecurityContext**. This maps to the single-container concepts in the Docker basics demo but highlights how Kubernetes manages execution.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **Pod**: A wrapper for one or more containers sharing storage and network namespaces.
2. **SecurityContext**: Pod/container security settings including user IDs, group IDs, privilege escalation controls, and Linux capabilities.
3. **Local Registry Integration**: Building and loading local images directly into a local Rancher Desktop Kubernetes cluster.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Build and Load the Image into Rancher Desktop

Kubernetes does not automatically search your local filesystem for images; it pulls them from registries. For local development with Rancher Desktop, you must load the image into the local cluster's container namespace.

Identify which container engine you configured Rancher Desktop to use (Settings -> Container Engine):

#### Option A: if using `containerd` (nerdctl)
Build the image directly into Kubernetes' active namespace (`k8s.io`):
```bash
nerdctl --namespace k8s.io build -t flask-basics:latest ./app
```

#### Option B: if using `dockerd` (moby/docker)
Build the image locally. Since Moby shares the docker daemon with K8s in Rancher Desktop, it is immediately available:
```bash
docker build -t flask-basics:latest ./app
```

---

### 2. Inspect the Manifest
Open [pod.yaml](file:///Users/kulsharm2/Demo/28052026/01-pod-basics-security/pod.yaml) and point out the `securityContext` section:
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 10001
  runAsGroup: 10001
```
*Explain to the audience that this ensures Kubernetes rejects the container if it attempts to run as root (`UID 0`), preventing privilege escalation attacks.*

---

### 3. Deploy the Pod
Deploy the manifest to Rancher Desktop:
```bash
kubectl apply -f pod.yaml
```

Check the pod status:
```bash
kubectl get pods
```

---

### 4. Access the Service & Test

Since we created a `Service` of type `NodePort`, the application is automatically accessible at:
[http://localhost:30081](http://localhost:30081)

This displays the web interface showing the running Flask app, showing the process **UID 10001** and **GID 10001** running securely.

Alternatively, you can port-forward directly to the Pod:
```bash
kubectl port-forward pod/flask-pod 8080:5000
```
Then visit [http://localhost:8080](http://localhost:8080).

---

### 5. Security Audit Verification
Open another terminal and verify the running process ID directly inside the container namespace:
```bash
kubectl exec -it flask-pod -- id
```
Output:
```text
uid=10001(appuser) gid=10001(appgroup) groups=10001(appgroup)
```
This confirms the container runs with the unprivileged user enforced by Kubernetes security policy!

---

### 🧼 Clean Up
Once done, delete the Pod:
```bash
kubectl delete -f pod.yaml
```
