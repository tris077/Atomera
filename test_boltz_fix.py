#!/usr/bin/env python3
"""
Test script to verify Boltz-2 command fix
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_simple_prediction():
    """Test a simple prediction with the fixed command"""
    print("🧬 Testing Boltz-2 command fix...")
    
    # Use a very short sequence to minimize processing time
    payload = {
        "protein": {
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "id": "insulin"
        },
        "ligand": {
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "id": "aspirin"
        },
        "use_msa": True,
        "confidence_threshold": 0.7
    }
    
    print("📤 Submitting prediction...")
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        print(f"✅ Job created: {job_id}")
        
        # Monitor job status
        print("⏳ Monitoring job status...")
        for i in range(15):  # Check up to 15 times (30 seconds)
            time.sleep(2)
            status_response = requests.get(f"{BASE_URL}/jobs/{job_id}")
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Status: {status_data['status']} ({status_data['progress']}%)")
                
                if status_data['status'] == 'completed':
                    print("🎉 SUCCESS! Job completed successfully!")
                    return True
                elif status_data['status'] == 'failed':
                    print("❌ Job failed - checking backend logs for details")
                    return False
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                return False
        
        print("⏰ Job still processing after 30 seconds")
        return False
    else:
        print(f"❌ Prediction submission failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

if __name__ == "__main__":
    print("🔧 Testing Boltz-2 Command Fix")
    print("=" * 40)
    
    success = test_simple_prediction()
    
    if success:
        print("\n✅ Fix successful! Boltz-2 is working correctly.")
    else:
        print("\n❌ Fix needs more work. Check the backend logs for details.")
