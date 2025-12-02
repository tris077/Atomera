# RunPod Integration Guide

This document explains how Atomera integrates with RunPod for GPU-accelerated Boltz-2 inference workloads.

## Overview

Atomera uses RunPod's GPU infrastructure to handle all Boltz-2 inference workloads. The integration allows Atomera to:

- Automatically send model jobs to RunPod
- Process inference on GPU infrastructure
- Return results to the Atomera interface
- Handle real-time job updates and status monitoring
- Scale efficiently for multiple users

## Architecture

```
Atomera Backend → RunPod Service → RunPod API → GPU Pod → Results → Atomera Backend
```

1. **Atomera Backend**: Receives prediction requests from the frontend
2. **RunPod Service**: Handles communication with RunPod API
3. **RunPod API**: Manages job submission and status
4. **GPU Pod**: Executes Boltz-2 inference on GPU
5. **Results**: Returned to Atomera for processing and display

## Setup Instructions

### 1. Create a RunPod Account

1. Sign up at [RunPod](https://www.runpod.io/)
2. Navigate to your account settings
3. Generate an API key

### 2. Create a RunPod Serverless Endpoint

You need to create a serverless endpoint that can run Boltz-2 inference. The endpoint should:

1. **Use a Docker image** with Boltz-2 installed
2. **Handle input data** in the format Atomera sends (base64-encoded YAML)
3. **Return results** in the expected format (JSON with base64-encoded files)

#### Example Endpoint Handler

Your RunPod endpoint handler should process requests like this:

```python
def handler(event):
    """
    RunPod serverless handler for Boltz-2 inference.
    
    Expected input:
    {
        "job_id": "atomera-job-id",
        "input_yaml": "base64-encoded-yaml-content",
        "request_data": {...},
        "config": {
            "devices": 1,
            "accelerator": "gpu",
            "diffusion_samples": 1,
            "use_msa_server": true
        }
    }
    
    Expected output:
    {
        "affinity_pred_value": -7.2,
        "affinity_probability_binary": 0.89,
        "confidence_score": 0.85,
        "pose_files": {
            "pose_0.cif": "base64-encoded-file-content",
            "pose_1.cif": "base64-encoded-file-content"
        },
        "output_files": {
            "affinity_result.json": "base64-encoded-json",
            "confidence_result.json": "base64-encoded-json"
        }
    }
    """
    import base64
    import json
    import tempfile
    import subprocess
    from pathlib import Path
    
    # Decode input YAML
    input_yaml_b64 = event["input"]["input_yaml"]
    input_yaml_content = base64.b64decode(input_yaml_b64).decode("utf-8")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Write input YAML
        input_yaml_path = tmpdir_path / "input.yaml"
        input_yaml_path.write_text(input_yaml_content)
        
        # Run Boltz-2 prediction
        output_dir = tmpdir_path / "output"
        output_dir.mkdir()
        
        cmd = [
            "boltz", "predict",
            str(input_yaml_path),
            "--out_dir", str(output_dir),
            "--devices", str(event["input"]["config"]["devices"]),
            "--accelerator", event["input"]["config"]["accelerator"],
            "--diffusion_samples", str(event["input"]["config"]["diffusion_samples"]),
        ]
        
        if event["input"]["config"]["use_msa_server"]:
            cmd.append("--use_msa_server")
        
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Read results
        predictions_dir = output_dir / "predictions"
        result_dir = next(predictions_dir.iterdir())
        
        # Parse affinity results
        affinity_file = result_dir / "affinity_input.json"
        affinity_data = json.loads(affinity_file.read_text()) if affinity_file.exists() else {}
        
        # Parse confidence results
        confidence_file = result_dir / "confidence_input_model_0.json"
        confidence_data = json.loads(confidence_file.read_text()) if confidence_file.exists() else {}
        
        # Encode pose files
        pose_files = {}
        for cif_file in result_dir.glob("*.cif"):
            pose_files[cif_file.name] = base64.b64encode(cif_file.read_bytes()).decode("utf-8")
        
        # Encode output files
        output_files = {}
        if affinity_file.exists():
            output_files["affinity_result.json"] = base64.b64encode(
                affinity_file.read_bytes()
            ).decode("utf-8")
        if confidence_file.exists():
            output_files["confidence_result.json"] = base64.b64encode(
                confidence_file.read_bytes()
            ).decode("utf-8")
        
        return {
            "affinity_pred_value": affinity_data.get("affinity_pred_value"),
            "affinity_probability_binary": affinity_data.get("affinity_probability_binary"),
            "confidence_score": confidence_data.get("confidence_score", 0.85),
            "pose_files": pose_files,
            "output_files": output_files,
        }
```

### 3. Configure Atomera

Set the following environment variables in your `.env` file:

```bash
# RunPod Configuration
RUNPOD_API_KEY=your_runpod_api_key_here
RUNPOD_ENDPOINT_ID=your_endpoint_id_here

# Optional: RunPod settings
USE_RUNPOD=true
RUNPOD_POLL_INTERVAL=5
RUNPOD_TIMEOUT=1800
```

Or set them in `backend/config.py`:

```python
runpod_api_key: str = "your_api_key"
runpod_endpoint_id: str = "your_endpoint_id"
use_runpod: bool = True
runpod_poll_interval: int = 5
runpod_timeout: int = 1800
```

### 4. Install Dependencies

Make sure all dependencies are installed:

```bash
cd backend
pip install -r requirements.txt
```

## How It Works

### Job Submission Flow

1. **User submits prediction request** via Atomera frontend
2. **Atomera backend** creates a job and generates input YAML
3. **RunPod service** encodes the YAML and submits to RunPod endpoint
4. **RunPod** queues the job and assigns it to a GPU pod
5. **GPU pod** executes Boltz-2 inference
6. **Results** are returned to Atomera via RunPod API
7. **Atomera** decodes and processes results for display

### Status Monitoring

The integration includes real-time status monitoring:

- **QUEUED**: Job is waiting in RunPod queue
- **IN_QUEUE**: Job is in queue, waiting for GPU
- **IN_PROGRESS**: Job is running on GPU
- **COMPLETED**: Job finished successfully
- **FAILED**: Job encountered an error
- **CANCELLED**: Job was cancelled
- **TIMED_OUT**: Job exceeded timeout

Progress updates are sent to the frontend in real-time.

### Data Transfer

- **Input**: YAML files are base64-encoded for transmission
- **Output**: Results and pose files are base64-encoded for return
- **Efficiency**: Only necessary data is transferred

## Configuration Options

### RunPod Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `use_runpod` | `true` | Enable/disable RunPod integration |
| `runpod_api_key` | `None` | RunPod API key (required) |
| `runpod_endpoint_id` | `None` | RunPod endpoint ID (required) |
| `runpod_poll_interval` | `5` | Seconds between status checks |
| `runpod_timeout` | `1800` | Maximum wait time (30 minutes) |

### Fallback Behavior

If RunPod is unavailable or misconfigured, Atomera will:
1. Log a warning
2. Fall back to local execution (if Boltz-2 is available)
3. Continue processing requests normally

## Troubleshooting

### Common Issues

1. **"RUNPOD_API_KEY must be set"**
   - Solution: Set `RUNPOD_API_KEY` environment variable

2. **"RUNPOD_ENDPOINT_ID must be set"**
   - Solution: Set `RUNPOD_ENDPOINT_ID` environment variable

3. **"Failed to submit job to RunPod"**
   - Check API key is valid
   - Verify endpoint ID exists
   - Check network connectivity

4. **"Job timed out"**
   - Increase `runpod_timeout` setting
   - Check RunPod endpoint is functioning
   - Verify GPU pods are available

5. **"Job failed on RunPod"**
   - Check RunPod endpoint logs
   - Verify Docker image has Boltz-2 installed
   - Check input data format

### Debugging

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check RunPod service initialization:

```python
from services.runpod_service import RunPodService
service = RunPodService()
print(f"API Key set: {bool(service.api_key)}")
print(f"Endpoint ID: {service.endpoint_id}")
```

## API Reference

### RunPodService Methods

- `submit_job(input_data, job_name)`: Submit a job to RunPod
- `get_job_status(job_id)`: Get current job status
- `get_job_output(job_id)`: Get job results
- `cancel_job(job_id)`: Cancel a running job
- `wait_for_job_completion(job_id)`: Wait for job to finish
- `prepare_boltz_input(job_id, yaml_path, request_data)`: Prepare input for RunPod
- `parse_boltz_output(runpod_output, output_dir)`: Parse and save results

## Performance Considerations

- **Latency**: Network latency between Atomera and RunPod
- **Queue Time**: Time waiting for GPU availability
- **Processing Time**: Actual inference time on GPU
- **Data Transfer**: Time to upload/download files

Optimize by:
- Using RunPod regions close to your server
- Configuring appropriate GPU types
- Minimizing data transfer size
- Using efficient serialization

## Security

- API keys are stored as environment variables
- Data is transmitted over HTTPS
- Base64 encoding is used for binary data
- No sensitive data is logged

## Next Steps

1. Set up your RunPod account and endpoint
2. Configure environment variables
3. Test with a simple prediction
4. Monitor performance and adjust settings
5. Scale as needed for production

For more information, see:
- [RunPod Documentation](https://docs.runpod.io/)
- [RunPod API Reference](https://docs.runpod.io/api-reference/overview)
- [Boltz-2 Documentation](backend/boltz2/README.md)

