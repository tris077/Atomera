"""
Integration tests for BoltzService that test real file operations.
"""

import json
import tempfile
import shutil
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule


def test_full_workflow():
    """Test the complete workflow from job creation to completion."""
    print("🧪 Testing Full BoltzService Workflow")
    print("=" * 50)
    
    # Create temporary directories
    temp_dir = tempfile.mkdtemp()
    output_dir = Path(temp_dir) / "output"
    temp_dir_path = Path(temp_dir) / "temp"
    
    try:
        # Mock settings
        with patch('services.boltz_service.settings') as mock_settings:
            mock_settings.output_base_dir = temp_dir
            mock_settings.predictions_dir = "output"
            mock_settings.temp_dir = "temp"
            mock_settings.boltz_command = "boltz"
            mock_settings.use_msa_server = False
            mock_settings.job_timeout_seconds = 300
            
            # Create service
            service = BoltzService()
            service.output_dir = output_dir
            service.temp_dir = temp_dir_path
            
            print("✅ Service created successfully")
            
            # Create sample request
            protein = ProteinSequence(
                sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
                id="insulin"
            )
            ligand = LigandMolecule(
                smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
                id="aspirin"
            )
            request = PredictionRequest(protein=protein, ligand=ligand, use_msa=True)
            
            print("✅ Sample request created")
            
            # Test 1: Create prediction job
            print("\n1. Creating prediction job...")
            job_id = service.create_prediction_job(request)
            print(f"   Job ID: {job_id}")
            
            # Verify job directory and metadata
            job_dir = service.output_dir / job_id
            assert job_dir.exists(), "Job directory should exist"
            
            metadata_file = job_dir / "metadata.json"
            assert metadata_file.exists(), "Metadata file should exist"
            
            with open(metadata_file) as f:
                metadata = json.load(f)
            
            assert metadata["job_id"] == job_id
            assert metadata["status"] == "pending"
            assert metadata["progress"] == 0.0
            print("   ✅ Job directory and metadata created")
            
            # Test 2: Check job status
            print("\n2. Checking job status...")
            status = service.get_job_status(job_id)
            assert status is not None
            assert status.job_id == job_id
            assert status.status == "pending"
            print("   ✅ Job status retrieved")
            
            # Test 3: Update job status
            print("\n3. Updating job status...")
            service._update_job_status(job_id, "running", 50.0)
            
            status = service.get_job_status(job_id)
            assert status.status == "running"
            assert status.progress == 50.0
            print("   ✅ Job status updated")
            
            # Test 4: Create input YAML
            print("\n4. Creating input YAML...")
            yaml_path = service._create_input_yaml(job_id, request)
            
            assert Path(yaml_path).exists()
            with open(yaml_path) as f:
                content = f.read()
            
            # Verify YAML content
            assert protein.id in content
            assert protein.sequence in content
            assert ligand.id in content
            assert ligand.smiles in content
            print("   ✅ Input YAML created")
            
            # Test 5: Mock Boltz-2 execution
            print("\n5. Testing Boltz-2 execution (mocked)...")
            
            # Create mock output files
            affinity_file = job_dir / "affinity_prediction.json"
            affinity_data = {
                "affinity_pred_value": -6.5,
                "affinity_probability_binary": 0.85,
                "confidence_score": 0.92
            }
            with open(affinity_file, 'w') as f:
                json.dump(affinity_data, f)
            
            # Mock subprocess call
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.returncode = 0
                mock_run.return_value.stdout = "Prediction completed"
                
                result = service._execute_boltz_prediction(yaml_path, job_dir)
                assert result == affinity_data
                print("   ✅ Boltz-2 execution mocked successfully")
            
            # Test 6: Complete prediction
            print("\n6. Completing prediction...")
            service._update_job_status(job_id, "completed", 100.0)
            
            status = service.get_job_status(job_id)
            assert status.status == "completed"
            assert status.progress == 100.0
            print("   ✅ Prediction completed")
            
            # Test 7: Cleanup
            print("\n7. Testing cleanup...")
            service._cleanup_temp_files(yaml_path)
            assert not Path(yaml_path).exists()
            print("   ✅ Temporary files cleaned up")
            
            print("\n" + "=" * 50)
            print("🎉 All tests passed! Workflow is working correctly.")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("🧹 Temporary files cleaned up")


def test_error_handling():
    """Test error handling scenarios."""
    print("\n🧪 Testing Error Handling")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    output_dir = Path(temp_dir) / "output"
    temp_dir_path = Path(temp_dir) / "temp"
    
    try:
        with patch('services.boltz_service.settings') as mock_settings:
            mock_settings.output_base_dir = temp_dir
            mock_settings.predictions_dir = "output"
            mock_settings.temp_dir = "temp"
            mock_settings.boltz_command = "boltz"
            mock_settings.use_msa_server = False
            mock_settings.job_timeout_seconds = 300
            
            service = BoltzService()
            service.output_dir = output_dir
            service.temp_dir = temp_dir_path
            
            # Test 1: Non-existent job status
            print("1. Testing non-existent job...")
            status = service.get_job_status("non-existent")
            assert status is None
            print("   ✅ Non-existent job handled correctly")
            
            # Test 2: Boltz-2 availability check failure
            print("2. Testing Boltz-2 availability failure...")
            with patch('subprocess.run') as mock_run:
                mock_run.side_effect = FileNotFoundError("boltz command not found")
                available = service.check_boltz_availability()
                assert available is False
                print("   ✅ Boltz-2 availability failure handled")
            
            # Test 3: Subprocess timeout
            print("3. Testing subprocess timeout...")
            with patch('subprocess.run') as mock_run:
                import subprocess
                mock_run.side_effect = subprocess.TimeoutExpired("boltz", 10)
                available = service.check_boltz_availability()
                assert available is False
                print("   ✅ Subprocess timeout handled")
            
            print("\n✅ All error handling tests passed!")
            
    except Exception as e:
        print(f"\n❌ Error handling test failed: {e}")
        raise
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    print("🚀 Starting BoltzService Integration Tests")
    print("=" * 60)
    
    try:
        test_full_workflow()
        test_error_handling()
        
        print("\n" + "=" * 60)
        print("🎉 All integration tests completed successfully!")
        print("\n💡 Next steps:")
        print("   - Run unit tests: pytest test_boltz_service.py -v")
        print("   - Test with real Boltz-2 installation")
        print("   - Add more edge case tests")
        
    except Exception as e:
        print(f"\n❌ Integration tests failed: {e}")
        exit(1)
