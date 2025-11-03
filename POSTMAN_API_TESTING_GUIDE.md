# Postman API Testing Guide

This guide provides all the information you need to test your Onboarding Tool API using Postman.

## Prerequisites

1. **Start the API server** by running:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
   The API will be available at: `http://127.0.0.1:8000`

2. **Install Postman** from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

## Base URL

```
http://127.0.0.1:8000
```

## API Endpoints Overview

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| GET | `/` | Health check | 200 |
| POST | `/users/` | Create a new user | 201 |
| GET | `/users/` | List all users | 200 |
| GET | `/users/{user_id}` | Get a specific user | 200 |
| PUT | `/users/{user_id}` | Replace/update entire user | 200 |
| PATCH | `/users/{user_id}` | Partially update user | 200 |
| DELETE | `/users/{user_id}` | Delete a user | 204 |

---

## 1. Health Check

**Method:** `GET`  
**URL:** `http://127.0.0.1:8000/`

**Headers:** None required

**Body:** None

**Expected Response (200 OK):**
```json
{
  "status": "ok",
  "message": "Onboarding API"
}
```

---

## 2. Create a New User (POST)

**Method:** `POST`  
**URL:** `http://127.0.0.1:8000/users/`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice.johnson@company.com",
  "role_id": 1,
  "start_date": "2025-11-01"
}
```

**Expected Response (201 Created):**
```json
{
  "first_name": "Alice",
  "last_name": "Johnson",
  "email": "alice.johnson@company.com",
  "role_id": 1,
  "start_date": "2025-11-01",
  "user_id": 3
}
```

**Error Cases:**

- **Duplicate Email (400 Bad Request):**
```json
{
  "detail": "Email already exists."
}
```

- **Invalid Email Format (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address"
    }
  ]
}
```

- **Missing Required Fields (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "first_name"],
      "msg": "Field required"
    }
  ]
}
```

---

## 3. List All Users (GET)

**Method:** `GET`  
**URL:** `http://127.0.0.1:8000/users/`

**Optional Query Parameters:**
- `skip` (integer): Number of records to skip (default: 0)
- `limit` (integer): Maximum number of records to return (default: 100)

**Example with parameters:**
```
http://127.0.0.1:8000/users/?skip=0&limit=10
```

**Headers:** None required

**Body:** None

**Expected Response (200 OK):**
```json
[
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@acme-corp.com",
    "role_id": 1,
    "start_date": "2024-01-15",
    "user_id": 1
  },
  {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@acme-corp.com",
    "role_id": 2,
    "start_date": "2024-02-01",
    "user_id": 2
  }
]
```

---

## 4. Get a Specific User (GET)

**Method:** `GET`  
**URL:** `http://127.0.0.1:8000/users/{user_id}`

**Example:**
```
http://127.0.0.1:8000/users/1
```

**Headers:** None required

**Body:** None

**Expected Response (200 OK):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@acme-corp.com",
  "role_id": 1,
  "start_date": "2024-01-15",
  "user_id": 1
}
```

**Error Cases:**

- **User Not Found (404 Not Found):**
```json
{
  "detail": "User not found."
}
```

---

## 5. Replace/Update Entire User (PUT)

**Method:** `PUT`  
**URL:** `http://127.0.0.1:8000/users/{user_id}`

**Example:**
```
http://127.0.0.1:8000/users/1
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "first_name": "John",
  "last_name": "Doe-Updated",
  "email": "john.doe.updated@acme-corp.com",
  "role_id": 3,
  "start_date": "2024-01-15"
}
```

**Expected Response (200 OK):**
```json
{
  "first_name": "John",
  "last_name": "Doe-Updated",
  "email": "john.doe.updated@acme-corp.com",
  "role_id": 3,
  "start_date": "2024-01-15",
  "user_id": 1
}
```

**Error Cases:**

- **User Not Found (404 Not Found):**
```json
{
  "detail": "User not found."
}
```

- **Email Already Exists (400 Bad Request):**
```json
{
  "detail": "Email already exists."
}
```

---

## 6. Partially Update User (PATCH)

**Method:** `PATCH`  
**URL:** `http://127.0.0.1:8000/users/{user_id}`

**Example:**
```
http://127.0.0.1:8000/users/1
```

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON) - Update only specific fields:**
```json
{
  "role_id": 5,
  "start_date": "2025-01-01"
}
```

**Note:** With PATCH, you only need to include the fields you want to update. Other fields remain unchanged.

**Expected Response (200 OK):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@acme-corp.com",
  "role_id": 5,
  "start_date": "2025-01-01",
  "user_id": 1
}
```

**Error Cases:**

- **User Not Found (404 Not Found):**
```json
{
  "detail": "User not found."
}
```

---

## 7. Delete a User (DELETE)

**Method:** `DELETE`  
**URL:** `http://127.0.0.1:8000/users/{user_id}`

**Example:**
```
http://127.0.0.1:8000/users/1
```

**Headers:** None required

**Body:** None

**Expected Response (204 No Content):**
- No body content
- Status code: 204

**Error Cases:**

- **User Not Found (404 Not Found):**
```json
{
  "detail": "User not found."
}
```

---

## Setting Up in Postman

### Step-by-Step Instructions:

1. **Create a New Collection:**
   - Open Postman
   - Click "New" → "Collection"
   - Name it "Onboarding API Tests"

2. **Set Base URL Variable:**
   - Click on the collection
   - Go to "Variables" tab
   - Add variable: `base_url` with value `http://127.0.0.1:8000`
   - Now you can use `{{base_url}}` in your requests

3. **Create Requests for Each Endpoint:**

   For each endpoint above:
   - Click "Add Request" in your collection
   - Set the HTTP method (GET, POST, PUT, PATCH, DELETE)
   - Enter the URL (use `{{base_url}}/users/` format)
   - Add headers if needed (Content-Type: application/json for POST, PUT, PATCH)
   - Add body content for POST, PUT, PATCH requests
   - Click "Send" to test

### Example Request Setup:

**Request Name:** Create User  
**Method:** POST  
**URL:** `{{base_url}}/users/`  
**Headers Tab:**
```
Key: Content-Type
Value: application/json
```
**Body Tab:**
- Select "raw"
- Select "JSON" from dropdown
- Paste the JSON body

---

## Testing Workflow Example

Here's a suggested order to test all functionality:

1. **GET /** - Verify API is running
2. **POST /users/** - Create a new user (save the `user_id`)
3. **GET /users/** - List all users (verify your new user appears)
4. **GET /users/{user_id}** - Get the specific user you created
5. **PATCH /users/{user_id}** - Update a field (e.g., role_id)
6. **PUT /users/{user_id}** - Replace all fields
7. **DELETE /users/{user_id}** - Delete the user
8. **GET /users/{user_id}** - Verify deletion (should return 404)

---

## Tips for Postman Testing

1. **Use Environment Variables:**
   - Store `base_url` as an environment variable
   - Store `user_id` from responses to use in subsequent requests
   - Example: In Tests tab, add: `pm.environment.set("user_id", pm.response.json().user_id);`

2. **Add Tests to Requests:**
   In the "Tests" tab of each request, add:
   ```javascript
   pm.test("Status code is 200", function () {
       pm.response.to.have.status(200);
   });
   
   pm.test("Response has user_id", function () {
       var jsonData = pm.response.json();
       pm.expect(jsonData).to.have.property('user_id');
   });
   ```

3. **Use Pre-request Scripts:**
   Generate unique emails automatically:
   ```javascript
   pm.variables.set("unique_email", "user" + Date.now() + "@test.com");
   ```
   Then in body use: `{{unique_email}}`

4. **Export Your Collection:**
   - Click "..." on your collection
   - Select "Export"
   - Save as JSON to share with team

---

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can test all endpoints directly in the browser using Swagger UI!

---

## Common Issues

1. **Connection Refused:** Make sure the API server is running
2. **404 Not Found:** Check that the base URL is correct
3. **422 Validation Error:** Check that all required fields are present and have correct data types
4. **400 Email Already Exists:** Use a unique email address for each test

---

## Sample Postman Collection JSON

You can import this directly into Postman:

```json
{
  "info": {
    "name": "Onboarding API Tests",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://127.0.0.1:8000"
    }
  ],
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/",
          "host": ["{{base_url}}"],
          "path": [""]
        }
      }
    },
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"first_name\": \"Alice\",\n  \"last_name\": \"Johnson\",\n  \"email\": \"alice.johnson@company.com\",\n  \"role_id\": 1,\n  \"start_date\": \"2025-11-01\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/users/",
          "host": ["{{base_url}}"],
          "path": ["users", ""]
        }
      }
    },
    {
      "name": "List Users",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/users/",
          "host": ["{{base_url}}"],
          "path": ["users", ""]
        }
      }
    },
    {
      "name": "Get User by ID",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/users/1",
          "host": ["{{base_url}}"],
          "path": ["users", "1"]
        }
      }
    },
    {
      "name": "Update User (PUT)",
      "request": {
        "method": "PUT",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"first_name\": \"John\",\n  \"last_name\": \"Doe-Updated\",\n  \"email\": \"john.updated@acme-corp.com\",\n  \"role_id\": 3,\n  \"start_date\": \"2024-01-15\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/users/1",
          "host": ["{{base_url}}"],
          "path": ["users", "1"]
        }
      }
    },
    {
      "name": "Partial Update User (PATCH)",
      "request": {
        "method": "PATCH",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"role_id\": 5\n}"
        },
        "url": {
          "raw": "{{base_url}}/users/1",
          "host": ["{{base_url}}"],
          "path": ["users", "1"]
        }
      }
    },
    {
      "name": "Delete User",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {
          "raw": "{{base_url}}/users/1",
          "host": ["{{base_url}}"],
          "path": ["users", "1"]
        }
      }
    }
  ]
}
```

Save this JSON to a file and import it into Postman using **File → Import**.
