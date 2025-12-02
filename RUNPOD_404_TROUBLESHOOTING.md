# RunPod 404 Error Troubleshooting

## Current Error

```
[RunPod] Submitting to URL: https://api.runpod.io/v2/lm0cjtlazfyx6f/run
[RunPod] Response status: 404
[RunPod] Response body: {"message":"Not Found"}
```

## What This Means

A 404 error on the `/run` endpoint means one of these:

1. **Endpoint not deployed/active** - The endpoint exists but no workers are running
2. **Endpoint ID incorrect** - The ID `lm0cjtlazfyx6f` doesn't exist
3. **API format changed** - RunPod updated their API structure
4. **Endpoint type mismatch** - Using serverless endpoint ID for pods API or vice versa

## URL Structure Analysis

**Current URLs we're using**:
- Submit job: `https://api.runpod.io/v2/{endpoint_id}/run`
- Get status: `https://api.runpod.io/v2/{endpoint_id}/status/{job_id}`
- Get output: Same as status (output is in status response)

**This is correct for RunPod Serverless v2 API.**

## How to Verify Your Endpoint

### Step 1: Check Endpoint in RunPod Console

1. Go to https://www.runpod.io/console/serverless
2. Find your endpoint in the list
3. Click on it

**Verify**:
- ✅ Status shows "Ready" or "Active"
- ✅ At least one worker is configured (Active or Max Workers > 0)
- ✅ The Endpoint ID matches: `lm0cjtlazfyx6f`
- ✅ Container image is set: `ghcr.io/tris077/atomera-boltz2:latest`

### Step 2: Check If Endpoint Needs Activation

Some endpoints need to be manually started:

1. In the endpoint details
2. Look for a "Start" or "Deploy" button
3. If present, click it to activate the endpoint

### Step 3: Verify Endpoint ID Format

The endpoint ID should be exactly as shown in RunPod console.

**Common mistakes**:
- ❌ Using pod ID instead of endpoint ID
- ❌ Extra characters or spaces
- ❌ Wrong casing (should be lowercase)

### Step 4: Test with RunPod's Test Feature

In the RunPod console:

1. Go to your endpoint
2. Look for "Test" tab or "Run" button
3. Try running a test job with:
   ```json
   {
     "input": {
       "test": "ping"
     }
   }
   ```

If this works in the console but not from our code, it's an API issue.
If this also fails, the endpoint isn't properly configured.

## Possible Solutions

### Solution 1: Endpoint Not Active

**If endpoint shows as "Stopped" or "Inactive"**:

1. Click "Start" or "Deploy" button
2. Wait for workers to spin up (1-2 minutes)
3. Try job submission again

### Solution 2: Wrong Endpoint Type

**If you created a "Pod" instead of "Serverless Endpoint"**:

You need to create a **Serverless Endpoint**, not a Pod.

1. Go to https://www.runpod.io/console/serverless
2. Click "+ New Endpoint"
3. Configure:
   - **Type**: Serverless (not Pods!)
   - **Container Image**: `ghcr.io/tris077/atomera-boltz2:latest`
   - **GPU**: RTX 3090 or similar
   - **Workers**: Active=0, Max=1
4. Copy the new Endpoint ID
5. Update `backend/.env`:
   ```
   RUNPOD_ENDPOINT_ID=NEW_ENDPOINT_ID_HERE
   ```

### Solution 3: API Key Permissions

**If API key doesn't have serverless permissions**:

1. Go to https://www.runpod.io/console/user/settings
2. API Keys section
3. Check your key has "Serverless" permissions
4. If not, create a new key with all permissions

### Solution 4: Use GraphQL API Instead

If REST API continues to fail, RunPod also has a GraphQL API.

We can update the code to use that instead (more complex but more reliable).

## What We Can Try in Code

I can add these improvements:

1. **Auto-retry with different paths**:
   - Try `/run` first
   - If 404, try `/runsync`
   - If still 404, report detailed error

2. **Better error messages**:
   - Show exact URL being called
   - Show full response
   - Suggest specific fixes

3. **Endpoint health check**:
   - Check if endpoint exists before submitting
   - Verify it's active and ready

Would you like me to implement any of these?

## Next Steps for You

1. **Verify endpoint in RunPod console**:
   - Go to serverless endpoints
   - Check status is "Ready"
   - Verify ID: `lm0cjtlazfyx6f`

2. **Test in RunPod console**:
   - Use their built-in test feature
   - If it works there, we have an API issue
   - If it doesn't work, endpoint isn't configured correctly

3. **Check container image**:
   - Verify `ghcr.io/tris077/atomera-boltz2:latest` exists
   - Make sure it's public or credentials are set in RunPod

4. **Report back**:
   - What does the endpoint status show?
   - Does test in console work?
   - What's the exact endpoint ID shown?

## Alternative: Direct Endpoint URL

Some RunPod endpoints have a direct URL like:
```
https://lm0cjtlazfyx6f-unique.proxy.runpod.net
```

If you see this in your endpoint details, we might need to use that instead of the generic API URL.

---

**Once you verify the endpoint status in RunPod console, let me know what you find and I can adjust the code accordingly.**
