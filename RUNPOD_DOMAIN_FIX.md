# RunPod API Domain Fix

## Problem

The backend was using the wrong domain for RunPod API calls:
- ❌ **Wrong**: `https://api.runpod.io/v2`
- ✅ **Correct**: `https://api.runpod.ai/v2`

This caused 404 errors when submitting jobs.

## Fix Applied

### File Changed

**`backend/services/runpod_service.py`** - Line 36

**Before**:
```python
self.base_url = "https://api.runpod.io/v2"
```

**After**:
```python
self.base_url = "https://api.runpod.ai/v2"
```

## Final URLs

All RunPod API endpoints now use the correct domain:

### 1. Submit Job
```
POST https://api.runpod.ai/v2/lm0cjtlazfyx6f/run
```

### 2. Get Job Status
```
GET https://api.runpod.ai/v2/lm0cjtlazfyx6f/status/{job_id}
```

### 3. Cancel Job
```
POST https://api.runpod.ai/v2/lm0cjtlazfyx6f/cancel/{job_id}
```

## Testing

Run the test script to verify:

```bash
cd backend
python test_job_submission.py
```

Expected output:
```
[RunPod] Submitting to URL: https://api.runpod.ai/v2/lm0cjtlazfyx6f/run
[RunPod] Response status: 200
[RunPod] ✅ Successfully submitted job to RunPod: xyz123
```

## Summary

**What was wrong**: Using `.io` instead of `.ai` domain
**What was changed**: One line - the base_url
**What now works**: All RunPod API calls use correct domain

The 404 error should now be resolved!
