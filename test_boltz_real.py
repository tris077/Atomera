#!/usr/bin/env python3
"""
Test script to verify real Boltz-2 execution with increased timeout.
"""

import requests
import time
import json

def test_real_boltz():
    """Test real Boltz-2 execution."""
    
    # Test data
    test_data = {
        "protein": {
            "sequence": "MKTVRQERLKSIVRILERSKEPVSGAQLAEELSVSRQVIVQDIAYLRSLGYNIVATPRGYVLAGG",
            "id": "A"
        },
        "ligand": {
            "smiles": "CCO",
            "id": "B"
        },
        "use_msa": True,
        "confidence_threshold": 0.5
    }
    
    print("🚀 Testing real Boltz-2 execution...")
    print(f"Protein sequence: {test_data['protein']['sequence'][:50]}...")
    print(f"Ligand SMILES: {test_data['ligand']['smiles']}")
    print()
    
    # Submit prediction
    print("📤 Submitting prediction...")
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        job_id = result["job_id"]
        print(f"✅ Job submitted successfully! Job ID: {job_id}")
    except Exception as e:
        print(f"❌ Failed to submit prediction: {e}")
        return
    
    # Monitor job status
    print("\n⏳ Monitoring job progress...")
    start_time = time.time()
    
    while True:
        try:
            # Get job status
            status_response = requests.get(f"http://localhost:8000/jobs/{job_id}")
            status_response.raise_for_status()
            status_data = status_response.json()
            
            status = status_data["status"]
            progress = status_data.get("progress", 0)
            elapsed = time.time() - start_time
            
            print(f"⏱️  [{elapsed:.1f}s] Status: {status} | Progress: {progress}%")
            
            if status == "completed":
                print("🎉 Job completed! Getting results...")
                break
            elif status == "failed":
                print("❌ Job failed!")
                print(f"Error: {status_data.get('error_message', 'Unknown error')}")
                return
            elif elapsed > 900:  # 15 minutes timeout
                print("⏰ Test timeout reached (15 minutes)")
                return
                
            time.sleep(5)  # Check every 5 seconds
            
        except Exception as e:
            print(f"❌ Error monitoring job: {e}")
            time.sleep(5)
    
    # Get results
    try:
        result_response = requests.get(f"http://localhost:8000/jobs/{job_id}/result")
        result_response.raise_for_status()
        result_data = result_response.json()
        
        print("\n📊 RESULTS:")
        print(f"  Job ID: {result_data['job_id']}")
        print(f"  Status: {result_data['status']}")
        print(f"  Affinity (log IC50): {result_data.get('affinity_pred_value', 'N/A')}")
        print(f"  Probability: {result_data.get('affinity_probability_binary', 'N/A')}")
        print(f"  Confidence: {result_data.get('confidence_score', 'N/A')}")
        print(f"  Processing time: {result_data.get('processing_time_seconds', 'N/A')}s")
        print(f"  Poses generated: {result_data.get('poses_generated', 'N/A')}")
        
        # Check if this is real Boltz-2 data or mock data
        if result_data.get('error_message'):
            print(f"  ⚠️  Error message: {result_data['error_message']}")
            print("  🤖 This appears to be MOCK DATA due to Boltz-2 failure")
        else:
            print("  ✅ This appears to be REAL BOLTZ-2 DATA!")
            
    except Exception as e:
        print(f"❌ Failed to get results: {e}")

if __name__ == "__main__":
    test_real_boltz()
