#!/bin/bash
# Build and push Atomera Boltz-2 Docker image to registry
# Usage: ./build_and_push_docker.sh

set -e  # Exit on error

echo "============================================================"
echo "  Atomera Docker Build and Push Script"
echo "============================================================"
echo

# === CONFIGURATION ===
# Edit these values before running!
# Choose one: "ghcr" for GitHub Container Registry, "dockerhub" for Docker Hub
REGISTRY_TYPE="ghcr"

# For GitHub Container Registry (ghcr.io):
GITHUB_USERNAME="tris077"

# For Docker Hub:
DOCKERHUB_USERNAME="YOUR-DOCKERHUB-USERNAME"

# Image tag (usually "latest" for production)
IMAGE_TAG="latest"

# === END CONFIGURATION ===

# Validate registry type and set image name
if [ "$REGISTRY_TYPE" = "ghcr" ]; then
    IMAGE_NAME="ghcr.io/$GITHUB_USERNAME/atomera-boltz2:$IMAGE_TAG"
    echo "Using GitHub Container Registry"
    echo "Image: $IMAGE_NAME"
elif [ "$REGISTRY_TYPE" = "dockerhub" ]; then
    IMAGE_NAME="$DOCKERHUB_USERNAME/atomera-boltz2:$IMAGE_TAG"
    echo "Using Docker Hub"
    echo "Image: $IMAGE_NAME"
else
    echo "ERROR: Invalid REGISTRY_TYPE. Must be 'ghcr' or 'dockerhub'"
    exit 1
fi

echo
echo "This will:"
echo "  1. Build the Docker image"
echo "  2. Login to the container registry"
echo "  3. Push the image to the registry"
echo
read -p "Continue? (y/n): " -r CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo
echo "[Step 1/3] Building Docker image..."
echo "============================================================"
docker build -t "$IMAGE_NAME" .

echo
echo "[Step 2/3] Logging in to container registry..."
echo "============================================================"
if [ "$REGISTRY_TYPE" = "ghcr" ]; then
    echo "Please login with:"
    echo "  Username: $GITHUB_USERNAME"
    echo "  Password: Your GitHub Personal Access Token"
    echo "  (Create one at: https://github.com/settings/tokens)"
    docker login ghcr.io
else
    echo "Please login with your Docker Hub credentials"
    docker login
fi

echo
echo "[Step 3/3] Pushing image to registry..."
echo "============================================================"
docker push "$IMAGE_NAME"

echo
echo "============================================================"
echo "  SUCCESS! Image pushed to registry"
echo "============================================================"
echo
echo "Your image is available at:"
echo "  $IMAGE_NAME"
echo
echo "Next steps:"
echo "  1. Go to RunPod console: https://www.runpod.io/console/serverless"
echo "  2. Create a new serverless endpoint"
echo "  3. Use this image: $IMAGE_NAME"
echo "  4. Copy the endpoint ID"
echo "  5. Run: python setup_runpod.py"
echo
