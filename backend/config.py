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
    devices: int = 1  # Use 1 CPU device since CUDA is not available

    # Output Configuration
    output_base_dir: str = "output"
    predictions_dir: str = "predictions"
    temp_dir: str = "temp"

    # Job Configuration
    max_concurrent_jobs: int = 4
    job_timeout_seconds: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
