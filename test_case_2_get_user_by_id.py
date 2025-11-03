"""
Test Case 2: GET User by ID
Validates that the GET /users/{user_id} endpoint returns a specific user.
"""
import requests

def test_get_user_by_id():
    """Test GET /users/{user_id} returns a specific user"""
    user_id = 1
    url = f"http://127.0.0.1:8000/users/{user_id}"
    
    try:
        response = requests.get(url)
        
        # Check status code
        if response.status_code == 200:
            user = response.json()
            print(f"[PASS] GET /users/{user_id} returned status 200")
            print(f"   User: {user.get('first_name', 'N/A')} {user.get('last_name', 'N/A')}")
            print(f"   Email: {user.get('email', 'N/A')}")
            return True
        else:
            print(f"[FAIL] Expected status 200, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Test Case 2: GET User by ID")
    print("=" * 60)
    result = test_get_user_by_id()
    print("=" * 60)
    exit(0 if result else 1)
