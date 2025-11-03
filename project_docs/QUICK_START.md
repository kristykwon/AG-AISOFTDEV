# Quick Start Guide - Onboarding Tool API

## ✅ Status: FIXED AND WORKING

Your API is now fully functional with the correct field names matching the database schema.

## 🚀 Running the Application

### Start the API Server:
```powershell
cd C:\Users\labadmin\Documents\AG-AISOFTDEV
python -m uvicorn app.main:app --reload
```

The API will be available at: http://127.0.0.1:8000

### View API Documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🧪 Running Tests

```powershell
# Run comprehensive test suite
python test_api_fix.py
```

Expected output: **8/8 tests passed ✅**

## 📊 API Endpoints

### Users Endpoints

| Method | Endpoint | Description | Example Body |
|--------|----------|-------------|--------------|
| GET | `/users/` | List all users | - |
| GET | `/users/{user_id}` | Get user by ID | - |
| POST | `/users/` | Create new user | See below |
| PUT | `/users/{user_id}` | Replace user | See below |
| PATCH | `/users/{user_id}` | Update user partially | See below |
| DELETE | `/users/{user_id}` | Delete user | - |

### Example Request Bodies

**Create User (POST):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "role_id": 1,
  "start_date": "2024-10-30"
}
```

**Update User (PATCH):**
```json
{
  "first_name": "Jane"
}
```

**Replace User (PUT):**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "email": "jane.smith@example.com",
  "role_id": 2,
  "start_date": "2024-11-01"
}
```

## 📝 Field Names Reference

**IMPORTANT:** Always use these exact field names:

| Field | Type | Description |
|-------|------|-------------|
| `user_id` | integer | Primary key (auto-generated) |
| `first_name` | string (max 50) | User's first name |
| `last_name` | string (max 50) | User's last name |
| `email` | string (max 100) | User's email (unique) |
| `role_id` | integer | Foreign key to roles table |
| `start_date` | string (YYYY-MM-DD) | User's start date |

## 🗃️ Database Information

**Location:** `artifacts/onboarding.db`  
**Backup:** `artifacts/onboarding_backup.db`

**Current Data:**
- 4 Roles (Engineer, Hiring Manager, HR Admin, IT Support)
- 4 Users (Alex Chen, Morgan Smith, Jamie Taylor, Riley Jordan)

## 🛠️ Utility Scripts

```powershell
# Check database schema
python check_db_schema.py

# Setup/verify test data
python setup_test_data.py

# Fix database issues (if needed)
python fix_database_schema.py
```

## 🧪 Testing with cURL

```powershell
# Get all users
curl http://127.0.0.1:8000/users/

# Get user by ID
curl http://127.0.0.1:8000/users/1

# Create user
curl -X POST http://127.0.0.1:8000/users/ `
  -H "Content-Type: application/json" `
  -d '{\"first_name\":\"Test\",\"last_name\":\"User\",\"email\":\"test@example.com\",\"role_id\":1,\"start_date\":\"2024-10-30\"}'

# Update user
curl -X PATCH http://127.0.0.1:8000/users/1 `
  -H "Content-Type: application/json" `
  -d '{\"first_name\":\"Updated\"}'

# Delete user
curl -X DELETE http://127.0.0.1:8000/users/5
```

## 🔍 Troubleshooting

### Issue: "Module not found" errors
```powershell
pip install fastapi uvicorn sqlalchemy pydantic email-validator
```

### Issue: Database errors
```powershell
# Fix the database schema
python fix_database_schema.py
```

### Issue: API not starting
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use a different port
python -m uvicorn app.main:app --reload --port 8001
```

## 📚 Next Steps

1. ✅ **API is working** - All field names fixed
2. ➡️ **Continue to Day 3 Lab 2** - Write test suite
3. ➡️ **Add more features** - Implement other endpoints (roles, tasks, etc.)
4. ➡️ **Frontend integration** - Connect React/Vue frontend
5. ➡️ **Deployment** - Deploy to production

## 📖 Related Documentation

- `plan.md` - Three approaches for fixing field inconsistencies
- `IMPLEMENTATION_SUMMARY.md` - Detailed implementation documentation
- `artifacts/schema.sql` - Database schema definition
- Lab notebook: `Labs/Day_03_Development_and_Coding/KK_D3_Lab1_AI_Driven_Backend_Development.ipynb`

---

**Status:** ✅ Ready for Development  
**Last Updated:** October 30, 2025  
**All Tests Passing:** 8/8 ✅
