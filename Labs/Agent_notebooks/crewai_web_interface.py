"""
Web Interface for CrewAI Agent System

This creates a simple web interface where you can:
1. Enter your business problem
2. Watch the AI agents work in real-time
3. Download the generated PRD

Usage:
    python crewai_web_interface.py
    Then open: http://localhost:8001
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import markdown
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from html.parser import HTMLParser

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv()

# Check for API keys
openai_key = os.getenv("OPENAI_API_KEY", "")
google_key = os.getenv("GOOGLE_API_KEY", "")

if not openai_key and not google_key:
    print("❌ ERROR: No API keys found!")
    print("\nPlease add one of these to your .env file:")
    print("  OPENAI_API_KEY=sk-your_key_here")
    print("  GOOGLE_API_KEY=your_key_here")
    sys.exit(1)

# Validate OpenAI key format if provided (support service account keys too)
if openai_key and not (openai_key.startswith("sk-proj-") or openai_key.startswith("sk-svcacct-") or (openai_key.startswith("sk-") and len(openai_key) > 20)):
    print("⚠️  WARNING: OpenAI API key format not recognized, will use Google API instead")
    if not google_key:
        print("❌ ERROR: Invalid OpenAI key and no Google API key found!")
        sys.exit(1)

app = FastAPI(title="CrewAI Agent System")

# Store for WebSocket connections
connections = []

# Store generated PRD content for download
last_generated_prd = {"content": "", "timestamp": None}

class BusinessProblem(BaseModel):
    problem: str
    dev_mode: bool = False

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the web interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CrewAI Agent System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .input-panel, .output-panel {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        
        .panel-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .icon {
            font-size: 1.3em;
        }
        
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .examples {
            margin: 20px 0;
        }
        
        .example-title {
            font-weight: 600;
            color: #555;
            margin-bottom: 10px;
        }
        
        .example-buttons {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .example-btn {
            background: #f5f5f5;
            border: 2px solid #e0e0e0;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
            text-align: left;
            transition: all 0.3s;
            font-size: 0.95em;
        }
        
        .example-btn:hover {
            background: #667eea;
            color: white;
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .generate-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            margin-top: 15px;
        }
        
        .generate-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .output-content {
            background: #f9f9f9;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .status {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
            font-weight: 500;
        }
        
        .status.working {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .loading {
            display: inline-block;
            width: 12px;
            height: 12px;
            border: 2px solid #856404;
            border-top-color: transparent;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 8px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .download-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e0e0e0;
        }
        
        .download-btn {
            width: 100%;
            padding: 12px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .download-btn:hover {
            background: #218838;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
        }
        
        .dev-mode-toggle {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 15px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #dee2e6;
        }
        
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 24px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.4s;
            border-radius: 24px;
        }
        
        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: 0.4s;
            border-radius: 50%;
        }
        
        input:checked + .toggle-slider {
            background-color: #667eea;
        }
        
        input:checked + .toggle-slider:before {
            transform: translateX(26px);
        }
        
        .dev-mode-label {
            font-weight: 600;
            color: #495057;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .dev-mode-info {
            font-size: 0.85em;
            color: #6c757d;
            margin-left: auto;
        }
        
        .log-entry {
            padding: 8px 12px;
            margin: 5px 0;
            background: #f8f9fa;
            border-left: 3px solid #667eea;
            border-radius: 4px;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }
        
        .log-entry.agent {
            border-left-color: #28a745;
        }
        
        .log-entry.task {
            border-left-color: #ffc107;
        }
        
        .log-entry.result {
            border-left-color: #17a2b8;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CrewAI Agent System</h1>
            <p>Transform business ideas into professional PRDs with AI agents</p>
        </div>
        
        <div class="main-content">
            <div class="input-panel">
                <div class="panel-title">
                    <span class="icon">💡</span>
                    <span>Your Business Problem</span>
                </div>
                
                <textarea id="businessProblem" placeholder="Describe your business problem here...

Example: We need a tool to help our company's new hires get up to speed. New employees often feel overwhelmed in their first weeks..."></textarea>
                
                <div class="examples">
                    <div class="example-title">📋 Try these examples:</div>
                    <div class="example-buttons">
                        <button class="example-btn" onclick="setExample(0)">🏢 Employee task assignment based on skills</button>
                        <button class="example-btn" onclick="setExample(1)">💰 Automated expense tracking and approval</button>
                        <button class="example-btn" onclick="setExample(2)">📊 Customer feedback analysis dashboard</button>
                        <button class="example-btn" onclick="setExample(3)">🔔 Real-time notification system for teams</button>
                    </div>
                </div>
                
                <div class="dev-mode-toggle">
                    <label class="toggle-switch">
                        <input type="checkbox" id="devModeToggle">
                        <span class="toggle-slider"></span>
                    </label>
                    <span class="dev-mode-label">
                        🔧 Dev Mode
                    </span>
                    <span class="dev-mode-info">Enable detailed logging</span>
                </div>
                
                <button class="generate-btn" id="generateBtn" onclick="generatePRD()">
                    🚀 Generate PRD with AI Agents
                </button>
            </div>
            
            <div class="output-panel">
                <div class="panel-title">
                    <span class="icon">📄</span>
                    <span>Generated PRD</span>
                </div>
                
                <div id="status"></div>
                
                <!-- Dev Mode Logs -->
                <div id="devLogs" class="hidden" style="background: #1e1e1e; padding: 15px; margin: 10px 0; border-radius: 8px; max-height: 300px; overflow-y: auto; font-family: 'Courier New', monospace; font-size: 12px;"></div>
                
                <div id="output" class="output-content">Waiting for input...</div>
                
                <div class="download-section" id="downloadSection" style="display: none;">
                    <button class="download-btn" onclick="downloadPRD()" style="margin-bottom: 10px;">
                        ⬇️ Download PRD as Markdown
                    </button>
                    <button class="download-btn" onclick="downloadPDF()" style="background: #dc3545;">
                        📄 Download PRD as PDF
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const examples = [
            "We need a system that automatically assigns tasks to employees based on their skills, availability, and current workload. Managers should be able to create tasks with required skills, deadlines, and priorities. The system should suggest the best employee for each task and track completion rates.",
            "Our company needs to streamline expense reporting. Employees submit receipts manually and wait weeks for approval. We want a mobile app where employees can photograph receipts, categorize expenses, and submit reports. Managers should get instant notifications and be able to approve/reject with one click.",
            "We receive customer feedback through multiple channels: email, social media, support tickets, and surveys. We need a centralized dashboard that aggregates all feedback, uses sentiment analysis to prioritize issues, identifies trends, and generates actionable insights for product improvement.",
            "Our distributed teams miss important updates because we use too many communication channels. We need a smart notification system that consolidates alerts from Slack, email, project management tools, and calendars. Users should be able to set preferences for what notifications they receive and how urgently."
        ];
        
        let ws;
        let generatedPRD = '';
        let devMode = false;
        
        function setExample(index) {
            document.getElementById('businessProblem').value = examples[index];
        }
        
        // Track dev mode toggle
        document.addEventListener('DOMContentLoaded', function() {
            const devToggle = document.getElementById('devModeToggle');
            devToggle.addEventListener('change', function() {
                devMode = this.checked;
                console.log('Dev mode:', devMode ? 'ON' : 'OFF');
                if (devMode) {
                    updateStatus('success', '🔧 Dev mode enabled - Detailed logging active');
                }
            });
        });
        
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'status') {
                    updateStatus(data.status, data.message);
                } else if (data.type === 'log' && devMode) {
                    // Display detailed logs when dev mode is enabled
                    addDevLog(data.log_type, data.message);
                } else if (data.type === 'prd') {
                    displayPRD(data.content);
                    generatedPRD = data.content;
                } else if (data.type === 'error') {
                    updateStatus('error', data.message);
                    document.getElementById('generateBtn').disabled = false;
                }
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        }
        
        function addDevLog(logType, message) {
            const logsDiv = document.getElementById('devLogs');
            if (!logsDiv) return;
            
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${logType}`;
            
            const timestamp = new Date().toLocaleTimeString();
            const icon = logType === 'agent' ? '🤖' : logType === 'task' ? '📋' : '✅';
            
            logEntry.innerHTML = `<span class="log-timestamp">${timestamp}</span> ${icon} ${message}`;
            logsDiv.appendChild(logEntry);
            logsDiv.scrollTop = logsDiv.scrollHeight; // Auto-scroll to bottom
        }
        
        function updateStatus(status, message) {
            const statusDiv = document.getElementById('status');
            statusDiv.className = `status ${status}`;
            
            if (status === 'working') {
                statusDiv.innerHTML = `<span class="loading"></span>${message}`;
            } else {
                statusDiv.textContent = message;
            }
        }
        
        function displayPRD(content) {
            document.getElementById('output').textContent = content;
            document.getElementById('downloadSection').style.display = 'block';
            document.getElementById('generateBtn').disabled = false;
            updateStatus('success', '✅ PRD generated successfully!');
        }
        
        async function generatePRD() {
            const problem = document.getElementById('businessProblem').value.trim();
            
            if (!problem) {
                alert('Please enter a business problem first!');
                return;
            }
            
            document.getElementById('generateBtn').disabled = true;
            document.getElementById('output').textContent = '';
            document.getElementById('downloadSection').style.display = 'none';
            generatedPRD = '';
            
            // Clear previous logs if dev mode is on
            if (devMode) {
                const logsDiv = document.getElementById('devLogs');
                if (logsDiv) {
                    logsDiv.innerHTML = '';
                    logsDiv.classList.remove('hidden');
                }
            }
            
            updateStatus('working', 'AI agents are analyzing your problem...');
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        problem: problem,
                        dev_mode: devMode
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to generate PRD');
                }
            } catch (error) {
                updateStatus('error', '❌ Error: ' + error.message);
                document.getElementById('generateBtn').disabled = false;
            }
        }
        
        function downloadPRD() {
            if (!generatedPRD) {
                alert('No PRD to download!');
                return;
            }
            
            const blob = new Blob([generatedPRD], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'product_requirements_document.md';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
        
        async function downloadPDF() {
            if (!generatedPRD) {
                alert('No PRD to download!');
                return;
            }
            
            try {
                updateStatus('working', '📄 Generating PDF...');
                const response = await fetch('/download-pdf');
                
                if (!response.ok) {
                    throw new Error('Failed to generate PDF');
                }
                
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'product_requirements_document.pdf';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                updateStatus('success', '✅ PRD generated successfully!');
            } catch (error) {
                updateStatus('error', '❌ Error generating PDF: ' + error.message);
            }
        }
        
        // Connect WebSocket on page load
        connectWebSocket();
    </script>
</body>
</html>
"""

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time updates"""
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove(websocket)

async def broadcast(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    for connection in connections:
        try:
            await connection.send_json(message)
        except:
            pass

@app.post("/generate")
async def generate_prd(problem: BusinessProblem):
    """Generate PRD using CrewAI agents"""
    try:
        # Import CrewAI components
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Configure LLM
        if openai_key:
            llm = ChatOpenAI(
                model='gpt-5',
                temperature=0.5,
                api_key=openai_key,
                base_url='https://api.openai.com/v1'
            )
        else:
            llm = ChatGoogleGenerativeAI(
                model='gemini-2.5-pro',
                temperature=0.5,
                google_api_key=google_key
            )
        
        # Dev mode: enable verbose logging for agents
        verbose_mode = problem.dev_mode
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'agent',
                'message': '🔧 Dev Mode Active - Initializing agents with verbose logging'
            })
        
        await broadcast({
            'type': 'status',
            'status': 'working',
            'message': '🔍 Requirements Analyst is analyzing your problem...'
        })
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'agent',
                'message': 'Creating Requirements Analyst agent...'
            })
        
        # Create agents
        requirements_analyst = Agent(
            role='Senior Requirements Analyst',
            goal='Analyze business problems and extract comprehensive user stories',
            backstory="""You are an experienced requirements analyst with 10+ years in software development.
            You excel at understanding business needs and translating them into structured user stories.""",
            llm=llm,
            verbose=verbose_mode,
            allow_delegation=False
        )
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'agent',
                'message': 'Creating Product Manager agent...'
            })
        
        product_manager = Agent(
            role='Senior Product Manager',
            goal='Create comprehensive PRDs from user stories',
            backstory="""You are a seasoned product manager who has launched multiple successful products.
            You synthesize requirements into clear, actionable PRDs.""",
            llm=llm,
            verbose=verbose_mode,
            allow_delegation=False
        )
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'agent',
                'message': 'Creating QA Reviewer agent...'
            })
        
        quality_reviewer = Agent(
            role='Senior QA Engineer',
            goal='Validate PRD quality and completeness',
            backstory="""You are a meticulous QA engineer who ensures all deliverables meet quality standards.""",
            llm=llm,
            verbose=verbose_mode,
            allow_delegation=False
        )
        
        # Create tasks
        await broadcast({
            'type': 'status',
            'status': 'working',
            'message': '📝 Generating user stories...'
        })
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'task',
                'message': 'Task 1: Requirements Analyst analyzing business problem...'
            })
        
        task_user_stories = Task(
            description=f"""Analyze this business problem and generate 5-7 user stories:
            
            {problem.problem}
            
            Format: "As a [persona], I want [goal], so that [benefit]"
            Include acceptance criteria for each story.""",
            agent=requirements_analyst,
            expected_output='Detailed user stories with acceptance criteria'
        )
        
        await broadcast({
            'type': 'status',
            'status': 'working',
            'message': '📄 Product Manager is creating the PRD...'
        })
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'task',
                'message': 'Task 2: Product Manager synthesizing PRD from user stories...'
            })
        
        task_generate_prd = Task(
            description="""Create a comprehensive PRD with these sections:
            
            # Product Requirements Document
            
            ## Introduction
            ## User Personas
            ## Features / User Stories
            ## Success Metrics
            ## Out of Scope
            
            Make it professional and production-ready.""",
            agent=product_manager,
            expected_output='Complete PRD in markdown format',
            context=[task_user_stories]
        )
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'task',
                'message': 'Task 3: QA Reviewer validating PRD quality...'
            })
        
        task_review_prd = Task(
            description="""Review the PRD for completeness and quality.
            Ensure all sections are present and well-written.
            Output the final approved PRD.""",
            agent=quality_reviewer,
            expected_output='Final approved PRD',
            context=[task_generate_prd]
        )
        
        # Create and execute crew
        await broadcast({
            'type': 'status',
            'status': 'working',
            'message': '🤖 AI agents are collaborating...'
        })
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'agent',
                'message': 'Crew assembled with 3 agents - Starting sequential execution...'
            })
        
        crew = Crew(
            agents=[requirements_analyst, product_manager, quality_reviewer],
            tasks=[task_user_stories, task_generate_prd, task_review_prd],
            process=Process.sequential,
            verbose=verbose_mode
        )
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'result',
                'message': 'Executing CrewAI workflow - This may take 60-120 seconds...'
            })
        
        # Execute in a thread pool to avoid blocking
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await asyncio.get_event_loop().run_in_executor(
                executor,
                crew.kickoff
            )
        
        if verbose_mode:
            await broadcast({
                'type': 'log',
                'log_type': 'result',
                'message': 'Crew execution completed! Processing output...'
            })
        
        # Extract PRD from result
        prd_content = str(result)
        
        # Clean up the output
        if '```markdown' in prd_content:
            prd_content = prd_content.split('```markdown')[1].split('```')[0].strip()
        elif '```' in prd_content:
            prd_content = prd_content.split('```')[1].split('```')[0].strip()
        
        # Store PRD for download
        last_generated_prd["content"] = prd_content
        last_generated_prd["timestamp"] = datetime.now()
        
        # Send final PRD
        await broadcast({
            'type': 'prd',
            'content': prd_content
        })
        
        return {"status": "success"}
        
    except Exception as e:
        error_message = f"Error generating PRD: {str(e)}"
        await broadcast({
            'type': 'error',
            'message': error_message
        })
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": error_message}
        )

@app.get("/download-pdf")
async def download_pdf():
    """Generate and download PRD as PDF using ReportLab"""
    try:
        if not last_generated_prd["content"]:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "No PRD available to download"}
            )
        
        # Create PDF buffer
        pdf_buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Container for PDF elements
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#764ba2'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        # Add header
        story.append(Paragraph("Product Requirements Document", title_style))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph("Generated by CrewAI Agent System", styles['Normal']))
        story.append(Paragraph(f"Created: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Process markdown content
        lines = last_generated_prd["content"].split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.1*inch))
                continue
            
            # Headers
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, heading1_style))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, heading2_style))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, styles['Heading3']))
            # Bullet points
            elif line.startswith('- ') or line.startswith('* '):
                text = '• ' + line[2:].strip()
                story.append(Paragraph(text, body_style))
            # Numbered lists
            elif line and line[0].isdigit() and '. ' in line:
                story.append(Paragraph(line, body_style))
            # Regular text
            else:
                # Escape special characters for reportlab
                text = line.replace('<', '&lt;').replace('>', '&gt;')
                story.append(Paragraph(text, body_style))
        
        # Add footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(f"Generated by CrewAI Agent System | {datetime.now().year}", footer_style))
        
        # Build PDF
        doc.build(story)
        pdf_buffer.seek(0)
        
        # Return PDF as streaming response
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=PRD_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            }
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Error generating PDF: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🌐 CREWAI AGENT SYSTEM - WEB INTERFACE")
    print("="*80 + "\n")
    print("✅ Starting web server...\n")
    print("🚀 Open your browser and go to:\n")
    print("   👉 http://localhost:8001\n")
    print("="*80 + "\n")
    print("Press CTRL+C to stop the server")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
