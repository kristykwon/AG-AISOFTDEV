# Field Mapping Reference

## ❌ Before (BROKEN) vs ✅ After (FIXED)

This document shows exactly what was changed to fix the field name inconsistencies.

---

## SQLAlchemy Model Changes

### ❌ BEFORE (Broken):
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)                    # WRONG
    name = Column(String, nullable=False)                                  # WRONG
    email = Column(String, nullable=False, unique=True, index=True)
    role = Column(String, nullable=False)                                  # WRONG
    created_at = Column(DateTime, nullable=False, server_default=...)      # WRONG
```

### ✅ AFTER (Fixed):
```python
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # ✓
    first_name = Column(String(50), nullable=False)                              # ✓
    last_name = Column(String(50), nullable=False)                               # ✓
    email = Column(String(100), nullable=False, unique=True, index=True)
    role_id = Column(Integer, nullable=False)                                    # ✓
    start_date = Column(String, nullable=False)                                  # ✓
```

---

## Pydantic Model Changes

### ❌ BEFORE (Broken):
```python
class UserBase(BaseModel):
    name: str = Field(..., max_length=255)        # WRONG
    email: EmailStr
    role: str                                      # WRONG

class UserRead(UserBase):
    id: int                                        # WRONG
    created_at: datetime                           # WRONG
    
    class Config:
        orm_mode = True
```

### ✅ AFTER (Fixed):
```python
class UserBase(BaseModel):
    first_name: str = Field(..., max_length=50)   # ✓
    last_name: str = Field(..., max_length=50)    # ✓
    email: EmailStr
    role_id: int                                   # ✓
    start_date: str                                # ✓

class UserRead(UserBase):
    user_id: int                                   # ✓
    
    class Config:
        from_attributes = True  # Pydantic v2
```

---

## Endpoint Changes

### ❌ BEFORE (Broken):
```python
@app.post("/users/")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user_in.name,           # WRONG
        email=user_in.email,
        role=user_in.role            # WRONG
    )
    # ...

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()  # WRONG
    # ...
```

### ✅ AFTER (Fixed):
```python
@app.post("/users/")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        first_name=user_in.first_name,    # ✓
        last_name=user_in.last_name,      # ✓
        email=user_in.email,
        role_id=user_in.role_id,          # ✓
        start_date=user_in.start_date     # ✓
    )
    # ...

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()  # ✓
    # ...
```

---

## Complete Field Mapping Table

| Database Column | Old (Wrong) | New (Correct) | Type | Notes |
|----------------|-------------|---------------|------|-------|
| `user_id` | `id` | `user_id` | INTEGER | Primary key |
| `first_name` | `name` (part) | `first_name` | VARCHAR(50) | Split from name |
| `last_name` | `name` (part) | `last_name` | VARCHAR(50) | Split from name |
| `email` | `email` ✓ | `email` ✓ | VARCHAR(100) | No change |
| `role_id` | `role` | `role_id` | INTEGER | FK to roles |
| `start_date` | `created_at` | `start_date` | DATE | Different field |

---

## Request/Response Changes

### ❌ BEFORE (Broken Request):
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "Engineer"
}
```

**Error:** `no such column: User.id`

### ✅ AFTER (Fixed Request):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "role_id": 1,
  "start_date": "2024-10-30"
}
```

**Success:** `201 Created`

### ✅ Response Format:
```json
{
  "user_id": 5,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "role_id": 1,
  "start_date": "2024-10-30"
}
```

---

## Database Schema (Reference)

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,              -- Use: user_id (not id)
    first_name VARCHAR(50) NOT NULL,         -- Use: first_name (not name)
    last_name VARCHAR(50) NOT NULL,          -- Use: last_name (not name)
    email VARCHAR(100) NOT NULL UNIQUE,      -- Use: email ✓
    role_id INT NOT NULL,                    -- Use: role_id (not role)
    start_date DATE NOT NULL,                -- Use: start_date (not created_at)
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
```

---

## Common Mistakes to Avoid

### ❌ Don't Do This:
```python
# Using wrong field names
user = User(name="John Doe", role="Engineer")

# Querying with wrong field
db.query(User).filter(User.id == 1)

# Response model with wrong fields
{"id": 1, "name": "John", "role": "Engineer"}
```

### ✅ Do This Instead:
```python
# Using correct field names
user = User(first_name="John", last_name="Doe", role_id=1, start_date="2024-10-30")

# Querying with correct field
db.query(User).filter(User.user_id == 1)

# Response model with correct fields
{"user_id": 1, "first_name": "John", "last_name": "Doe", "role_id": 1, "start_date": "2024-10-30"}
```

---

## Validation Checklist

When adding new code, verify:

- [ ] Using `user_id` not `id`
- [ ] Using `first_name` and `last_name` separately (not combined `name`)
- [ ] Using `role_id` (integer) not `role` (string)
- [ ] Using `start_date` not `created_at`
- [ ] All field names match the database schema exactly
- [ ] Pydantic models use `from_attributes = True` for ORM compatibility

---

**Quick Reference:** Always check `artifacts/schema.sql` for the authoritative field names!

**Test Command:** `python test_api_fix.py` - Should show 8/8 tests passing ✅
