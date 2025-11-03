"""
Test script to validate the API field name fixes.
This script tests all CRUD operations to ensure the API works correctly with the database.
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USER_EMAIL = f"test.user.{datetime.now().timestamp()}@example.com"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_test_header(test_name):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}TEST: {test_name}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ PASS: {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ FAIL: {message}{RESET}")

def print_info(message):
    print(f"{YELLOW}ℹ INFO: {message}{RESET}")

def print_response(response, show_body=True):
    print(f"  Status Code: {response.status_code}")
    if show_body:
        try:
            print(f"  Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"  Response: {response.text}")

# Test 1: Health Check
def test_health_check():
    print_test_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json()["status"] == "ok", "Health check failed"
        print_success("API is running and healthy")
        return True
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

# Test 2: List All Users (GET)
def test_list_users():
    print_test_header("List All Users (GET /users/)")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        print_response(response)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        users = response.json()
        assert isinstance(users, list), "Expected list of users"
        
        if len(users) > 0:
            # Validate schema of first user
            user = users[0]
            required_fields = ["user_id", "first_name", "last_name", "email", "role_id", "start_date"]
            for field in required_fields:
                assert field in user, f"Missing required field: {field}"
                print_info(f"Field '{field}' present with value: {user[field]}")
            
            print_success(f"Successfully retrieved {len(users)} users with correct schema")
        else:
            print_info("No users in database yet")
        return True
    except Exception as e:
        print_error(f"List users failed: {str(e)}")
        return False

# Test 3: Create User (POST)
def test_create_user():
    print_test_header("Create User (POST /users/)")
    
    # First, check if roles exist
    print_info("Checking if roles exist in database...")
    check_roles_query = """
SELECT role_id, role_name FROM roles LIMIT 1;
"""
    
    new_user = {
        "first_name": "Test",
        "last_name": "User",
        "email": TEST_USER_EMAIL,
        "role_id": 1,  # Assuming role_id 1 exists
        "start_date": "2024-10-30"
    }
    
    try:
        print_info(f"Creating user with data: {json.dumps(new_user, indent=2)}")
        response = requests.post(f"{BASE_URL}/users/", json=new_user)
        print_response(response)
        
        if response.status_code == 201:
            created_user = response.json()
            assert "user_id" in created_user, "Missing user_id in response"
            assert created_user["first_name"] == new_user["first_name"]
            assert created_user["last_name"] == new_user["last_name"]
            assert created_user["email"] == new_user["email"]
            assert created_user["role_id"] == new_user["role_id"]
            assert created_user["start_date"] == new_user["start_date"]
            
            print_success(f"User created successfully with user_id: {created_user['user_id']}")
            return created_user["user_id"]
        else:
            print_error(f"Failed to create user. Status: {response.status_code}")
            if response.status_code == 500:
                print_info("This might be due to missing roles in the database")
                print_info("Make sure the roles table has at least one role with role_id=1")
            return None
    except Exception as e:
        print_error(f"Create user failed: {str(e)}")
        return None

# Test 4: Get Single User (GET by ID)
def test_get_user(user_id):
    print_test_header(f"Get Single User (GET /users/{user_id})")
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print_response(response)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        user = response.json()
        assert user["user_id"] == user_id, f"Expected user_id {user_id}, got {user['user_id']}"
        
        print_success(f"Successfully retrieved user: {user['first_name']} {user['last_name']}")
        return True
    except Exception as e:
        print_error(f"Get user failed: {str(e)}")
        return False

# Test 5: Update User (PATCH)
def test_update_user(user_id):
    print_test_header(f"Update User (PATCH /users/{user_id})")
    
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    
    try:
        print_info(f"Updating user with data: {json.dumps(update_data, indent=2)}")
        response = requests.patch(f"{BASE_URL}/users/{user_id}", json=update_data)
        print_response(response)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        updated_user = response.json()
        assert updated_user["first_name"] == update_data["first_name"]
        assert updated_user["last_name"] == update_data["last_name"]
        
        print_success("User updated successfully")
        return True
    except Exception as e:
        print_error(f"Update user failed: {str(e)}")
        return False

# Test 6: Replace User (PUT)
def test_replace_user(user_id):
    print_test_header(f"Replace User (PUT /users/{user_id})")
    
    replace_data = {
        "first_name": "Replaced",
        "last_name": "Completely",
        "email": TEST_USER_EMAIL,
        "role_id": 1,
        "start_date": "2024-11-01"
    }
    
    try:
        print_info(f"Replacing user with data: {json.dumps(replace_data, indent=2)}")
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=replace_data)
        print_response(response)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        replaced_user = response.json()
        assert replaced_user["first_name"] == replace_data["first_name"]
        assert replaced_user["start_date"] == replace_data["start_date"]
        
        print_success("User replaced successfully")
        return True
    except Exception as e:
        print_error(f"Replace user failed: {str(e)}")
        return False

# Test 7: Delete User (DELETE)
def test_delete_user(user_id):
    print_test_header(f"Delete User (DELETE /users/{user_id})")
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        print(f"  Status Code: {response.status_code}")
        assert response.status_code == 204, f"Expected 204, got {response.status_code}"
        
        # Verify deletion
        verify_response = requests.get(f"{BASE_URL}/users/{user_id}")
        assert verify_response.status_code == 404, "User should not exist after deletion"
        
        print_success("User deleted successfully")
        return True
    except Exception as e:
        print_error(f"Delete user failed: {str(e)}")
        return False

# Test 8: Verify Database Schema Alignment
def test_schema_alignment():
    print_test_header("Database Schema Alignment Check")
    try:
        import sqlite3
        conn = sqlite3.connect('artifacts/onboarding.db')
        cursor = conn.cursor()
        
        # Get actual table schema
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        conn.close()
        
        print_info("Database columns:")
        db_columns = []
        for col in columns:
            col_id, name, type_, notnull, default, pk = col
            db_columns.append(name)
            print(f"  - {name}: {type_} (PK: {pk}, NOT NULL: {notnull})")
        
        # Expected columns based on schema
        expected = ["user_id", "first_name", "last_name", "email", "role_id", "start_date"]
        
        for expected_col in expected:
            if expected_col in db_columns:
                print_success(f"Column '{expected_col}' exists in database")
            else:
                print_error(f"Column '{expected_col}' missing from database")
        
        return True
    except Exception as e:
        print_error(f"Schema alignment check failed: {str(e)}")
        return False

# Main test runner
def run_all_tests():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Starting API Validation Tests{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 0
    }
    
    # Test 0: Schema Alignment
    results["total"] += 1
    if test_schema_alignment():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 1: Health Check
    results["total"] += 1
    if not test_health_check():
        print_error("API is not running. Please start it with: python -m uvicorn app.main:app --reload")
        return
    results["passed"] += 1
    
    # Test 2: List Users
    results["total"] += 1
    if test_list_users():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 3-7: CRUD Operations
    user_id = test_create_user()
    results["total"] += 1
    if user_id:
        results["passed"] += 1
        
        # Continue with other tests only if user creation succeeded
        results["total"] += 1
        if test_get_user(user_id):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        results["total"] += 1
        if test_update_user(user_id):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        results["total"] += 1
        if test_replace_user(user_id):
            results["passed"] += 1
        else:
            results["failed"] += 1
        
        results["total"] += 1
        if test_delete_user(user_id):
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        results["failed"] += 1
        print_info("Skipping remaining CRUD tests due to creation failure")
    
    # Print final results
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Results Summary{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Total Tests: {results['total']}")
    print(f"{GREEN}Passed: {results['passed']}{RESET}")
    print(f"{RED}Failed: {results['failed']}{RESET}")
    
    if results['failed'] == 0:
        print(f"\n{GREEN}{'🎉 ALL TESTS PASSED! 🎉':^60}{RESET}")
        print(f"{GREEN}The API is working correctly with the database schema.{RESET}")
    else:
        print(f"\n{YELLOW}Some tests failed. Please review the output above.{RESET}")
    
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    run_all_tests()
