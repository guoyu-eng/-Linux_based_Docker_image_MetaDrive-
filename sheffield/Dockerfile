
# ===============================
# Dockerfile for MetaDrive Map Generator
# ===============================

# Base image: Ubuntu + Python
FROM python:3.8-slim

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

COPY requirements /app/requirements





# Install Python dependencies (including MetaDrive from GitHub)
#RUN pip install --no-cache-dir git+https://github.com/metadriverse/metadrive.git
RUN pip install --no-cache-dir -r requirements

# Default command (can be overridden)
CMD ["python", "map_batch_generation.py"]

#CMD ["python", "maping.py"]


