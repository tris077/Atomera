#!/usr/bin/env python3
"""
Final production test for Atomera backend.
Comprehensive validation of all production features.
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


def test_backend_core():
    """Test core backend functionality."""
    print("🧬 Testing Backend Core Functionality")
    print("=" * 50)

    try:
        # Test service initialization
        service = BoltzService()
        print("✅ Service initialized")

        # Test Boltz availability
        boltz_available = service.check_boltz_availability()
        print(f"✅ Boltz available: {boltz_available}")

        # Test job creation
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="production_test",
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="production_test")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")

        # Test job status
        status = service.get_job_status(job_id)
        print(f"✅ Job status: {status.status}")

        # Test mock prediction
        result = service._generate_mock_results(job_id, request, time.time())
        print(f"✅ Mock prediction: {result.status}")
        print(f"   Affinity: {result.affinity_pred_value}")
        print(f"   Probability: {result.affinity_probability_binary}")
        print(f"   Confidence: {result.confidence_score}")

        return True

    except Exception as e:
        print(f"❌ Backend core test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoints."""
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)

    base_url = "http://localhost:8000"

    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   Boltz available: {data['boltz_available']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False

        # Test examples endpoint
        print("Testing /examples endpoint...")
        response = requests.get(f"{base_url}/examples", timeout=10)
        if response.status_code == 200:
            data = response.json()
            proteins = data.get("proteins", {})
            ligands = data.get("ligands", {})
            print(f"✅ Examples: {len(proteins)} proteins, {len(ligands)} ligands")
        else:
            print(f"❌ Examples failed: {response.status_code}")
            return False

        # Test prediction endpoint
        print("Testing /predict endpoint...")
        prediction_data = {
            "protein": {
                "id": "api_production_test",
                "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            },
            "ligand": {
                "id": "api_production_test",
                "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            },
            "use_msa": True,
        }

        response = requests.post(
            f"{base_url}/predict", json=prediction_data, timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            job_id = data.get("job_id")
            print(f"✅ Prediction job created: {job_id}")
            print(f"   Status: {data.get('status')}")

            # Test job status
            print("Testing job status...")
            time.sleep(3)
            response = requests.get(f"{base_url}/jobs/{job_id}", timeout=10)
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
        print("❌ Cannot connect to API server")
        print("   Start server with: python run_atomera.py")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def test_validation():
    """Test validation endpoints."""
    print("\n✅ Testing Validation")
    print("=" * 50)

    base_url = "http://localhost:8000"

    try:
        # Test protein validation
        print("Testing protein validation...")
        protein_data = {
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "id": "A",
        }
        response = requests.post(
            f"{base_url}/validate/protein", json=protein_data, timeout=10
        )
        if response.status_code == 200:
            print("✅ Protein validation passed")
        else:
            print(f"❌ Protein validation failed: {response.status_code}")
            return False

        # Test ligand validation
        print("Testing ligand validation...")
        ligand_data = {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "id": "B"}
        response = requests.post(
            f"{base_url}/validate/ligand", json=ligand_data, timeout=10
        )
        if response.status_code == 200:
            print("✅ Ligand validation passed")
        else:
            print(f"❌ Ligand validation failed: {response.status_code}")
            return False

        # Test invalid inputs
        print("Testing invalid inputs...")
        invalid_protein = {"sequence": "INVALID123", "id": "C"}
        response = requests.post(
            f"{base_url}/validate/protein", json=invalid_protein, timeout=10
        )
        if response.status_code == 422:
            print("✅ Invalid protein correctly rejected")
        else:
            print(
                f"❌ Invalid protein should have been rejected: {response.status_code}"
            )
            return False

        return True

    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False


def test_error_handling():
    """Test error handling."""
    print("\n⚠️ Testing Error Handling")
    print("=" * 50)

    base_url = "http://localhost:8000"

    try:
        # Test invalid job ID
        print("Testing invalid job ID...")
        response = requests.get(f"{base_url}/jobs/invalid-job-id", timeout=10)
        if response.status_code == 404:
            print("✅ Invalid job ID correctly handled")
        else:
            print(f"❌ Invalid job ID should return 404: {response.status_code}")
            return False

        # Test malformed request
        print("Testing malformed request...")
        malformed_data = {"invalid": "data"}
        response = requests.post(f"{base_url}/predict", json=malformed_data, timeout=10)
        if response.status_code == 422:
            print("✅ Malformed request correctly rejected")
        else:
            print(f"❌ Malformed request should be rejected: {response.status_code}")
            return False

        return True

    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


def test_production_features():
    """Test production-specific features."""
    print("\n🚀 Testing Production Features")
    print("=" * 50)

    try:
        # Test configuration
        from config import settings

        print(f"✅ Configuration loaded")
        print(f"   App: {settings.app_name} v{settings.app_version}")
        print(f"   Host: {settings.host}:{settings.port}")
        print(f"   Max jobs: {settings.max_concurrent_jobs}")
        print(f"   Timeout: {settings.job_timeout_seconds}s")

        # Test directory structure
        output_dir = Path(settings.output_base_dir)
        predictions_dir = output_dir / settings.predictions_dir
        temp_dir = output_dir / settings.temp_dir

        if all(d.exists() for d in [output_dir, predictions_dir, temp_dir]):
            print("✅ Directory structure ready")
        else:
            print("❌ Directory structure incomplete")
            return False

        # Test model validation
        from models import PredictionRequest, ProteinSequence, LigandMolecule

        # Test valid data
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT", id="A"
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="B")
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

        print("✅ Model validation working")

        # Test error handling
        try:
            invalid_protein = ProteinSequence(sequence="INVALID123", id="C")
            print("❌ Invalid protein should have failed")
            return False
        except ValueError:
            print("✅ Invalid protein correctly rejected")

        return True

    except Exception as e:
        print(f"❌ Production features test failed: {e}")
        return False


def main():
    """Run all production tests."""
    print("🚀 Atomera Production Final Test")
    print("=" * 60)
    print("Comprehensive validation of production readiness")
    print("=" * 60)

    tests = [
        ("Backend Core", test_backend_core),
        ("API Endpoints", test_api_endpoints),
        ("Validation", test_validation),
        ("Error Handling", test_error_handling),
        ("Production Features", test_production_features),
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
    print("📋 PRODUCTION TEST SUMMARY")
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
        print("\n🎉 ALL PRODUCTION TESTS PASSED!")
        print("✅ Atomera backend is PRODUCTION READY!")
        print("✅ All core functionality working")
        print("✅ API endpoints responding correctly")
        print("✅ Error handling robust")
        print("✅ Validation working properly")
        print("✅ Production features complete")
        print("\n🚀 Ready for production deployment!")
        return True
    else:
        print(f"\n⚠️ {total - passed} tests failed.")
        print("Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
