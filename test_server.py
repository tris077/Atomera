#!/usr/bin/env python3
"""
Minimal test server to verify the setup works.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test Server")


@app.get("/")
async def root():
    return {"message": "Test server is working!"}


@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Test server running"}


if __name__ == "__main__":
    print("Starting test server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)















