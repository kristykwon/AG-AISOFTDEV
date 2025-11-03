"""
FastAPI wrapper for the AutoGen PRD Generation System.

This creates REST API endpoints to interact with the AutoGen system programmatically.
You can send business problems and get back structured artifacts via HTTP requests.

Usage:
    uvicorn autogen_prd_api:app --reload --port 8000
    
Then visit: http://localhost:8000/docs for interactive API documentation
"""

import os
import sys
import json
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import save_artifact, load_artifact

# Initialize FastAPI app
app = FastAPI(
    title="AutoGen PRD Generation API",
    description="REST API for automated Product Requirements Document generation using multi-agent AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request/Response Models
class BusinessProblem(BaseModel):
    """Input model for business problem"""
    problem_statement: str = Field(
        ..., 
        description="Description of the business problem to solve",
        example="We need a tool to help our company's new hires get up to speed."
    )
    project_name: Optional[str] = Field(
        None,
        description="Optional project name for artifact naming",
        example="onboarding_tool"
    )

class JobStatus(BaseModel):
    """Status of a PRD generation job"""
    job_id: str
    status: str  # pending, processing, completed, failed
    created_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None
    artifacts: Optional[Dict[str, str]] = None

class UserStory(BaseModel):
    """User story model"""
    id: int
    persona: str
    user_story: str
    acceptance_criteria: List[str]

class GenerationResponse(BaseModel):
    """Response after submitting a generation request"""
    job_id: str
    status: str
    message: str
    artifacts_url: str

# In-memory job storage (in production, use Redis or database)
jobs: Dict[str, JobStatus] = {}


# Health Check Endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - returns API information"""
    return {
        "service": "AutoGen PRD Generation API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "generate": "POST /api/v1/generate",
            "status": "GET /api/v1/jobs/{job_id}",
            "artifacts": "GET /api/v1/artifacts/{job_id}/{artifact_type}"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "active_jobs": len([j for j in jobs.values() if j.status == "processing"])
    }


# Main Generation Endpoint
@app.post("/api/v1/generate", response_model=GenerationResponse, tags=["Generation"])
async def generate_prd(
    problem: BusinessProblem,
    background_tasks: BackgroundTasks
):
    """
    Generate PRD artifacts from a business problem.
    
    This endpoint:
    1. Accepts a business problem statement
    2. Creates a background job to run the AutoGen agents
    3. Returns a job ID to check status and retrieve artifacts
    
    The generation process takes 5-10 minutes.
    """
    # Create job
    job_id = str(uuid.uuid4())
    job = JobStatus(
        job_id=job_id,
        status="pending",
        created_at=datetime.utcnow().isoformat()
    )
    jobs[job_id] = job
    
    # Add background task
    background_tasks.add_task(
        run_autogen_workflow,
        job_id,
        problem.problem_statement,
        problem.project_name
    )
    
    return GenerationResponse(
        job_id=job_id,
        status="pending",
        message="PRD generation started. Check status at /api/v1/jobs/{job_id}",
        artifacts_url=f"/api/v1/artifacts/{job_id}"
    )


@app.get("/api/v1/jobs/{job_id}", response_model=JobStatus, tags=["Jobs"])
async def get_job_status(job_id: str):
    """
    Get the status of a PRD generation job.
    
    Returns current status and links to artifacts when complete.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]


@app.get("/api/v1/jobs", tags=["Jobs"])
async def list_jobs():
    """List all jobs (for admin/debugging)"""
    return {
        "total_jobs": len(jobs),
        "jobs": list(jobs.values())
    }


@app.get("/api/v1/artifacts/{job_id}", tags=["Artifacts"])
async def get_artifacts(job_id: str):
    """
    Get all artifacts for a completed job.
    
    Returns links to download each artifact type.
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(
            status_code=400, 
            detail=f"Job status is '{job.status}'. Artifacts only available when status is 'completed'."
        )
    
    return {
        "job_id": job_id,
        "artifacts": job.artifacts,
        "download_urls": {
            "user_stories": f"/api/v1/artifacts/{job_id}/user_stories",
            "prd": f"/api/v1/artifacts/{job_id}/prd",
            "schema": f"/api/v1/artifacts/{job_id}/schema"
        }
    }


@app.get("/api/v1/artifacts/{job_id}/{artifact_type}", tags=["Artifacts"])
async def download_artifact(job_id: str, artifact_type: str):
    """
    Download a specific artifact.
    
    Available types: user_stories, prd, schema
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Artifacts not ready yet")
    
    if not job.artifacts or artifact_type not in job.artifacts:
        raise HTTPException(status_code=404, detail=f"Artifact '{artifact_type}' not found")
    
    file_path = job.artifacts[artifact_type]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Artifact file not found on disk")
    
    # Determine media type
    media_types = {
        "user_stories": "application/json",
        "prd": "text/markdown",
        "schema": "application/sql"
    }
    
    return FileResponse(
        path=file_path,
        media_type=media_types.get(artifact_type, "text/plain"),
        filename=os.path.basename(file_path)
    )


# Background task to run AutoGen workflow
async def run_autogen_workflow(job_id: str, problem_statement: str, project_name: Optional[str]):
    """
    Background task that runs the AutoGen multi-agent workflow.
    
    This is a simplified version - in production, you'd import and run
    the actual AutoGen agents from autogen_prd_system.ipynb
    """
    try:
        # Update status
        jobs[job_id].status = "processing"
        
        # Simulate workflow (replace with actual AutoGen calls)
        import time
        time.sleep(2)  # Simulate processing
        
        # In production, you would:
        # 1. Import the AutoGen setup from autogen_prd_system
        # 2. Run the three workflows
        # 3. Capture the generated artifacts
        
        # For now, create placeholder artifacts
        artifact_dir = os.path.join(project_root, "artifacts", f"job_{job_id}")
        os.makedirs(artifact_dir, exist_ok=True)
        
        # Placeholder artifacts
        user_stories_path = os.path.join(artifact_dir, "user_stories.json")
        prd_path = os.path.join(artifact_dir, "prd.md")
        schema_path = os.path.join(artifact_dir, "schema.sql")
        
        # Create placeholder content
        user_stories_content = json.dumps([
            {
                "id": 1,
                "persona": "New Hire",
                "user_story": f"As a new hire, I want {problem_statement}",
                "acceptance_criteria": ["Given I am a new hire", "When I access the system", "Then I can complete onboarding"]
            }
        ], indent=2)
        
        prd_content = f"# Product Requirements Document\n\n## Problem Statement\n{problem_statement}\n\n## Generated by AutoGen"
        schema_content = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);"
        
        # Save artifacts
        with open(user_stories_path, 'w') as f:
            f.write(user_stories_content)
        with open(prd_path, 'w') as f:
            f.write(prd_content)
        with open(schema_path, 'w') as f:
            f.write(schema_content)
        
        # Update job with completion
        jobs[job_id].status = "completed"
        jobs[job_id].completed_at = datetime.utcnow().isoformat()
        jobs[job_id].artifacts = {
            "user_stories": user_stories_path,
            "prd": prd_path,
            "schema": schema_path
        }
        
    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)
        jobs[job_id].completed_at = datetime.utcnow().isoformat()


# Example data endpoint
@app.get("/api/v1/examples", tags=["Examples"])
async def get_examples():
    """Get example business problems to try"""
    return {
        "examples": [
            {
                "name": "Employee Onboarding",
                "problem_statement": "We need a tool to help our company's new hires get up to speed. New employees often feel overwhelmed in their first weeks."
            },
            {
                "name": "Customer Support",
                "problem_statement": "We need a customer support ticketing system that helps our support team manage inquiries efficiently."
            },
            {
                "name": "Project Management",
                "problem_statement": "We need a lightweight project management tool for small teams to track tasks and deadlines."
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AutoGen PRD API Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Alternative docs: http://localhost:8000/redoc")
    uvicorn.run(app, host="0.0.0.0", port=8000)
