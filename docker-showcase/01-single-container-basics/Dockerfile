# Step 1: Use an official, minimal Python runtime as the parent image
FROM python:3.11-slim

# Step 2: Set the working directory inside the container's isolated file system
WORKDIR /app

# Step 3: Create a non-root system user and group for security
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

# Step 4: Copy only the dependency list first to optimize image layer caching
COPY requirements.txt .

# Step 5: Install the Python packages without saving cache files (minimizes final image size)
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the local source code into the container's working directory
COPY . .

# Step 7: Change ownership of the app files to the unprivileged user
RUN chown -R appuser:appgroup /app

# Step 8: Switch to the non-root user for executing subsequent commands
USER appuser

# Step 9: Inform Docker that the process inside listens on port 5000
EXPOSE 5000

# Step 10: Define the execution command to launch the app when the container spawns
CMD ["python", "app.py"]
