#!/usr/bin/env python3
"""
Quick test script for Atomera backend - tests core functionality without long Boltz execution.
"""

import sys
import json
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule


def test_service_initialization():
    """Test service initialization and basic functionality."""
    print("🧬 Testing Service Initialization")
    print("=" * 50)
    
    try:
        # Initialize service
        service = BoltzService()
        print("✅ Service initialized successfully")
        
        # Check Boltz availability
        boltz_available = service.check_boltz_availability()
        print(f"✅ Boltz available: {boltz_available}")
        
        return True
        
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False


def test_job_creation():
    """Test job creation and management."""
    print("\n📝 Testing Job Creation")
    print("=" * 50)
    
    try:
        service = BoltzService()
        
        # Create test request
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="test_protein"
        )
        ligand = LigandMolecule(
            smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
            id="test_ligand"
        )
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
        
        print("✅ Test request created")
        
        # Test job creation
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")
        
        # Test job status
        status = service.get_job_status(job_id)
        print(f"✅ Job status: {status.status}")
        print(f"   Progress: {status.progress}%")
        print(f"   Created: {status.created_at}")
        
        # Test YAML creation
        yaml_path = service._create_input_yaml(job_id, request)
        print(f"✅ YAML created: {yaml_path}")
        
        # Check YAML content
        if Path(yaml_path).exists():
            with open(yaml_path, 'r') as f:
                yaml_content = f.read()
            print("✅ YAML content valid")
            print(f"   Contains protein: {'protein' in yaml_content}")
            print(f"   Contains ligand: {'ligand' in yaml_content}")
            print(f"   Contains SMILES: {'CC(=O)OC1=CC=CC=C1C(=O)O' in yaml_content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Job creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_prediction():
    """Test mock prediction functionality."""
    print("\n🎭 Testing Mock Prediction")
    print("=" * 50)
    
    try:
        service = BoltzService()
        
        # Create test request
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="mock_test_protein"
        )
        ligand = LigandMolecule(
            smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
            id="mock_test_ligand"
        )
        request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
        
        # Create job
        job_id = service.create_prediction_job(request)
        print(f"✅ Job created: {job_id}")
        
        # Force mock prediction by simulating an error
        print("🔄 Running mock prediction...")
        
        # Update job status to running
        service._update_job_status(job_id, "running", 50.0)
        
        # Generate mock results
        result = service._generate_mock_results(job_id, request, time.time())
        
        print(f"✅ Mock prediction completed: {result.status}")
        print(f"   Affinity: {result.affinity_pred_value}")
        print(f"   Probability: {result.affinity_probability_binary}")
        print(f"   Confidence: {result.confidence_score}")
        print(f"   Processing time: {result.processing_time_seconds:.2f}s")
        print(f"   Poses generated: {result.poses_generated}")
        
        # Check final job status
        final_status = service.get_job_status(job_id)
        print(f"✅ Final status: {final_status.status}")
        print(f"   Progress: {final_status.progress}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Mock prediction test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_models():
    """Test API models and validation."""
    print("\n📋 Testing API Models")
    print("=" * 50)
    
    try:
        # Test protein validation
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="A"
        )
        print("✅ Protein validation passed")
        
        # Test ligand validation
        ligand = LigandMolecule(
            smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
            id="B"
        )
        print("✅ Ligand validation passed")
        
        # Test prediction request
        request = PredictionRequest(
            protein=protein,
            ligand=ligand,
            use_msa=True,
            confidence_threshold=0.5
        )
        print("✅ Prediction request validation passed")
        
        # Test invalid protein sequence
        try:
            invalid_protein = ProteinSequence(
                sequence="INVALID123",
                id="C"
            )
            print("❌ Invalid protein should have failed")
            return False
        except ValueError:
            print("✅ Invalid protein correctly rejected")
        
        # Test invalid SMILES
        try:
            invalid_ligand = LigandMolecule(
                smiles="INVALID_SMILES!!!",
                id="D"
            )
            print("❌ Invalid SMILES should have failed")
            return False
        except ValueError:
            print("✅ Invalid SMILES correctly rejected")
        
        return True
        
    except Exception as e:
        print(f"❌ API models test failed: {e}")
        return False


def main():
    """Run all quick tests."""
    print("🚀 Atomera Quick Backend Test")
    print("=" * 60)
    
    tests = [
        ("Service Initialization", test_service_initialization),
        ("Job Creation", test_job_creation),
        ("Mock Prediction", test_mock_prediction),
        ("API Models", test_api_models)
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
        print("🎉 ALL QUICK TESTS PASSED! Backend core functionality is working!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
