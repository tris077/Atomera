"""
RunPod service for GPU-accelerated inference workloads.
Handles job submission, status monitoring, and result retrieval from RunPod.
"""

import os
import json
import time
import base64
import requests
from typing import Optional, Dict, Any, List
from pathlib import Path
from enum import Enum

from config import settings


class RunPodJobStatus(str, Enum):
    """RunPod job status enumeration."""
    QUEUED = "QUEUED"
    IN_QUEUE = "IN_QUEUE"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"


class RunPodService:
    """Service for interacting with RunPod API for GPU inference."""

    def __init__(self):
        """Initialize the RunPod service."""
        self.api_key = os.getenv("RUNPOD_API_KEY", settings.runpod_api_key)
        self.endpoint_id = os.getenv("RUNPOD_ENDPOINT_ID", settings.runpod_endpoint_id)
        self.base_url = "https://api.runpod.ai/v2"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        if not self.api_key:
            raise ValueError("RUNPOD_API_KEY must be set in environment or config")
        if not self.endpoint_id:
            raise ValueError("RUNPOD_ENDPOINT_ID must be set in environment or config")

    def submit_job(
        self,
        input_data: Dict[str, Any],
        job_name: Optional[str] = None,
    ) -> str:
        """
        Submit a job to RunPod endpoint.

        Args:
            input_data: Dictionary containing job input data
            job_name: Optional name for the job

        Returns:
            Job ID from RunPod
        """
        # RunPod Serverless v2 API - async job submission
        url = f"{self.base_url}/{self.endpoint_id}/run"
        
        payload = {
            "input": input_data,
        }
        
        if job_name:
            payload["jobName"] = job_name
        
        try:
            print(f"[RunPod] Submitting to URL: {url}")
            print(f"[RunPod] Payload keys: {list(payload.keys())}")
            print(f"[RunPod] Input data keys: {list(input_data.keys())}")

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )

            print(f"[RunPod] Response status: {response.status_code}")
            print(f"[RunPod] Response body: {response.text[:500]}")

            response.raise_for_status()

            result = response.json()
            job_id = result.get("id")

            if not job_id:
                print(f"[RunPod] ERROR: No job ID in response: {result}")
                raise ValueError(f"RunPod API did not return a job ID: {result}")

            print(f"[RunPod] ✅ Successfully submitted job to RunPod: {job_id}")
            return job_id

        except requests.exceptions.RequestException as e:
            print(f"[RunPod] ❌ Error submitting job to RunPod: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[RunPod] Response status: {e.response.status_code}")
                print(f"[RunPod] Response body: {e.response.text}")
            raise RuntimeError(f"Failed to submit job to RunPod: {str(e)}")

    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a RunPod job.
        
        Args:
            job_id: RunPod job ID
            
        Returns:
            Dictionary containing job status information
        """
        # RunPod serverless endpoint status API format
        url = f"{self.base_url}/{self.endpoint_id}/status/{job_id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=30,
            )

            print(f"[RunPod] Status check - Response code: {response.status_code}")

            response.raise_for_status()

            status_data = response.json()
            print(f"[RunPod] Job {job_id} status: {status_data.get('status')}")

            # Log error details if job failed
            if status_data.get('status') in ['FAILED', 'CANCELLED', 'TIMED_OUT']:
                print(f"[RunPod] ❌ Job {job_id} failed!")
                print(f"[RunPod] Error: {status_data.get('error', 'No error message')}")
                print(f"[RunPod] Full response: {json.dumps(status_data, indent=2)}")

            return status_data

        except requests.exceptions.RequestException as e:
            print(f"[RunPod] ❌ Error getting job status from RunPod: {job_id}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[RunPod] Response status: {e.response.status_code}")
                print(f"[RunPod] Response body: {e.response.text}")
            raise RuntimeError(f"Failed to get job status from RunPod: {str(e)}")

    def get_job_output(self, job_id: str) -> Dict[str, Any]:
        """
        Get the output/result of a completed RunPod job.
        
        Args:
            job_id: RunPod job ID
            
        Returns:
            Dictionary containing job output
        """
        status = self.get_job_status(job_id)

        if status.get("status") != RunPodJobStatus.COMPLETED:
            print(f"[RunPod] ❌ Cannot get output - job not completed. Status: {status.get('status')}")
            raise ValueError(
                f"Job {job_id} is not completed. Current status: {status.get('status')}"
            )

        output = status.get("output", {})
        print(f"[RunPod] Raw output type: {type(output)}")
        print(f"[RunPod] Raw output: {str(output)[:500]}")

        # Handle different output formats
        if isinstance(output, str):
            try:
                output = json.loads(output)
                print(f"[RunPod] Parsed JSON output successfully")
            except json.JSONDecodeError:
                print(f"[RunPod] WARNING: Output is string but not JSON")
                # If it's not JSON, return as string
                pass

        print(f"[RunPod] Final output keys: {list(output.keys()) if isinstance(output, dict) else 'Not a dict'}")
        return output

    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a RunPod job.
        
        Args:
            job_id: RunPod job ID
            
        Returns:
            True if cancellation was successful
        """
        url = f"{self.base_url}/{self.endpoint_id}/cancel/{job_id}"
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error cancelling job on RunPod: {job_id}: {e}")
            return False

    def wait_for_job_completion(
        self,
        job_id: str,
        poll_interval: int = 5,
        timeout: int = 1800,
    ) -> Dict[str, Any]:
        """
        Wait for a job to complete, polling status periodically.
        
        Args:
            job_id: RunPod job ID
            poll_interval: Seconds between status checks
            timeout: Maximum time to wait in seconds
            
        Returns:
            Final job status dictionary
        """
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(
                    f"Job {job_id} did not complete within {timeout} seconds"
                )
            
            status_data = self.get_job_status(job_id)
            status = status_data.get("status")
            
            print(f"Job {job_id} status: {status} (elapsed: {elapsed:.1f}s)")
            
            if status == RunPodJobStatus.COMPLETED:
                return status_data
            elif status in [RunPodJobStatus.FAILED, RunPodJobStatus.CANCELLED, RunPodJobStatus.TIMED_OUT]:
                error_msg = status_data.get("error", f"Job {status.lower()}")
                raise RuntimeError(f"Job {job_id} {status.lower()}: {error_msg}")
            
            # Wait before next poll
            time.sleep(poll_interval)

    def encode_file_to_base64(self, file_path: str) -> str:
        """
        Encode a file to base64 string for transmission.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Base64 encoded string
        """
        with open(file_path, "rb") as f:
            file_data = f.read()
            return base64.b64encode(file_data).decode("utf-8")

    def decode_base64_to_file(self, base64_string: str, output_path: str):
        """
        Decode a base64 string to a file.
        
        Args:
            base64_string: Base64 encoded string
            output_path: Path where to save the decoded file
        """
        file_data = base64.b64decode(base64_string)
        with open(output_path, "wb") as f:
            f.write(file_data)

    def prepare_boltz_input(
        self,
        job_id: str,
        input_yaml_path: str,
        request_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Prepare input data for RunPod Boltz-2 inference.
        
        Args:
            job_id: Atomera job ID
            input_yaml_path: Path to the input YAML file
            request_data: Original request data
            
        Returns:
            Dictionary ready for RunPod submission
        """
        # Read the YAML file content
        with open(input_yaml_path, "r") as f:
            yaml_content = f.read()
        
        # Encode YAML content as base64 for transmission
        yaml_base64 = base64.b64encode(yaml_content.encode("utf-8")).decode("utf-8")
        
        # Prepare RunPod input
        runpod_input = {
            "job_id": job_id,
            "input_yaml": yaml_base64,
            "request_data": request_data,
            "config": {
                "devices": settings.devices,
                "accelerator": settings.accelerator,
                "diffusion_samples": settings.diffusion_samples,
                "use_msa_server": settings.use_msa_server,
            },
        }
        
        return runpod_input

    def parse_boltz_output(
        self,
        runpod_output: Dict[str, Any],
        output_dir: Path,
    ) -> Dict[str, Any]:
        """
        Parse RunPod output and save files to local directory.
        
        Args:
            runpod_output: Output dictionary from RunPod
            output_dir: Directory where to save output files
            
        Returns:
            Parsed result dictionary
        """
        result_data = {}
        
        # Extract affinity results
        if "affinity_pred_value" in runpod_output:
            result_data["affinity_pred_value"] = runpod_output["affinity_pred_value"]
        if "affinity_probability_binary" in runpod_output:
            result_data["affinity_probability_binary"] = runpod_output[
                "affinity_probability_binary"
            ]
        if "confidence_score" in runpod_output:
            result_data["confidence_score"] = runpod_output["confidence_score"]
        
        # Extract pose files (base64 encoded)
        if "pose_files" in runpod_output:
            pose_files = []
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for pose_name, pose_base64 in runpod_output["pose_files"].items():
                pose_path = output_dir / pose_name
                self.decode_base64_to_file(pose_base64, str(pose_path))
                pose_files.append(pose_name)
            
            result_data["pose_files"] = pose_files
            result_data["poses_generated"] = len(pose_files)
        
        # Extract other output files
        if "output_files" in runpod_output:
            for file_name, file_base64 in runpod_output["output_files"].items():
                file_path = output_dir / file_name
                self.decode_base64_to_file(file_base64, str(file_path))
        
        return result_data

