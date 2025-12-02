import requests
import json

# Simple test data
data = {
    "protein": {
        "sequence": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
        "id": "A",
    },
    "ligand": {"smiles": "CCO", "id": "B"},
    "use_msa": True,
    "confidence_threshold": 0.5,
}

print("Submitting prediction...")
try:
    response = requests.post("http://localhost:8000/predict", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Job ID: {result['job_id']}")
        print("✅ Prediction submitted successfully!")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")





















