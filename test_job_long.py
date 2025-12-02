#!/usr/bin/env python3
"""
Test job submission with longer timeout.
"""

import requests
import json
import time

def test_job_with_timeout():
    """Test job submission with longer timeout."""
    print("=== TESTING JOB WITH LONGER TIMEOUT ===")
    
    # Test data
    data = {
        "protein": {
            "id": "test_protein",
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"
        },
        "ligand": {
            "id": "test_ligand", 
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"
        },
        "use_msa": True,
        "confidence_threshold": 0.5
    }
    
    print("Submitting job with 10-minute timeout...")
    print("This may take several minutes for real Boltz-2 execution...")
    
    try:
        response = requests.post('http://localhost:8000/predict', json=data, timeout=600)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: Job completed!")
            print(f"Job ID: {result.get('job_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            
            if 'affinity_pred_value' in result:
                print(f"Affinity: {result['affinity_pred_value']}")
            if 'ligand_mw' in result:
                print(f"Ligand MW: {result['ligand_mw']}")
            if 'error_message' in result:
                print(f"Error: {result['error_message']}")
        else:
            print(f"ERROR: Job failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("TIMEOUT: Job is still running after 10 minutes")
        print("This is normal for real Boltz-2 execution")
        print("Check the backend logs for progress")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_job_with_timeout()
