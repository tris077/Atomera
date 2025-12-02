#!/usr/bin/env python3
"""
Setup script for running Atomera on Google Colab.
This creates a notebook that can run the full application in the cloud.
"""

colab_notebook = """
# 🧬 Atomera on Google Colab
# Run this in Google Colab for free GPU/TPU access

# Install dependencies
!pip install fastapi uvicorn python-multipart boltz rdkit-pypi

# Download the Atomera code
!git clone https://github.com/your-repo/atomera.git
%cd atomera

# Start the backend server
!python backend/main.py &
# Wait a moment for server to start
import time
time.sleep(5)

# Test the API
import requests
response = requests.get('http://localhost:8000/health')
print("Backend Status:", response.json())

# Now you can submit jobs with real Boltz-2 execution!
# The cloud environment has much more power than your local PC
"""

with open("atomera_colab.ipynb", "w") as f:
    f.write(colab_notebook)

print("Created atomera_colab.ipynb for Google Colab")
print("Upload this to Google Colab and run it for cloud computing!")















