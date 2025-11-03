# CrewAI Testing - Quick Reference Card

**One-page reference for testing the CrewAI Agent System**

---

## ⚡ Quick Commands

```bash
# Run all tests
cd Labs/Agent_notebooks
python test_crewai_system.py

# Check test results
cat test_logs/test_report_*.json

# View latest log
cat test_logs/crewai_test_*.log

# Start web interface
python crewai_web_interface.py
```

---

## 📊 Test Results Interpretation

| Symbol | Meaning | Action |
|--------|---------|--------|
| ✅ | Test passed | No action needed |
| ❌ | Test failed | Check error details |
| ⏭️ | Test skipped | Review skip reason |
| 🧪 | Test starting | Wait for completion |

---

## 🐛 Common Issues & Quick Fixes

### "No module named 'langchain_google_genai'"
```bash
pip install langchain-google-genai==2.0.5
```

### "No API keys found"
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### "ModuleNotFoundError: No module named 'crewai'"
```bash
pip install -r requirements_crewai.txt
```

### Test timeouts
- Check internet connection
- Verify API key is valid
- Try Google Gemini instead of OpenAI

---

## 📁 File Locations

| File | Purpose |
|------|---------|
| `test_crewai_system.py` | Test suite |
| `test_logs/` | Test execution logs |
| `test_outputs/` | Generated PRDs |
| `CREWAI_ISSUES_LOG.md` | Known issues |
| `TEST_EXECUTION_REPORT.md` | Latest results |
| `TESTING_GUIDE.md` | Full testing guide |

---

## 🎯 Success Criteria

**Minimum Acceptable**: 8/10 tests pass  
**Ideal**: 10/10 tests pass  
**Duration**: 60-120 seconds  

---

## 📞 Help

1. Check `CREWAI_ISSUES_LOG.md` for known issues
2. Review `TESTING_GUIDE.md` for detailed help
3. Check test logs in `test_logs/`
4. Verify environment setup

---

## 🔍 Test Coverage

1. ✅ API Keys Configuration
2. ✅ Dependencies Import
3. ✅ Agent Creation
4. ✅ Task Creation
5. ✅ Crew Execution
6. ✅ Full PRD Generation
7. ✅ Web Interface
8. ✅ Error Handling
9. ✅ Output Quality
10. ✅ Performance Metrics

---

## 📈 Expected Performance

| Operation | Time | Cost |
|-----------|------|------|
| Test suite | 60-120s | $0.02-0.05 |
| Simple PRD | 30-60s | $0.01-0.03 |
| Complex PRD | 90-120s | $0.03-0.05 |

---

## 🚦 Status Indicators

| Issue Status | Meaning |
|--------------|---------|
| ✅ RESOLVED | Fixed and verified |
| 🔍 Open | Known, has workaround |
| ⏳ PENDING | Scheduled for fix |
| ❌ BLOCKED | Needs attention |

---

**Quick Reference v1.0** | For full details see `TESTING_GUIDE.md`
