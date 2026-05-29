# ==========================================
# STAGE 1: Build the React Application
# ==========================================
FROM node:18-alpine AS builder

WORKDIR /app

# Copy dependency configs first to leverage cache layers
COPY package.json ./

# Install project dependencies
RUN npm install

# Copy application source files
COPY . .

# Compile the application into static files (creates the /app/build folder)
RUN npm run build


# ==========================================
# STAGE 2: Serve static files using Nginx
# ==========================================
FROM nginx:1.25-alpine

# Copy compiled static assets from builder stage into Nginx static file folder
COPY --from=builder /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
