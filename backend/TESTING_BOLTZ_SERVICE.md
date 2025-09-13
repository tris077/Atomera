# 🧪 Testing BoltzService

This guide covers how to test the `BoltzService` class in `services/boltz_service.py`.

## 🚀 Quick Start

### 1. Install Testing Dependencies

```bash
cd backend
pip install -r requirements-test.txt
```

### 2. Run All Tests

```bash
# Option A: Use the test runner script
python run_tests.py

# Option B: Use pytest directly
pytest test_boltz_service.py -v

# Option C: Run with coverage
pytest test_boltz_service.py -v --cov=services.boltz_service --cov-report=html
```

## 📋 Test Coverage

The test suite covers:

### ✅ **Service Initialization**
- Directory creation
- Settings validation
- Error handling

### ✅ **Boltz-2 Availability**
- Command availability check
- Subprocess error handling
- Timeout handling

### ✅ **Job Management**
- Job creation with metadata
- Status updates and progress tracking
- Job status retrieval
- Cleanup operations

### ✅ **Input/Output Processing**
- YAML file generation
- File validation
- Temporary file cleanup

### ✅ **Prediction Execution**
- Subprocess command execution
- Output parsing
- Error handling
- Success/failure scenarios

### ✅ **Edge Cases**
- Missing files
- Corrupted data
- Network timeouts
- Invalid inputs

## 🔧 Running Specific Tests

### Run Individual Test Methods

```bash
# Test specific method
pytest test_boltz_service.py::TestBoltzService::test_create_prediction_job -v

# Test with pattern matching
pytest test_boltz_service.py -k "prediction" -v

# Test specific class
pytest test_boltz_service.py::TestBoltzService -v
```

### Run with Different Output Levels

```bash
# Verbose output
pytest test_boltz_service.py -v

# Very verbose output
pytest test_boltz_service.py -vv

# Show local variables on failure
pytest test_boltz_service.py -l

# Stop on first failure
pytest test_boltz_service.py -x
```

## 🧩 Test Structure

### Fixtures

- **`temp_dirs`**: Creates temporary directories for testing
- **`mock_settings`**: Mocks configuration settings
- **`service`**: Creates BoltzService instance with mocked dependencies
- **`sample_request`**: Provides sample prediction request data

### Test Categories

1. **Unit Tests**: Test individual methods in isolation
2. **Integration Tests**: Test method interactions
3. **Mock Tests**: Test with mocked external dependencies
4. **Error Tests**: Test error handling and edge cases

## 🐛 Debugging Tests

### Enable Debug Output

```bash
# Show print statements
pytest test_boltz_service.py -s

# Show local variables on failure
pytest test_boltz_service.py -l

# Run with pdb on failure
pytest test_boltz_service.py --pdb
```

### Check Test Coverage

```bash
# Generate coverage report
pytest test_boltz_service.py --cov=services.boltz_service --cov-report=html

# View coverage in terminal
pytest test_boltz_service.py --cov=services.boltz_service --cov-report=term-missing
```

## 🔍 Manual Testing

### Test Service Methods Directly

```python
# In Python REPL or script
from services.boltz_service import BoltzService
from models import PredictionRequest, ProteinSequence, LigandMolecule

# Create service instance
service = BoltzService()

# Test Boltz-2 availability
available = service.check_boltz_availability()
print(f"Boltz-2 available: {available}")

# Create sample request
protein = ProteinSequence(sequence="MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKT", id="insulin")
ligand = LigandMolecule(smiles="CC(=O)OC1=CC=CC=C1C(=O)O", id="aspirin")
request = PredictionRequest(protein=protein, ligand=ligand)

# Test job creation
job_id = service.create_prediction_job(request)
print(f"Created job: {job_id}")

# Check job status
status = service.get_job_status(job_id)
print(f"Job status: {status}")
```

## 🧪 Testing Scenarios

### 1. **Happy Path Testing**
- Valid protein sequences
- Valid SMILES strings
- Successful Boltz-2 execution
- Proper output parsing

### 2. **Error Path Testing**
- Invalid protein sequences
- Invalid SMILES strings
- Boltz-2 command failures
- File system errors
- Network timeouts

### 3. **Edge Case Testing**
- Empty sequences
- Very long sequences
- Special characters in SMILES
- Missing output files
- Corrupted JSON data

### 4. **Performance Testing**
- Large protein sequences
- Multiple concurrent jobs
- Memory usage under load
- Cleanup efficiency

## 🚨 Common Issues

### Import Errors
```bash
# Make sure you're in the backend directory
cd backend

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Path Issues
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Add current directory to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Permission Issues
```bash
# Check file permissions
ls -la test_boltz_service.py

# Make executable if needed
chmod +x test_boltz_service.py
```

## 📊 Test Results Interpretation

### Exit Codes
- **0**: All tests passed
- **1**: Some tests failed
- **2**: Test execution error
- **5**: No tests collected

### Output Format
```
test_boltz_service.py::TestBoltzService::test_create_prediction_job PASSED
test_boltz_service.py::TestBoltzService::test_check_boltz_availability_success PASSED
...
```

## 🎯 Next Steps

After running tests successfully:

1. **Add More Tests**: Cover additional edge cases
2. **Performance Tests**: Add benchmarking tests
3. **Integration Tests**: Test with real Boltz-2 installation
4. **CI/CD Integration**: Add to automated testing pipeline

## 💡 Pro Tips

- Use `pytest-xdist` for parallel test execution
- Use `pytest-benchmark` for performance testing
- Use `pytest-mock` for advanced mocking
- Use `pytest-cov` for coverage analysis
- Use `pytest-html` for HTML test reports

---

**Happy Testing! 🧬✨**
