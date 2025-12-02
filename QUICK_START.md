# ⚡ Quick Start - RunPod Deployment

**Time needed**: 15 minutes

---

## Prerequisites

- RunPod account
- Docker installed
- GitHub or Docker Hub account

---

## Step 1: Get RunPod API Key (2 min)

1. Go to https://www.runpod.io/console/user/settings
2. Click "API Keys" → "+ API Key"
3. Copy the key (save it somewhere safe)

---

## Step 2: Build & Push Docker Image (5 min)

### Windows:
```bash
# 1. Edit build_and_push_docker.bat and set your username
# 2. Run:
build_and_push_docker.bat
```

### Linux/Mac:
```bash
# 1. Edit build_and_push_docker.sh and set your username
# 2. Make executable and run:
chmod +x build_and_push_docker.sh
./build_and_push_docker.sh
```

**What it does:**
- Builds Docker image with Boltz-2
- Logs you into registry (you'll need to enter password)
- Pushes image to registry
- Shows next steps

---

## Step 3: Create RunPod Endpoint (3 min)

1. Go to https://www.runpod.io/console/serverless
2. Click **"+ New Endpoint"**
3. Fill in:
   - **Name**: `atomera-boltz2`
   - **Image**: Use the image from Step 2 (it will show at the end of the script)
   - **GPU**: RTX 3090
   - **Workers**: Active=0, Max=1
   - **Timeouts**: Idle=5, Execution=1800
4. Click **"Deploy"**
5. **Copy the Endpoint ID** (looks like: `abc123def456`)

---

## Step 4: Configure Atomera (2 min)

```bash
# Run the setup wizard
python setup_runpod.py
```

**It will ask for:**
- RunPod API Key (from Step 1)
- RunPod Endpoint ID (from Step 3)
- Polling interval (press Enter for default: 5)
- Job timeout (press Enter for default: 1800)

**It will:**
- Create `backend/.env` file
- Test your connection
- Show success message

---

## Step 5: Start Atomera (2 min)

**Terminal 1** (Backend):
```bash
cd backend
python main.py
```

You should see: `✅ RunPod service initialized`

**Terminal 2** (Frontend):
```bash
cd frontend
npm run dev
```

---

## Step 6: Test (1 min)

1. Open browser to `http://localhost:5173`
2. Click **"New Job"**
3. Enter:
   - **Name**: "Test RunPod"
   - **Protein**: `MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV`
   - **Ligand**: `CCO`
4. Click **"Create Job"**
5. Watch status page → Should complete in ~2-5 minutes

---

## ✅ Success Checklist

- [ ] Backend shows "✅ RunPod service initialized"
- [ ] Job status changes from "Queued" → "Running"
- [ ] Job completes in a few minutes
- [ ] Results page shows binding affinity
- [ ] Pose files are downloadable

---

## ❌ Something Wrong?

### Connection test fails
→ Check `.env` file in `backend/` directory
→ Verify API key and endpoint ID are correct (no extra spaces)

### Job stays "Queued"
→ Check RunPod console - workers may be starting up
→ Wait 1-2 minutes for first job (cold start)

### Docker build fails
→ Make sure Docker is running
→ Check internet connection for downloads

### Need more help?
→ See [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) for detailed guide
→ See troubleshooting section in that file

---

## What You Just Did

You deployed Atomera's Boltz-2 inference to RunPod GPU cloud!

**Architecture:**
```
Your Computer (Frontend + Backend)
         ↓
    RunPod API
         ↓
   GPU Worker (Your Docker Image)
         ↓
     Boltz-2 Prediction
         ↓
      Results
```

**Benefits:**
- ✅ No local GPU needed
- ✅ Pay only for compute time
- ✅ Auto-scaling
- ✅ Fast predictions

**Costs:**
- ~$0.01-0.05 per prediction (short proteins)
- ~$0.30/hour when GPU is active
- $0/hour when idle (auto-shutdown after 5s)

---

## Next Steps

- Monitor costs in RunPod dashboard
- Try different protein sequences
- Adjust GPU type if needed
- Read full docs in [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md)

---

**That's it! You're running Atomera on RunPod GPU! 🎉**
