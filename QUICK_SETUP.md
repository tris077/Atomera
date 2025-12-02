# Quick Setup Guide for RunPod Integration

## What You Need

Based on your pod information, here's what we need to complete the integration:

### Option 1: Use Serverless Endpoint (Recommended - Current Integration)

**What you need:**
1. ✅ **RunPod API Key** - Get from: Account Settings → API Keys
2. ⚠️ **Serverless Endpoint ID** - You'll need to create a serverless endpoint

**Steps:**
1. Go to RunPod Dashboard → Serverless
2. Create a new endpoint with a handler that can process Boltz-2 requests
3. Copy the endpoint ID
4. Set in `.env`:
   ```bash
   RUNPOD_API_KEY=your_api_key_here
   RUNPOD_ENDPOINT_ID=your_endpoint_id_here
   ```

### Option 2: Use Your Existing Pod (SSH-Based - Alternative)

**What you need:**
1. ✅ **Pod ID**: `ei5zbysk7svqp5` (you have this)
2. ✅ **SSH Access**: `ssh ei5zbysk7svqp5-64411dcd@ssh.runpod.io` (you have this)
3. ✅ **SSH Key**: `~/.ssh/id_ed25519` (you have this)
4. ⚠️ **RunPod API Key** - Still needed for some operations

**Note:** This requires modifying the integration to use SSH instead of API calls.

## Current Status

Your pod shows:
- **Pod ID**: `ei5zbysk7svqp5`
- **SSH Available**: ✅ Yes
- **HTTP Services**: ⚠️ Not ready (port 8888)
- **Direct TCP**: ✅ Available (66.92.198.178:11380)

## Next Steps

**Please provide:**
1. Your RunPod API Key (or confirm if you want to use SSH-based approach)
2. Whether you want to:
   - **A)** Create a serverless endpoint (recommended)
   - **B)** Use your existing pod via SSH (I'll modify the code)

Once you provide this, I can complete the setup!

