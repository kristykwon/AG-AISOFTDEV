# AutoGen PRD Generation System

## Overview

This directory contains an advanced **AutoGen-based multi-agent system** that automates the entire Product Requirements Document (PRD) generation workflow. The system demonstrates how AI agents can collaborate like a real software development team to transform vague business ideas into production-ready technical artifacts.

## 🚀 Quick Start - Web Interface

**Want to start typing prompts right away?**

1. Start the web interface:
   ```powershell
   cd Labs\Agent_notebooks
   python web_interface.py
   ```

2. Open in your browser:
   ```
   http://localhost:8001
   ```

3. Type your business problem and watch AI agents work!

📚 **See:** `WEB_INTERFACE_GUIDE.md` and `PORTS_REFERENCE.md` for details.

## What This System Does

The AutoGen PRD system takes a simple business problem statement and automatically generates:

1. **Structured User Stories** (JSON) - Complete with personas and acceptance criteria
2. **Product Requirements Document** (Markdown) - Professional, template-driven PRD
3. **Database Schema** (SQL) - Normalized, production-ready database design
4. **Architectural Decision Records** (Optional) - Documented technical decisions

## Architecture

### Agent Team Structure

The system employs **5 specialized agents** that work together:

| Agent | Role | Responsibilities |
|-------|------|------------------|
| **Requirements Analyst** | Requirements Engineer | Extracts user stories, defines personas, creates acceptance criteria |
| **Product Manager** | Product Strategy | Synthesizes requirements into comprehensive PRDs |
| **Technical Architect** | System Design | Designs database schemas, creates ADRs, makes technical decisions |
| **Quality Reviewer** | QA Engineer | Validates all artifacts for completeness and quality |
| **User Proxy (Coordinator)** | Workflow Manager | Orchestrates the team, executes code, manages artifacts |

### Workflow Design

The system executes **3 sequential workflows**:

```
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW 1: User Story Generation                           │
│ Input: Business Problem Statement                           │
│ Agents: Requirements Analyst → Quality Reviewer             │
│ Output: autogen_user_stories.json                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW 2: PRD Generation                                  │
│ Input: User Stories JSON + PRD Template                     │
│ Agents: Product Manager → Quality Reviewer                  │
│ Output: autogen_prd.md                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ WORKFLOW 3: Schema Generation                               │
│ Input: PRD Content                                          │
│ Agents: Technical Architect → Quality Reviewer              │
│ Output: autogen_schema.sql                                 │
└─────────────────────────────────────────────────────────────┘
```

## Files in This Directory

### Main Notebook
- **`autogen_prd_system.ipynb`** - Complete implementation of the multi-agent PRD generation system

### Helper Module
- **`autogen_prd_helpers.py`** - Utility functions for content extraction, validation, and artifact management

### Generated Artifacts
All generated artifacts are saved to the `artifacts/` directory:
- `autogen_user_stories.json` - Structured user stories
- `autogen_prd.md` - Product Requirements Document
- `autogen_schema.sql` - Database schema
- `autogen_adr_001.md` - Architectural Decision Record (optional)

## Prerequisites

### Required Python Packages

```bash
pip install pyautogen python-dotenv
```

### Environment Configuration

Create a `.env` file in the project root with at least one of these API keys:

```bash
# Option 1: OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Option 2: Google Gemini
GOOGLE_API_KEY=your_google_api_key_here
```

### Directory Structure

Ensure the following directories exist:
```
AG-AISOFTDEV/
├── Labs/
│   └── Agent_notebooks/
│       ├── autogen_prd_system.ipynb
│       ├── autogen_prd_helpers.py
│       └── README_AUTOGEN_PRD_SYSTEM.md
├── artifacts/
├── templates/
│   └── prd_template.md
└── utils/
```

## Quick Start

### 1. Open the Notebook

```bash
cd Labs/Agent_notebooks
jupyter notebook autogen_prd_system.ipynb
```

### 2. Run All Cells

Execute all cells in sequence. The notebook will:
- Configure the AutoGen agents
- Process the default business problem
- Generate all artifacts
- Display a comprehensive summary

### 3. Review Generated Artifacts

Check the `artifacts/` directory for:
- `autogen_user_stories.json`
- `autogen_prd.md`
- `autogen_schema.sql`

## Usage Examples

### Example 1: Default Business Problem

The notebook includes a default problem statement about employee onboarding. Simply run all cells to see the system in action.

### Example 2: Custom Business Problem

Modify the `business_problem` variable in cell 4:

```python
business_problem = """
We need a customer support ticketing system that helps our support team
manage customer inquiries efficiently. Support agents need to track tickets,
prioritize urgent issues, and collaborate on complex problems. Customers
should be able to submit tickets and track their status.
"""
```

Then run all cells to generate artifacts for your custom problem.

### Example 3: Using the Helper Module

```python
from autogen_prd_helpers import (
    extract_json_from_text,
    validate_user_stories,
    ArtifactTracker
)

# Track artifacts
tracker = ArtifactTracker()
tracker.register("User Stories", "artifacts/autogen_user_stories.json", stories)
tracker.register("PRD", "artifacts/autogen_prd.md", prd_content)

# Get summary
print(tracker.get_summary())
```

## Key Features

### 1. Automated Quality Assurance

The Quality Reviewer agent validates:
- JSON structure and completeness
- PRD section coverage
- SQL schema normalization
- Acceptance criteria testability

### 2. Template-Driven Generation

The system uses templates to ensure consistency:
- PRD follows a standard template structure
- User stories follow Agile best practices
- ADRs follow industry-standard format

### 3. Multi-Provider Support

Works with multiple LLM providers:
- OpenAI (GPT-4, GPT-4o)
- Google (Gemini 2.5 Pro)
- Easily extensible to other providers

### 4. Conversation Persistence

All agent conversations are captured, allowing you to:
- Review the decision-making process
- Debug issues
- Understand agent reasoning

## Customization

### Modify Agent Behavior

Edit the `system_message` for any agent to change its behavior:

```python
requirements_analyst = autogen.AssistantAgent(
    name="RequirementsAnalyst",
    system_message="Your custom instructions here...",
    llm_config=llm_config,
)
```

### Add New Agents

Create specialized agents for new capabilities:

```python
cost_estimator = autogen.AssistantAgent(
    name="CostEstimator",
    system_message="You are a cost estimation expert. Analyze PRDs and estimate development effort...",
    llm_config=llm_config,
)
```

### Extend Workflows

Add new workflows for additional artifacts:

```python
# Workflow 4: Test Plan Generation
test_plan_task = f"""
Generate a comprehensive test plan based on the user stories and PRD...
"""

user_proxy.initiate_chat(test_plan_manager, message=test_plan_task)
```

## Integration with Course Labs

This AutoGen system integrates with the course material:

### Day 1 Labs (Planning & Requirements)
- **Lab 1**: AI-Powered Requirements & User Stories → **Workflow 1**
- **Lab 2**: Generating PRDs → **Workflow 2**

### Day 2 Labs (Design & Architecture)
- **Lab 1**: System Design & Database Seeding → **Workflow 3**
- **Lab 2**: ADRs → **Optional Workflow**

### Comparison

| Aspect | Manual Labs | AutoGen System |
|--------|-------------|----------------|
| Time | ~3-4 hours | ~5-10 minutes |
| Consistency | Variable | High |
| Iteration | Manual rework | Automated |
| Team Simulation | Single user | Multi-agent collaboration |
| Quality Gates | Manual review | Automated validation |

## Troubleshooting

### Issue: "No API keys found"

**Solution**: Ensure your `.env` file is in the project root with valid API keys.

### Issue: Agents not responding

**Solution**: 
- Check your API key has sufficient credits/quota
- Increase `timeout` in `llm_config`
- Verify internet connectivity

### Issue: Invalid JSON output

**Solution**: 
- Make the Requirements Analyst's prompt more explicit about JSON format
- Increase `temperature` to 0.2 or lower for more deterministic outputs
- Add explicit examples in the system message

### Issue: Incomplete PRD

**Solution**:
- Verify the PRD template exists at `templates/prd_template.md`
- Increase `max_round` in the GroupChat configuration
- Make the Product Manager's instructions more specific

## Performance Optimization

### Reduce API Costs

1. Use smaller models for simpler tasks
2. Reduce `max_round` in GroupChat configurations
3. Cache intermediate results

### Improve Speed

1. Use faster models (e.g., GPT-4o-mini instead of GPT-4o)
2. Run workflows in parallel (when dependencies allow)
3. Reduce conversation rounds

### Enhance Quality

1. Increase `temperature` to 0 for more deterministic outputs
2. Add more specific examples in system messages
3. Increase validation rigor in Quality Reviewer

## Advanced Topics

### Parallel Workflow Execution

For independent workflows, use Python's `asyncio`:

```python
import asyncio

async def run_workflows():
    task1 = asyncio.create_task(generate_user_stories())
    task2 = asyncio.create_task(generate_adr())
    await asyncio.gather(task1, task2)
```

### Custom Validation Rules

Extend the helper module with domain-specific validation:

```python
def validate_healthcare_compliance(prd_text: str) -> bool:
    """Check PRD includes HIPAA compliance sections."""
    required = ["Data Privacy", "Security Controls", "Audit Logging"]
    return all(section in prd_text for section in required)
```

### Integration with External Tools

Export artifacts to external systems:

```python
# Export to Jira
import jira_client
for story in user_stories:
    jira_client.create_issue(
        project="ONBOARD",
        summary=story['user_story'],
        description=story['acceptance_criteria']
    )
```

## Learning Outcomes

By working with this AutoGen system, you will:

1. ✅ Understand multi-agent collaboration patterns
2. ✅ Learn to design specialized agent roles
3. ✅ Master workflow orchestration with GroupChat
4. ✅ Implement automated quality assurance
5. ✅ Practice artifact-driven development
6. ✅ Experience AI-assisted software engineering at scale

## Resources

### AutoGen Documentation
- [Official AutoGen Docs](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)

### Course Materials
- Day 1 Labs: `Labs/Day_01_Planning_and_Requirements/`
- Day 2 Labs: `Labs/Day_02_Design_and_Architecture/`
- Templates: `templates/`

### Related Notebooks
- `agents_setup_AutoGen.ipynb` - Basic AutoGen introduction
- Day 1 Lab 1: Manual user story generation
- Day 1 Lab 2: Manual PRD generation

## Contributing

To extend this system:

1. Fork the repository
2. Create a new agent or workflow
3. Add tests in `autogen_prd_helpers.py`
4. Document your changes in this README
5. Submit a pull request

## License

This system is part of the AI-Driven Software Engineering Program course materials.

## Support

For issues or questions:
- Check the Troubleshooting section above
- Review the AutoGen documentation
- Consult the course instructors
- Open an issue in the course repository

---

**Last Updated**: October 31, 2025  
**Version**: 1.0  
**Maintainer**: AI-Driven Software Engineering Program Team
