# 🔌 AutoGen System - Ports Reference

## Quick Reference

| Service | Port | URL | File | Purpose |
|---------|------|-----|------|---------|
| **🌐 Web Interface** | **8001** | http://localhost:8001 | `web_interface.py` | Interactive browser UI - **USE THIS TO TYPE PROMPTS** |
| 🔧 REST API | 8000 | http://localhost:8000 | `autogen_prd_api.py` | Programmatic API access |
| 📄 Documentation Server | 8080 | http://localhost:8080 | (http.server) | View markdown files |

---

## ⚠️ Important: Two Different Interfaces

### 1. **Web Interface (Port 8001)** ← USE THIS ONE!
```
http://localhost:8001
```
- ✅ **Beautiful graphical interface**
- ✅ **Type prompts in a text box**
- ✅ **Watch agents work in real-time**
- ✅ **Click examples to try**

**To Start:**
```powershell
cd Labs\Agent_notebooks
python web_interface.py
```

---

### 2. **REST API (Port 8000)**
```
http://localhost:8000
```
- ⚙️ Returns JSON responses
- ⚙️ For integration with other tools
- ⚙️ Requires HTTP POST requests
- ⚙️ See `API_USAGE_GUIDE.md` for details

**To Start:**
```powershell
cd Labs\Agent_notebooks
python autogen_prd_api.py
```

---

## 🎯 What You're Looking For

### ❓ "I want to type my business problem in a web browser"
**Answer:** Go to http://localhost:8001 (Web Interface)

### ❓ "I want to integrate AutoGen into my application"
**Answer:** Use http://localhost:8000 (REST API)

### ❓ "I want to run it in Python/Jupyter"
**Answer:** Use `autogen_prd_system.ipynb` (notebook)

---

## 🚨 If You See JSON Instead of a Form

You're on the wrong port! 

**Seeing this?**
```json
{"status":"ok","message":"Onboarding API"}
```
or
```json
{"message": "Welcome to AutoGen PRD API", "version": "1.0"}
```

**Solution:** Change the URL to http://localhost:8001

---

## 🔧 Port Already in Use?

If you get an error that a port is already in use:

### Option 1: Stop the conflicting service
```powershell
# Find what's using the port
netstat -ano | findstr :8001

# Kill the process (use PID from above)
taskkill /PID <PID> /F
```

### Option 2: Use a different port
Edit the Python file and change the port number:

**In `web_interface.py`:**
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to 8002, 8003, etc.
```

---

## ✅ Quick Health Check

### Test Web Interface
```powershell
# Open in browser or use curl
curl http://localhost:8001
```
**Expected:** HTML page loads with form

### Test REST API
```powershell
curl http://localhost:8000/health
```
**Expected:** JSON response `{"status": "healthy"}`

---

## 📝 Summary

- **Port 8001** = Web Interface with forms → **This is what you want for typing prompts!**
- **Port 8000** = REST API with JSON → For programmatic access
- **Port 8080** = File viewer → For reading documentation

---

**👉 For your use case (typing prompts), always go to: http://localhost:8001**
