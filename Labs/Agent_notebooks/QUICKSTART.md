# Quick Start Guide: AutoGen PRD System

Get your AutoGen PRD system up and running in **5 minutes**!

## Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Jupyter Notebook or VS Code with Jupyter extension
- [ ] An OpenAI API key OR Google API key
- [ ] Internet connection

## Step 1: Install Dependencies (2 minutes)

Open a terminal in the project root directory and run:

```bash
# Install required packages
pip install pyautogen python-dotenv jupyter

# Verify installation
python -c "import autogen; print('✓ AutoGen installed successfully')"
```

## Step 2: Configure API Keys (1 minute)

Create or edit the `.env` file in the project root:

```bash
# Windows PowerShell
notepad .env

# Mac/Linux
nano .env
```

Add your API key (choose one):

```bash
# Option 1: OpenAI (Recommended)
OPENAI_API_KEY=sk-your-api-key-here

# Option 2: Google Gemini
GOOGLE_API_KEY=your-google-api-key-here
```

Save and close the file.

## Step 3: Launch the Notebook (1 minute)

```bash
cd Labs/Agent_notebooks
jupyter notebook autogen_prd_system.ipynb
```

**VS Code Users**: Simply open `autogen_prd_system.ipynb` in VS Code.

## Step 4: Run the System (1 minute)

In the Jupyter notebook:

1. Click **"Cell"** → **"Run All"**
2. Wait 3-5 minutes for all workflows to complete
3. Check the `artifacts/` directory for generated files

That's it! You now have:
- ✅ User stories (JSON)
- ✅ Product Requirements Document (Markdown)
- ✅ Database schema (SQL)

## What You'll See

### Expected Output Timeline

| Time | Workflow | Output |
|------|----------|--------|
| 0:00 | Setup | Environment configured |
| 0:30 | Workflow 1 | User stories generated |
| 2:00 | Workflow 2 | PRD created |
| 4:00 | Workflow 3 | Database schema designed |
| 5:00 | Summary | All artifacts validated |

### Generated Files

After completion, check these files:

```
artifacts/
├── autogen_user_stories.json  ← Structured requirements
├── autogen_prd.md             ← Product Requirements Doc
└── autogen_schema.sql         ← Database design
```

## Quick Test

To verify everything works, look for these success indicators:

```
✓ Environment configured successfully
✓ All agents initialized successfully
✓ Generated 5 user stories
✓ Generated PRD
✓ Generated database schema
✅ All workflows completed successfully!
```

## Common Issues

### ❌ "No API keys found"

**Fix**: Ensure `.env` file is in the **project root** directory (not in `Labs/Agent_notebooks/`)

```bash
# Check location
cd AG-AISOFTDEV  # Project root
ls .env           # Should see .env file here
```

### ❌ "Module 'autogen' not found"

**Fix**: Install in the correct Python environment

```bash
# Verify Python version
python --version

# Install for specific Python
python3 -m pip install pyautogen
```

### ❌ Agents not responding after 30 seconds

**Fix**: Check API key validity and quota

```bash
# Test OpenAI key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# Test Google key
curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_API_KEY"
```

### ❌ "Could not extract user stories"

**Fix**: The LLM output format may be incorrect. Try:
1. Reduce temperature to 0.2 in cell 2
2. Re-run the specific workflow cell
3. Check conversation logs for error messages

## Next Steps

### Customize for Your Project

**Change the business problem** (Cell 4):
```python
business_problem = """
Your custom business problem here...
"""
```

**Use a different model** (Cell 2):
```python
config_list = [{
    'model': 'gpt-4o-mini',  # Cheaper, faster
    'api_key': os.getenv("OPENAI_API_KEY"),
}]
```

**Adjust agent behavior** (Cell 3):
```python
requirements_analyst = autogen.AssistantAgent(
    name="RequirementsAnalyst",
    system_message="Your custom instructions...",
    llm_config=llm_config,
)
```

### Run from Command Line

For automation without Jupyter:

```bash
cd Labs/Agent_notebooks
python autogen_prd_example.py
```

### Batch Process Multiple Problems

Edit `autogen_config.yaml` and add your problems, then:

```python
import yaml

with open('autogen_config.yaml') as f:
    config = yaml.safe_load(f)

for problem in config['example_problems']:
    print(f"Processing: {problem['name']}")
    # Run workflows...
```

## Learning Path

1. **Start Here**: Run the default example
2. **Customize**: Modify the business problem
3. **Extend**: Add a new agent (e.g., CostEstimator)
4. **Integrate**: Connect to Jira, GitHub, or Slack
5. **Production**: Use the example script for CI/CD

## Getting Help

**Documentation**:
- `README_AUTOGEN_PRD_SYSTEM.md` - Full documentation
- `autogen_prd_helpers.py` - Helper function reference
- Course labs in `Labs/Day_01_*/` and `Labs/Day_02_*/`

**Troubleshooting**:
- Check the "Troubleshooting" section in README
- Review conversation logs in notebook output
- Verify API keys have sufficient quota

**AutoGen Resources**:
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AutoGen Examples](https://github.com/microsoft/autogen/tree/main/notebook)
- [AutoGen Discord](https://discord.gg/pAbnFJrkgZ)

## Success Checklist

You're ready to use the system in production when you can:

- [ ] Run all workflows without errors
- [ ] Generate valid JSON user stories
- [ ] Create complete PRDs with all sections
- [ ] Design normalized database schemas
- [ ] Customize business problems easily
- [ ] Understand what each agent does
- [ ] Validate outputs programmatically

## Estimated Costs

Per full workflow execution (all 3 workflows):

| Model | Tokens | Cost |
|-------|--------|------|
| GPT-4o | ~8,000 | $0.16 |
| GPT-4o-mini | ~8,000 | $0.02 |
| Gemini 2.5 Pro | ~8,000 | $0.14 |

**Note**: Costs are approximate and vary by conversation length.

## Ready to Scale?

Once comfortable with the basics:

1. **Add More Agents**: Cost estimator, risk analyzer, test planner
2. **Create Pipelines**: Chain multiple workflows
3. **Build Integrations**: Export to JIRA, GitHub, Confluence
4. **Enable Monitoring**: Track agent performance and costs
5. **Implement Caching**: Reduce API calls and costs

---

**Need help?** Check the [full README](README_AUTOGEN_PRD_SYSTEM.md) or consult course materials.

**Ready to start?** Open `autogen_prd_system.ipynb` and click "Run All"! 🚀
