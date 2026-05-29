# ☸️ Step 05: Scaling & Load Balancing

This step demonstrates how Kubernetes handles application scaling and external load balancing. 

This maps directly to Step 05 of the Docker showcase (where Nginx was manually configured to load balance scaled Flask containers). In Kubernetes, we show how these features are native, declarative, and completely handled by the platform using **Replicas**, **Service LoadBalancers**, and **Ingress Controllers**.

---

## 💡 Key Kubernetes Concepts Demonstrated
1. **Replicas**: Scaling pods horizontally by declaring the desired number of instances.
2. **Service Type LoadBalancer**: Integrates with local cluster load balancers (Klipper in Rancher Desktop) to allocate an external IP and route traffic to the pods.
3. **Ingress**: An API object that manages external access to the services in a cluster, typically HTTP. It acts as an advanced reverse proxy supporting hostname-based routing.

---

## 🛠️ Step-by-Step Presentation Guide

### 1. Inspect the Manifests

Show the audience the scaling and routing configurations:
- **[flask-deployment.yaml](file:///Users/kulsharm2/Demo/28052026/05-scaling-load-balancing/flask-deployment.yaml)**: Note that `replicas` is set to `3`.
- **[flask-service-lb.yaml](file:///Users/kulsharm2/Demo/28052026/05-scaling-load-balancing/flask-service-lb.yaml)**: Exposes the pods externally using `type: LoadBalancer` on port `8082`.
- **[flask-ingress.yaml](file:///Users/kulsharm2/Demo/28052026/05-scaling-load-balancing/flask-ingress.yaml)**: Defines an Ingress routing rules for `flask-app.local` using Rancher's Traefik ingress controller.

---

### 2. Deploy the Stack
Apply all manifests in the directory:
```bash
kubectl apply -f .
```

Verify that 3 Flask pods and 1 Postgres pod are active:
```bash
kubectl get pods -o wide
```

---

### 3. Verify Round-Robin Load Balancing
Open your browser and navigate to:
[http://localhost:8082](http://localhost:8082)

* Note the count incrementing on each refresh.
* **Observe the "Web Pod Name" on the page**: Refresh rapidly and note how the hostname (pod name) switches between the 3 active pod IDs. This shows Kubernetes' internal service layer distributing traffic using IPVS/iptables round-robin load balancing!

---

### 4. Dynamic Live Scaling
Demonstrate K8s' ability to scale up and down instantly:
1. Scale the Flask replicas to 5 live:
   ```bash
   kubectl scale deployment flask-deployment --replicas=5
   ```
2. Watch the cluster spin up two new pods in real time:
   ```bash
   kubectl get pods -w
   ```
3. Once they are `Running`, reload [http://localhost:8082](http://localhost:8082) and show that the two new pod names have joined the load balancer rotation!
4. Scale back down to 3:
   ```bash
   kubectl scale deployment flask-deployment --replicas=3
   ```

---

### 5. Ingress Controller routing (Advanced Demo)
Show how host-based routing works using Traefik:
1. Map `flask-app.local` to localhost on your machine. Add this line to your `/etc/hosts` file (or `C:\Windows\System32\drivers\etc\hosts` on Windows):
   ```text
   127.0.0.1 flask-app.local
   ```
2. Open your browser and navigate to [http://flask-app.local](http://flask-app.local) (Rancher Desktop binds Traefik to port `80` by default).
3. Explain that Traefik read the `flask-ingress` rules, identified the header `Host: flask-app.local`, and routed the traffic to the corresponding `flask-service`!

---

### 🧼 Clean Up
Once done, clean up:
```bash
kubectl delete -f .
```
