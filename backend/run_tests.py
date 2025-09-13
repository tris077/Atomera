#!/usr/bin/env python3
"""
Simple test runner for BoltzService tests.
"""

import sys
import subprocess
import os

def run_tests():
    """Run the test suite."""
    print("🧪 Running BoltzService Tests")
    print("=" * 40)
    
    # Check if pytest is available
    try:
        import pytest
        print("✅ pytest is available")
    except ImportError:
        print("❌ pytest not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-test.txt"])
    
    # Run the tests
    print("\n🚀 Starting test execution...")
    test_files = [
        "test_boltz_service.py",
        "test_simple.py"  # Include the existing simple tests
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Running {test_file}...")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"
                ], capture_output=False)
                
                if result.returncode == 0:
                    print(f"✅ {test_file} passed")
                else:
                    print(f"❌ {test_file} failed")
                    
            except Exception as e:
                print(f"❌ Error running {test_file}: {e}")
        else:
            print(f"⚠️  {test_file} not found, skipping")
    
    print("\n" + "=" * 40)
    print("🎉 Test execution completed!")

if __name__ == "__main__":
    run_tests()
