#!/usr/bin/env python3
"""
Hybrid setup: Local frontend + Cloud backend
This allows you to develop locally but run Boltz-2 in the cloud.
"""

import requests
import json


class CloudBackend:
    """Connect to a cloud-hosted backend for Boltz-2 execution."""

    def __init__(self, cloud_url="https://your-cloud-instance.com"):
        self.base_url = cloud_url

    def submit_job(self, protein_sequence, ligand_smiles):
        """Submit job to cloud backend."""
        data = {
            "protein": {"id": "local_protein", "sequence": protein_sequence},
            "ligand": {"id": "local_ligand", "smiles": ligand_smiles},
            "use_msa": True,
            "confidence_threshold": 0.5,
        }

        try:
            response = requests.post(f"{self.base_url}/predict", json=data, timeout=600)
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def setup_hybrid_development():
    """Setup instructions for hybrid development."""
    print("=== HYBRID DEVELOPMENT SETUP ===")
    print()
    print("1. LOCAL FRONTEND (Your PC):")
    print("   - Run: cd frontend && npm run dev")
    print("   - Access: http://localhost:5173")
    print("   - Fast development and testing")
    print()
    print("2. CLOUD BACKEND (Google Colab/AWS):")
    print("   - Deploy backend to cloud")
    print("   - Get cloud URL (e.g., https://abc123.run.app)")
    print("   - Update frontend to use cloud URL")
    print()
    print("3. BENEFITS:")
    print("   - Fast local development")
    print("   - Powerful cloud computation")
    print("   - No local resource usage")
    print("   - Cost-effective")
    print()
    print("4. SETUP STEPS:")
    print("   a) Deploy backend to Google Colab")
    print("   b) Get the public URL")
    print("   c) Update frontend config to use cloud URL")
    print("   d) Run frontend locally")
    print()
    print("5. EXAMPLE CLOUD URLS:")
    print("   - Google Colab: https://abc123-8000.proxy.run.app")
    print("   - AWS EC2: http://your-ec2-ip:8000")
    print("   - GCP: http://your-gcp-ip:8000")


if __name__ == "__main__":
    setup_hybrid_development()















