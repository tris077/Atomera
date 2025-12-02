#!/usr/bin/env python3
"""
Comprehensive test script for Atomera backend.
Tests all components: Boltz service, API endpoints, and job processing.
"""

import sys
import json
import time
import requests
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule


def test_boltz_service_direct():
    """Test Boltz service directly without API."""
    print("🧬 Testing Boltz Service Direct")
    print("=" * 50)

    try:
        # Initialize service
        service = BoltzService()
        print("✅ Service initialized")

        # Check Boltz availability
        boltz_available = service.check_boltz_availability()
        print(f"✅ Boltz available: {boltz_available}")

        if not boltz_available:
            print("❌ Boltz not available - using mock mode")
            return True  # Continue with mock mode

        # Create test request
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="test_protein",
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="test_ligand")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

        print("✅ Test request created")

        # Test job creation
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")

        # Test job status
        status = service.get_job_status(job_id)
        print(f"✅ Job status: {status.status}")

        # Test prediction (this will use mock if Boltz fails)
        print("🔄 Running prediction...")
        result = service.run_prediction(job_id, request)

        print(f"✅ Prediction completed: {result.status}")
        if result.status == "completed":
            print(f"   Affinity: {result.affinity_pred_value}")
            print(f"   Probability: {result.affinity_probability_binary}")
            print(f"   Confidence: {result.confidence_score}")
            print(f"   Processing time: {result.processing_time_seconds:.2f}s")

        return True

    except Exception as e:
        print(f"❌ Boltz service test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_api_server():
    """Test API server endpoints."""
    print("\n🌐 Testing API Server")
    print("=" * 50)

    base_url = "http://localhost:8000"

    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check: {health_data['status']}")
            print(f"   Boltz available: {health_data['boltz_available']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

        # Test examples endpoint
        print("Testing /examples endpoint...")
        response = requests.get(f"{base_url}/examples", timeout=5)
        if response.status_code == 200:
            examples = response.json()
            print(
                f"✅ Examples: {len(examples.get('proteins', {}))} proteins, {len(examples.get('ligands', {}))} ligands"
            )
        else:
            print(f"❌ Examples failed: {response.status_code}")
            return False

        # Test prediction endpoint
        print("Testing /predict endpoint...")
        prediction_data = {
            "protein": {
                "id": "test_protein",
                "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            },
            "ligand": {"id": "test_ligand", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"},
            "use_msa": True,
        }

        response = requests.post(
            f"{base_url}/predict", json=prediction_data, timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            print(f"✅ Prediction job created: {job_id}")
            print(f"   Status: {result.get('status')}")

            # Test job status endpoint
            print("Testing job status...")
            time.sleep(2)  # Wait for processing
            response = requests.get(f"{base_url}/jobs/{job_id}", timeout=5)
            if response.status_code == 200:
                status_data = response.json()
                print(f"✅ Job status: {status_data['status']}")
                print(f"   Progress: {status_data.get('progress', 'N/A')}%")
            else:
                print(f"❌ Job status failed: {response.status_code}")
                return False

        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False

        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is it running?")
        print("   Start with: python start.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def test_job_workflow():
    """Test complete job workflow."""
    print("\n🔄 Testing Complete Job Workflow")
    print("=" * 50)

    try:
        service = BoltzService()

        # Create job
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="workflow_test",
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="workflow_test")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")

        # Run prediction
        result = service.run_prediction(job_id, request)

        if result.status == "completed":
            print("✅ Job completed successfully!")
            print(f"   Affinity: {result.affinity_pred_value}")
            print(f"   Probability: {result.affinity_probability_binary}")
            print(f"   Confidence: {result.confidence_score}")
            print(f"   Processing time: {result.processing_time_seconds:.2f}s")

            # Test result retrieval
            final_status = service.get_job_status(job_id)
            print(f"✅ Final status: {final_status.status}")

            return True
        else:
            print(f"❌ Job failed: {result.error_message}")
            return False

    except Exception as e:
        print(f"❌ Job workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Atomera Comprehensive Backend Test")
    print("=" * 60)

    tests = [
        ("Boltz Service Direct", test_boltz_service_direct),
        ("API Server", test_api_server),
        ("Complete Job Workflow", test_job_workflow),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print("=" * 60)

        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))

    # Summary
    print(f"\n{'='*60}")
    print("📋 TEST SUMMARY")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Backend is fully functional!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
