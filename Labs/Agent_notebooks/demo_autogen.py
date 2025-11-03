"""
Simple demo of the AutoGen AI Agent System.

This script shows you how the agents work together in a minimal example.
Run this to see the AI agents in action!

Usage:
    python demo_autogen.py
"""

import os
import sys
from dotenv import load_dotenv

# Setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv()

# Check for API keys
if not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    print("❌ ERROR: No API keys found!")
    print("\nPlease add one of these to your .env file:")
    print("  OPENAI_API_KEY=your_key_here")
    print("  GOOGLE_API_KEY=your_key_here")
    sys.exit(1)

# Import AutoGen
try:
    from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
    print("✅ AutoGen imported successfully!")
except ImportError:
    print("❌ AutoGen not installed. Run: pip install pyautogen==0.2.35")
    sys.exit(1)

print("\n" + "="*80)
print("🤖 AUTOGEN AI AGENT SYSTEM - LIVE DEMO")
print("="*80)

# Configure LLM
if os.getenv("OPENAI_API_KEY"):
    config_list = [{
        'model': 'gpt-4o-mini',  # Using mini for faster/cheaper demo
        'api_key': os.getenv("OPENAI_API_KEY"),
    }]
    print("\n✅ Using OpenAI GPT-4o-mini")
else:
    config_list = [{
        'model': 'gemini-2.5-pro',
        'api_key': os.getenv("GOOGLE_API_KEY"),
    }]
    print("\n✅ Using Google Gemini 2.5 Pro")

llm_config = {
    "config_list": config_list,
    "temperature": 0.3,
}

print("\n" + "="*80)
print("SCENARIO: Creating a simple requirements document")
print("="*80)

# Create the agents
print("\n🔧 Setting up AI agents...")

analyst = AssistantAgent(
    name="RequirementsAnalyst",
    system_message="""You are a Requirements Analyst. When given a business problem, 
    create a simple list of 3 user stories in this format:
    1. As a [user], I want [feature], so that [benefit]
    2. As a [user], I want [feature], so that [benefit]
    3. As a [user], I want [feature], so that [benefit]
    
    Keep it simple and clear.""",
    llm_config=llm_config,
)

reviewer = AssistantAgent(
    name="QualityReviewer",
    system_message="""You are a Quality Reviewer. Review the user stories and either:
    - Approve them by saying "APPROVED" if they're good, OR
    - Provide brief feedback if they need improvement.""",
    llm_config=llm_config,
)

user_proxy = UserProxyAgent(
    name="Coordinator",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=6,
    is_termination_msg=lambda x: "APPROVED" in x.get("content", "").upper() or "TERMINATE" in x.get("content", ""),
    code_execution_config=False,  # No code execution needed for this demo
)

print("✅ Agents ready:")
print("   - RequirementsAnalyst (generates user stories)")
print("   - QualityReviewer (reviews and approves)")
print("   - Coordinator (manages the workflow)")

# Create group chat
print("\n🤝 Creating agent team...")
groupchat = GroupChat(
    agents=[user_proxy, analyst, reviewer],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)
print("✅ Team assembled!")

# Run the demo
print("\n" + "="*80)
print("🚀 STARTING AGENT CONVERSATION")
print("="*80)
print("\nBusiness Problem:")
print("'We need a simple tool to help new employees find answers to common questions.'\n")
print("-"*80)
print("Watch the agents work together below:")
print("-"*80 + "\n")

# Start the conversation
try:
    user_proxy.initiate_chat(
        manager,
        message="""Business problem: We need a simple tool to help new employees find 
        answers to common questions like 'Where is the cafeteria?' or 'How do I request time off?'
        
        RequirementsAnalyst: Please create 3 simple user stories for this.
        QualityReviewer: Please review them and approve if they're good.
        
        When approved, respond with TERMINATE."""
    )
    
    print("\n" + "="*80)
    print("✅ DEMO COMPLETE!")
    print("="*80)
    
    print("\n📊 What just happened:")
    print("  1. The Coordinator gave the business problem to the team")
    print("  2. The RequirementsAnalyst generated user stories")
    print("  3. The QualityReviewer checked and approved them")
    print("  4. All agents worked together without human intervention!")
    
    print("\n💡 In the full system (autogen_prd_system.ipynb):")
    print("  - More specialized agents (Product Manager, Technical Architect)")
    print("  - Longer workflows (User Stories → PRD → Database Schema)")
    print("  - Automated artifact generation (JSON, Markdown, SQL files)")
    print("  - Takes 5-10 minutes to generate complete documentation")
    
    print("\n🎯 Next Steps:")
    print("  1. Run the full notebook: autogen_prd_system.ipynb")
    print("  2. Check generated files in: artifacts/ directory")
    print("  3. Customize the business problem in the notebook")
    
except KeyboardInterrupt:
    print("\n\n⚠️  Demo interrupted by user")
except Exception as e:
    print(f"\n\n❌ Error: {e}")
    print("\nIf you see 'rate limit' errors, wait a minute and try again.")

print("\n" + "="*80)
print("Thank you for trying the AutoGen AI Agent System demo!")
print("="*80 + "\n")
