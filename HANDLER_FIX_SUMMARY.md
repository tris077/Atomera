# RunPod Handler Fix - Container Stays Alive

## Changes Made

### 1. Updated Handler (`runpod_handler_template.py`)

**Added import at top** (Line 13):
```python
import runpod
```

**Updated serverless start** (Lines 210-212):
```python
if __name__ == "__main__":
    print("Starting RunPod Serverless Worker...")
    runpod.serverless.start({"handler": handler})
```

### 2. Verified Dockerfile

**Already correct** - No changes needed:
```dockerfile
# Copy handler
COPY runpod_handler_template.py /app/handler.py

# Start the handler
CMD ["python3", "-u", "/app/handler.py"]
```

### 3. Handler Function Signature

**Already correct**:
```python
def handler(event: Dict[str, Any]) -> Dict[str, Any]:
    """RunPod serverless handler for Boltz-2 inference."""
    # ... handler logic ...
```

## How It Works

1. **Container starts**: Runs `python3 -u /app/handler.py`
2. **Handler loads**: Imports all dependencies including `runpod`
3. **Serverless starts**: `runpod.serverless.start()` is called
4. **Worker listens**: Container stays alive, listening for jobs from RunPod
5. **Job received**: RunPod calls `handler(event)` function
6. **Job processed**: Handler runs Boltz-2 and returns results
7. **Loop continues**: Worker continues listening for more jobs

## Expected Behavior

### When Container Starts

**Console output**:
```
Starting RunPod Serverless Worker...
--- Starting Serverless Worker |  Version 1.x.x ---
```

**Container status**: Running (stays alive indefinitely)

### When Job is Received

**Console output**:
```
Processing job: atomera-job-123
Decoded YAML content (XX chars)
Created input YAML: /tmp/xxx/input.yaml
Running command: boltz predict ...
Boltz-2 execution completed successfully
Job atomera-job-123 completed successfully
```

### If Container Exits Immediately

**Problem**: Handler not properly initialized
**Symptom**: Container exits right after start
**Cause**: `runpod.serverless.start()` not called or failed

## Testing Locally (Optional)

### Test Handler Function

Before building Docker image, test the handler works:

```bash
cd c:\Users\trist\atomera
python test_handler_locally.py
```

**Expected**: Handler processes test job successfully

### Test Docker Container

After building, verify container stays alive:

```bash
docker build -t test-handler .
docker run test-handler
```

**Expected output**:
```
Starting RunPod Serverless Worker...
--- Starting Serverless Worker |  Version 1.x.x ---
```

**Container**: Should stay running (press Ctrl+C to stop)

## Rebuild and Deploy

### Step 1: Rebuild Docker Image

```bash
cd c:\Users\trist\atomera
build_and_push_docker.bat
```

Or manually:
```bash
docker build -t ghcr.io/tris077/atomera-boltz2:latest .
docker push ghcr.io/tris077/atomera-boltz2:latest
```

### Step 2: Update RunPod Endpoint

The endpoint will automatically pull the new image when workers restart.

**Force immediate update**:
1. Go to RunPod console
2. Stop all workers (if any running)
3. Start a new worker
4. New worker will pull latest image

### Step 3: Test Job Submission

```bash
cd backend
python test_job_submission.py
```

**Expected**:
- Job submits successfully (no 404)
- Job status shows IN_QUEUE → IN_PROGRESS → COMPLETED
- Results returned with affinity values

## Verification Checklist

After deploying:

- [ ] Docker build completes without errors
- [ ] Image pushed to registry successfully
- [ ] RunPod worker starts and stays running
- [ ] Worker shows "Starting Serverless Worker" in logs
- [ ] Test job submission succeeds (no 404)
- [ ] Job progresses to COMPLETED status
- [ ] Results contain affinity values and pose files

## Files Modified

1. **`runpod_handler_template.py`**:
   - Added `import runpod` at top
   - Added print statement before start
   - Cleaned up serverless start call

2. **`Dockerfile`**: No changes (already correct)

3. **`test_handler_locally.py`**: NEW - Local handler test script

4. **`HANDLER_FIX_SUMMARY.md`**: This file

## Summary

**What was fixed**:
- ✅ Handler imports `runpod` at module level
- ✅ Handler calls `runpod.serverless.start()` when run
- ✅ Dockerfile correctly starts the handler
- ✅ Container will stay alive and listen for jobs

**What to do**:
1. Rebuild Docker image
2. Push to registry
3. RunPod will auto-pull new image
4. Test job submission

**Expected result**: Container stays alive, jobs process successfully!
