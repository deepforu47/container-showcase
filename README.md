# 🐳 Advanced Docker & Container Showcase Suite

Welcome to the Advanced Docker Showcase. This suite is a progressive, hands-on demonstration designed to walk developers and administrators from basic container concepts up to production-grade architectures.

Each folder in this repository contains a self-contained project showcasing specific Docker features and best practices.

---

## 📂 Progressive Roadmap & Directory Structure

| Step | Directory | Key Docker Capabilities Showcased | Difficulty |
| :--- | :--- | :--- | :--- |
| **01** | **[01-single-container-basics](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/01-single-container-basics)** | Dockerfile syntax, layer caching, `.dockerignore`, **unprivileged non-root user execution** | Beginner |
| **02** | **[02-bind-mounts-development](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/02-bind-mounts-development)** | **Bind Mounts**, container environment variables, **live hot-reloading** developer workflow | Beginner |
| **03** | **[03-manual-multi-container](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/03-manual-multi-container)** | User-defined bridge networks, **persistent named volumes**, container DNS resolution, data survival test | Intermediate |
| **04** | **[04-compose-healthcheck-config](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/04-compose-healthcheck-config)** | **Docker Compose**, `.env` variable segregation, PostgreSQL **healthchecks**, sequential service dependency startup | Intermediate |
| **05** | **[05-scaling-load-balancing](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/05-scaling-load-balancing)** | Horizontal container scaling (`--scale`), **Nginx reverse-proxy load balancing**, secure internal networking | Advanced |
| **06** | **[06-multi-stage-builds](file:///Users/kulsharm2/Demo/25052026/advanced-container-showcase/06-multi-stage-builds)** | **Multi-stage build pipelines**, compilation environments (Node) vs run environments (Nginx), **image size optimization** | Advanced |

---

## ⚙️ Prerequisites
Ensure you have the following installed on your demonstration machine:
- **Docker Desktop** (version 20.10+ recommended)
- A terminal shell (Bash, Zsh, or PowerShell)
- A text editor (VS Code or similar) for modifying files in Step 02.

---

## 🧹 Quick Reset Script (Recommended before starting)
To ensure no leftover container names, networks, or volumes collide during your presentation, run this reset script:

```bash
# Stop and remove any active containers that might conflict
docker stop $(docker ps -a -q) 2>/dev/null
docker rm $(docker ps -a -q) 2>/dev/null

# Clean up presentation networks & volumes
docker network rm manual-net 2>/dev/null
docker volume rm postgres-volume 2>/dev/null

# Clean dangling build caches
docker builder prune -f
```

---

## 📺 Presentation Tips
- **Demo 01**: Show the `UID/GID` output on the web page to highlight that it's *not* running as root. This is a very common security audit gap.
- **Demo 02**: Position your editor and web browser side-by-side. Make a simple color or text change in `app.py`, save, and immediately reload the page to display instant hot-reloading.
- **Demo 03**: Stop and remove the `db-node` container and reload the page to show it failing. Relaunch it with the same volume, reload, and show that the count survives.
- **Demo 04**: Run `docker compose ps` repeatedly during startup to show the database status transitioning from `starting` to `healthy` before the web container starts.
- **Demo 05**: Refresh the page rapidly and show the container node IDs rotating in the distribution list. Scale the web nodes up and down live.
- **Demo 06**: Build the image, then query `docker images` to highlight the final package size of less than 30MB. Contrast this with the size of node-based images (over 1GB).
