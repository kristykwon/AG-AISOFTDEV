"""
Example script demonstrating programmatic use of the AutoGen PRD System.

This script shows how to use the AutoGen agents outside of a Jupyter notebook
for automation, CI/CD integration, or batch processing.
"""

import os
import sys
import json
from dotenv import load_dotenv
import autogen

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils import save_artifact
from autogen_prd_helpers import (
    extract_from_conversation,
    validate_user_stories,
    create_validation_report,
    ArtifactTracker
)


def setup_agents(api_provider="openai", model="gpt-4o"):
    """
    Configure and return AutoGen agents.
    
    Args:
        api_provider: 'openai' or 'google'
        model: Model name to use
        
    Returns:
        Tuple of (agents dict, llm_config)
    """
    load_dotenv()
    
    # Configure LLM
    if api_provider == "openai":
        config_list = [{
            'model': model,
            'api_key': os.getenv("OPENAI_API_KEY"),
        }]
    else:  # google
        config_list = [{
            'model': model,
            'api_key': os.getenv("GOOGLE_API_KEY"),
            'api_type': 'google',
        }]
    
    llm_config = {
        "config_list": config_list,
        "temperature": 0.3,
        "timeout": 120,
    }
    
    # Create agents
    agents = {
        'analyst': autogen.AssistantAgent(
            name="RequirementsAnalyst",
            system_message="""You are a Senior Requirements Analyst. Generate detailed 
            user stories in JSON format with id, persona, user_story, and acceptance_criteria.""",
            llm_config=llm_config,
        ),
        'pm': autogen.AssistantAgent(
            name="ProductManager",
            system_message="""You are a Senior Product Manager. Create comprehensive 
            PRDs in markdown format with all required sections.""",
            llm_config=llm_config,
        ),
        'architect': autogen.AssistantAgent(
            name="TechnicalArchitect",
            system_message="""You are a Staff Software Engineer. Design normalized 
            SQL database schemas with proper constraints and relationships.""",
            llm_config=llm_config,
        ),
        'reviewer': autogen.AssistantAgent(
            name="QualityReviewer",
            system_message="""You are a QA Engineer. Validate all artifacts for 
            completeness and quality. Reply 'APPROVED' if perfect, otherwise provide feedback.""",
            llm_config=llm_config,
        ),
        'proxy': autogen.UserProxyAgent(
            name="Coordinator",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=15,
            is_termination_msg=lambda x: "WORKFLOW_COMPLETE" in x.get("content", ""),
            code_execution_config={"work_dir": "autogen_workspace", "use_docker": False},
        )
    }
    
    return agents, llm_config


def generate_user_stories(business_problem: str, agents: dict, llm_config: dict) -> list:
    """
    Generate user stories from a business problem.
    
    Args:
        business_problem: Description of the business problem
        agents: Dictionary of AutoGen agents
        llm_config: LLM configuration
        
    Returns:
        List of user story dictionaries
    """
    print("\n" + "="*80)
    print("GENERATING USER STORIES")
    print("="*80)
    
    groupchat = autogen.GroupChat(
        agents=[agents['proxy'], agents['analyst'], agents['reviewer']],
        messages=[],
        max_round=8
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    task = f"""
    Generate user stories from this business problem:
    {business_problem}
    
    RequirementsAnalyst: Create at least 5 user stories in JSON format.
    QualityReviewer: Validate the JSON structure.
    
    Reply with "WORKFLOW_COMPLETE" when done.
    """
    
    agents['proxy'].initiate_chat(manager, message=task)
    
    # Extract user stories
    user_stories = extract_from_conversation(groupchat.messages, 'json')
    
    if user_stories:
        print(f"\n✓ Generated {len(user_stories)} user stories")
        return user_stories
    else:
        print("\n✗ Failed to generate user stories")
        return []


def generate_prd(user_stories: list, agents: dict, llm_config: dict) -> str:
    """
    Generate PRD from user stories.
    
    Args:
        user_stories: List of user story dictionaries
        agents: Dictionary of AutoGen agents
        llm_config: LLM configuration
        
    Returns:
        PRD markdown content
    """
    print("\n" + "="*80)
    print("GENERATING PRD")
    print("="*80)
    
    groupchat = autogen.GroupChat(
        agents=[agents['proxy'], agents['pm'], agents['reviewer']],
        messages=[],
        max_round=10
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    task = f"""
    Create a PRD from these user stories:
    {json.dumps(user_stories, indent=2)}
    
    ProductManager: Generate a comprehensive PRD with Introduction, User Personas, 
    Features, Success Metrics, and Out of Scope sections.
    QualityReviewer: Validate completeness.
    
    Reply with "WORKFLOW_COMPLETE" when done.
    """
    
    agents['proxy'].initiate_chat(manager, message=task)
    
    # Extract PRD
    prd_content = extract_from_conversation(groupchat.messages, 'markdown')
    
    if prd_content:
        print("\n✓ Generated PRD")
        return prd_content
    else:
        print("\n✗ Failed to generate PRD")
        return ""


def generate_schema(prd_content: str, agents: dict, llm_config: dict) -> str:
    """
    Generate database schema from PRD.
    
    Args:
        prd_content: PRD markdown content
        agents: Dictionary of AutoGen agents
        llm_config: LLM configuration
        
    Returns:
        SQL schema content
    """
    print("\n" + "="*80)
    print("GENERATING DATABASE SCHEMA")
    print("="*80)
    
    groupchat = autogen.GroupChat(
        agents=[agents['proxy'], agents['architect'], agents['reviewer']],
        messages=[],
        max_round=8
    )
    
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    task = f"""
    Design a database schema for this PRD:
    {prd_content[:1000]}...
    
    TechnicalArchitect: Create normalized SQL schema with users and onboarding_tasks tables.
    QualityReviewer: Validate the schema.
    
    Reply with "WORKFLOW_COMPLETE" when done.
    """
    
    agents['proxy'].initiate_chat(manager, message=task)
    
    # Extract schema
    schema = extract_from_conversation(groupchat.messages, 'sql')
    
    if schema:
        print("\n✓ Generated database schema")
        return schema
    else:
        print("\n✗ Failed to generate schema")
        return ""


def main():
    """Main execution function."""
    
    # Example business problem
    business_problem = """
    We need a tool to help our company's new hires get up to speed. 
    New employees often feel overwhelmed in their first weeks and don't know 
    what tasks to complete or who to talk to. We want to create a system that 
    guides them through onboarding, tracks their progress, and helps managers 
    monitor completion.
    """
    
    print("AutoGen PRD Generation System - Example Script")
    print("=" * 80)
    print(f"\nBusiness Problem:\n{business_problem.strip()}")
    
    # Setup
    agents, llm_config = setup_agents(api_provider="openai", model="gpt-4o")
    tracker = ArtifactTracker()
    
    # Workflow 1: User Stories
    user_stories = generate_user_stories(business_problem, agents, llm_config)
    if user_stories:
        # Validate
        is_valid, errors = validate_user_stories(user_stories)
        if not is_valid:
            print("\n⚠ Validation errors:")
            for error in errors:
                print(f"  - {error}")
        
        # Save
        save_artifact(
            json.dumps(user_stories, indent=2),
            "artifacts/example_user_stories.json",
            overwrite=True
        )
        tracker.register(
            "User Stories", 
            "artifacts/example_user_stories.json", 
            user_stories
        )
    
    # Workflow 2: PRD
    if user_stories:
        prd_content = generate_prd(user_stories, agents, llm_config)
        if prd_content:
            save_artifact(
                prd_content,
                "artifacts/example_prd.md",
                overwrite=True
            )
            tracker.register(
                "PRD",
                "artifacts/example_prd.md",
                prd_content
            )
    
    # Workflow 3: Schema
    if prd_content:
        schema = generate_schema(prd_content, agents, llm_config)
        if schema:
            save_artifact(
                schema,
                "artifacts/example_schema.sql",
                overwrite=True
            )
            tracker.register(
                "Database Schema",
                "artifacts/example_schema.sql",
                schema
            )
    
    # Summary
    print("\n" + "=" * 80)
    print("EXECUTION SUMMARY")
    print("=" * 80)
    print(tracker.get_summary())
    
    # Validation report
    artifacts_dict = {
        name: (info['path'], info['content'])
        for name, info in tracker.artifacts.items()
    }
    print("\n" + create_validation_report(artifacts_dict))
    
    if tracker.validate_all():
        print("\n✅ All workflows completed successfully!")
        return 0
    else:
        print("\n⚠️  Some workflows failed. Check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
