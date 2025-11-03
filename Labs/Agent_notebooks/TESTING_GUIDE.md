
C:\Users\labadmin\AppData\Local\Programs\Python\Python311\Lib\site-packages\flaml\__init__.py:20: UserWarning: flaml.automl is not available. Please install flaml[automl] to enable AutoML functionalities.

**Quick Reference for Testing the PRD Generation System**

---

## 🚀 Quick Start

### Prerequisites
```bash
# 1. Ensure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements_crewai.txt

# 3. Verify langchain-google-genai is installed
pip show langchain-google-genai
```

### Run All Tests
```bash
cd Labs/Agent_notebooks
python test_crewai_system.py
```

**Expected Output**:
```
🚀 STARTING CREWAI AGENT SYSTEM TEST SUITE
========================================
🧪 Starting test: API Keys Configuration
✅ PASSED: API Keys Configuration (0.00s)
...
📊 TEST SUMMARY
========================================
Total Tests: 10
✅ Passed: 10
❌ Failed: 0
⏭️  Skipped: 0
⏱️  Duration: ~60s
```

---

## 📋 Test Checklist

### Before Running Tests

- [ ] Virtual environment activated
- [ ] All dependencies installed (`pip install -r requirements_crewai.txt`)
- [ ] API keys configured in `.env` file:
  ```
  OPENAI_API_KEY=sk-your-key-here
  # OR
  GOOGLE_API_KEY=your-key-here
  ```
- [ ] Working directory is `Labs/Agent_notebooks/`

### After Running Tests

- [ ] Check test logs: `test_logs/crewai_test_*.log`
- [ ] Review JSON report: `test_logs/test_report_*.json`
- [ ] Verify outputs generated: `test_outputs/test_prd_*.md`
- [ ] Check for failed tests and review errors

---

## 🧪 Individual Test Descriptions

### Test 1: API Keys Configuration
**Purpose**: Verify API keys are properly configured  
**Duration**: <1s  
**What it checks**:
- Environment variables set
- Key format validation
- Both OpenAI and Google support

**Manual Test**:
```python
from test_crewai_system import test_api_keys
result = test_api_keys()
print(result.to_dict())
```

### Test 2: Dependencies Import
**Purpose**: Verify all required packages can be imported  
**Duration**: <1s (or 30-40s if importing for first time)  
**What it checks**:
- crewai
- langchain
- langchain_openai
- langchain_google_genai
- fastapi, uvicorn, websockets, pydantic

**Manual Test**:
```python
from test_crewai_system import test_dependencies_import
result = test_dependencies_import()
print(result.to_dict())
```

### Test 3: CrewAI Agent Creation
**Purpose**: Test creating agents with LLM configuration  
**Duration**: <1s  
**What it checks**:
- Agent initialization
- LLM backend configuration
- Agent properties

**Manual Test**:
```python
from test_crewai_system import test_crewai_agent_creation
result = test_crewai_agent_creation()
print(result.to_dict())
```

### Test 4: CrewAI Task Creation
**Purpose**: Test creating and linking tasks  
**Duration**: <1s  
**What it checks**:
- Task description
- Agent assignment
- Expected output definition

**Manual Test**:
```python
from test_crewai_system import test_crewai_task_creation
result = test_crewai_task_creation()
print(result.to_dict())
```

### Test 5: CrewAI Crew Execution
**Purpose**: Test executing a simple workflow with actual API call  
**Duration**: 5-15s (makes real API call)  
**What it checks**:
- Crew initialization
- Task execution
- Output generation
- Output format validation

**Cost**: ~$0.001-0.002 (uses GPT-4o-mini)

**Manual Test**:
```python
from test_crewai_system import test_crewai_crew_execution
result = test_crewai_crew_execution()
print(result.to_dict())
```

### Test 6: Full PRD Generation Workflow
**Purpose**: Test complete multi-agent PRD generation  
**Duration**: 30-60s (makes multiple API calls)  
**What it checks**:
- Multi-agent collaboration
- Sequential task execution
- PRD structure validation
- Output file creation

**Cost**: ~$0.01-0.03 (uses GPT-4o-mini for multiple agents)

**Output**: Creates file in `test_outputs/test_prd_*.md`

**Manual Test**:
```python
from test_crewai_system import test_full_prd_generation
result = test_full_prd_generation()
print(result.to_dict())
```

### Test 7: Web Interface Imports
**Purpose**: Verify web interface dependencies  
**Duration**: <1s  
**What it checks**:
- crewai_web_interface.py exists
- FastAPI, Uvicorn, WebSockets available
- Version information

**Manual Test**:
```python
from test_crewai_system import test_web_interface_imports
result = test_web_interface_imports()
print(result.to_dict())
```

### Test 8: Error Handling
**Purpose**: Test system behavior with invalid inputs  
**Duration**: <1s  
**What it checks**:
- Empty task handling
- Missing LLM errors
- Graceful failure modes

**Manual Test**:
```python
from test_crewai_system import test_error_handling
result = test_error_handling()
print(result.to_dict())
```

### Test 9: Output Quality Validation
**Purpose**: Analyze generated output quality  
**Duration**: <1s  
**What it checks**:
- Output directory existence
- File count
- Content structure
- Quality metrics

**Manual Test**:
```python
from test_crewai_system import test_output_quality
result = test_output_quality()
print(result.to_dict())
```

### Test 10: Performance Metrics
**Purpose**: Collect system performance data  
**Duration**: <1s  
**What it checks**:
- Python version
- Platform info
- Memory usage
- Working directory

**Manual Test**:
```python
from test_crewai_system import test_performance_metrics
result = test_performance_metrics()
print(result.to_dict())
```

---

## 🔍 Troubleshooting Test Failures

### "No API keys found"
**Cause**: Missing `.env` file or keys not set  
**Fix**:
```bash
# Create .env file in Labs/Agent_notebooks/
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### "No module named 'langchain_google_genai'"
**Cause**: Package not installed  
**Fix**:
```bash
pip install langchain-google-genai==2.0.5
```

### "ModuleNotFoundError: No module named 'crewai'"
**Cause**: Dependencies not installed  
**Fix**:
```bash
pip install -r requirements_crewai.txt
```

### Tests timing out
**Cause**: API calls taking too long  
**Fix**:
- Check internet connection
- Verify API key is valid
- Try with Google Gemini instead of OpenAI

### "UnicodeEncodeError" in logs
**Cause**: Windows terminal encoding  
**Impact**: Cosmetic only - tests still work  
**Fix**: Can be ignored, or see Issue #NEW-2 in CREWAI_ISSUES_LOG.md

---

## 📊 Reading Test Results

### Console Output

```
🧪 Starting test: API Keys Configuration
✅ PASSED: API Keys Configuration (0.00s)
```

- 🧪 = Test starting
- ✅ = Test passed
- ❌ = Test failed
- ⏭️ = Test skipped
- Duration shown in parentheses

### JSON Report

Located in: `test_logs/test_report_*.json`

```json
{
  "timestamp": "2025-10-31T...",
  "tests": [
    {
      "test_name": "API Keys Configuration",
      "status": "passed",
      "duration": 0.002,
      "error": null,
      "details": {
        "openai_key_present": true,
        ...
      }
    }
  ],
  "summary": {
    "total": 10,
    "passed": 10,
    "failed": 0,
    "skipped": 0
  }
}
```

### Log File

Located in: `test_logs/crewai_test_*.log`

Contains detailed execution logs with timestamps, including:
- Test start/end times
- Error messages and stack traces
- Detailed results
- Summary statistics

---

## 🎯 Test Success Criteria

### Minimum Acceptable

- [ ] At least 8/10 tests pass
- [ ] No blocking errors
- [ ] At least one successful PRD generation

### Ideal

- [ ] 10/10 tests pass
- [ ] All outputs generated successfully
- [ ] Performance within expected ranges
- [ ] No warnings or errors

---

## 🔄 Continuous Testing

### Before Committing Code

```bash
# Run quick smoke tests
python test_crewai_system.py

# Check for any failures
if [ $? -eq 0 ]; then
  echo "All tests passed! ✅"
else
  echo "Tests failed! ❌"
  exit 1
fi
```

### After Major Changes

1. Run full test suite
2. Generate sample PRDs via web interface
3. Compare outputs with previous versions
4. Check performance metrics

### Before Deployment

1. Full test suite on clean environment
2. Integration tests with real API
3. Load testing (multiple concurrent requests)
4. Security validation

---

## 📈 Performance Benchmarks

### Expected Execution Times

| Test | Expected Duration | API Calls |
|------|------------------|-----------|
| API Keys Config | <1s | 0 |
| Dependencies Import | 1-40s | 0 |
| Agent Creation | <1s | 0 |
| Task Creation | <1s | 0 |
| Crew Execution | 5-15s | 1 |
| Full PRD Generation | 30-60s | 3-5 |
| Web Interface | <1s | 0 |
| Error Handling | <1s | 0-1 |
| Output Quality | <1s | 0 |
| Performance Metrics | <1s | 0 |

**Total Suite**: 60-120 seconds

### API Cost Estimates

- **Full Test Suite**: $0.02-0.05 per run (GPT-4o-mini)
- **Single PRD Test**: $0.01-0.03
- **Using Gemini**: Free (within quota)

---

## 🛠️ Advanced Testing

### Custom Test Business Problems

Create your own test cases:

```python
# In test_crewai_system.py, modify test_full_prd_generation():
test_problem = """Your custom business problem here"""
```

### Testing with Different LLMs

```python
# Force OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# Force Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)

# Try GPT-4 for higher quality (more expensive)
llm = ChatOpenAI(model="gpt-4", temperature=0.3)
```

### Performance Profiling

```bash
# Run with profiling
python -m cProfile -o profile.stats test_crewai_system.py

# Analyze results
python -m pstats profile.stats
```

### Memory Profiling

```bash
# Install memory profiler
pip install memory-profiler

# Run with memory profiling
python -m memory_profiler test_crewai_system.py
```

---

## 📚 Related Documentation

- **Issues Log**: `CREWAI_ISSUES_LOG.md` - Known issues and fixes
- **Test Report**: `TEST_EXECUTION_REPORT.md` - Latest test results
- **System README**: `README_CREWAI_PRD_SYSTEM.md` - System overview
- **Quick Start**: `CREWAI_QUICKSTART.md` - Getting started guide

---

## 🤝 Contributing Tests

### Adding New Tests

1. Add test function to `test_crewai_system.py`:
```python
def test_your_feature() -> TestResult:
    """Test your new feature"""
    result = TestResult("Your Feature Name")
    result.start()
    
    try:
        # Your test logic here
        result.pass_test({"detail": "value"})
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result
```

2. Add to `test_functions` list in `run_all_tests()`:
```python
test_functions = [
    # ... existing tests
    test_your_feature,
]
```

3. Update this guide with test description

---

## 📞 Support

**Issues?**
1. Check `CREWAI_ISSUES_LOG.md` for known issues
2. Review test logs in `test_logs/`
3. Verify environment setup
4. Check API key configuration

**Still stuck?**
- Review error messages in log files
- Compare with expected output in this guide
- Check that all dependencies are installed
- Ensure API keys are valid and have quota

---

**Guide Version**: 1.0  
**Last Updated**: 2025-10-31  
**For System Version**: CrewAI 0.86.0
