#!/usr/bin/env python3
"""
Download Boltz-2 models to avoid timeout on first run.
"""

import sys
import os

sys.path.append("backend/boltz2/src")

from boltz.main import download_boltz2
from pathlib import Path


def download_models():
    """Download Boltz-2 models."""
    print("🔄 Downloading Boltz-2 models...")
    print("This may take several minutes on first run...")

    # Set cache directory
    cache_dir = Path.home() / ".boltz"
    cache_dir.mkdir(exist_ok=True)

    try:
        download_boltz2(cache_dir)
        print("✅ Models downloaded successfully!")

        # Check what was downloaded
        model_files = list(cache_dir.glob("*.ckpt"))
        print(f"📁 Downloaded {len(model_files)} model files:")
        for model_file in model_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            print(f"  - {model_file.name} ({size_mb:.1f} MB)")

    except Exception as e:
        print(f"❌ Error downloading models: {e}")
        return False

    return True


if __name__ == "__main__":
    success = download_models()
    if success:
        print("\n🎉 Boltz-2 models are ready! You can now run predictions.")
    else:
        print("\n❌ Failed to download models. Check your internet connection.")





















