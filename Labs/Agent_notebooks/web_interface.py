"""
Web Interface for AutoGen AI Agent System

This creates a simple web interface where you can:
1. Enter your business problem
2. Watch the AI agents work in real-time
3. Download the generated artifacts

Usage:
    python web_interface.py
    Then open: http://localhost:8000
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
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

app = FastAPI(title="AutoGen AI Agent System")

# Store for WebSocket connections
connections = []

class BusinessProblem(BaseModel):
    problem: str

@app.get("/", response_class=HTMLResponse)
async def get_home():
    """Serve the web interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AutoGen AI Agent System</title>
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
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        button {
            flex: 1;
            padding: 15px 30px;
            font-size: 1.1em;
            font-weight: 600;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .btn-download {
            background: #4caf50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            margin-top: 15px;
            width: 100%;
            transition: all 0.3s;
        }
        
        .btn-download:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
        }
        
        .download-section {
            margin-top: 20px;
            padding: 15px;
            background: #e8f5e9;
            border-radius: 10px;
            border-left: 4px solid #4caf50;
            display: none;
        }
        
        .output-container {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        .message {
            margin-bottom: 15px;
            padding: 12px;
            border-radius: 8px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message-system {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
        }
        
        .message-agent {
            background: #f3e5f5;
            border-left: 4px solid #9c27b0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .message-agent code {
            background: white;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        .message-agent pre {
            background: white;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .message-success {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }
        
        .message-error {
            background: #ffebee;
            border-left: 4px solid #f44336;
        }
        
        .agent-name {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .status-bar {
            background: white;
            padding: 15px 25px;
            border-radius: 10px;
            margin-top: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #4caf50;
            animation: pulse 2s infinite;
        }
        
        .status-dot.inactive {
            background: #ccc;
            animation: none;
        }
        
        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }
        
        .examples {
            margin-top: 15px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .examples h4 {
            color: #666;
            margin-bottom: 10px;
            font-size: 0.9em;
        }
        
        .example-item {
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.9em;
        }
        
        .example-item:hover {
            background: #667eea;
            color: white;
            transform: translateX(5px);
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
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
            <h1>🤖 AutoGen AI Agent System</h1>
            <p>Transform your business ideas into comprehensive Product Requirement Documents</p>
        </div>
        
        <div class="main-content">
            <div class="input-panel">
                <div class="panel-title">
                    <span class="icon">💭</span>
                    <span>Your Business Problem</span>
                </div>
                <textarea id="businessProblem" placeholder="Describe your business problem or idea here...

Example: We need a mobile app to help users track their daily water intake and remind them to stay hydrated throughout the day."></textarea>
                
                <div class="button-group">
                    <button id="generateBtn" class="btn-primary" onclick="generatePRD()">
                        ✨ Generate PRD
                    </button>
                    <button class="btn-secondary" onclick="clearOutput()">
                        🗑️ Clear
                    </button>
                </div>
                
                <div class="examples">
                    <h4>💡 Quick Examples (click to use):</h4>
                    <div class="example-item" onclick="useExample(0)">
                        🏢 Employee task assignment based on skills
                    </div>
                    <div class="example-item" onclick="useExample(1)">
                        � Automated expense tracking and approval
                    </div>
                    <div class="example-item" onclick="useExample(2)">
                        � Customer feedback analysis dashboard
                    </div>
                    <div class="example-item" onclick="useExample(3)">
                        🔔 Real-time notification system for teams
                    </div>
                </div>
            </div>
            
            <div class="output-panel">
                <div class="panel-title">
                    <span class="icon">📄</span>
                    <span>Generated PRD</span>
                </div>
                <div id="output" class="output-container">
                    <div class="message message-system">
                        <strong>Ready to Generate</strong><br>
                        Enter your business problem and click "Generate PRD" to create your Product Requirements Document!
                    </div>
                </div>
                <div id="downloadSection" class="download-section">
                    <strong>📥 Download Your PRD</strong>
                    <button id="downloadBtn" class="btn-download" onclick="downloadPRD()">
                        💾 Download PRD as Markdown
                    </button>
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            <div class="status-indicator">
                <div id="statusDot" class="status-dot inactive"></div>
                <span id="statusText">Ready</span>
            </div>
            <div>
                <span id="agentCount">0 agents active</span>
            </div>
        </div>
    </div>
    
    <script>
        const examples = [
            "We need a system that automatically assigns employees to tasks based on their skills, experience, and current workload to optimize team productivity.",
            "Build an automated expense tracking and approval system where employees can submit expenses, managers can review and approve them, and finance can process payments efficiently.",
            "Create a customer feedback analysis dashboard that collects reviews from multiple channels, analyzes sentiment, identifies trends, and generates actionable insights for product improvements.",
            "Develop a real-time notification system that keeps team members informed about project updates, deadlines, and important announcements across multiple communication channels."
        ];
        
        let ws = null;
        let generatedPRD = null;
        
        function useExample(index) {
            document.getElementById('businessProblem').value = examples[index];
        }
        
        function clearOutput() {
            document.getElementById('output').innerHTML = '<div class="message message-system"><strong>Ready to Generate</strong><br>Enter your business problem and click "Generate PRD" to create your Product Requirements Document!</div>';
            document.getElementById('downloadSection').style.display = 'none';
            generatedPRD = null;
            setStatus('Ready', false);
        }
        
        function downloadPRD() {
            if (!generatedPRD) {
                alert('No PRD available to download. Please generate a PRD first.');
                return;
            }
            
            // Create a blob with the PRD content
            const blob = new Blob([generatedPRD], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            
            // Create a temporary download link
            const a = document.createElement('a');
            a.href = url;
            a.download = 'product_requirements_document.md';
            document.body.appendChild(a);
            a.click();
            
            // Clean up
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        
        function setStatus(text, active) {
            document.getElementById('statusText').textContent = text;
            const dot = document.getElementById('statusDot');
            if (active) {
                dot.classList.remove('inactive');
            } else {
                dot.classList.add('inactive');
            }
        }
        
        function addMessage(content, type = 'system') {
            const output = document.getElementById('output');
            const message = document.createElement('div');
            message.className = `message message-${type}`;
            message.innerHTML = content;
            output.appendChild(message);
            output.scrollTop = output.scrollHeight;
        }
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'agent_message') {
                    // Only show ProductManager's PRD (hide other agent conversations)
                    if (data.agent === 'ProductManager' && data.content.includes('# Product Requirements Document')) {
                        // Clear previous content and show only the PRD
                        document.getElementById('output').innerHTML = '';
                        addMessage(`<div style="white-space: pre-wrap; line-height: 1.6;">${data.content}</div>`, 'agent');
                        
                        // Store the PRD for download
                        generatedPRD = data.content;
                        console.log('PRD stored for download, length:', generatedPRD.length);
                    }
                } else if (data.type === 'status') {
                    // Show status updates
                    if (data.content.includes('Starting') || data.content.includes('Using')) {
                        addMessage(`<strong>${data.content}</strong>`, 'system');
                    }
                } else if (data.type === 'success') {
                    addMessage(`<strong>✅ ${data.content}</strong>`, 'success');
                    setStatus('Complete', false);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').innerHTML = '✨ Generate PRD';
                    
                    // Show download section
                    console.log('Success received, generatedPRD:', generatedPRD ? 'exists' : 'null');
                    const downloadSection = document.getElementById('downloadSection');
                    if (downloadSection && generatedPRD) {
                        console.log('Showing download section');
                        downloadSection.style.display = 'block';
                    } else {
                        console.log('Cannot show download section:', !downloadSection ? 'element not found' : 'no PRD');
                    }
                } else if (data.type === 'error') {
                    addMessage(`<strong>❌ Error:</strong> ${data.content}`, 'error');
                    setStatus('Error', false);
                    document.getElementById('generateBtn').disabled = false;
                    document.getElementById('generateBtn').innerHTML = '✨ Generate PRD';
                }
            };
            
            ws.onerror = function(error) {
                addMessage('<strong>Connection error</strong><br>Please refresh the page.', 'error');
            };
            
            ws.onclose = function() {
                console.log('WebSocket closed');
            };
        }
        
        async function generatePRD() {
            const problem = document.getElementById('businessProblem').value.trim();
            
            if (!problem) {
                alert('Please enter a business problem first!');
                return;
            }
            
            // Disable button and show loading
            const btn = document.getElementById('generateBtn');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner"></span> Generating...';
            
            // Clear output
            document.getElementById('output').innerHTML = '';
            
            // Update status
            setStatus('AI Agents Working...', true);
            document.getElementById('agentCount').textContent = '5 agents active';
            
            // Connect WebSocket
            connectWebSocket();
            
            // Send request
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ problem: problem })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to start generation');
                }
            } catch (error) {
                addMessage(`<strong>❌ Error:</strong> ${error.message}`, 'error');
                setStatus('Error', false);
                btn.disabled = false;
                btn.innerHTML = '✨ Generate PRD';
            }
        }
        
        // Initialize
        window.addEventListener('load', function() {
            console.log('AutoGen AI Agent System loaded');
        });
    </script>
</body>
</html>
    """

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections.remove(websocket)

async def broadcast(message: dict):
    """Send message to all connected clients"""
    for connection in connections[:]:
        try:
            await connection.send_json(message)
        except:
            connections.remove(connection)

@app.post("/api/generate")
async def generate_prd(request: BusinessProblem):
    """Start PRD generation process"""
    
    # Import AutoGen here to avoid startup issues
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    
    # Send initial status
    await broadcast({"type": "status", "content": "🚀 Starting AI Agent System..."})
    
    # Configure LLM - Use OpenAI with service account key
    openai_key = os.getenv("OPENAI_API_KEY", "")
    
    if not openai_key:
        raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY in your .env file")
    
    # Use OpenAI GPT-4o-mini (works with service account keys)
    config_list = [{
        'model': 'gpt-4o-mini',
        'api_key': openai_key,
        'base_url': 'https://api.openai.com/v1',  # Explicitly set base URL
    }]
    model_name = "OpenAI GPT-4o-mini"
    
    await broadcast({"type": "status", "content": f"🤖 Using {model_name}"})
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0.3,
    }
    
    try:
        # Create agents
        await broadcast({"type": "status", "content": "🔧 Assembling AI agent team..."})
        
        analyst = AssistantAgent(
            name="RequirementsAnalyst",
            system_message="""You are a Requirements Analyst. Create 5 detailed user stories 
            in JSON format with: id, title, description, acceptance_criteria, priority.""",
            llm_config=llm_config,
        )
        
        pm = AssistantAgent(
            name="ProductManager",
            system_message="""You are a Product Manager. Review user stories and create a 
            comprehensive PRD with: Overview, Features, User Stories, Success Metrics.""",
            llm_config=llm_config,
        )
        
        reviewer = AssistantAgent(
            name="QualityReviewer",
            system_message="""You are a Quality Reviewer. Review the PRD and either APPROVE 
            it or provide constructive feedback.""",
            llm_config=llm_config,
        )
        
        user_proxy = UserProxyAgent(
            name="Coordinator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper() or "TERMINATE" in x.get("content", ""),
            code_execution_config=False,
        )
        
        await broadcast({"type": "status", "content": "✅ Team assembled: 4 agents ready"})
        
        # Create group chat
        groupchat = GroupChat(
            agents=[user_proxy, analyst, pm, reviewer],
            messages=[],
            max_round=15
        )
        
        manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
        
        await broadcast({"type": "status", "content": "🎬 Starting agent conversation..."})
        
        # Capture messages
        original_messages = groupchat.messages.copy()
        
        # Start the conversation
        user_proxy.initiate_chat(
            manager,
            message=f"""Business Problem: {request.problem}

Step 1: RequirementsAnalyst - Create 5 user stories
Step 2: ProductManager - Create comprehensive PRD
Step 3: QualityReviewer - Review and APPROVE

When approved, respond with TERMINATE."""
        )
        
        # Broadcast only the final PRD (filter out intermediate agent conversations)
        prd_message = None
        for msg in groupchat.messages:
            if msg.get("content") and msg.get("name") == "ProductManager":
                content = msg["content"]
                # Look for the final approved PRD (after revisions)
                if "# Product Requirements Document" in content and len(content) > 1000:
                    prd_message = content
        
        # Send the final PRD
        if prd_message:
            await broadcast({
                "type": "agent_message",
                "agent": "ProductManager",
                "content": prd_message
            })
            await asyncio.sleep(0.2)
        
        # Success - provide summary
        await broadcast({
            "type": "success",
            "content": f"PRD Generation Complete! Click the download button below to save your PRD as a markdown file."
        })
        
        return {
            "status": "success", 
            "message": "PRD generated successfully",
            "message_count": len(groupchat.messages)
        }
        
    except Exception as e:
        await broadcast({"type": "error", "content": str(e)})
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🌐 AUTOGEN AI AGENT SYSTEM - WEB INTERFACE")
    print("="*80)
    print("\n✅ Starting web server...")
    print("\n🚀 Open your browser and go to:")
    print("\n   👉 http://localhost:8001")
    print("\n" + "="*80)
    print("\nPress CTRL+C to stop the server")
    print("="*80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="warning")
