"""
Unit tests for BoltzService class.
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule
import os


class TestBoltzService:
    """Test cases for BoltzService."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        temp_dir = tempfile.mkdtemp()
        output_dir = Path(temp_dir) / "output"
        temp_dir_path = Path(temp_dir) / "temp"

        yield {"output": output_dir, "temp": temp_dir_path, "base": temp_dir}

        shutil.rmtree(temp_dir)

    @pytest.fixture
    def mock_settings(self):
        """Mock settings for testing."""
        with patch("services.boltz_service.settings") as mock_settings:
            mock_settings.output_base_dir = "/tmp/test"
            mock_settings.predictions_dir = "predictions"
            mock_settings.temp_dir = "temp"
            mock_settings.boltz_command = "boltz"
            mock_settings.use_msa_server = False
            mock_settings.job_timeout_seconds = 300
            yield mock_settings

    @pytest.fixture
    def service(self, temp_dirs, mock_settings):
        """Create BoltzService instance for testing."""
        with patch("services.boltz_service.settings") as mock_settings:
            mock_settings.output_base_dir = str(temp_dirs["base"])
            mock_settings.predictions_dir = "output"
            mock_settings.temp_dir = "temp"
            mock_settings.boltz_command = "boltz"
            mock_settings.use_msa_server = False
            mock_settings.job_timeout_seconds = 300

            service = BoltzService()
            # Override the actual directories with our temp ones
            service.output_dir = temp_dirs["output"]
            service.temp_dir = temp_dirs["temp"]
            return service

    @pytest.fixture
    def sample_request(self):
        """Create a sample prediction request."""
        protein = ProteinSequence(
            sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            id="insulin",
        )
        ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="aspirin")
        return PredictionRequest(protein=protein, ligand=ligand, use_msa=True)

    def test_init_creates_directories(self, temp_dirs):
        """Test that service initialization creates required directories."""
        with patch("services.boltz_service.settings") as mock_settings:
            mock_settings.output_base_dir = str(temp_dirs["base"])
            mock_settings.predictions_dir = "output"
            mock_settings.temp_dir = "temp"

            service = BoltzService()
            service.output_dir = temp_dirs["output"]
            service.temp_dir = temp_dirs["temp"]

            assert service.output_dir.exists()
            assert service.temp_dir.exists()

    def test_check_boltz_availability_success(self, service):
        """Test successful Boltz-2 availability check."""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Boltz-2 version 1.0.0"

            result = service.check_boltz_availability()
            assert result is True
            mock_run.assert_called_once()

    def test_check_boltz_availability_failure(self, service):
        """Test failed Boltz-2 availability check."""
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("boltz command not found")

            result = service.check_boltz_availability()
            assert result is False

    def test_create_prediction_job(self, service, sample_request):
        """Test prediction job creation."""
        job_id = service.create_prediction_job(sample_request)

        # Check that job directory was created
        job_dir = service.output_dir / job_id
        assert job_dir.exists()

        # Check metadata file
        metadata_file = job_dir / "metadata.json"
        assert metadata_file.exists()

        with open(metadata_file) as f:
            metadata = json.load(f)

        assert metadata["job_id"] == job_id
        assert metadata["status"] == "pending"
        assert metadata["progress"] == 0.0
        assert "request" in metadata

    def test_create_input_yaml(self, service, sample_request):
        """Test input YAML file creation."""
        job_id = "test-job-123"
        yaml_path = service._create_input_yaml(job_id, sample_request)

        assert Path(yaml_path).exists()

        with open(yaml_path) as f:
            content = f.read()

        # Check that protein and ligand info is in the YAML
        assert sample_request.protein.id in content
        assert sample_request.protein.sequence in content
        assert sample_request.ligand.id in content
        assert sample_request.ligand.smiles in content

    @patch("subprocess.run")
    def test_execute_boltz_prediction_success(self, mock_run, service, temp_dirs):
        """Test successful Boltz-2 prediction execution."""
        # Mock subprocess result
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Prediction completed"

        # Create mock output files
        output_dir = temp_dirs["output"]
        output_dir.mkdir(exist_ok=True)

        # Create mock affinity result file
        affinity_file = output_dir / "affinity_prediction.json"
        affinity_data = {
            "affinity_pred_value": -6.5,
            "affinity_probability_binary": 0.85,
            "confidence_score": 0.92,
        }
        with open(affinity_file, "w") as f:
            json.dump(affinity_data, f)

        input_yaml = "/tmp/test_input.yaml"
        result = service._execute_boltz_prediction(input_yaml, output_dir)

        assert result == affinity_data
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_execute_boltz_prediction_no_output(self, mock_run, service, temp_dirs):
        """Test Boltz-2 execution with no output files."""
        mock_run.return_value.returncode = 0

        output_dir = temp_dirs["output"]
        output_dir.mkdir(exist_ok=True)

        input_yaml = "/tmp/test_input.yaml"

        with pytest.raises(RuntimeError, match="No output files generated by Boltz-2"):
            service._execute_boltz_prediction(input_yaml, output_dir)

    def test_update_job_status(self, service, sample_request):
        """Test job status updates."""
        # Create a job first
        job_id = service.create_prediction_job(sample_request)

        # Update status
        service._update_job_status(job_id, "running", 50.0)

        # Check metadata was updated
        metadata_file = service.output_dir / job_id / "metadata.json"
        with open(metadata_file) as f:
            metadata = json.load(f)

        assert metadata["status"] == "running"
        assert metadata["progress"] == 50.0

    def test_get_job_status(self, service, sample_request):
        """Test retrieving job status."""
        # Create a job
        job_id = service.create_prediction_job(sample_request)

        # Get status
        status = service.get_job_status(job_id)

        assert status is not None
        assert status.job_id == job_id
        assert status.status == "pending"
        assert status.progress == 0.0

    def test_get_job_status_not_found(self, service):
        """Test getting status for non-existent job."""
        status = service.get_job_status("non-existent-job")
        assert status is None

    def test_cleanup_temp_files(self, service):
        """Test temporary file cleanup."""
        # Create a temporary file
        temp_file = service.temp_dir / "test_temp.yaml"
        temp_file.write_text("test content")

        # Clean it up
        service._cleanup_temp_files(str(temp_file))

        # Check it's gone
        assert not temp_file.exists()

    def test_cleanup_completed_jobs(self, service, sample_request):
        """Test cleanup of old completed jobs."""
        # Create a completed job
        job_id = service.create_prediction_job(sample_request)
        service._update_job_status(job_id, "completed", 100.0)

        # Mock old timestamp by modifying file mtime
        metadata_file = service.output_dir / job_id / "metadata.json"
        old_time = 1000000000  # Old timestamp
        os.utime(metadata_file, (old_time, old_time))

        # Clean up old jobs (older than 1 hour)
        service.cleanup_completed_jobs(max_age_hours=1)

        # Check job was cleaned up
        assert not (service.output_dir / job_id).exists()

    @patch("subprocess.run")
    def test_run_prediction_success(self, mock_run, service, sample_request, temp_dirs):
        """Test successful prediction run."""
        # Mock subprocess result
        mock_run.return_value.returncode = 0

        # Create mock output files in the job directory
        job_dir = service.output_dir / "test-job"
        job_dir.mkdir(exist_ok=True)

        affinity_file = job_dir / "affinity_prediction.json"
        affinity_data = {
            "affinity_pred_value": -6.5,
            "affinity_probability_binary": 0.85,
            "confidence_score": 0.92,
        }
        with open(affinity_file, "w") as f:
            json.dump(affinity_data, f)

        # Run prediction
        result = service.run_prediction("test-job", sample_request)

        assert result.status == "completed"
        assert result.affinity_pred_value == -6.5
        assert result.affinity_probability_binary == 0.85
        assert result.confidence_score == 0.92
        assert result.processing_time_seconds > 0

    @patch("subprocess.run")
    def test_run_prediction_failure(self, mock_run, service, sample_request):
        """Test prediction run failure."""
        # Mock subprocess failure
        mock_run.side_effect = RuntimeError("Boltz-2 failed")

        # Run prediction
        result = service.run_prediction("test-job", sample_request)

        assert result.status == "failed"
        assert "Boltz-2 failed" in result.error_message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
