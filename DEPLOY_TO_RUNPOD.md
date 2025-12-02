# Complete RunPod Deployment Guide for Atomera

This guide will walk you through deploying Atomera's Boltz-2 inference to RunPod, step by step.

## Prerequisites

- Docker installed on your machine
- GitHub account (for container registry)
- RunPod account with API key

## Step 1: Get Your RunPod API Key

1. Go to [RunPod.io](https://www.runpod.io/) and sign in
2. Click on your profile → **Settings** → **API Keys**
3. Click **+ API Key** to create a new key
4. **Copy and save this key somewhere safe** - you'll need it shortly

## Step 2: Build and Push the Docker Image

### Option A: Using GitHub Container Registry (Recommended)

```bash
# 1. Login to GitHub Container Registry
docker login ghcr.io
# Username: your-github-username
# Password: use a Personal Access Token (create at https://github.com/settings/tokens)

# 2. Build the Docker image (from the atomera directory)
cd c:\Users\trist\atomera
docker build -t ghcr.io/YOUR-GITHUB-USERNAME/atomera-boltz2:latest .

# 3. Push to GitHub Container Registry
docker push ghcr.io/YOUR-GITHUB-USERNAME/atomera-boltz2:latest
```

**Important**: Replace `YOUR-GITHUB-USERNAME` with your actual GitHub username in the commands above.

### Option B: Using Docker Hub

```bash
# 1. Login to Docker Hub
docker login
# Enter your Docker Hub username and password

# 2. Build the Docker image
cd c:\Users\trist\atomera
docker build -t YOUR-DOCKERHUB-USERNAME/atomera-boltz2:latest .

# 3. Push to Docker Hub
docker push YOUR-DOCKERHUB-USERNAME/atomera-boltz2:latest
```

**Important**: Replace `YOUR-DOCKERHUB-USERNAME` with your actual Docker Hub username.

## Step 3: Create RunPod Serverless Endpoint

1. Go to [RunPod Console](https://www.runpod.io/console/serverless)
2. Click **+ New Endpoint**

### Endpoint Configuration:

- **Endpoint Name**: `atomera-boltz2` (or any name you prefer)
- **Container Image**:
  - If using GitHub: `ghcr.io/YOUR-GITHUB-USERNAME/atomera-boltz2:latest`
  - If using Docker Hub: `YOUR-DOCKERHUB-USERNAME/atomera-boltz2:latest`
- **Container Registry Credentials** (if using private registry):
  - Username: your registry username
  - Password: your registry password/token
- **GPU Type**: Start with **RTX 3090** or **RTX 4090** (good balance of cost/performance)
- **Active Workers**: 0 (serverless will auto-scale)
- **Max Workers**: 1-3 (start small, scale up if needed)
- **Idle Timeout**: 5 seconds (to reduce costs)
- **Execution Timeout**: 1800 seconds (30 minutes)
- **Container Start Command**: Leave empty (uses default CMD from Dockerfile)

### Advanced Settings:

- **Environment Variables**: None needed for now
- **Volume Mounts**: None needed

Click **Deploy** and wait for the endpoint to initialize.

## Step 4: Get Your Endpoint ID

Once the endpoint is created:

1. You'll see your endpoint in the dashboard
2. Click on your endpoint name
3. Copy the **Endpoint ID** - it looks like: `abc123def456ghi789`
4. **Save this ID** - you'll need it in the next step

## Step 5: Configure Atomera Backend

1. Create a `.env` file in the `backend` directory:

```bash
cd c:\Users\trist\atomera\backend
```

2. Create/edit the file `backend\.env` with these contents:

```env
# RunPod Configuration
USE_RUNPOD=true
RUNPOD_API_KEY=YOUR_RUNPOD_API_KEY_HERE
RUNPOD_ENDPOINT_ID=YOUR_ENDPOINT_ID_HERE
RUNPOD_POLL_INTERVAL=5
RUNPOD_TIMEOUT=1800
```

**Important**: Replace:
- `YOUR_RUNPOD_API_KEY_HERE` with the API key from Step 1
- `YOUR_ENDPOINT_ID_HERE` with the Endpoint ID from Step 4

## Step 6: Test the Connection

```bash
# Navigate to backend directory
cd c:\Users\trist\atomera\backend

# Run the connection test
python test_runpod_connection.py
```

**Expected output:**
```
✅ API key valid
✅ Your endpoints:
  - atomera-boltz2 (abc123def456ghi789) - Active
```

If you see errors, double-check:
- API key is correct and not expired
- Endpoint ID is correct
- `.env` file is in the `backend` directory
- No extra spaces or quotes around the values

## Step 7: Start Atomera

```bash
# From the atomera root directory
cd c:\Users\trist\atomera

# Start the backend (in one terminal)
cd backend
python main.py

# In another terminal, start the frontend
cd frontend
npm run dev
```

The backend should print:
```
✅ RunPod service initialized
```

## Step 8: Test with a Real Job

1. Open Atomera in your browser (usually `http://localhost:5173`)
2. Click **New Job**
3. Enter:
   - **Job Name**: "Test RunPod Integration"
   - **Protein**: Paste a short sequence like `MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV`
   - **Ligand**: Enter a SMILES string like `CCO` (ethanol)
4. Click **Create Job**
5. Watch the job status page - it should show:
   - Status: Running
   - Progress updates every 5 seconds
   - Completion with binding affinity results

## Troubleshooting

### Error: "RUNPOD_API_KEY must be set"
- Check that `.env` file exists in the `backend` directory
- Verify the API key is on a line like: `RUNPOD_API_KEY=xxx` (no spaces around `=`)

### Error: "Failed to submit job to RunPod"
- Verify endpoint ID is correct
- Check that the endpoint is "Active" in RunPod console
- Ensure the Docker image is publicly accessible or credentials are configured

### Job stays in "Queued" status
- Check RunPod console to see if workers are starting
- Verify GPU availability in your region
- Increase max workers if all are busy

### Job fails with "Container failed to start"
- Check RunPod logs for the container
- Verify Dockerfile builds successfully locally: `docker build -t test .`
- Ensure `runpod_handler_template.py` exists in the repo root

### Job times out after 30 minutes
- Normal for very large proteins/complex ligands
- Consider:
  - Using shorter protein sequences for testing
  - Increasing `RUNPOD_TIMEOUT` in `.env`
  - Upgrading to faster GPU

## Cost Optimization Tips

1. **Use auto-scaling**: Set Active Workers to 0, let RunPod scale up on demand
2. **Short idle timeout**: Use 5-10 seconds to shut down workers quickly
3. **Right-size GPU**: Start with RTX 3090, only upgrade if you need more VRAM
4. **Set spending limits**: Configure in RunPod account settings
5. **Monitor usage**: Check RunPod dashboard regularly for cost tracking

## What Happens When You Submit a Job

1. Frontend sends protein + ligand to Atomera backend
2. Backend creates input YAML file
3. Backend encodes YAML as base64 and sends to RunPod endpoint
4. RunPod spins up GPU worker (if not already running)
5. Worker runs Boltz-2 prediction
6. Worker encodes results (affinity, confidence, pose files) as base64
7. RunPod returns results to Atomera backend
8. Backend decodes and saves files locally
9. Frontend polls for status and displays results

## Next Steps

- **Production deployment**: Deploy backend to a cloud server (AWS, GCP, Azure)
- **Monitoring**: Set up logging and alerting for job failures
- **Scaling**: Increase max workers for concurrent job processing
- **Optimization**: Cache model weights in custom Docker image for faster startup

## Support

If you encounter issues:
1. Check RunPod logs in the console
2. Check Atomera backend logs
3. Review the test script output: `python test_runpod_connection.py`
4. Verify all environment variables are set correctly

---

**You're all set!** Atomera is now connected to RunPod for GPU-accelerated Boltz-2 inference.
