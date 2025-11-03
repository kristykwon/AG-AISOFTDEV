# AutoGen PRD API - Usage Guide

## 🌐 Accessing the Tools Online

You now have **two ways** to interact with the AutoGen PRD system:

### Option 1: Local File Viewer (Already Running)
**URL:** http://localhost:8080

This serves your documentation files as a simple file browser:
- Browse markdown documentation
- View generated artifacts
- Read configuration files

### Option 2: REST API Endpoints (New!)
**URL:** http://localhost:8000

This provides programmatic access via HTTP API endpoints.

---

## 🚀 Starting the API Server

### Step 1: Start the FastAPI Server

Open a new terminal and run:

```powershell
cd Labs\Agent_notebooks
python autogen_prd_api.py
```

Or using uvicorn directly:

```powershell
uvicorn autogen_prd_api:app --reload --port 8000
```

### Step 2: View Interactive API Documentation

Open your browser to:

**📚 Swagger UI (Interactive):** http://localhost:8000/docs
- Try out endpoints directly in the browser
- See request/response examples
- Test API calls without writing code

**📖 ReDoc (Documentation):** http://localhost:8000/redoc
- Cleaner, read-only documentation
- Better for sharing with team

---

## 📡 API Endpoints Reference

### 1. Health Check
```http
GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-31T12:00:00",
  "active_jobs": 0
}
```

### 2. Generate PRD (Main Endpoint)
```http
POST http://localhost:8000/api/v1/generate
Content-Type: application/json

{
  "problem_statement": "We need a tool to help our company's new hires get up to speed.",
  "project_name": "onboarding_tool"
}
```

**Response:**
```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "pending",
  "message": "PRD generation started. Check status at /api/v1/jobs/{job_id}",
  "artifacts_url": "/api/v1/artifacts/abc123-def456-ghi789"
}
```

### 3. Check Job Status
```http
GET http://localhost:8000/api/v1/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "abc123-def456-ghi789",
  "status": "completed",
  "created_at": "2025-10-31T12:00:00",
  "completed_at": "2025-10-31T12:05:00",
  "artifacts": {
    "user_stories": "/path/to/user_stories.json",
    "prd": "/path/to/prd.md",
    "schema": "/path/to/schema.sql"
  }
}
```

**Status values:**
- `pending` - Job queued
- `processing` - Agents working
- `completed` - All artifacts ready
- `failed` - Error occurred

### 4. Get All Artifacts
```http
GET http://localhost:8000/api/v1/artifacts/{job_id}
```

**Response:**
```json
{
  "job_id": "abc123-def456-ghi789",
  "artifacts": { ... },
  "download_urls": {
    "user_stories": "/api/v1/artifacts/abc123.../user_stories",
    "prd": "/api/v1/artifacts/abc123.../prd",
    "schema": "/api/v1/artifacts/abc123.../schema"
  }
}
```

### 5. Download Specific Artifact
```http
GET http://localhost:8000/api/v1/artifacts/{job_id}/user_stories
GET http://localhost:8000/api/v1/artifacts/{job_id}/prd
GET http://localhost:8000/api/v1/artifacts/{job_id}/schema
```

Returns the file directly.

### 6. Get Example Problems
```http
GET http://localhost:8000/api/v1/examples
```

Returns pre-made example business problems to try.

---

## 💻 Using the API - Code Examples

### Python (using requests)

```python
import requests
import time

# 1. Submit a generation request
response = requests.post(
    "http://localhost:8000/api/v1/generate",
    json={
        "problem_statement": "We need an inventory management system for our warehouse."
    }
)
job_id = response.json()["job_id"]
print(f"Job ID: {job_id}")

# 2. Poll for completion
while True:
    status_response = requests.get(f"http://localhost:8000/api/v1/jobs/{job_id}")
    status = status_response.json()["status"]
    print(f"Status: {status}")
    
    if status == "completed":
        break
    elif status == "failed":
        print("Generation failed!")
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again

# 3. Download artifacts
user_stories = requests.get(
    f"http://localhost:8000/api/v1/artifacts/{job_id}/user_stories"
).json()

prd_text = requests.get(
    f"http://localhost:8000/api/v1/artifacts/{job_id}/prd"
).text

schema_sql = requests.get(
    f"http://localhost:8000/api/v1/artifacts/{job_id}/schema"
).text

print("✅ All artifacts downloaded!")
```

### JavaScript (using fetch)

```javascript
// 1. Submit generation request
const response = await fetch('http://localhost:8000/api/v1/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    problem_statement: 'We need a customer support ticketing system.'
  })
});

const { job_id } = await response.json();
console.log('Job ID:', job_id);

// 2. Check status
const checkStatus = async () => {
  const statusResponse = await fetch(`http://localhost:8000/api/v1/jobs/${job_id}`);
  const { status, artifacts } = await statusResponse.json();
  
  if (status === 'completed') {
    console.log('✅ Generation complete!');
    return artifacts;
  }
  
  // Check again in 5 seconds
  setTimeout(checkStatus, 5000);
};

await checkStatus();
```

### cURL (Command Line)

```bash
# 1. Generate PRD
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"problem_statement": "We need a project management tool."}'

# 2. Check status
curl "http://localhost:8000/api/v1/jobs/YOUR_JOB_ID_HERE"

# 3. Download PRD
curl "http://localhost:8000/api/v1/artifacts/YOUR_JOB_ID_HERE/prd" -o prd.md
```

### PowerShell

```powershell
# 1. Generate PRD
$body = @{
    problem_statement = "We need an employee onboarding tool."
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/generate" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$jobId = $response.job_id
Write-Host "Job ID: $jobId"

# 2. Check status
$status = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/jobs/$jobId"
Write-Host "Status: $($status.status)"

# 3. Download artifacts when complete
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/artifacts/$jobId/prd" `
    -OutFile "generated_prd.md"
```

---

## 🎯 Typical Workflow

1. **Start the API server** (one time)
   ```powershell
   python autogen_prd_api.py
   ```

2. **Submit a business problem** via POST to `/api/v1/generate`

3. **Get the job_id** from the response

4. **Poll the status** every 5-10 seconds via GET to `/api/v1/jobs/{job_id}`

5. **Download artifacts** when status is "completed"

6. **Use the artifacts** in your project

---

## 🔧 Current Limitations & Next Steps

### Current State (MVP)
- ✅ API structure is set up
- ✅ Endpoints are defined
- ⚠️ Uses placeholder data (not real AutoGen agents yet)

### To Make It Production-Ready

You need to integrate the actual AutoGen workflow. Replace the `run_autogen_workflow` function in `autogen_prd_api.py` with:

```python
async def run_autogen_workflow(job_id: str, problem_statement: str, project_name: Optional[str]):
    """Run the actual AutoGen multi-agent system"""
    try:
        jobs[job_id].status = "processing"
        
        # Import the AutoGen setup
        from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
        
        # Set up agents (copy from autogen_prd_system.ipynb)
        # Run workflows 1, 2, 3
        # Capture generated artifacts
        
        # Real implementation here...
        
        jobs[job_id].status = "completed"
        jobs[job_id].artifacts = {
            "user_stories": actual_user_stories_path,
            "prd": actual_prd_path,
            "schema": actual_schema_path
        }
    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)
```

---

## 📊 Monitoring the API

### View Active Jobs
```http
GET http://localhost:8000/api/v1/jobs
```

Shows all jobs with their statuses.

### Health Check
```http
GET http://localhost:8000/health
```

Shows API health and number of active jobs.

---

## 🌍 Exposing to the Internet (Optional)

### Using ngrok
```bash
ngrok http 8000
```

This creates a public URL like `https://abc123.ngrok.io` that tunnels to your local API.

### Using Cloudflare Tunnel
```bash
cloudflare tunnel --url http://localhost:8000
```

---

## 📚 Additional Resources

- **Interactive API Docs**: http://localhost:8000/docs
- **Documentation Viewer**: http://localhost:8000 (file browser)
- **API Code**: `autogen_prd_api.py`
- **Notebook**: `autogen_prd_system.ipynb`

---

## 🎉 Quick Test

Try this in your browser:

1. Go to: http://localhost:8000/docs
2. Click on **POST /api/v1/generate**
3. Click **"Try it out"**
4. Enter a business problem
5. Click **"Execute"**
6. Copy the `job_id` from the response
7. Paste it into **GET /api/v1/jobs/{job_id}** and check status

That's it! You now have a REST API for your AutoGen PRD system! 🚀
