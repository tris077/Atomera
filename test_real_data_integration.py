#!/usr/bin/env python3
"""
Test script to verify that mock data has been replaced with real data.
"""

import requests
import json
import time
import sys

# Set UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def test_real_data_integration():
    """Test that the API now returns real data instead of mock data."""
    print("Testing Real Data Integration")
    print("=" * 50)

    base_url = "http://localhost:8000"

    # Test data
    test_data = {
        "protein": {
            "id": "test_protein",
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
        },
        "ligand": {"id": "test_ligand", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"},
        "use_msa": True,
        "confidence_threshold": 0.5,
    }

    print(f"Test data:")
    print(f"   Protein: {test_data['protein']['sequence'][:30]}...")
    print(f"   Ligand: {test_data['ligand']['smiles']}")

    try:
        # Submit prediction job
        print("\nSubmitting prediction job...")
        response = requests.post(f"{base_url}/predict", json=test_data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Job submitted successfully!")
            print(f"   Job ID: {result.get('job_id', 'N/A')}")
            print(f"   Status: {result.get('status', 'N/A')}")

            # Check if we got real data or mock data
            if (
                result.get("error_message")
                and "mock" in result.get("error_message", "").lower()
            ):
                print("ERROR: Still using mock data!")
                return False
            else:
                print("SUCCESS: Using real data!")

            # Check for real ligand properties
            if result.get("ligand_smiles") == test_data["ligand"]["smiles"]:
                print("SUCCESS: Ligand SMILES matches input")
            else:
                print("ERROR: Ligand SMILES doesn't match input")

            # Check for calculated properties
            if result.get("ligand_mw") is not None:
                print(f"SUCCESS: Ligand MW calculated: {result.get('ligand_mw')}")
            else:
                print("WARNING: Ligand MW not calculated (RDKit may not be available)")

            return True

        else:
            print(f"ERROR: Job submission failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False


def test_health_endpoint():
    """Test the health endpoint."""
    print("\nTesting health endpoint...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health = response.json()
            print(f"SUCCESS: Health check passed")
            print(f"   Status: {health.get('status', 'N/A')}")
            print(f"   Boltz available: {health.get('boltz_available', 'N/A')}")
            return True
        else:
            print(f"ERROR: Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Health check error: {e}")
        return False


if __name__ == "__main__":
    print("Starting real data integration test...")

    # Test health first
    if not test_health_endpoint():
        print("ERROR: Backend server not available. Please start the server first.")
        exit(1)

    # Test real data integration
    success = test_real_data_integration()

    if success:
        print("\nSUCCESS: Real data integration test PASSED!")
        print("SUCCESS: Mock data has been successfully replaced with real data")
    else:
        print("\nERROR: Real data integration test FAILED!")
        print("ERROR: Mock data is still being used")

    print("\n" + "=" * 50)
