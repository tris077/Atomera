# 🧪 Testing Atomera Backend

This guide shows you how to test the backend API without needing a frontend or external tools.

## 🚀 Quick Start

### 1. Start the Server

```bash
cd backend
pip install -r requirements.txt
python start.py
```

The server will start at `http://localhost:8000`

### 2. Test the API

#### Option A: Built-in Test Script (Recommended)

```bash
# In a new terminal
python test_simple.py
```

This script tests all endpoints using only Python's built-in libraries.

#### Option B: Interactive API Documentation

Open your browser and go to:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive testing interfaces where you can:

- See all available endpoints
- Test requests directly in the browser
- View request/response schemas
- Execute API calls with sample data

#### Option C: Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Get examples
curl http://localhost:8000/examples

# Validate protein
curl -X POST "http://localhost:8000/validate/protein" \
     -H "Content-Type: application/json" \
     -d '{"sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT", "id": "A"}'

# Validate ligand
curl -X POST "http://localhost:8000/validate/ligand" \
     -H "Content-Type: application/json" \
     -d '{"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "id": "B"}'

# Create prediction job
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "protein": {"sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT", "id": "A"},
       "ligand": {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "id": "B"}
     }'
```

## 🔍 What to Test

### Basic Endpoints

1. **Root** (`/`) - API information
2. **Health** (`/health`) - System status and Boltz-2 availability
3. **Examples** (`/examples`) - Sample molecules for testing

### Validation Endpoints

4. **Protein Validation** (`/validate/protein`) - Validate amino acid sequences
5. **Ligand Validation** (`/validate/ligand`) - Validate SMILES strings

### Core Functionality

6. **Prediction** (`/predict`) - Create binding affinity prediction jobs
7. **Job Status** (`/jobs/{id}`) - Check prediction progress and results

## 📊 Expected Results

### Health Check

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "boltz_available": true,
  "timestamp": "2025-01-19T..."
}
```

### Examples

```json
{
  "proteins": {
    "insulin": {
      "name": "Human Insulin",
      "sequence": "MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT"
    },
    "lysozyme": {
      "name": "Hen Egg White Lysozyme",
      "sequence": "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGDGMNAWVAWRNRCKGTDVQAWIRGCRL"
    }
  },
  "ligands": {
    "aspirin": { "name": "Aspirin", "smiles": "CC(=O)OC1=CC=CC=C1C(=O)O" },
    "caffeine": { "name": "Caffeine", "smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C" }
  }
}
```

### Prediction Job

```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "processing_time_seconds": 0.0
}
```

## 🐛 Troubleshooting

### Server Won't Start

- Check Python version (3.10+ required)
- Install dependencies: `pip install -r requirements.txt`
- Check if port 8000 is already in use

### Import Errors

- Make sure you're in the `backend` directory
- Install missing packages: `pip install fastapi uvicorn pydantic`

### Boltz-2 Not Available

- Install Boltz-2: `pip install boltz[cuda] -U`
- The API will still work but show "degraded" status

### Connection Refused

- Make sure the server is running
- Check the URL (should be `http://localhost:8000`)
- Verify no firewall is blocking the connection

## 🎯 Next Steps

Once testing is successful:

1. **Build Frontend** - The API is ready to connect to any frontend
2. **Custom Molecules** - Test with your own protein sequences and SMILES
3. **Integration** - Connect other tools to the REST API
4. **Production** - Deploy with proper configuration and monitoring

## 💡 Pro Tips

- Use the `/docs` endpoint for the best testing experience
- The built-in test script (`test_simple.py`) is great for CI/CD
- All endpoints return proper HTTP status codes
- Error responses include detailed messages
- The API is CORS-enabled for frontend integration

---

**Happy testing! 🧬✨**
