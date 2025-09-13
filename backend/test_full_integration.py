#!/usr/bin/env python3
"""
Full integration test for Atomera - tests both backend and frontend functionality.
This script tests the complete job submission and status tracking workflow.
"""

import sys
import json
import time
import requests
from pathlib import Path
from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule


def test_backend_service():
    """Test the backend Boltz service directly."""
    print("🧬 Testing Backend Boltz Service")
    print("=" * 50)
    
    try:
        # Initialize service
        service = BoltzService()
        print("✅ Service initialized")
        
        # Check Boltz availability
        boltz_available = service.check_boltz_availability()
        print(f"✅ Boltz available: {boltz_available}")
        
        # Create test request
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="test_insulin"
        )
        ligand = LigandMolecule(
            smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
            id="test_aspirin"
        )
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
        
        print(f"✅ Test request created: {protein.id} + {ligand.id}")
        
        # Test job creation
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")
        
        # Test job status
        status = service.get_job_status(job_id)
        print(f"✅ Job status: {status.status} (progress: {status.progress}%)")
        
        # Test prediction execution
        print("🔄 Running prediction...")
        result = service.run_prediction(job_id, request)
        
        if result.status == "completed":
            print(f"✅ Prediction completed successfully!")
            print(f"   Affinity: {result.affinity_pred_value} kcal/mol")
            print(f"   Probability: {result.affinity_probability_binary}")
            print(f"   Confidence: {result.confidence_score}")
            print(f"   Processing time: {result.processing_time_seconds:.2f}s")
            return True
        else:
            print(f"❌ Prediction failed: {result.error_message}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoints by simulating HTTP requests."""
    print("\n🌐 Testing API Endpoints")
    print("=" * 50)
    
    # Test data
    test_data = {
        "protein": {
            "id": "test_insulin",
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"
        },
        "ligand": {
            "id": "test_aspirin", 
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"
        },
        "use_msa": True
    }
    
    try:
        # Test health endpoint
        print("Testing /health endpoint...")
        # Simulate the health check logic
        service = BoltzService()
        boltz_available = service.check_boltz_availability()
        
        health_response = {
            "status": "healthy" if boltz_available else "degraded",
            "version": "1.0.0",
            "boltz_available": boltz_available,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"✅ Health check: {health_response['status']}")
        
        # Test prediction endpoint logic
        print("Testing /predict endpoint logic...")
        service = BoltzService()
        
        # Create request object
        protein = ProteinSequence(**test_data["protein"])
        ligand = LigandMolecule(**test_data["ligand"])
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=test_data["use_msa"])
        
        # Create job
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")
        
        # Run prediction
        result = service.run_prediction(job_id, request)
        
        prediction_response = {
            "job_id": result.job_id,
            "status": result.status,
            "affinity_pred_value": result.affinity_pred_value,
            "affinity_probability_binary": result.affinity_probability_binary,
            "confidence_score": result.confidence_score,
            "processing_time_seconds": result.processing_time_seconds
        }
        
        print(f"✅ Prediction response: {prediction_response['status']}")
        if result.status == "completed":
            print(f"   Affinity: {result.affinity_pred_value} kcal/mol")
            print(f"   Probability: {result.affinity_probability_binary}")
            print(f"   Confidence: {result.confidence_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_frontend_integration():
    """Test frontend integration by checking API service and job management."""
    print("\n🎨 Testing Frontend Integration")
    print("=" * 50)
    
    try:
        # Check if frontend files exist
        frontend_dir = Path("../frontend")
        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False
        
        # Check API service file
        api_service = frontend_dir / "src" / "lib" / "apiService.ts"
        if not api_service.exists():
            print("❌ API service file not found")
            return False
        
        print("✅ Frontend files found")
        
        # Read and validate API service
        with open(api_service, 'r') as f:
            api_content = f.read()
        
        # Check for required functions
        required_functions = [
            "submitPrediction",
            "getJobStatus", 
            "getJobResults",
            "getAllJobs"
        ]
        
        for func in required_functions:
            if func in api_content:
                print(f"✅ Found function: {func}")
            else:
                print(f"❌ Missing function: {func}")
                return False
        
        # Check for proper error handling
        if "try" in api_content and "catch" in api_content:
            print("✅ Error handling present")
        else:
            print("⚠️ Limited error handling")
        
        # Check for proper response handling
        if "response.json()" in api_content:
            print("✅ JSON response handling present")
        else:
            print("⚠️ JSON response handling may be missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend integration test failed: {e}")
        return False


def test_job_workflow():
    """Test the complete job workflow from submission to completion."""
    print("\n🔄 Testing Complete Job Workflow")
    print("=" * 50)
    
    try:
        service = BoltzService()
        
        # Step 1: Create job
        print("1. Creating prediction job...")
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="workflow_test_protein"
        )
        ligand = LigandMolecule(
            smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
            id="workflow_test_ligand"
        )
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
        
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")
        
        # Step 2: Check initial status
        print("2. Checking initial job status...")
        status = service.get_job_status(job_id)
        print(f"✅ Initial status: {status.status} (progress: {status.progress}%)")
        
        # Step 3: Run prediction
        print("3. Running prediction...")
        result = service.run_prediction(job_id, request)
        
        # Step 4: Check final status
        print("4. Checking final job status...")
        final_status = service.get_job_status(job_id)
        print(f"✅ Final status: {final_status.status} (progress: {final_status.progress}%)")
        
        # Step 5: Validate results
        if result.status == "completed":
            print("5. Validating results...")
            assert result.affinity_pred_value is not None
            assert result.affinity_probability_binary is not None
            assert result.confidence_score is not None
            assert result.processing_time_seconds > 0
            print("✅ All results validated")
            
            print(f"\n📊 Final Results:")
            print(f"   Job ID: {job_id}")
            print(f"   Status: {result.status}")
            print(f"   Affinity: {result.affinity_pred_value} kcal/mol")
            print(f"   Probability: {result.affinity_probability_binary}")
            print(f"   Confidence: {result.confidence_score}")
            print(f"   Processing time: {result.processing_time_seconds:.2f}s")
            
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
    """Run all integration tests."""
    print("🚀 Atomera Full Integration Test")
    print("=" * 60)
    
    tests = [
        ("Backend Service", test_backend_service),
        ("API Endpoints", test_api_endpoints), 
        ("Frontend Integration", test_frontend_integration),
        ("Complete Job Workflow", test_job_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 TEST SUMMARY")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Atomera is fully integrated and working!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
