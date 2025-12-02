"""
Configuration management for Atomera backend.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Configuration
    app_name: str = "Atomera API"
    app_version: str = "1.0.0"
    app_description: str = "Binding affinity research platform powered by Boltz-2"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Boltz-2 Configuration
    boltz_command: str = "boltz"
    use_msa_server: bool = True
    max_sequence_length: int = 10000
    max_smiles_length: int = 1000
    devices: int = 1  # Number of devices to use
    accelerator: str = "auto"  # "auto", "cpu", "gpu" - auto-detect GPU availability
    diffusion_samples: int = (
        1  # Number of diffusion samples (1 for speed, 3+ for quality)
    )

    # Output Configuration
    output_base_dir: str = "output"
    predictions_dir: str = "predictions"
    temp_dir: str = "temp"

    # Job Configuration - Cloud Optimized
    max_concurrent_jobs: int = 2  # Allow 2 concurrent jobs for cloud instances
    job_timeout_seconds: int = 1800  # 30 minutes for cloud GPU execution

    # RunPod Configuration
    use_runpod: bool = True  # Enable RunPod for GPU inference
    runpod_api_key: Optional[str] = None  # RunPod API key (set via env var RUNPOD_API_KEY)
    runpod_endpoint_id: Optional[str] = None  # RunPod endpoint ID (set via env var RUNPOD_ENDPOINT_ID)
    runpod_poll_interval: int = 5  # Seconds between status checks
    runpod_timeout: int = 1800  # Maximum time to wait for job completion (30 minutes)

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
