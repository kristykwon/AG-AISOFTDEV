# CrewAI PRD System - Quick Start Guide

Get your PRD generation system running in 5 minutes!

## 🚀 Fast Track

```bash
# 1. Install dependencies (30 seconds)
pip install -r requirements_crewai.txt

# 2. Set up API key (1 minute)
# Create/edit .env file in project root
echo "OPENAI_API_KEY=sk-your_key_here" > .env

# 3. Start web interface (10 seconds)
cd Labs/Agent_notebooks
python crewai_web_interface.py

# 4. Open browser
# Navigate to: http://localhost:8001
```

## ✅ Verification

### Check Installation
```bash
python -c "import crewai; print(f'CrewAI {crewai.__version__} installed!')"
```

Expected output: `CrewAI 0.86.0 installed!`

### Test API Key
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ API key found!' if os.getenv('OPENAI_API_KEY') or os.getenv('GOOGLE_API_KEY') else '✗ No API key')"
```

## 🎯 First PRD Generation

1. **Open the web interface**: http://localhost:8001
2. **Click an example button** (e.g., "Employee task assignment")
3. **Click "Generate PRD"**
4. **Wait 30-60 seconds** for agents to work
5. **Download your PRD** using the green button

## 📁 Where Are My Files?

Generated artifacts are saved to:
```
AG-AISOFTDEV/
└── artifacts/
    ├── crewai_user_stories.json
    ├── crewai_prd.md
    └── crewai_schema.sql
```

## 🔑 API Key Setup Options

### Option 1: .env File (Recommended)
```bash
# In project root: AG-AISOFTDEV/.env
OPENAI_API_KEY=sk-your_key_here
```

### Option 2: Google Gemini
```bash
# In project root: AG-AISOFTDEV/.env
GOOGLE_API_KEY=your_google_key_here
```

### Option 3: Both (Fallback)
```bash
# System uses OpenAI first, falls back to Google
OPENAI_API_KEY=sk-your_key_here
GOOGLE_API_KEY=your_google_key_here
```

## 🐛 Common Issues

### "No module named 'crewai'"
```bash
pip install -r requirements_crewai.txt
```

### "Port 8001 already in use"
```bash
# Windows:
Get-NetTCPConnection -LocalPort 8001 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
python crewai_web_interface.py

# Linux/Mac:
lsof -ti:8001 | xargs kill -9
python crewai_web_interface.py
```

### "No API keys found"
```bash
# Check .env file location (should be in project root)
cat .env  # Linux/Mac
type .env  # Windows

# Verify content
OPENAI_API_KEY=sk-your_key_here
```

### Agents are slow
```bash
# Switch to faster model
# Edit crewai_web_interface.py:
# Change: model='gpt-4o-mini'  # Already default, fastest
```

## 📝 Using the Notebook

If you prefer Jupyter notebooks:

```bash
# 1. Start Jupyter
jupyter notebook

# 2. Open crewai_prd_system.ipynb

# 3. Run all cells (Cell → Run All)

# 4. Check artifacts/ directory for outputs
```

## 🎨 Try Different Business Problems

### Example 1: Task Management
```
We need a system for project managers to assign tasks to team members 
based on their skills and availability. The system should track task 
progress and send reminders for upcoming deadlines.
```

### Example 2: Expense Tracking
```
Our sales team submits expense reports manually. We need an app where 
they can photograph receipts, categorize expenses, and get instant 
manager approval.
```

### Example 3: Customer Feedback
```
We receive customer feedback through email, social media, and support 
tickets. We need a dashboard to centralize all feedback and use AI to 
identify trends and prioritize issues.
```

## 🔄 Workflow Overview

```
Your Business Idea
        ↓
Requirements Analyst → Extract user stories
        ↓
Quality Reviewer → Validate stories
        ↓
Product Manager → Write PRD
        ↓
Quality Reviewer → Validate PRD
        ↓
Technical Architect → Design schema
        ↓
Quality Reviewer → Final review
        ↓
Download PRD! 🎉
```

## 📊 What You Get

### 1. User Stories (JSON)
```json
[
  {
    "id": 1,
    "persona": "New Employee",
    "user_story": "As a new employee, I want to see my onboarding tasks...",
    "acceptance_criteria": ["Given...", "When...", "Then..."]
  }
]
```

### 2. PRD (Markdown)
```markdown
# Product Requirements Document

## Introduction
[Clear problem statement]

## User Personas
[Who will use this system]

## Features / User Stories
[Detailed features]

## Success Metrics
[How we measure success]

## Out of Scope
[What we won't build]
```

### 3. Database Schema (SQL)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    ...
);
```

## ⚡ Performance Tips

1. **Use gpt-4o-mini**: Already configured, fastest OpenAI model
2. **Use gemini-2.0-flash-exp**: Fastest Google model
3. **Fewer user stories**: Request 5 instead of 10 for speed
4. **Close other apps**: Free up system resources

## 🎓 Next Steps

After generating your first PRD:

1. **Review the output** - Check that it meets your needs
2. **Try different problems** - Test with various business ideas
3. **Customize agents** - Edit backstories for different expertise
4. **Add new tasks** - Extend the workflow with additional steps
5. **Explore the notebook** - See detailed agent interactions

## 📚 Documentation

- **Full README**: `README_CREWAI_PRD_SYSTEM.md`
- **Web Interface Guide**: This file!
- **CrewAI Docs**: https://docs.crewai.com/

## 🆘 Still Having Issues?

1. **Check terminal output** for specific error messages
2. **Verify Python version**: Python 3.8+ required
3. **Update pip**: `pip install --upgrade pip`
4. **Reinstall dependencies**: 
   ```bash
   pip uninstall crewai crewai-tools -y
   pip install -r requirements_crewai.txt
   ```

---

**Ready to generate your first PRD?** → http://localhost:8001 🚀
