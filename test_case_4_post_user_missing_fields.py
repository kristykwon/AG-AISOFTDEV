"""
Test Case 4: POST User with Missing Fields
Validates that the POST /users/ endpoint returns 422 for missing required fields.
"""
import requests

def test_post_user_missing_fields():
    """Test POST /users/ with missing fields returns 422"""
    url = "http://127.0.0.1:8000/users/"
    
    # Missing email and role_id
    incomplete_user = {
        "first_name": "Incomplete",
        "last_name": "User"
    }
    
    try:
        response = requests.post(url, json=incomplete_user)
        
        # Check status code - should be 422 for validation error
        if response.status_code == 422:
            print(f"[PASS] POST /users/ with missing fields returned status 422")
            print(f"   Validation correctly rejected incomplete data")
            return True
        else:
            print(f"[FAIL] Expected status 422, got {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"[FAIL] Exception occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Test Case 4: POST User with Missing Fields")
    print("=" * 60)
    result = test_post_user_missing_fields()
    print("=" * 60)
    exit(0 if result else 1)
