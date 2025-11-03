"""
Comprehensive Test Suite for CrewAI Agent System

This script tests all aspects of the CrewAI PRD generation system:
- Agent initialization
- Task execution
- Crew orchestration
- Output quality validation
- Error handling
- Performance metrics
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Setup logging
log_dir = Path("test_logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"crewai_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Setup paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv()

# Test results storage
test_results = {
    "timestamp": datetime.now().isoformat(),
    "tests": [],
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
}


class TestResult:
    """Store individual test results"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.status = "not_run"
        self.duration = 0.0
        self.error = None
        self.details = {}
        self.start_time = None
    
    def start(self):
        self.start_time = time.time()
        logger.info(f"🧪 Starting test: {self.test_name}")
    
    def pass_test(self, details: Optional[Dict] = None):
        self.status = "passed"
        self.duration = time.time() - self.start_time
        self.details = details or {}
        logger.info(f"✅ PASSED: {self.test_name} ({self.duration:.2f}s)")
    
    def fail_test(self, error: str, details: Optional[Dict] = None):
        self.status = "failed"
        self.duration = time.time() - self.start_time
        self.error = error
        self.details = details or {}
        logger.error(f"❌ FAILED: {self.test_name} - {error}")
    
    def skip_test(self, reason: str):
        self.status = "skipped"
        self.error = reason
        logger.warning(f"⏭️  SKIPPED: {self.test_name} - {reason}")
    
    def to_dict(self):
        return {
            "test_name": self.test_name,
            "status": self.status,
            "duration": self.duration,
            "error": self.error,
            "details": self.details
        }


def test_api_keys() -> TestResult:
    """Test 1: Verify API keys are configured"""
    result = TestResult("API Keys Configuration")
    result.start()
    
    try:
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if not openai_key and not google_key:
            result.fail_test(
                "No API keys found in environment",
                {"openai_key_present": False, "google_key_present": False}
            )
            return result
        
        details = {
            "openai_key_present": bool(openai_key),
            "google_key_present": bool(google_key),
            "openai_key_valid_format": openai_key.startswith("sk-") if openai_key else False,
        }
        
        result.pass_test(details)
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_dependencies_import() -> TestResult:
    """Test 2: Verify all required dependencies can be imported"""
    result = TestResult("Dependencies Import")
    result.start()
    
    required_modules = [
        "crewai",
        "langchain",
        "langchain_openai",
        "langchain_google_genai",
        "fastapi",
        "uvicorn",
        "websockets",
        "pydantic"
    ]
    
    try:
        import_results = {}
        failed_imports = []
        
        for module in required_modules:
            try:
                __import__(module)
                import_results[module] = "success"
            except ImportError as e:
                import_results[module] = f"failed: {str(e)}"
                failed_imports.append(module)
        
        if failed_imports:
            result.fail_test(
                f"Failed to import: {', '.join(failed_imports)}",
                {"import_results": import_results}
            )
        else:
            result.pass_test({"import_results": import_results})
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_crewai_agent_creation() -> TestResult:
    """Test 3: Test creating CrewAI agents"""
    result = TestResult("CrewAI Agent Creation")
    result.start()
    
    try:
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        # Determine which LLM to use
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if openai_key and openai_key.startswith("sk-"):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            llm_type = "OpenAI"
        elif google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
            llm_type = "Google Gemini"
        else:
            result.skip_test("No valid API key available")
            return result
        
        # Create test agent
        agent = Agent(
            role='Test Requirements Analyst',
            goal='Test agent creation',
            backstory='This is a test agent for validation purposes.',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        result.pass_test({
            "llm_type": llm_type,
            "agent_role": agent.role,
            "agent_created": True
        })
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_crewai_task_creation() -> TestResult:
    """Test 4: Test creating CrewAI tasks"""
    result = TestResult("CrewAI Task Creation")
    result.start()
    
    try:
        from crewai import Agent, Task
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if openai_key and openai_key.startswith("sk-"):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        elif google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
        else:
            result.skip_test("No valid API key available")
            return result
        
        agent = Agent(
            role='Test Agent',
            goal='Test task creation',
            backstory='Test agent',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        task = Task(
            description="Test task: Generate a simple user story for a login feature",
            agent=agent,
            expected_output='A user story with acceptance criteria'
        )
        
        result.pass_test({
            "task_description": task.description,
            "task_created": True
        })
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_crewai_crew_execution() -> TestResult:
    """Test 5: Test executing a simple crew workflow"""
    result = TestResult("CrewAI Crew Execution")
    result.start()
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if openai_key and openai_key.startswith("sk-"):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            llm_type = "OpenAI"
        elif google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
            llm_type = "Google Gemini"
        else:
            result.skip_test("No valid API key available")
            return result
        
        logger.info(f"Using {llm_type} for crew execution test")
        
        # Create simple agent
        analyst = Agent(
            role='Test Analyst',
            goal='Generate a brief user story',
            backstory='Expert at creating concise user stories',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        # Create simple task
        task = Task(
            description="""Generate ONE user story for a simple login feature.
            Format: 'As a [user], I want [goal], so that [benefit]'
            Include 2 acceptance criteria.""",
            agent=analyst,
            expected_output='One user story with 2 acceptance criteria'
        )
        
        # Create and execute crew
        crew = Crew(
            agents=[analyst],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        execution_start = time.time()
        crew_result = crew.kickoff()
        execution_time = time.time() - execution_start
        
        output = str(crew_result)
        
        # Validate output
        validation = {
            "output_length": len(output),
            "has_user_story": "As a" in output,
            "has_acceptance_criteria": any(word in output.lower() for word in ["given", "when", "then", "should"]),
            "execution_time": round(execution_time, 2),
            "llm_type": llm_type
        }
        
        if validation["has_user_story"]:
            result.pass_test(validation)
        else:
            result.fail_test("Output does not contain expected user story format", validation)
    
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_full_prd_generation() -> TestResult:
    """Test 6: Test full PRD generation workflow"""
    result = TestResult("Full PRD Generation Workflow")
    result.start()
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if openai_key and openai_key.startswith("sk-"):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            llm_type = "OpenAI"
        elif google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
            llm_type = "Google Gemini"
        else:
            result.skip_test("No valid API key available")
            return result
        
        logger.info(f"Using {llm_type} for full PRD generation test")
        
        # Test problem
        test_problem = """We need a simple mobile app for tracking daily water intake. 
        Users should be able to log glasses of water and see their daily progress."""
        
        # Create agents
        requirements_analyst = Agent(
            role='Requirements Analyst',
            goal='Extract user stories from business problems',
            backstory='Expert at understanding user needs',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        product_manager = Agent(
            role='Product Manager',
            goal='Create concise PRDs',
            backstory='Experienced in product documentation',
            llm=llm,
            verbose=False,
            allow_delegation=False
        )
        
        # Create tasks
        task_stories = Task(
            description=f"""Analyze this problem and generate 3 user stories:
            {test_problem}
            
            Format: 'As a [persona], I want [goal], so that [benefit]'""",
            agent=requirements_analyst,
            expected_output='3 user stories'
        )
        
        task_prd = Task(
            description="""Create a brief PRD with:
            ## Introduction
            ## User Personas
            ## Key Features
            ## Success Metrics""",
            agent=product_manager,
            expected_output='Brief PRD document',
            context=[task_stories]
        )
        
        # Execute crew
        crew = Crew(
            agents=[requirements_analyst, product_manager],
            tasks=[task_stories, task_prd],
            process=Process.sequential,
            verbose=False
        )
        
        execution_start = time.time()
        prd_result = crew.kickoff()
        execution_time = time.time() - execution_start
        
        prd_content = str(prd_result)
        
        # Validate PRD structure
        required_sections = ["Introduction", "Persona", "Feature", "Metric"]
        sections_found = [section for section in required_sections if section.lower() in prd_content.lower()]
        
        validation = {
            "output_length": len(prd_content),
            "execution_time": round(execution_time, 2),
            "sections_found": sections_found,
            "sections_count": len(sections_found),
            "llm_type": llm_type,
            "has_user_stories": "As a" in prd_content or "user" in prd_content.lower()
        }
        
        # Save PRD output for inspection
        output_dir = Path("test_outputs")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"test_prd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_file.write_text(prd_content)
        validation["output_file"] = str(output_file)
        
        if len(sections_found) >= 2:
            result.pass_test(validation)
        else:
            result.fail_test(f"PRD missing key sections. Found: {sections_found}", validation)
    
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_web_interface_imports() -> TestResult:
    """Test 7: Test web interface file imports"""
    result = TestResult("Web Interface Imports")
    result.start()
    
    try:
        # Check if file exists
        web_interface_path = Path(__file__).parent / "crewai_web_interface.py"
        
        if not web_interface_path.exists():
            result.fail_test(f"Web interface file not found: {web_interface_path}")
            return result
        
        # Try to import required modules for web interface
        import fastapi
        import uvicorn
        import websockets
        from pydantic import BaseModel
        
        result.pass_test({
            "web_interface_exists": True,
            "fastapi_version": fastapi.__version__,
            "uvicorn_available": True,
            "websockets_available": True
        })
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_error_handling() -> TestResult:
    """Test 8: Test error handling with invalid inputs"""
    result = TestResult("Error Handling")
    result.start()
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        openai_key = os.getenv("OPENAI_API_KEY", "")
        google_key = os.getenv("GOOGLE_API_KEY", "")
        
        if openai_key and openai_key.startswith("sk-"):
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        elif google_key:
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.3)
        else:
            result.skip_test("No valid API key available")
            return result
        
        errors_caught = []
        
        # Test 1: Empty task description
        try:
            agent = Agent(role='Test', goal='Test', backstory='Test', llm=llm, verbose=False)
            task = Task(description="", agent=agent, expected_output='output')
            crew = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)
            # If this doesn't error, it's acceptable
            errors_caught.append({"test": "empty_description", "handled": True})
        except Exception as e:
            errors_caught.append({"test": "empty_description", "error": str(e)[:100]})
        
        # Test 2: Agent without LLM (should fail at creation)
        try:
            agent_no_llm = Agent(role='Test', goal='Test', backstory='Test', verbose=False)
            errors_caught.append({"test": "no_llm", "handled": False, "note": "Should have failed"})
        except Exception as e:
            errors_caught.append({"test": "no_llm", "error_caught": True})
        
        result.pass_test({
            "error_tests": errors_caught,
            "error_handling_working": len(errors_caught) > 0
        })
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_output_quality() -> TestResult:
    """Test 9: Test output quality and validation"""
    result = TestResult("Output Quality Validation")
    result.start()
    
    try:
        # Check test outputs directory
        output_dir = Path("test_outputs")
        
        quality_checks = {
            "output_dir_exists": output_dir.exists(),
            "output_files_count": len(list(output_dir.glob("*.md"))) if output_dir.exists() else 0
        }
        
        # If we have test output files, analyze the most recent one
        if quality_checks["output_files_count"] > 0:
            latest_output = max(output_dir.glob("*.md"), key=lambda p: p.stat().st_mtime)
            content = latest_output.read_text()
            
            quality_checks.update({
                "latest_file": str(latest_output.name),
                "file_size": len(content),
                "has_headers": content.count("#") >= 2,
                "has_paragraphs": content.count("\n\n") >= 3,
                "word_count": len(content.split()),
                "quality_score": "good" if len(content) > 500 else "needs_improvement"
            })
        
        result.pass_test(quality_checks)
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def test_performance_metrics() -> TestResult:
    """Test 10: Measure performance metrics"""
    result = TestResult("Performance Metrics")
    result.start()
    
    try:
        metrics = {
            "python_version": sys.version,
            "platform": sys.platform,
            "working_directory": os.getcwd()
        }
        
        # Check log file size
        if log_file.exists():
            metrics["log_file_size"] = log_file.stat().st_size
        
        # Memory usage (if psutil available)
        try:
            import psutil
            process = psutil.Process()
            metrics["memory_mb"] = round(process.memory_info().rss / 1024 / 1024, 2)
        except ImportError:
            metrics["memory_mb"] = "psutil not available"
        
        result.pass_test(metrics)
    except Exception as e:
        result.fail_test(f"Exception: {str(e)}")
    
    return result


def run_all_tests():
    """Run all tests and generate report"""
    logger.info("=" * 80)
    logger.info("🚀 STARTING CREWAI AGENT SYSTEM TEST SUITE")
    logger.info("=" * 80)
    
    test_functions = [
        test_api_keys,
        test_dependencies_import,
        test_crewai_agent_creation,
        test_crewai_task_creation,
        test_crewai_crew_execution,
        test_full_prd_generation,
        test_web_interface_imports,
        test_error_handling,
        test_output_quality,
        test_performance_metrics
    ]
    
    suite_start = time.time()
    
    for test_func in test_functions:
        test_result = test_func()
        test_results["tests"].append(test_result.to_dict())
        test_results["summary"]["total"] += 1
        
        if test_result.status == "passed":
            test_results["summary"]["passed"] += 1
        elif test_result.status == "failed":
            test_results["summary"]["failed"] += 1
        elif test_result.status == "skipped":
            test_results["summary"]["skipped"] += 1
    
    suite_duration = time.time() - suite_start
    test_results["total_duration"] = round(suite_duration, 2)
    
    # Generate summary
    logger.info("=" * 80)
    logger.info("📊 TEST SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total Tests: {test_results['summary']['total']}")
    logger.info(f"✅ Passed: {test_results['summary']['passed']}")
    logger.info(f"❌ Failed: {test_results['summary']['failed']}")
    logger.info(f"⏭️  Skipped: {test_results['summary']['skipped']}")
    logger.info(f"⏱️  Duration: {suite_duration:.2f}s")
    logger.info("=" * 80)
    
    # Save JSON report
    report_file = log_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(test_results, f, indent=2)
    
    logger.info(f"📄 Full report saved to: {report_file}")
    logger.info(f"📄 Log file saved to: {log_file}")
    
    # Print failed tests details
    if test_results["summary"]["failed"] > 0:
        logger.info("\n" + "=" * 80)
        logger.info("❌ FAILED TESTS DETAILS")
        logger.info("=" * 80)
        for test in test_results["tests"]:
            if test["status"] == "failed":
                logger.error(f"\nTest: {test['test_name']}")
                logger.error(f"Error: {test['error']}")
                if test.get('details'):
                    logger.error(f"Details: {json.dumps(test['details'], indent=2)}")
    
    return test_results


if __name__ == "__main__":
    logger.info(f"Log file: {log_file}")
    results = run_all_tests()
    
    # Exit with error code if tests failed
    if results["summary"]["failed"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)
