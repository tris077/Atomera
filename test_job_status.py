#!/usr/bin/env python3
"""
Test job status monitoring
"""

import requests
import time

# API base URL
BASE_URL = "http://localhost:8000"


def check_job_status(job_id):
    """Check the status of a specific job"""
    response = requests.get(f"{BASE_URL}/jobs/{job_id}")
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error checking job status: {response.status_code}")
        return None


def monitor_job(job_id, max_checks=20):
    """Monitor a job until completion or failure"""
    print(f"🔍 Monitoring job: {job_id}")

    for i in range(max_checks):
        status_data = check_job_status(job_id)
        if not status_data:
            print("❌ Failed to get job status")
            return False

        print(
            f"   Check {i+1}: Status = {status_data['status']}, Progress = {status_data.get('progress', 0)}%"
        )

        if status_data["status"] == "completed":
            print("✅ Job completed successfully!")
            return True
        elif status_data["status"] == "failed":
            print("❌ Job failed")
            return False

        time.sleep(2)  # Wait 2 seconds between checks

    print("⏰ Job still processing after maximum checks")
    return False


if __name__ == "__main__":
    # Test with the job ID from the logs
    job_id = "ad5bb76c-896b-49c4-9d81-c46cf80e027f"
    monitor_job(job_id)
