# 🌐 AutoGen AI Agent System - Web Interface Guide

## 🎯 Quick Start

The **Web Interface** provides an easy-to-use graphical interface where you can type business problems and watch AI agents work in real-time.

### 🚀 Starting the Web Interface

```powershell
cd Labs\Agent_notebooks
python web_interface.py
```

Then open in your browser:
```
http://localhost:8001
```

---

## 🖥️ Two Ways to Use AutoGen

### 1️⃣ **Web Interface** (Recommended for Interactive Use)
- **Port:** 8001
- **URL:** http://localhost:8001
- **File:** `web_interface.py`
- **Best For:** 
  - Typing prompts directly in a browser
  - Seeing AI agents work in real-time
  - Interactive exploration
  - Visual feedback

### 2️⃣ **REST API** (For Programmatic Access)
- **Port:** 8000
- **URL:** http://localhost:8000
- **File:** `autogen_prd_api.py`
- **Best For:**
  - Integration with other tools
  - Automated workflows
  - Server-to-server communication
  - See: `API_USAGE_GUIDE.md`

---

## ✨ Using the Web Interface

### What You'll See

**Left Panel - Input:**
- Large text box to type your business problem
- "Generate PRD" button to start the AI agents
- "Clear" button to reset
- Quick example prompts you can click

**Right Panel - Output:**
- Real-time conversation between AI agents
- See RequirementsAnalyst, ProductManager, and QualityReviewer work together
- Watch the PRD being created live

### Step-by-Step Usage

1. **Open the interface** at http://localhost:8001

2. **Enter your business problem** in the text box. For example:
   ```
   We need a mobile app to help users track their daily water intake 
   and remind them to stay hydrated throughout the day.
   ```

3. **Click "Generate PRD"** button

4. **Watch the AI agents work:**
   - 🤖 **RequirementsAnalyst** will create user stories
   - 👔 **ProductManager** will build a comprehensive PRD
   - ✅ **QualityReviewer** will review and approve

5. **Get your results** displayed in real-time!

---

## 📝 Example Prompts

Click these in the interface or type similar ones:

### 📱 **Mobile Apps**
```
We need a fitness tracking app that helps users log workouts, 
track progress, and connect with personal trainers.
```

### 🛒 **E-Commerce**
```
Build an e-commerce platform with AI-powered product recommendations 
based on user browsing history and purchase patterns.
```

### 📚 **Education**
```
Create an online learning platform where instructors can upload courses, 
students can track progress, and everyone can participate in discussions.
```

### 🏥 **Healthcare**
```
Develop a healthcare appointment scheduling system that allows patients 
to book appointments, receive reminders, and access medical records.
```

### 💼 **Business Tools**
```
We need a project management tool that helps teams collaborate, 
track tasks, and manage deadlines efficiently.
```

---

## 🎨 Interface Features

### Visual Feedback
- **Status Indicator:** Green dot pulses when agents are active
- **Agent Messages:** Color-coded by agent type
- **Real-time Updates:** See conversation as it happens
- **Smooth Animations:** Messages slide in smoothly

### Message Types
- 🔵 **Blue boxes** = System messages
- 🟣 **Purple boxes** = Agent conversations
- 🟢 **Green boxes** = Success messages
- 🔴 **Red boxes** = Error messages

---

## 🔧 Technical Details

### Requirements
- Python 3.8+
- AutoGen 0.2.35
- FastAPI
- uvicorn
- websockets
- OpenAI API key OR Google API key

### Configuration
- API keys loaded from `.env` file
- Automatic model selection (OpenAI GPT-4o-mini or Google Gemini)
- WebSocket connection for real-time updates

### Port Configuration
- **Default Web Interface Port:** 8001
- **Why 8001?** Port 8000 is used by your existing onboarding API
- To change port: Edit `web_interface.py` line with `uvicorn.run(..., port=8001)`

---

## 🚨 Troubleshooting

### "Can't type anything / See only JSON"
- **Problem:** Wrong port - you're viewing port 8000 (the REST API)
- **Solution:** Go to http://localhost:8001 (the web interface)

### "Connection Error"
- **Problem:** Web server not running
- **Solution:** 
  ```powershell
  cd Labs\Agent_notebooks
  python web_interface.py
  ```

### "API Key Error"
- **Problem:** No API keys configured
- **Solution:** Add to your `.env` file:
  ```
  OPENAI_API_KEY=your_key_here
  # OR
  GOOGLE_API_KEY=your_key_here
  ```

### "Page Not Loading"
- **Problem:** Port conflict or server not started
- **Solution:** Check terminal for error messages, try a different port

---

## 💡 Tips

1. **Start Simple:** Try the example prompts first
2. **Be Specific:** More detailed problems get better results
3. **Watch the Process:** The AI agents teach you how they think
4. **Experiment:** Try different types of business problems
5. **Full Output:** Check terminal for complete conversation logs

---

## 🎯 Next Steps

After using the web interface:

1. **Check the notebook** (`autogen_prd_system.ipynb`) for the full workflow
2. **Explore the API** (`autogen_prd_api.py`) for programmatic access
3. **Read documentation** (`README_AUTOGEN_PRD_SYSTEM.md`) for details
4. **Customize agents** to fit your specific needs

---

## 📊 Comparison: Web Interface vs API vs Notebook

| Feature | Web Interface | REST API | Notebook |
|---------|---------------|----------|----------|
| **URL** | http://localhost:8001 | http://localhost:8000 | N/A |
| **Input Method** | Browser text box | HTTP requests | Python code |
| **Real-time View** | ✅ Yes | ❌ No | ✅ Yes |
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Integration** | ❌ No | ✅ Yes | ❌ No |
| **Best For** | Quick testing | Automation | Development |

---

## 🎉 Enjoy!

You now have a beautiful, interactive way to use your AutoGen AI Agent System!

**Questions or issues?** Check the main documentation at `README_AUTOGEN_PRD_SYSTEM.md`
