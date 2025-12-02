# Atomera RunPod Integration

This directory contains everything you need to deploy Atomera's Boltz-2 inference to RunPod GPU cloud.

## 📚 Documentation Files

Start here based on your needs:

### 🚀 Want to deploy right now?
→ **[QUICK_START.md](QUICK_START.md)** - 15-minute deployment guide

### 📖 Want detailed instructions?
→ **[DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md)** - Complete step-by-step guide with troubleshooting

### ✅ Want to understand what was done?
→ **[RUNPOD_INTEGRATION_COMPLETE.md](RUNPOD_INTEGRATION_COMPLETE.md)** - Full summary of the integration

### 🔧 Technical documentation?
→ **[RUNPOD_INTEGRATION.md](RUNPOD_INTEGRATION.md)** - Technical architecture and API reference
→ **[RUNPOD_ENDPOINT_SETUP.md](RUNPOD_ENDPOINT_SETUP.md)** - Endpoint configuration details

## 🛠️ Tools Provided

### Deployment Scripts

- **`build_and_push_docker.bat`** (Windows) - Build and push Docker image
- **`build_and_push_docker.sh`** (Linux/Mac) - Build and push Docker image
- **`setup_runpod.py`** (All platforms) - Interactive configuration wizard

### Core Files

- **`Dockerfile`** - Production Docker image for RunPod
- **`runpod_handler_template.py`** - Handler executed on RunPod GPU
- **`backend/.env.example`** - Environment variables template

### Testing

- **`backend/test_runpod_connection.py`** - Test RunPod connection

## ⚡ Quick Deployment

```bash
# 1. Build Docker image
build_and_push_docker.bat  # Windows
./build_and_push_docker.sh # Linux/Mac

# 2. Create RunPod endpoint (via web console)
# → https://www.runpod.io/console/serverless

# 3. Configure Atomera
python setup_runpod.py

# 4. Start Atomera
cd backend && python main.py
```

See [QUICK_START.md](QUICK_START.md) for details.

## 📋 What You Need

Before deploying:

- [ ] RunPod account (sign up at https://www.runpod.io)
- [ ] RunPod API key (get from settings)
- [ ] Docker installed on your machine
- [ ] GitHub or Docker Hub account (for image registry)

## 🎯 Status

**Integration Status**: ✅ **COMPLETE AND READY**

All code is written and verified. You just need to:
1. Build the Docker image
2. Create a RunPod endpoint
3. Enter your credentials

## 💰 Cost Estimates

- **Per job**: $0.01 - $0.15 (typical)
- **Per hour**: ~$0.30 (RTX 3090) when active
- **Idle cost**: $0 (auto-shutdown after 5 seconds)

## 🏗️ Architecture

```
Frontend (React)
    ↓
Backend (FastAPI)
    ↓
RunPod API
    ↓
GPU Worker (Docker Container)
    ↓
Boltz-2 Prediction
    ↓
Results
```

## 📞 Support

- **Quick issues**: See troubleshooting in [DEPLOY_TO_RUNPOD.md](DEPLOY_TO_RUNPOD.md)
- **RunPod help**: https://docs.runpod.io
- **Boltz-2 help**: https://github.com/jwohlwend/boltz

## 📝 Files Created

This integration added:

- `Dockerfile` - Production image
- `build_and_push_docker.bat` - Windows build script
- `build_and_push_docker.sh` - Linux/Mac build script
- `setup_runpod.py` - Setup wizard
- `QUICK_START.md` - Quick deployment guide
- `DEPLOY_TO_RUNPOD.md` - Detailed deployment guide
- `RUNPOD_INTEGRATION_COMPLETE.md` - Integration summary
- `README_RUNPOD.md` - This file

Existing files (already working):
- `backend/services/runpod_service.py` - RunPod API client
- `backend/services/boltz_service.py` - Boltz-2 service with RunPod
- `runpod_handler_template.py` - RunPod handler
- `backend/test_runpod_connection.py` - Connection test
- Other integration files...

## ✨ Features

- ✅ GPU-accelerated Boltz-2 predictions
- ✅ Auto-scaling (pay only for what you use)
- ✅ Automatic fallback to local if RunPod unavailable
- ✅ Real-time job status updates
- ✅ Progress tracking (0-100%)
- ✅ Error handling and recovery
- ✅ Pose file downloads
- ✅ Cost-optimized (5s idle timeout)

## 🔍 Testing

After deployment, test with:

```bash
# Test connection
cd backend
python test_runpod_connection.py

# Expected output:
# ✅ API key valid
# ✅ Your endpoints:
#   - atomera-boltz2 (abc123...) - Active
```

Then create a job in the UI and verify it completes successfully.

---

**Ready to deploy?** Start with [QUICK_START.md](QUICK_START.md)!
