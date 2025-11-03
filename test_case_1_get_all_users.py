"""
Test Case 1: GET All Users
Validates that the GET /users/ endpoint returns a list of users.
"""
import requests

def test_get_all_users():
    """Test GET /users/ returns a list of users"""
    url = "http://127.0.0.1:8000/users/"
    
    try:
        response = requests.get(url)
        
        # Check status code
        if response.status_code == 200:
            users = response.json()
            print(f"[PASS] GET /users/ returned status 200")
            print(f"   Found {len(users)} users")
            if len(users) > 0:
                print(f"   Sample user: {users[0].get('first_name', 'N/A')} {users[0].get('last_name', 'N/A')}")
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
    print("Test Case 1: GET All Users")
    print("=" * 60)
    result = test_get_all_users()
    print("=" * 60)
    exit(0 if result else 1)
