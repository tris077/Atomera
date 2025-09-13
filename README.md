# 🧬 Atomera - Binding Affinity Research Platform

A modern, user-friendly platform for exploring molecular interactions and binding affinities, powered by the cutting-edge Boltz-2 molecular modeling framework.

## 🚀 What is Atomera?

Atomera is a research platform that makes advanced molecular modeling accessible to researchers, students, and drug discovery teams. Instead of building new molecular models from scratch, we wrap the powerful Boltz-2 framework with a clean, modern interface that provides:

- **Protein-Ligand Binding Affinity Prediction** - Core molecular modeling functionality
- **Interactive Web Interface** - User-friendly frontend for exploring molecular interactions
- **RESTful API** - Clean backend for integration with other tools and workflows
- **Educational Features** - Designed to help students and researchers understand molecular interactions

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Atomera Platform                     │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Future)  │  Backend API  │  Boltz-2 Framework   │
│  - React/Next.js    │  - FastAPI    │  - Molecular Models  │
│  - Interactive UI   │  - REST API   │  - Affinity Predict  │
│  - Visualization    │  - Validation │  - Structure Models  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
atomera/
├── backend/                 # Python FastAPI backend
│   ├── main.py            # Main API application
│   ├── config.py          # Configuration management
│   ├── models.py          # Pydantic data models
│   ├── services/          # Business logic services
│   ├── requirements.txt   # Python dependencies
│   ├── start.py           # Simple startup script
│   ├── test_simple.py     # Built-in testing script
│   ├── TESTING.md         # Testing guide
│   └── README.md          # Backend documentation
├── frontend/              # Frontend application (future)
└── README.md             # This file
```

## 🎯 Core Goals

1. **Wrap Boltz-2 Functionality** - Provide clean API access to molecular modeling
2. **Modern User Experience** - Build an intuitive interface for researchers
3. **Educational Platform** - Help students understand molecular interactions
4. **Competition Ready** - Scale into a Diamond Challenge demo
5. **Modular Design** - Separate backend and frontend for flexibility

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- Boltz-2 framework (optional for basic testing)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd atomera
   ```

2. **Start the backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   python start.py
   ```

3. **Test the API**

   ```bash
   # In a new terminal
   python test_simple.py
   ```

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Examples: http://localhost:8000/examples

## 🧪 Testing Without Frontend

The backend is fully testable without a frontend using multiple methods:

### 1. Built-in Test Script

```bash
python test_simple.py
```

Tests all endpoints using only Python's built-in libraries.

### 2. Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Command Line Testing

```bash
# Health check
curl http://localhost:8000/health

# Get examples
curl http://localhost:8000/examples
```

See [TESTING.md](backend/TESTING.md) for complete testing instructions.

## 🔬 Key Features

### Molecular Modeling

- **Protein-Ligand Binding Affinity Prediction** using Boltz-2
- **Input Validation** for protein sequences and SMILES strings
- **Asynchronous Processing** for long-running predictions
- **Job Management** with progress tracking

### API Endpoints

- `POST /predict` - Asynchronous affinity prediction
- `POST /predict/sync` - Synchronous prediction for quick results
- `GET /jobs/{id}` - Check prediction job status
- `POST /validate/*` - Validate molecular inputs
- `GET /examples` - Example molecules for testing

### Developer Experience

- **Interactive Documentation** with Swagger UI
- **Type Safety** with Pydantic models
- **Error Handling** with detailed error messages
- **Configuration Management** with environment variables

## 🧪 Example Usage

### Predict Binding Affinity

```python
import requests

# Create prediction request
data = {
    "protein": {
        "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT",
        "id": "A"
    },
    "ligand": {
        "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O",  # Aspirin
        "id": "B"
    }
}

# Submit prediction
response = requests.post("http://localhost:8000/predict", json=data)
job_id = response.json()["job_id"]

# Check results
status = requests.get(f"http://localhost:8000/jobs/{job_id}")
print(status.json())
```

## 🚀 Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start development server
python start.py

# Test the API
python test_simple.py
```

### Adding New Features

1. **New API Endpoints** - Add to `main.py`
2. **New Services** - Create in `services/` directory
3. **New Models** - Add to `models.py`
4. **Configuration** - Extend `config.py`

## 🔧 Configuration

Copy `backend/env.example` to `backend/.env` and customize:

```bash
# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Boltz-2 settings
USE_MSA_SERVER=true
MAX_CONCURRENT_JOBS=4
JOB_TIMEOUT_SECONDS=300
```

## 📚 Documentation

- **Backend API**: [Backend README](backend/README.md)
- **Testing Guide**: [TESTING.md](backend/TESTING.md)
- **API Docs**: http://localhost:8000/docs (when running)
- **Boltz-2**: [Official Documentation](https://github.com/jwohlwend/boltz)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 🎓 Educational Use

Atomera is designed to be an educational platform:

- **Interactive Learning** - Visual molecular interactions
- **Real Research Tools** - Use actual molecular modeling frameworks
- **Student Friendly** - Clear explanations and examples
- **Research Ready** - Professional-grade tools for serious research

## 🏆 Competition Goals

This platform is designed to scale into a competition-ready demo:

- **Diamond Challenge Ready** - Professional presentation capabilities
- **Scalable Architecture** - Handle multiple users and complex workflows
- **Visual Impact** - Interactive molecular visualizations
- **Research Validation** - Real scientific applications

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **Boltz-2 Team** - For the powerful molecular modeling framework
- **FastAPI** - For the excellent web framework
- **Pydantic** - For robust data validation

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint when running
- **Testing**: See [TESTING.md](backend/TESTING.md)

---

**Built with ❤️ for the molecular biology research community**

_Making advanced molecular modeling accessible to everyone_
