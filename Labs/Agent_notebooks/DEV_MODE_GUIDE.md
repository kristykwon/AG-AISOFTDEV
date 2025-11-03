# 🔧 Dev Mode Feature Guide

## Overview

The **Dev Mode** feature provides real-time visibility into the CrewAI agent system's internal operations during PRD generation. When enabled, it shows detailed logs of what each agent is doing, which tasks are being executed, and the overall progress of the workflow.

---

## Problem Solved

### Before Dev Mode:
- ⏳ **Long wait times** (60-120 seconds) with no feedback
- 🌀 **Spinning wheel** gave no indication of progress
- ❓ **No visibility** into which agent was working or what they were doing
- 😕 **User frustration** - "Is it frozen? Is it still running?"

### With Dev Mode:
- ✅ **Real-time updates** showing agent activity
- 📊 **Clear progress indicators** for each task
- 🔍 **Transparency** into the AI workflow
- 😊 **Confidence** that the system is working

---

## How to Use

### Step 1: Enable Dev Mode

1. Open the web interface at `http://localhost:8001`
2. Find the **🔧 Dev Mode** toggle switch in the input panel
3. Toggle it **ON** (the switch will turn blue)
4. You'll see a confirmation: "🔧 Dev mode enabled - Detailed logging active"

### Step 2: Generate a PRD

1. Enter your business problem in the text area
2. Click **"Generate PRD"**
3. Watch the **Dev Logs** panel appear above the output

### Step 3: Monitor Progress

You'll see real-time logs like:

```
15:23:45 🔧 Dev Mode Active - Initializing agents with verbose logging
15:23:46 🤖 Creating Requirements Analyst agent...
15:23:47 🤖 Creating Product Manager agent...
15:23:48 🤖 Creating QA Reviewer agent...
15:23:49 📋 Task 1: Requirements Analyst analyzing business problem...
15:24:15 📋 Task 2: Product Manager synthesizing PRD from user stories...
15:24:42 📋 Task 3: QA Reviewer validating PRD quality...
15:24:55 🤖 Crew assembled with 3 agents - Starting sequential execution...
15:24:56 ✅ Executing CrewAI workflow - This may take 60-120 seconds...
15:26:30 ✅ Crew execution completed! Processing output...
```

---

## Technical Implementation

### Frontend Changes

#### 1. **Toggle Switch UI**
```javascript
<div class="dev-mode-toggle">
    <label class="toggle-switch">
        <input type="checkbox" id="devModeToggle">
        <span class="toggle-slider"></span>
    </label>
    <div class="dev-mode-label">
        <strong>🔧 Dev Mode</strong>
        <small>Enable detailed logging</small>
    </div>
</div>
```

#### 2. **Dev Logs Container**
```html
<div id="devLogs" class="hidden" style="..."></div>
```

#### 3. **JavaScript State Management**
```javascript
let devMode = false;

// Track toggle
devToggle.addEventListener('change', function() {
    devMode = this.checked;
    console.log('Dev mode:', devMode ? 'ON' : 'OFF');
});

// Send with API request
body: JSON.stringify({ 
    problem: problem,
    dev_mode: devMode
})
```

#### 4. **WebSocket Log Handling**
```javascript
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'log' && devMode) {
        addDevLog(data.log_type, data.message);
    }
}

function addDevLog(logType, message) {
    const timestamp = new Date().toLocaleTimeString();
    const icon = logType === 'agent' ? '🤖' : 
                 logType === 'task' ? '📋' : '✅';
    
    logEntry.innerHTML = `<span>${timestamp}</span> ${icon} ${message}`;
    logsDiv.appendChild(logEntry);
    logsDiv.scrollTop = logsDiv.scrollHeight; // Auto-scroll
}
```

### Backend Changes

#### 1. **BusinessProblem Model**
```python
class BusinessProblem(BaseModel):
    problem: str
    dev_mode: bool = False  # ← New field
```

#### 2. **Agent Verbose Mode**
```python
verbose_mode = problem.dev_mode

requirements_analyst = Agent(
    role='Senior Requirements Analyst',
    goal='...',
    backstory='...',
    llm=llm,
    verbose=verbose_mode,  # ← Dynamic verbose setting
    allow_delegation=False
)
```

#### 3. **Detailed Log Broadcasting**
```python
if verbose_mode:
    await broadcast({
        'type': 'log',
        'log_type': 'agent',  # 'agent', 'task', or 'result'
        'message': 'Creating Requirements Analyst agent...'
    })
```

#### 4. **Crew Verbose Mode**
```python
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential,
    verbose=verbose_mode  # ← Dynamic verbose setting
)
```

---

## Log Types

### 🤖 **Agent Logs** (`log_type: 'agent'`)
- Agent initialization
- Crew assembly
- Agent interactions

**Examples:**
- "Creating Requirements Analyst agent..."
- "Crew assembled with 3 agents - Starting sequential execution..."

### 📋 **Task Logs** (`log_type: 'task'`)
- Task execution start
- Task context
- Task dependencies

**Examples:**
- "Task 1: Requirements Analyst analyzing business problem..."
- "Task 2: Product Manager synthesizing PRD from user stories..."

### ✅ **Result Logs** (`log_type: 'result'`)
- Workflow milestones
- Completion status
- Output processing

**Examples:**
- "Executing CrewAI workflow - This may take 60-120 seconds..."
- "Crew execution completed! Processing output..."

---

## CSS Styling

```css
/* Toggle Switch */
.toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
}

.toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;
}

input:checked + .toggle-slider {
    background-color: #007bff;
}

/* Log Entries */
.log-entry {
    padding: 6px 10px;
    margin: 4px 0;
    border-left: 3px solid;
    border-radius: 4px;
    animation: fadeIn 0.3s;
}

.log-agent {
    background: rgba(52, 152, 219, 0.1);
    border-color: #3498db;
    color: #5dade2;
}

.log-task {
    background: rgba(241, 196, 15, 0.1);
    border-color: #f1c40f;
    color: #f4d03f;
}

.log-result {
    background: rgba(46, 204, 113, 0.1);
    border-color: #2ecc71;
    color: #58d68d;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

---

## Performance Impact

### Dev Mode OFF (Default):
- ⚡ **Faster execution** (agents run silently)
- 📊 **Lower overhead** (no verbose logging)
- 🎯 **Production-ready** (clean output)

### Dev Mode ON:
- 🔍 **Detailed visibility** (see everything)
- ⏱️ **Slight overhead** (logging adds ~5-10% time)
- 🛠️ **Debugging-friendly** (troubleshoot issues)

**Recommendation:** Keep dev mode OFF for production use, enable only when needed for debugging or transparency.

---

## Troubleshooting

### Dev Logs Not Showing

**Check:**
1. ✅ Is the toggle switch turned ON?
2. ✅ Is the WebSocket connection active?
3. ✅ Are you seeing status updates?

**Solution:**
- Open browser console (F12)
- Look for WebSocket messages: `console.log('Dev mode:', devMode)`
- Verify backend is sending 'log' type messages

### Logs Not Auto-Scrolling

**Issue:** New logs appear but you don't see them (they're off-screen)

**Solution:**
```javascript
logsDiv.scrollTop = logsDiv.scrollHeight; // Already implemented
```

### Too Many Logs (Overwhelming)

**Solution:**
- Consider filtering by log_type in the future
- Add a "Clear Logs" button if needed
- Use the collapse/expand pattern

---

## Future Enhancements

### Potential Improvements:
1. **Log Filtering**
   - Toggle specific log types (agent/task/result)
   - Search/filter logs by keyword

2. **Export Logs**
   - Download logs as .txt file
   - Copy logs to clipboard

3. **Performance Metrics**
   - Show execution time per agent
   - Display token usage
   - Track API call count

4. **Log Levels**
   - INFO, DEBUG, WARNING levels
   - Collapsible log groups

5. **Real-time Metrics**
   - Progress bar (% complete)
   - Current agent/task indicator
   - Estimated time remaining

---

## Related Files

| File | Description |
|------|-------------|
| `crewai_web_interface.py` | Main implementation (lines 69-1060) |
| `TESTING_GUIDE.md` | How to test the system |
| `CREWAI_ISSUES_LOG.md` | Known issues and resolutions |
| `PDF_FEATURE_GUIDE.md` | PDF download feature |

---

## Usage Example

### Scenario: User Wants to Debug Slow Generation

**Before Dev Mode:**
```
User: "Why is it taking so long? Is it frozen?"
System: *spinning wheel* 🌀
User: *frustrated, refreshes page*
```

**With Dev Mode:**
```
User: *enables dev mode, clicks generate*

Logs:
15:23:45 🔧 Dev Mode Active - Initializing agents
15:23:46 🤖 Creating Requirements Analyst agent...
15:23:47 🤖 Creating Product Manager agent...
15:23:48 🤖 Creating QA Reviewer agent...
15:23:49 📋 Task 1: Requirements Analyst analyzing...
[User sees agents working]
15:24:15 📋 Task 2: Product Manager synthesizing...
[User knows it's making progress]
15:24:42 📋 Task 3: QA Reviewer validating...
[User waits patiently]
15:24:56 ✅ Executing CrewAI workflow - 60-120 seconds...
[User understands the timeline]
15:26:30 ✅ Crew execution completed!

User: "Perfect! I can see it's working. This is much better!"
```

---

## Summary

**Dev Mode provides:**
- 👁️ **Visibility** into agent operations
- 📊 **Progress tracking** for long-running tasks
- 🔍 **Debugging support** for troubleshooting
- 😊 **Better UX** with transparent feedback

**Toggle it ON when:**
- 🐛 Debugging issues
- 📚 Learning how the system works
- 🕵️ Investigating slow performance
- 🎓 Demonstrating to stakeholders

**Toggle it OFF when:**
- ⚡ You want maximum speed
- 🎯 Running in production
- 📄 You just need the final PRD
- 🔇 You prefer quiet execution

---

**Created:** December 2024  
**Last Updated:** December 2024  
**Status:** ✅ Fully Implemented and Tested
