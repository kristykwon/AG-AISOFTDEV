"""
Test Case 3: POST Create User
Validates that the POST /users/ endpoint creates a new user with valid data.
"""
import requests
import random

def test_post_user():
    """Test POST /users/ creates a new user and returns 201"""
    url = "http://127.0.0.1:8000/users/"
    
    # Generate unique email to avoid duplicates
    random_num = random.randint(1000, 9999)
    new_user = {
        "first_name": "Test",
        "last_name": "User",
        "email": f"test.user.{random_num}@example.com",
        "role_id": 1,
        "start_date": "2025-10-30"
    }
    
    try:
        response = requests.post(url, json=new_user)
        
        # Check status code
        if response.status_code == 201:
            created_user = response.json()
            print(f"[PASS] POST /users/ returned status 201")
            print(f"   Created user ID: {created_user.get('user_id', 'N/A')}")
            print(f"   Name: {created_user.get('first_name', 'N/A')} {created_user.get('last_name', 'N/A')}")
            print(f"   Email: {created_user.get('email', 'N/A')}")
            return True
        else:
            print(f"[FAIL] Expected status 201, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Test Case 3: POST Create User")
    print("=" * 60)
    result = test_post_user()
    print("=" * 60)
    exit(0 if result else 1)
