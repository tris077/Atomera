# 🚀 Quick Cloud Setup Guide

## 🟢 RunPod Setup (Recommended)

### Step 1: Launch Instance

1. Go to [RunPod.io](https://runpod.io)
2. Click "Community GPU"
3. Select **L4 (24GB)** or **A10G (24GB)**
4. Choose **PyTorch** template
5. Click "Deploy"

### Step 2: Connect & Setup

```bash
# SSH into your instance
ssh root@<your-runpod-ip>

# Clone Atomera
git clone https://github.com/your-repo/atomera.git
cd atomera

# Run cloud deployment script
python deploy_cloud.py

# Start backend
cd backend && python main.py
```

### Step 3: Access Your App

- **API**: `http://<your-runpod-ip>:8000`
- **Docs**: `http://<your-runpod-ip>:8000/docs`

---

## 🟣 Lambda Labs Setup

### Step 1: Launch Instance

1. Go to [Lambda Labs](https://lambdalabs.com)
2. Click "GPU Cloud"
3. Select **A10 (24GB)** or **A100 (40GB)**
4. Choose **PyTorch** environment
5. Click "Launch"

### Step 2: Connect & Setup

```bash
# SSH into your instance
ssh ubuntu@<your-lambda-ip>

# Clone Atomera
git clone https://github.com/your-repo/atomera.git
cd atomera

# Run cloud deployment script
python deploy_cloud.py

# Start backend
cd backend && python main.py
```

### Step 3: Access Your App

- **API**: `http://<your-lambda-ip>:8000`
- **Docs**: `http://<your-lambda-ip>:8000/docs`

---

## 🔵 AWS EC2 Setup

### Step 1: Launch Instance

1. Go to [AWS EC2 Console](https://console.aws.amazon.com/ec2/)
2. Click "Launch Instance"
3. Search for "Deep Learning AMI"
4. Select **g5.xlarge** (A10G GPU)
5. Configure security group to allow port 8000
6. Launch instance

### Step 2: Connect & Setup

```bash
# SSH into your instance
ssh -i your-key.pem ec2-user@<your-ec2-ip>

# Clone Atomera
git clone https://github.com/your-repo/atomera.git
cd atomera

# Run cloud deployment script
python deploy_cloud.py

# Start backend
cd backend && python main.py
```

### Step 3: Access Your App

- **API**: `http://<your-ec2-ip>:8000`
- **Docs**: `http://<your-ec2-ip>:8000/docs`

---

## ⚡ Performance Expectations

| Provider          | GPU       | Expected Job Time | Cost/Hour |
| ----------------- | --------- | ----------------- | --------- |
| **RunPod L4**     | L4 24GB   | 1-2 minutes       | $0.40     |
| **RunPod A10G**   | A10G 24GB | 1-2 minutes       | $0.60     |
| **Lambda A10**    | A10 24GB  | 1-2 minutes       | $0.50     |
| **Lambda A100**   | A100 40GB | 30-60 seconds     | $1.10     |
| **AWS g5.xlarge** | A10G 16GB | 1-2 minutes       | $1.20     |

---

## 🔧 Configuration Tips

### For Maximum Performance:

```bash
# Set in backend/.env
ACCELERATOR=gpu
DEVICES=1
DIFFUSION_SAMPLES=3
MAX_CONCURRENT_JOBS=2
```

### For Cost Optimization:

```bash
# Set in backend/.env
ACCELERATOR=gpu
DEVICES=1
DIFFUSION_SAMPLES=1
MAX_CONCURRENT_JOBS=1
```

---

## 🎯 Recommended Workflow

1. **Development**: Use Google Colab (free)
2. **Testing**: Use RunPod L4 ($0.40/hour)
3. **Production**: Use Lambda A10 ($0.50/hour) or AWS g5.xlarge ($1.20/hour)

---

## 🆘 Troubleshooting

### GPU Not Detected:

```bash
# Check GPU status
nvidia-smi

# Install CUDA if needed
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Memory Issues:

```bash
# Reduce concurrent jobs
echo "MAX_CONCURRENT_JOBS=1" >> backend/.env

# Reduce diffusion samples
echo "DIFFUSION_SAMPLES=1" >> backend/.env
```

### Port Access Issues:

```bash
# Check if port 8000 is open
netstat -tlnp | grep 8000

# Open port in firewall (Ubuntu)
sudo ufw allow 8000
```

---

**🎉 You're ready to run Boltz-2 at scale!**
