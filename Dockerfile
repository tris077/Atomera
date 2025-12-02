# Production Dockerfile for Boltz-2 RunPod Handler
# This image contains Boltz-2 and the RunPod handler for inference

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip3 install --no-cache-dir --upgrade pip

# Install PyTorch with CUDA support
RUN pip3 install --no-cache-dir \
    torch==2.1.0 \
    torchvision==0.16.0 \
    torchaudio==2.1.0 \
    --index-url https://download.pytorch.org/whl/cu121

# Install Boltz-2 and its dependencies
RUN pip3 install --no-cache-dir boltz

# Create Boltz-2 cache directory
RUN mkdir -p /app/boltz_cache

# Set Boltz cache environment variable
ENV BOLTZ_CACHE=/app/boltz_cache

# Pre-download Boltz-2 model weights during build
# This prevents "No space left on device" errors at runtime
RUN python3 -c "from boltz.main import download_boltz2; from pathlib import Path; download_boltz2(Path('/app/boltz_cache'))" && \
    echo "Boltz-2 models pre-downloaded successfully" && \
    ls -lh /app/boltz_cache/

# Copy the RunPod handler
COPY runpod_handler_template.py /app/handler.py

# Install RunPod SDK
RUN pip3 install --no-cache-dir runpod

# Create directories for temporary files
RUN mkdir -p /tmp/boltz_output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0

# Start the RunPod handler
CMD ["python3", "-u", "/app/handler.py"]
