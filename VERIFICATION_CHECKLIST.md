# RunPod Integration Verification Checklist

Use this checklist to verify that everything is working correctly after deployment.

## Pre-Deployment Verification

### Files Present

- [ ] `Dockerfile` exists in repo root
- [ ] `runpod_handler_template.py` exists in repo root
- [ ] `backend/services/runpod_service.py` exists
- [ ] `backend/services/boltz_service.py` exists
- [ ] `backend/test_runpod_connection.py` exists
- [ ] `backend/config.py` has RunPod settings
- [ ] `backend/env.example` has RunPod variables

### Documentation Present

- [ ] `QUICK_START.md` - Quick deployment guide
- [ ] `DEPLOY_TO_RUNPOD.md` - Detailed guide
- [ ] `RUNPOD_INTEGRATION_COMPLETE.md` - Summary
- [ ] `README_RUNPOD.md` - Overview

### Tools Present

- [ ] `build_and_push_docker.bat` - Windows script
- [ ] `build_and_push_docker.sh` - Linux/Mac script
- [ ] `setup_runpod.py` - Setup wizard

## Deployment Verification

### Docker Image

- [ ] Docker image builds successfully
  ```bash
  docker build -t test-atomera .
  # Should complete without errors
  ```

- [ ] Docker image pushed to registry
  ```bash
  # After running build_and_push script
  # Check registry (GitHub/Docker Hub) - image should be visible
  ```

### RunPod Endpoint

- [ ] Endpoint created in RunPod console
- [ ] Endpoint shows as "Active" or "Ready"
- [ ] Endpoint ID copied and saved
- [ ] Container image URL matches your pushed image
- [ ] GPU type selected (RTX 3090 recommended)
- [ ] Timeouts configured (Idle: 5s, Execution: 1800s)
- [ ] Workers configured (Active: 0, Max: 1-3)

### Configuration

- [ ] `.env` file created in `backend/` directory
- [ ] `USE_RUNPOD=true` in `.env`
- [ ] `RUNPOD_API_KEY` set correctly in `.env`
- [ ] `RUNPOD_ENDPOINT_ID` set correctly in `.env`
- [ ] No extra spaces or quotes around values
- [ ] File is named exactly `.env` (not `.env.txt`)

### Connection Test

- [ ] Test script runs successfully
  ```bash
  cd backend
  python test_runpod_connection.py
  ```

- [ ] Output shows: "✅ API key valid"
- [ ] Output shows: "✅ Your endpoints:"
- [ ] Your endpoint is listed
- [ ] No error messages

## Runtime Verification

### Backend Startup

- [ ] Backend starts without errors
  ```bash
  cd backend
  python main.py
  ```

- [ ] Console shows: "✅ RunPod service initialized"
- [ ] No errors about missing API key or endpoint ID
- [ ] Server starts on port 8000

### Frontend Startup

- [ ] Frontend starts without errors
  ```bash
  cd frontend
  npm run dev
  ```

- [ ] No console errors
- [ ] Can access at `http://localhost:5173`

### Job Creation

- [ ] Can create new job through UI
- [ ] Job appears in jobs list
- [ ] Job status changes from "Queued" to "Running"
- [ ] No errors in browser console
- [ ] No errors in backend logs

### RunPod Execution

- [ ] Check RunPod console - job appears in dashboard
- [ ] Worker spins up (first job may take 1-2 minutes)
- [ ] Worker shows "Running" status
- [ ] No container errors in RunPod logs
- [ ] Job progresses through execution

### Job Completion

- [ ] Job status updates to "Completed" (2-10 minutes for short sequences)
- [ ] Results page loads without errors
- [ ] Binding affinity value is displayed
- [ ] Confidence score is shown
- [ ] Processing time is shown
- [ ] Pose files section appears
- [ ] Can download pose files (if generated)

### Data Verification

- [ ] `affinity_pred_value` is a number (e.g., -7.2)
- [ ] `confidence_score` is between 0 and 1 (e.g., 0.85)
- [ ] `processing_time_seconds` is reasonable (e.g., 120-300s)
- [ ] Job metadata saved in `backend/output/predictions/{job_id}/metadata.json`
- [ ] Output files saved in job directory

## Error Handling Verification

### Invalid Input

- [ ] Submitting invalid protein sequence shows error
- [ ] Submitting invalid SMILES shows error
- [ ] Error messages are user-friendly

### RunPod Failures

- [ ] If endpoint is stopped, shows appropriate error
- [ ] If API key is invalid, shows clear error message
- [ ] If job times out, updates status to "Failed"

### Fallback Mode

- [ ] Setting `USE_RUNPOD=false` in `.env` works
- [ ] Backend falls back to local execution
- [ ] Jobs still complete (if Boltz-2 installed locally)

## Performance Verification

### Cold Start

- [ ] First job completes within 5 minutes
- [ ] RunPod worker starts successfully
- [ ] Subsequent jobs are faster (warm start)

### Polling

- [ ] Job status updates every ~5 seconds
- [ ] Progress percentage increases over time
- [ ] No excessive API calls (check backend logs)

### Cost Optimization

- [ ] Workers shut down after 5-10 seconds of idle time
- [ ] Check RunPod usage dashboard - charges are reasonable
- [ ] No workers running when no jobs active

## Integration Verification

### Frontend → Backend

- [ ] Frontend can create jobs via backend API
- [ ] Frontend can fetch job status
- [ ] Frontend can retrieve results
- [ ] Frontend can download pose files
- [ ] All API endpoints work correctly

### Backend → RunPod

- [ ] Backend can submit jobs to RunPod
- [ ] Backend can poll job status
- [ ] Backend can retrieve results
- [ ] Backend decodes files correctly
- [ ] Backend handles errors gracefully

### End-to-End

- [ ] Complete flow works: Submit → Execute → Results
- [ ] Multiple jobs can run sequentially
- [ ] Jobs are tracked correctly in frontend
- [ ] Results persist after page refresh
- [ ] Job cleanup works for old jobs

## Security Verification

### Credentials

- [ ] `.env` file is not committed to git
- [ ] `.env` is in `.gitignore`
- [ ] API key is not exposed in logs
- [ ] API key is not sent to frontend

### API Security

- [ ] Backend validates input data
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities in frontend
- [ ] File uploads are validated

## Documentation Verification

### Accuracy

- [ ] Instructions match actual deployment steps
- [ ] Screenshots/examples are current
- [ ] Troubleshooting section covers common issues
- [ ] Code examples work as shown

### Completeness

- [ ] All steps documented
- [ ] Prerequisites listed
- [ ] Next steps provided
- [ ] Support resources linked

## Final Verification

### Complete Test Job

Run a complete test from start to finish:

1. [ ] Create job with test data:
   - Protein: `MKFLKFSLLTAVLLSVVFAFSSCGDDDDTGYLPPSQAIQDLLKRMKV`
   - Ligand: `CCO`

2. [ ] Wait for completion (2-5 minutes)

3. [ ] Verify results:
   - Affinity value present
   - Confidence score present
   - Pose files available
   - No errors

4. [ ] Check RunPod dashboard:
   - Job completed successfully
   - Reasonable execution time
   - Worker shut down after completion

5. [ ] Check costs:
   - Charge is reasonable (~$0.01-0.05)
   - No unexpected charges

### Sign-Off

If all items are checked:

- [ ] **Integration is VERIFIED and WORKING** ✅
- [ ] Ready for production use
- [ ] Documentation is accurate
- [ ] System is stable

---

## Troubleshooting Reference

If any checks fail, see:
- [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md) - Troubleshooting section
- [RUNPOD_INTEGRATION.md](RUNPOD_INTEGRATION.md) - Technical details
- RunPod logs in dashboard
- Backend logs in console

---

**Date Verified**: __________

**Verified By**: __________

**Notes**:
_______________________________________
_______________________________________
_______________________________________
