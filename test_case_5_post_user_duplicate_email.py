"""
Test Case 5: POST User with Duplicate Email
Validates that the POST /users/ endpoint returns 400 for duplicate email addresses.
"""
import requests

def test_post_user_duplicate_email():
    """Test POST /users/ with duplicate email returns 400"""
    url = "http://127.0.0.1:8000/users/"
    
    # Use an email that already exists in the database
    duplicate_user = {
        "first_name": "Duplicate",
        "last_name": "User",
        "email": "alex.chen@example.com",  # This email should already exist
        "role_id": 1,
        "start_date": "2025-10-30"
    }
    
    try:
        response = requests.post(url, json=duplicate_user)
        
        # Check status code - should be 400 for duplicate email
        if response.status_code == 400:
            print(f"[PASS] POST /users/ with duplicate email returned status 400")
            print(f"   Duplicate email correctly rejected")
            return True
        else:
            print(f"[FAIL] Expected status 400, got {response.status_code}")
            print(f"   Response: {response.text}")
            print(f"   Note: Test assumes alex.chen@example.com exists in database")
            return False
    except Exception as e:
        print(f"[FAIL] Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Test Case 5: POST User with Duplicate Email")
    print("=" * 60)
    result = test_post_user_duplicate_email()
    print("=" * 60)
    exit(0 if result else 1)
