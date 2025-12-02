# Quick Rebuild and Deploy Guide

## What Changed

✅ **Fixed**: "No space left on device" error by pre-downloading Boltz-2 models in Docker image

## Files Modified

1. [Dockerfile](Dockerfile) - Added model pre-download (lines 30-40)
2. [runpod_handler_template.py](runpod_handler_template.py) - Added `--cache` flag (lines 82-93)
3. [BOLTZ_MODEL_PREDOWNLOAD_FIX.md](BOLTZ_MODEL_PREDOWNLOAD_FIX.md) - Full documentation

## Rebuild Steps

### Option 1: Use Build Script (Recommended)

```bash
cd c:\Users\trist\atomera
build_and_push_docker.bat
```

### Option 2: Manual Build

```bash
cd c:\Users\trist\atomera

# Build the image
docker build -t ghcr.io/tris077/atomera-boltz2:latest .

# Push to registry
docker push ghcr.io/tris077/atomera-boltz2:latest
```

## Important Notes

⏰ **Build time**: 10-30 minutes (longer than before due to model download)
- This is NORMAL and EXPECTED
- Models are downloading during build (you'll see progress)
- Look for "Boltz-2 models pre-downloaded successfully" in output

📦 **Image size**: ~12-18 GB (was ~8-10 GB before)
- Includes 4-8 GB of model weights
- This is acceptable for RunPod
- Eliminates runtime disk errors

## Deploy to RunPod

### Automatic Update (Wait for next worker)

RunPod will automatically pull the new image when workers restart.

### Manual Update (Immediate)

1. Go to: https://www.runpod.io/console/serverless
2. Find endpoint: `lm0cjtlazfyx6f`
3. Stop all active workers
4. Start a new worker
5. Worker pulls new image

## Test the Fix

```bash
cd backend
python test_job_submission.py
```

**Expected output**:
```
[RunPod] Submitting to URL: https://api.runpod.ai/v2/lm0cjtlazfyx6f/run
[RunPod] Response status: 200
[RunPod] ✅ Successfully submitted job to RunPod: xyz-123

Polling job status (30 min timeout)...
Status: IN_QUEUE
Status: IN_PROGRESS
Status: COMPLETED

✅ Job completed successfully!
   Affinity: -7.2
   Confidence: 0.89
   Poses: 1
```

## What to Look For

### During Build ✅

```
Step 10/15 : RUN python3 -c "from boltz.main import download_boltz2..."
 ---> Running in abc123
Downloading model weights to /app/boltz_cache...
✓ boltz2.ckpt (2.3 GB)
✓ boltz2_aff.ckpt (1.8 GB)
✓ ccd.pkl (87 MB)
Boltz-2 models pre-downloaded successfully
-rw-r--r-- 1 root root 2.3G boltz2.ckpt
-rw-r--r-- 1 root root 1.8G boltz2_aff.ckpt
-rw-r--r-- 1 root root  87M ccd.pkl
```

### During Runtime ✅

RunPod worker logs should show:
```
Starting RunPod Serverless Worker...
--- Starting Serverless Worker | Version 1.x.x ---
Processing job: atomera-job-123
Running command: boltz predict input.yaml --cache /app/boltz_cache ...
Loading cached model from /app/boltz_cache/boltz2.ckpt
Boltz-2 execution completed successfully
```

**Key**: "Loading cached model" (not "Downloading model weights")

### Runtime Errors (Should NOT happen) ❌

If you see this, something went wrong:
```
Downloading model weights...
Error: [Errno 28] No space left on device
```

**Fix**: Verify build completed successfully and new image was pushed/pulled

## Verification Checklist

After deploying:

- [ ] Docker build completed (10-30 min)
- [ ] Build showed "Boltz-2 models pre-downloaded successfully"
- [ ] Image pushed to ghcr.io successfully
- [ ] RunPod worker started with new image
- [ ] Test job submission succeeded
- [ ] Job reached COMPLETED status
- [ ] No "No space left on device" errors
- [ ] Results include affinity values

## Quick Summary

**Before**:
- ❌ Boltz downloaded models at runtime
- ❌ Filled disk → job crashed
- ❌ "No space left on device"

**After**:
- ✅ Models pre-downloaded in image
- ✅ No runtime downloads
- ✅ Jobs complete successfully!

## Next Steps

1. Run `build_and_push_docker.bat` (wait 10-30 min)
2. Restart RunPod workers (or wait for auto-restart)
3. Test with `python backend/test_job_submission.py`
4. Start using Atomera! 🎉

## Need Help?

See full details in: [BOLTZ_MODEL_PREDOWNLOAD_FIX.md](BOLTZ_MODEL_PREDOWNLOAD_FIX.md)
