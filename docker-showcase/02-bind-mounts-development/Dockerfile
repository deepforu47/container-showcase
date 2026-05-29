FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code. In production, this forms the image build.
# In development, this is mounted over at runtime to enable hot-reloading.
COPY . .

EXPOSE 5000

# Set Python to unbuffered mode to see logs instantly in Docker output
ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
