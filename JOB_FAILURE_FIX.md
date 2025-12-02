# Job Failure Fix - RunPod Handler Initialization

## Problem Summary

**Issue**: All jobs immediately fail after creation. Jobs appear in the UI but status quickly becomes FAILED.

**Root Cause**: The RunPod handler was not properly initialized to work with RunPod's serverless architecture. The handler function existed but was never registered with the RunPod SDK.

---

## What Was Wrong

### Critical Issue: Missing RunPod Serverless Initialization

**File**: `runpod_handler_template.py`

The handler function was defined but **never registered** with RunPod's serverless system. The file was missing:

```python
if __name__ == "__main__":
    import runpod
    runpod.serverless.start({"handler": handler})
```

Without this, RunPod couldn't call the handler function, causing all jobs to fail immediately.

### Secondary Issue: Dockerfile CMD

**File**: `Dockerfile`

The CMD was incorrect and didn't properly start the handler as a RunPod serverless worker.

---

## Fixes Applied

### Fix 1: Added RunPod Serverless Initialization

**File**: `runpod_handler_template.py` - Lines 209-212 (added)

Added the RunPod serverless startup code at the end of the file:

```python
if __name__ == "__main__":
    # RunPod serverless mode
    import runpod
    runpod.serverless.start({"handler": handler})
```

**What this does**:
- Registers the `handler` function with RunPod SDK
- Starts the serverless worker loop
- Listens for incoming jobs from RunPod API
- Processes jobs and returns results

### Fix 2: Updated Dockerfile CMD

**File**: `Dockerfile` - Lines 43-44 (updated)

Changed from:
```dockerfile
CMD ["python3", "-u", "handler.py"]
```

To:
```dockerfile
# Start the RunPod handler
CMD ["python3", "-u", "/app/handler.py"]
```

(Added explicit path to ensure handler is found correctly)

### Fix 3: Enhanced Logging for Debugging

**File**: `backend/services/runpod_service.py`

Added comprehensive logging throughout:

**Lines 72-96** - submit_job():
- Logs URL, payload structure, input data keys
- Logs response status and body
- Logs successful submission or detailed errors

**Lines 119-145** - get_job_status():
- Logs status check responses
- **Logs full error details when job fails**
- Shows RunPod error messages, full status response

**Lines 157-180** - get_job_output():
- Logs raw output type and content
- Logs JSON parsing success/failure
- Shows final output structure

**Why this helps**:
- Identifies exactly where jobs fail
- Shows RunPod error messages
- Reveals payload/response mismatches
- Makes debugging much easier

---

## Handler Request/Response Format

### Request Format (Backend → RunPod)

The backend sends:

```json
{
  "input": {
    "job_id": "atomera-job-uuid",
    "input_yaml": "base64-encoded-yaml",
    "request_data": {
      "protein": {"id": "A", "sequence": "MKFL..."},
      "ligand": {"id": "B", "smiles": "CCO"},
      "use_msa": true,
      "confidence_threshold": 0.5
    },
    "config": {
      "devices": 1,
      "accelerator": "gpu",
      "diffusion_samples": 1,
      "use_msa_server": true
    }
  }
}
```

**Key**: RunPod expects `{"input": {...}}` wrapper.

### Response Format (Handler → Backend)

The handler returns:

```json
{
  "affinity_pred_value": -7.2,
  "affinity_probability_binary": 0.89,
  "confidence_score": 0.85,
  "pose_files": {
    "pose_0.cif": "base64-encoded-content",
    "pose_1.cif": "base64-encoded-content"
  },
  "output_files": {
    "affinity_result.json": "base64-encoded-content",
    "confidence_result.json": "base64-encoded-content"
  }
}
```

Or on error:

```json
{
  "error": "Error message here",
  "affinity_pred_value": null,
  "affinity_probability_binary": null,
  "confidence_score": null,
  "pose_files": {},
  "output_files": {}
}
```

---

## Files Modified

### 1. `runpod_handler_template.py`
   - **Added**: RunPod serverless initialization (lines 209-212)
   - **Effect**: Handler now registers with RunPod SDK

### 2. `Dockerfile`
   - **Updated**: CMD to use explicit path (line 44)
   - **Effect**: Ensures handler starts correctly

### 3. `backend/services/runpod_service.py`
   - **Updated**: submit_job() with detailed logging (lines 72-103)
   - **Updated**: get_job_status() with error logging (lines 119-145)
   - **Updated**: get_job_output() with output logging (lines 157-180)
   - **Effect**: Full visibility into RunPod communication

### 4. `backend/test_job_submission.py` (NEW)
   - **Created**: Diagnostic test script
   - **Purpose**: Test job submission and show detailed diagnostics

---

## What You Need to Do

### Step 1: Rebuild and Push Docker Image

The handler has been fixed, so you need to rebuild and push the image:

```bash
# Option A: Use the build script
build_and_push_docker.bat

# Option B: Manual
cd c:\Users\trist\atomera
docker build -t ghcr.io/tris077/atomera-boltz2:latest .
docker push ghcr.io/tris077/atomera-boltz2:latest
```

### Step 2: Restart RunPod Endpoint (if needed)

In RunPod console:
1. Go to your endpoint
2. If workers are running, they'll pull the new image automatically
3. Or stop/start the endpoint to force image refresh

### Step 3: Restart Backend

The logging changes require a backend restart:

```bash
# Stop backend (Ctrl+C)
cd c:\Users\trist\atomera\backend
python main.py
```

**You should now see detailed `[RunPod]` logs.**

### Step 4: Test with Diagnostic Script (Optional)

Run the test script to see full diagnostics:

```bash
cd c:\Users\trist\atomera\backend
python test_job_submission.py
```

This will:
- Create a test job
- Submit to RunPod
- Show all logging output
- Report success or detailed failure

### Step 5: Test in UI

1. Go to http://localhost:5173
2. Create a new job
3. Watch backend logs for `[RunPod]` messages
4. Job should now progress: PENDING → RUNNING → COMPLETED

---

## Expected Job Flow

### Successful Job

**Backend logs**:
```
[RunPod] Submitting to URL: https://api.runpod.io/v2/lm0cjtlazfyx6f/run
[RunPod] Payload keys: ['input', 'jobName']
[RunPod] Input data keys: ['job_id', 'input_yaml', 'request_data', 'config']
[RunPod] Response status: 200
[RunPod] ✅ Successfully submitted job to RunPod: xyz123

[RunPod] Status check - Response code: 200
[RunPod] Job xyz123 status: IN_QUEUE
[RunPod] Job xyz123 status: IN_PROGRESS
[RunPod] Job xyz123 status: COMPLETED

[RunPod] Raw output type: <class 'dict'>
[RunPod] Final output keys: ['affinity_pred_value', 'affinity_probability_binary', ...]
```

**UI**: Job shows COMPLETED with results

### Failed Job (now with details!)

**Backend logs**:
```
[RunPod] Job xyz123 status: FAILED
[RunPod] ❌ Job xyz123 failed!
[RunPod] Error: Container failed to start
[RunPod] Full response: {
  "status": "FAILED",
  "error": "Container image pull failed",
  ...
}
```

**UI**: Job shows FAILED
**Benefit**: You can see the exact error in backend logs!

---

## Limitations & Requirements

### Minimum Input Requirements

- **Protein**: At least 1 amino acid (no max enforced by handler)
- **Ligand**: Valid SMILES string
- **Format**: Must be plain text (not file upload yet)

### Timeouts

- **Job timeout**: 1800 seconds (30 minutes)
- **Polling interval**: 5 seconds
- **First job**: May take 2-5 minutes (cold start)
- **Subsequent jobs**: Faster (~1-3 minutes)

### RunPod Endpoint Requirements

- **GPU**: Recommended RTX 3090 or better
- **Workers**: Active=0, Max=1-3 (auto-scale)
- **Timeout**: 1800 seconds
- **Image**: Must be the rebuilt image with fixes

---

## Troubleshooting

### Job Still Fails After Rebuild

**Check**:
1. Did you rebuild and push the Docker image?
2. Did RunPod pull the new image? (Check workers in console)
3. Are backend logs showing `[RunPod]` messages?

**Solution**:
- Run `docker images` and verify image was rebuilt
- Check RunPod worker logs for container startup errors
- Restart RunPod endpoint to force image refresh

### "Container failed to start"

**Possible causes**:
- Docker image not pushed correctly
- RunPod can't pull the image
- Image is private and credentials not set

**Solution**:
- Verify image is public on ghcr.io or Docker Hub
- Check RunPod endpoint container image URL matches
- Add registry credentials in RunPod if using private image

### Job Timeout

**Causes**:
- Protein sequence too long
- RunPod worker not starting
- Boltz-2 taking too long

**Solution**:
- Use shorter protein sequences for testing (20-50 residues)
- Check RunPod console for worker status
- Increase timeout in backend/.env: `RUNPOD_TIMEOUT=3600`

### No [RunPod] Logs

**Cause**: Backend not restarted after code changes

**Solution**:
```bash
# Stop backend (Ctrl+C)
cd backend
python main.py
```

---

## Summary

### What Was Wrong
- ❌ Handler function not registered with RunPod SDK
- ❌ Dockerfile CMD incorrect
- ❌ No detailed logging for debugging

### What Was Fixed
- ✅ Added `runpod.serverless.start()` to handler
- ✅ Fixed Dockerfile CMD
- ✅ Added comprehensive logging throughout

### What You Need to Do
1. **Rebuild Docker image** (handler was fixed)
2. **Push to registry**
3. **Restart backend** (for new logging)
4. **Test job** - should now work!

### Expected Outcome
- Jobs progress: PENDING → RUNNING → COMPLETED
- Backend shows detailed `[RunPod]` logs
- Failures show clear error messages
- Results appear in UI

---

## Next Steps

After fixing:

1. **Test with simple job** (short protein, simple SMILES)
2. **Monitor logs** for any remaining issues
3. **Test with complex job** (longer protein, complex ligand)
4. **Tune performance** (adjust workers, GPU type)
5. **Monitor costs** in RunPod dashboard

---

**The job failure issue should now be fixed once you rebuild and push the Docker image!** 🎉
