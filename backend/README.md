# Atomera Backend API

A modern, scalable backend API for binding affinity research, powered by the Boltz-2 molecular modeling framework.

## 🚀 Overview

Atomera is a binding affinity research platform that provides a clean, user-friendly interface to Boltz-2's advanced molecular modeling capabilities. This backend serves as the computational engine, exposing Boltz-2's functionality through well-documented REST API endpoints.

### Key Features

- **Protein-Ligand Binding Affinity Prediction**: Core functionality using Boltz-2
- **Asynchronous Job Processing**: Handle long-running predictions without timeouts
- **Input Validation**: Robust validation of protein sequences and SMILES strings
- **Job Management**: Track prediction progress and retrieve results
- **Health Monitoring**: System health checks and Boltz-2 availability monitoring
- **RESTful API**: Clean, documented endpoints for seamless frontend integration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Atomera API   │    │   Boltz-2       │
│   (Future)      │◄──►│   (FastAPI)     │◄──►│   Framework     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Job Queue     │
                       │   & Storage     │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.10+
- Boltz-2 framework installed and accessible
- CUDA-compatible GPU (recommended for performance)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd atomera/backend
   ```

2. **Install Boltz-2**
   ```bash
   # Install Boltz-2 with CUDA support (recommended)
   pip install boltz[cuda] -U
   
   # Or CPU-only version
   pip install boltz -U
   ```

3. **Install Atomera dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Boltz-2 installation**
   ```bash
   boltz --version
   ```

## 🚀 Quick Start

### Running the API Server

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API

1. **Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Get Examples**
   ```bash
   curl http://localhost:8000/examples
   ```

3. **Run a Prediction**
   ```bash
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{
          "protein": {
            "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
            "id": "A"
          },
          "ligand": {
            "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
            "id": "B"
          }
        }'
   ```

## 📚 API Reference

### Core Endpoints

#### `POST /predict`
Asynchronous binding affinity prediction. Returns a job ID for tracking.

**Request Body:**
```json
{
  "protein": {
    "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
    "id": "A"
  },
  "ligand": {
    "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "id": "B"
  },
  "use_msa": true,
  "confidence_threshold": 0.5
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "processing_time_seconds": 0.0
}
```

#### `POST /predict/sync`
Synchronous binding affinity prediction. Use for quick predictions.

#### `GET /jobs/{job_id}`
Get the status and results of a specific prediction job.

#### `GET /health`
System health check including Boltz-2 availability.

### Validation Endpoints

#### `POST /validate/protein`
Validate a protein sequence without running prediction.

#### `POST /validate/ligand`
Validate a SMILES string without running prediction.

### Utility Endpoints

#### `GET /examples`
Get example protein sequences and SMILES for testing.

#### `GET /docs`
Interactive API documentation (Swagger UI).

#### `GET /redoc`
Alternative API documentation (ReDoc).

## 🔧 Configuration

Configuration is managed through environment variables and the `config.py` file:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Boltz-2 Configuration
BOLTZ_COMMAND=boltz
USE_MSA_SERVER=true
MAX_SEQUENCE_LENGTH=10000
MAX_SMILES_LENGTH=1000

# Job Configuration
MAX_CONCURRENT_JOBS=4
JOB_TIMEOUT_SECONDS=300
```

## 🧪 Development

### Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── models.py            # Pydantic data models
├── services/            # Business logic services
│   ├── __init__.py
│   └── boltz_service.py # Boltz-2 integration service
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Adding New Features

1. **New Endpoints**: Add to `main.py` with proper validation
2. **New Services**: Create in `services/` directory
3. **New Models**: Add to `models.py` with Pydantic validation
4. **Configuration**: Extend `config.py` as needed

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_boltz_service.py
```

### Code Quality

The project uses:
- **Pydantic** for data validation
- **FastAPI** for modern, fast web framework
- **Type hints** throughout for better code quality
- **Async/await** for non-blocking operations

## 🚀 Production Deployment

### Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

Set production environment variables:
```bash
export DEBUG=false
export MAX_CONCURRENT_JOBS=8
export JOB_TIMEOUT_SECONDS=600
```

### Monitoring

- Health check endpoint: `/health`
- Job status tracking
- Error logging and monitoring
- Performance metrics

## 🔍 Troubleshooting

### Common Issues

1. **Boltz-2 not found**
   - Ensure Boltz-2 is installed: `pip install boltz[cuda]`
   - Check PATH: `which boltz`

2. **CUDA errors**
   - Verify CUDA installation: `nvidia-smi`
   - Install CPU version if GPU unavailable: `pip install boltz`

3. **Memory issues**
   - Reduce `MAX_CONCURRENT_JOBS` in config
   - Monitor system resources during predictions

4. **Timeout errors**
   - Increase `JOB_TIMEOUT_SECONDS` for complex molecules
   - Use async endpoint for long-running predictions

### Logs

Check application logs for detailed error information:
```bash
tail -f logs/atomera.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Boltz-2 Team**: For the powerful molecular modeling framework
- **FastAPI**: For the excellent web framework
- **Pydantic**: For robust data validation

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint when running
- **Community**: Join our development discussions

---

**Built with ❤️ for the molecular biology research community**
