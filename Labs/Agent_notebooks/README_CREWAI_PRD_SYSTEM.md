# CrewAI PRD Generation System

## Overview

This system uses **CrewAI** to automate the generation of Product Requirement Documents (PRDs) from business ideas. It orchestrates multiple AI agents working together like a real product development team.

## 🎯 What It Does

Transforms vague business ideas into:
1. **Structured User Stories** (JSON format with acceptance criteria)
2. **Professional PRDs** (following standard templates)
3. **Database Schemas** (normalized SQL)
4. **Architectural Decision Records** (ADRs)

## 🤖 The Crew

### 1. Requirements Analyst
- **Role**: Senior Requirements Analyst
- **Goal**: Extract user stories from business problems
- **Output**: JSON array of user stories with acceptance criteria

### 2. Product Manager
- **Role**: Senior Product Manager
- **Goal**: Create comprehensive PRDs
- **Output**: Complete PRD in markdown format

### 3. Technical Architect
- **Role**: Staff Software Engineer
- **Goal**: Design database schemas and document technical decisions
- **Output**: SQL schemas and ADRs

### 4. Quality Reviewer
- **Role**: Senior QA Engineer
- **Goal**: Validate all artifacts for quality
- **Output**: Approved, validated documents

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)

```bash
# 1. Install dependencies
pip install -r requirements_crewai.txt

# 2. Set up your API key in .env file
OPENAI_API_KEY=sk-your_key_here
# OR
GOOGLE_API_KEY=your_key_here

# 3. Start the web interface
python crewai_web_interface.py

# 4. Open your browser
# Go to: http://localhost:8001
```

### Option 2: Jupyter Notebook

```bash
# 1. Install dependencies
pip install -r requirements_crewai.txt

# 2. Open the notebook
jupyter notebook crewai_prd_system.ipynb

# 3. Run all cells
```

## 📋 Requirements

- Python 3.8+
- OpenAI API key OR Google API key
- Dependencies listed in `requirements_crewai.txt`

### Installing Dependencies

```bash
pip install -r requirements_crewai.txt
```

This installs:
- `crewai==0.86.0` - Multi-agent orchestration framework
- `crewai-tools==0.17.0` - Additional tools for agents
- `langchain-openai` - OpenAI integration
- `langchain-google-genai` - Google Gemini integration
- `fastapi` & `uvicorn` - Web interface
- Other supporting libraries

## 🌐 Web Interface Features

- **Interactive Form**: Enter business problems in a text area
- **Example Templates**: Quick-start with pre-written business scenarios
- **Real-time Updates**: Watch agents work via WebSocket
- **Download Button**: Save generated PRD as markdown file
- **Clean Output**: Shows only the final PRD (not agent conversations)

## 📂 Generated Artifacts

All artifacts are saved to the `artifacts/` directory:

```
artifacts/
├── crewai_user_stories.json    # User stories with acceptance criteria
├── crewai_prd.md               # Complete Product Requirements Document
├── crewai_schema.sql           # Database schema
└── crewai_adr_001.md           # Architectural Decision Record (optional)
```

## 🔑 API Keys

### OpenAI (Recommended)
```bash
OPENAI_API_KEY=sk-proj-your_key_here
# OR for service accounts:
OPENAI_API_KEY=sk-svcacct-your_key_here
```

### Google Gemini (Alternative)
```bash
GOOGLE_API_KEY=your_google_key_here
```

The system will use OpenAI if available, otherwise falls back to Google Gemini.

## 💡 Example Business Problems

### 1. Employee Onboarding
```
We need a tool to help our company's new hires get up to speed. 
New employees often feel overwhelmed in their first weeks and don't know 
what tasks to complete or who to talk to. We want to create a system that 
guides them through onboarding, tracks their progress, and helps managers 
monitor completion.
```

### 2. Task Assignment
```
We need a system that automatically assigns tasks to employees based on 
their skills, availability, and current workload. Managers should be able 
to create tasks with required skills, deadlines, and priorities.
```

### 3. Expense Tracking
```
Our company needs to streamline expense reporting. Employees submit receipts 
manually and wait weeks for approval. We want a mobile app where employees 
can photograph receipts, categorize expenses, and submit reports.
```

## 🔧 How It Works

### CrewAI Process

1. **Sequential Execution**: Tasks execute in order
2. **Context Sharing**: Later tasks can access outputs from earlier tasks
3. **Agent Specialization**: Each agent has a specific role and expertise
4. **Quality Gates**: Reviewer agent validates outputs before final delivery

### Task Flow

```
Business Problem
    ↓
Requirements Analyst → User Stories
    ↓
Quality Reviewer → Validated User Stories
    ↓
Product Manager → PRD Draft
    ↓
Quality Reviewer → Final PRD
    ↓
Technical Architect → Database Schema
    ↓
Quality Reviewer → Validated Schema
```

## 🎨 Customization

### Modify Agents

Edit the agent definitions in `crewai_prd_system.ipynb` or `crewai_web_interface.py`:

```python
custom_agent = Agent(
    role='Your Custom Role',
    goal='Your agent goal',
    backstory='Your agent backstory',
    llm=llm,
    verbose=True,
    allow_delegation=False
)
```

### Add New Tasks

```python
custom_task = Task(
    description='Your task description',
    agent=your_agent,
    expected_output='What you expect to receive',
    context=[previous_task]  # Optional: use outputs from other tasks
)
```

### Change LLM Model

```python
# For OpenAI
llm = ChatOpenAI(
    model='gpt-4o',  # or 'gpt-4', 'gpt-3.5-turbo'
    temperature=0.3,
    api_key=openai_key
)

# For Google
llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',  # or 'gemini-pro'
    temperature=0.3,
    google_api_key=google_key
)
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill existing process on port 8001
# Windows:
Get-NetTCPConnection -LocalPort 8001 | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }

# Linux/Mac:
lsof -ti:8001 | xargs kill -9
```

### Import Errors
```bash
# Reinstall dependencies
pip uninstall crewai crewai-tools -y
pip install -r requirements_crewai.txt
```

### API Key Issues
- OpenAI service account keys (sk-svcacct-...) are supported
- Make sure your .env file is in the correct location
- Check that your API key has sufficient credits

### Slow Performance
- Use `gpt-4o-mini` instead of `gpt-4o` for faster responses
- Use `gemini-2.0-flash-exp` instead of `gemini-pro`
- Reduce the number of user stories requested

## 📊 Comparison: CrewAI vs AutoGen

| Feature | CrewAI | AutoGen |
|---------|--------|---------|
| **Framework Style** | Task-oriented | Conversation-oriented |
| **Agent Communication** | Sequential/Hierarchical | Group chat |
| **Context Passing** | Explicit (context parameter) | Implicit (chat history) |
| **Complexity** | Simpler, more structured | More flexible, more complex |
| **Best For** | Clear workflows | Dynamic interactions |

## 🎓 Learning Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [LangChain Documentation](https://python.langchain.com/)

## 📄 License

This is part of the AI-Driven Software Engineering course materials.

## 🤝 Contributing

This system is designed for educational purposes. Feel free to:
- Add new agents
- Create custom tasks
- Extend the PRD template
- Add new examples

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API keys are correct
3. Ensure all dependencies are installed
4. Check the terminal output for specific error messages

---

**Built with CrewAI** - Orchestrating AI agents for software engineering workflows
