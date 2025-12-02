#!/usr/bin/env python3
"""
Test Boltz-2 installation and job execution.
"""

def test_boltz_installation():
    """Test if Boltz-2 is properly installed."""
    print("=== TESTING BOLTZ-2 INSTALLATION ===")
    
    try:
        import boltz
        print("SUCCESS: Boltz imported")
        print(f"Version: {getattr(boltz, '__version__', 'unknown')}")
        return True
    except ImportError as e:
        print(f"ERROR: Boltz not installed: {e}")
        return False

def test_job_submission():
    """Test submitting a job to see what error occurs."""
    print("\n=== TESTING JOB SUBMISSION ===")
    
    try:
        import requests
        import json
        
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
        
        print("Submitting test job...")
        response = requests.post('http://localhost:8000/predict', json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: Job submitted")
            print(f"Job ID: {result.get('job_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            
            if 'error_message' in result:
                print(f"Error: {result['error_message']}")
        else:
            print(f"ERROR: Job submission failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    boltz_ok = test_boltz_installation()
    test_job_submission()
    
    if not boltz_ok:
        print("\n=== SOLUTION ===")
        print("Boltz-2 is not installed. You need to:")
        print("1. Install Boltz-2: pip install boltz")
        print("2. Or use the mock mode for testing")
        print("3. Or install from source if needed")
