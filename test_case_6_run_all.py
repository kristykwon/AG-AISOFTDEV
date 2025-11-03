"""
Test Case 6: Run All Tests
Executes all test cases and provides a summary report.
"""
import subprocess
import sys

def run_test_script(script_name):
    """Run a test script and return True if it passed"""
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"[FAIL] {script_name} timed out")
        return False
    except Exception as e:
        print(f"[FAIL] Error running {script_name}: {str(e)}")
        return False

def main():
    """Run all test cases and generate summary"""
    print("=" * 60)
    print("Running All Test Cases")
    print("=" * 60)
    print()
    
    test_scripts = [
        "test_case_1_get_all_users.py",
        "test_case_2_get_user_by_id.py",
        "test_case_3_post_user.py",
        "test_case_4_post_user_missing_fields.py",
        "test_case_5_post_user_duplicate_email.py"
    ]
    
    results = {}
    
    for script in test_scripts:
        print(f"\n{'=' * 60}")
        print(f"Running: {script}")
        print('=' * 60)
        passed = run_test_script(script)
        results[script] = passed
        print()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed_count = sum(1 for passed in results.values() if passed)
    total_count = len(results)
    
    for script, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status}: {script}")
    
    print("=" * 60)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("=" * 60)
    
    return passed_count == total_count

if __name__ == "__main__":
    all_passed = main()
    exit(0 if all_passed else 1)
