# Multi-stage lightweight Dockerfile for AIMap Platform on GCP Cloud Run
FROM python:3.11-slim

# Prevent Python from writing pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY frontend/ ./frontend/
COPY start.py .

# Expose Streamlit default port
EXPOSE 8501

# Run entrypoint launcher
CMD ["python", "start.py"]
