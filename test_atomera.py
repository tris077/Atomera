#!/usr/bin/env python3
"""
Simple test script for Atomera API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Health: {data['status']}")
        print(f"✅ Boltz-2 Available: {data['boltz_available']}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_examples():
    """Test the examples endpoint"""
    print("\n📚 Testing examples endpoint...")
    response = requests.get(f"{BASE_URL}/examples")
    if response.status_code == 200:
        data = response.json()
        print("✅ Examples loaded successfully")
        print(f"   Proteins: {list(data['proteins'].keys())}")
        print(f"   Ligands: {list(data['ligands'].keys())}")
        return data
    else:
        print(f"❌ Examples failed: {response.status_code}")
        return None

def test_prediction():
    """Test a simple prediction"""
    print("\n🧬 Testing prediction...")
    
    # Use example data
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
    
    # Submit prediction
    response = requests.post(f"{BASE_URL}/predict", json=payload)
    if response.status_code == 200:
        data = response.json()
        job_id = data['job_id']
        print(f"✅ Job created: {job_id}")
        
        # Check job status
        print("⏳ Checking job status...")
        for i in range(10):  # Check up to 10 times
            time.sleep(2)
            status_response = requests.get(f"{BASE_URL}/jobs/{job_id}")
            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"   Status: {status_data['status']} ({status_data['progress']}%)")
                
                if status_data['status'] == 'completed':
                    print("✅ Job completed successfully!")
                    return job_id
                elif status_data['status'] == 'failed':
                    print("❌ Job failed")
                    return None
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                return None
        
        print("⏰ Job still processing after 20 seconds")
        return job_id
    else:
        print(f"❌ Prediction failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_results(job_id):
    """Test getting job results"""
    if not job_id:
        return
    
    print(f"\n📊 Testing results for job {job_id}...")
    response = requests.get(f"{BASE_URL}/jobs/{job_id}/result")
    if response.status_code == 200:
        data = response.json()
        print("✅ Results retrieved successfully!")
        print(f"   Status: {data['status']}")
        print(f"   Affinity: {data.get('affinity_pred_value', 'N/A')}")
        print(f"   Confidence: {data.get('confidence_score', 'N/A')}")
        print(f"   Poses: {data.get('poses_generated', 'N/A')}")
        return True
    else:
        print(f"❌ Results failed: {response.status_code}")
        return False

def main():
    """Run all tests"""
    print("🧬 Atomera API Test Suite")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed. Make sure the backend is running.")
        return
    
    # Test examples
    examples = test_examples()
    if not examples:
        print("\n❌ Examples test failed.")
        return
    
    # Test prediction
    job_id = test_prediction()
    
    # Test results
    if job_id:
        test_results(job_id)
    
    print("\n🎉 Test suite completed!")
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:8081 in your browser")
    print("   2. Create a new job using the web interface")
    print("   3. Watch the real-time processing")

if __name__ == "__main__":
    main()
