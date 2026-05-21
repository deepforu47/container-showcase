# Demo 06: Multi-Stage Build Image Optimization

This demo showcases **Multi-Stage Builds**, one of the most powerful features for optimizing Docker images. We will build a React frontend application, compiling it in a Node.js build stage and serving it in a clean, minimal Nginx runtime container. We will compare this approach to a traditional single-stage build.

---

## 💡 Key Concepts
1. **The Size Dilemma**: Compiling React requires Node.js, `npm install`, and massive `node_modules` folders, resulting in a single-stage image size of **over 1.2 GB**.
2. **Multi-Stage Builds**: Using multiple `FROM` blocks in a single Dockerfile:
   - **Stage 1 (builder)**: Uses a heavy `node` environment to download packages and run `npm run build` (creating static files in `/app/build`).
   - **Stage 2 (runner)**: Uses a lightweight `nginx:alpine` image. It copies *only* the compiled assets from Stage 1 using `COPY --from=builder` and discards the Node runtime environment.
3. **Optimized Results**: The final production image size drops to **~25 MB**—an index size reduction of over 95%! It is highly secure since it does not contain node compilers, dev tools, or source code.

---

## 📂 Files Overview
- `frontend/package.json`, `public/index.html`, `src/App.js`, `src/index.js`: Simple React project files.
- `frontend/Dockerfile`: Multi-stage Dockerfile containing both builder and runner environments.
- `frontend/.dockerignore`: Excludes build files from the Docker context.
- `README.md`: Detailed commands and presentation script.

---

## 🛠️ Step-by-Step Demo Execution

Follow these commands in sequence during your presentation:

### Step 1: Build the Multi-Stage Docker Image
Compile the React code. The build will take 1-2 minutes as it runs `npm install` and compiles the assets inside the container.

```bash
docker build -t multistage-frontend:1.0 ./frontend
```

---

### Step 2: Spin Up the Container
Run the built container mapping port 8080 to the internal Nginx port 80.
```bash
docker run -d -p 8080:80 --name running-frontend multistage-frontend:1.0
```

---

### Step 3: Verify the App in Web Browser
Open your browser and navigate to:
👉 **[http://localhost:8080](http://localhost:8080)**

You should see a green success card displaying the **"Multi-Stage Build Success!"** dashboard and an image size analysis table.

---

### Step 4: Verify the Image Size (The Wow Moment)
Show the audience the final image size on your host computer:
```bash
docker images multistage-frontend:1.0
```
Point out the size column in the terminal output. The image is only about **25 MB to 30 MB** (depending on the exact Alpine Nginx version)! 

*Presenter Note to Audience:*
> "Notice the image size is under 30MB, yet it contains an entire, functional React application running on an Nginx web server. If we had package-bundled Node.js and our `node_modules` folder inside the final image, it would be over 1 GB. By using multi-stage builds, we get the best of both worlds: a full development pipeline for compilation, and a tiny, secure, fast-to-deploy image in production."

---

## 🧹 Housekeeping & Cleanup

```bash
docker stop running-frontend
docker rm running-frontend
docker rmi multistage-frontend:1.0
```
