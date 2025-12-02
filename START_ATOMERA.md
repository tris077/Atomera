# Start Atomera with RunPod Integration

## ✅ Configuration Complete

Your RunPod integration is fully configured:
- ✅ Docker image: `ghcr.io/tris077/atomera-boltz2:latest`
- ✅ RunPod Endpoint ID: `lm0cjtlazfyx6f`
- ✅ API Key configured in `backend/.env`
- ✅ Backend services ready
- ✅ Handler format verified

---

## 🚀 Start Commands

### Step 1: Start the Backend

Open a terminal/command prompt and run:

```bash
cd c:\Users\trist\atomera\backend
python main.py
```

**Expected output:**
```
✅ RunPod service initialized
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open** - the backend needs to stay running.

---

### Step 2: Start the Frontend

Open a **NEW** terminal/command prompt and run:

```bash
cd c:\Users\trist\atomera\frontend
npm run dev
```

**Expected output:**
```
  VITE v...

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**Keep this terminal open** - the frontend needs to stay running.

---

### Step 3: Open Atomera in Browser

Go to: **http://localhost:5173**

---

## 🧪 Test Job

Create a test job to verify RunPod integration:

### In the Atomera UI:

1. Click **"New Job"** button

2. Fill in the form:
   - **Job Name**: `RunPod Test`
   - **Protein Input**: Switch to "Text Input" tab
   - **Protein Data**: Paste this short sequence:
     ```
     MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV
     ```
   - **Ligand Input**: Switch to "SMILES Input" tab
   - **SMILES String**: Enter:
     ```
     CCO
     ```

3. Click **"Create Job"**

4. You'll be redirected to the job status page

### What to Expect:

**Status Updates (every 5 seconds):**
```
Queued (0%) → Running (40%) → Running (70%) → Completed (100%)
```

**Timeline:**
- **0-30 seconds**: Job queued, being sent to RunPod
- **30-120 seconds**: RunPod spins up GPU worker (cold start)
- **120-300 seconds**: Boltz-2 running prediction
- **300 seconds**: Results returned

**First job may take 3-5 minutes** (worker cold start). Subsequent jobs will be faster.

### Success Indicators:

✅ **Job status changes to "Running"**
✅ **Progress updates appear**
✅ **After 3-5 minutes, status changes to "Completed"**
✅ **Results page shows:**
   - Binding affinity value (e.g., -7.2)
   - Confidence score (e.g., 0.85)
   - Processing time
   - Pose files (if generated)

---

## 🔍 Monitoring

### Backend Logs

Watch the backend terminal for:
```
[OK] Starting prediction for job ...
[OK] Using RunPod: True
[OK] Submitting job to RunPod
[OK] Successfully submitted job to RunPod: <runpod-job-id>
[OK] Job <id> status: IN_PROGRESS
[OK] RunPod execution completed successfully
[OK] Job <id> completed successfully
```

### RunPod Dashboard

Check your jobs in RunPod console:
1. Go to: https://www.runpod.io/console/serverless
2. Click on your endpoint: `atomera-boltz2`
3. See running/completed jobs
4. View logs and costs

---

## ❌ Troubleshooting

### Backend won't start

**Error: "RUNPOD_API_KEY must be set"**
→ Check that `backend/.env` file exists
→ Verify it contains your API key

**Error: Module not found**
→ Install dependencies: `pip install -r requirements.txt`

### Frontend won't start

**Error: npm not found**
→ Install Node.js from https://nodejs.org

**Error: Dependencies not installed**
→ Run: `npm install` in frontend directory

### Job stays in "Queued"

→ Wait 1-2 minutes for RunPod worker to start
→ Check RunPod console for worker status
→ Verify endpoint is active

### Job fails immediately

**Check backend logs for errors:**
- Invalid API key → Verify in `.env`
- Invalid endpoint ID → Check RunPod console
- Network error → Check internet connection

**Check RunPod logs:**
- Go to endpoint in RunPod console
- Click on the failed job
- View logs for errors

### "Container failed to start" in RunPod

→ Verify Docker image exists: `ghcr.io/tris077/atomera-boltz2:latest`
→ Check image is public or registry credentials are set
→ Review RunPod container logs

---

## 💰 Cost Monitoring

After your test job:

1. Go to RunPod dashboard
2. Check usage and costs
3. Verify worker shut down after job completed

**Expected cost for test job:** $0.01 - $0.05

---

## 🎯 What Happens During a Job

1. **Frontend** → Sends protein + ligand to backend
2. **Backend** → Creates YAML, encodes as base64
3. **Backend** → Submits to RunPod endpoint
4. **RunPod** → Spins up GPU worker
5. **Worker** → Pulls Docker image
6. **Handler** → Decodes YAML, runs Boltz-2
7. **Boltz-2** → Predicts binding affinity
8. **Handler** → Encodes results, returns to RunPod
9. **Backend** → Polls status, gets results
10. **Backend** → Decodes files, saves locally
11. **Frontend** → Displays results

---

## ✨ Success!

If your test job completes successfully:

✅ **Your Atomera instance is fully connected to RunPod!**
✅ **All Boltz-2 predictions now run on GPU cloud**
✅ **No local GPU needed**
✅ **Auto-scaling and cost optimization enabled**

---

## 📋 Quick Reference

**Backend URL:** http://localhost:8000
**Frontend URL:** http://localhost:5173
**RunPod Console:** https://www.runpod.io/console/serverless

**Config file:** `backend/.env`
**Docker image:** `ghcr.io/tris077/atomera-boltz2:latest`
**Endpoint ID:** `lm0cjtlazfyx6f`

---

## 🔄 Stopping Atomera

When you're done:

1. **Stop Frontend**: Press `Ctrl+C` in the frontend terminal
2. **Stop Backend**: Press `Ctrl+C` in the backend terminal
3. **RunPod Workers**: Will auto-shutdown after 5 seconds of idle time

---

**Ready? Run the commands above and test your first RunPod job!** 🚀
