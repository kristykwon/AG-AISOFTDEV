# Field Inconsistency Resolution Plan

## Problem Summary

The FastAPI application (`app/main.py`) has field name mismatches with the actual SQLite database schema:

**Database Schema (from `artifacts/onboarding.db`):**
- Primary Key: `user_id` (not `id`)
- Fields: `first_name`, `last_name`, `email`, `role_id`, `start_date`

**Current `app/main.py` Issues:**
- SQLAlchemy model uses `id` instead of `user_id`
- Uses `name` instead of `first_name` and `last_name`
- Uses `role` (string) instead of `role_id` (integer foreign key)
- Uses `created_at` instead of `start_date`
- Missing critical fields: `first_name`, `last_name`, `role_id`, `start_date`

**Result:** GET requests fail with operational errors because the ORM is trying to access columns that don't exist in the database.

---

## Three Approaches to Resolve

### **Approach 1: Fix Python Code to Match Existing Database (RECOMMENDED)**

**Overview:** Update all Python files (`app/main.py` and any generated artifacts) to use the exact column names from the database schema.

**Pros:**
- Preserves existing database structure and any data
- Aligns with the lab's intent (schema.sql drives the design)
- No data migration required
- Respects foreign key relationships already in database

**Cons:**
- Requires manual code fixes
- Need to regenerate or manually update all three code files

**Implementation Steps:**
1. **Update SQLAlchemy Model in `app/main.py`:**
   ```python
   class User(Base):
       __tablename__ = "users"
       user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
       first_name = Column(String(50), nullable=False)
       last_name = Column(String(50), nullable=False)
       email = Column(String(100), nullable=False, unique=True, index=True)
       role_id = Column(Integer, nullable=False)
       start_date = Column(Date, nullable=False)
   ```

2. **Update Pydantic Models:**
   ```python
   class UserBase(BaseModel):
       first_name: str = Field(..., max_length=50)
       last_name: str = Field(..., max_length=50)
       email: EmailStr
       role_id: int
       start_date: date
   
   class UserRead(UserBase):
       user_id: int
       class Config:
           from_attributes = True  # Pydantic v2
   ```

3. **Update all endpoint code** to use `user_id` instead of `id`, and correct field names.

4. **Re-run notebook cells** with enhanced prompts that explicitly list the exact column names from the schema.

**Estimated Time:** 30-45 minutes

---

### **Approach 2: Regenerate Everything from Notebook with Stricter Prompts**

**Overview:** Re-execute the notebook cells (Challenge 1, 2, and 3) with enhanced prompts that include explicit field validation rules.

**Pros:**
- Leverages the AI-driven workflow as intended by the lab
- Tests the prompt engineering improvements
- Generates clean, consistent code from scratch
- Educational value in learning proper prompt engineering

**Cons:**
- May still produce incorrect code if LLM doesn't follow instructions
- Requires multiple iterations to validate output
- Generated files must be inspected before use

**Implementation Steps:**
1. **Enhance Cell 6 (Challenge 1) prompt:**
   - Add explicit field list: "The users table MUST have these exact fields: user_id (primary key), first_name, last_name, email, role_id, start_date"
   - Add validation: "Before generating code, list out each field name you will use"

2. **Enhance Cell 8 (Challenge 2) prompt:**
   - Add pre-flight instruction: "First, extract and list every column name from the schema"
   - Add post-generation validation: "Verify your generated model uses user_id not id"

3. **Enhance Cell 10 (Challenge 3) prompt:**
   - Add explicit mapping rules for each field
   - Include example query: `db.query(User).filter(User.user_id == user_id).first()`

4. **Execute cells 6, 8, and 10** in sequence and verify output after each.

5. **Test the generated `app/main.py`** with a simple GET request.

**Estimated Time:** 45-60 minutes (includes testing iterations)

---

### **Approach 3: Hybrid - Manual Fix + Database Migration Script**

**Overview:** Fix the Python code manually for immediate functionality, then create a migration script to handle future schema changes.

**Pros:**
- Immediate fix provides working API
- Migration script prepares for production scenarios
- Demonstrates real-world engineering practices
- Most robust long-term solution

**Cons:**
- Most time-intensive approach
- Requires understanding of database migrations
- Overkill for a lab exercise (but good for learning)

**Implementation Steps:**
1. **Manually fix `app/main.py`** (same as Approach 1, steps 1-3).

2. **Create `app/db_models.py`** as a separate module:
   ```python
   # Separate concerns: models in one file, API in another
   from sqlalchemy import Column, Integer, String, Date, ForeignKey
   from sqlalchemy.orm import declarative_base, relationship
   
   Base = declarative_base()
   
   class User(Base):
       __tablename__ = "users"
       user_id = Column(Integer, primary_key=True, autoincrement=True)
       first_name = Column(String(50), nullable=False)
       last_name = Column(String(50), nullable=False)
       email = Column(String(100), nullable=False, unique=True)
       role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
       start_date = Column(Date, nullable=False)
   
   class Role(Base):
       __tablename__ = "roles"
       role_id = Column(Integer, primary_key=True, autoincrement=True)
       role_name = Column(String(50), nullable=False, unique=True)
   ```

3. **Import models in `app/main.py`:**
   ```python
   from app.db_models import User, Role, Base, engine, SessionLocal
   ```

4. **Create `migrations/verify_schema.py`** script:
   ```python
   # Script to verify database schema matches ORM models
   import sqlite3
   from app.db_models import Base
   
   def verify_schema():
       # Compare database columns with ORM model attributes
       # Raise warnings for mismatches
       pass
   ```

5. **Add schema validation** to application startup.

**Estimated Time:** 60-90 minutes

---

## Recommendation

**For immediate success in the lab: Use Approach 1**
- Fastest path to a working application
- Teaches manual integration skills (key learning objective)
- Aligns with lab's "senior developer integration" narrative

**For learning prompt engineering: Use Approach 2**
- Better understanding of AI limitations
- Practice iterative prompt refinement
- More aligned with "AI-Driven Development" theme

**For real-world preparation: Use Approach 3**
- Industry best practices
- Separation of concerns
- Production-ready architecture

---

## Quick Decision Matrix

| Criteria | Approach 1 | Approach 2 | Approach 3 |
|----------|-----------|-----------|-----------|
| Time to Working API | ⭐⭐⭐ (30 min) | ⭐⭐ (45-60 min) | ⭐ (60-90 min) |
| Learning Value | ⭐⭐ (Integration) | ⭐⭐⭐ (Prompt Eng.) | ⭐⭐⭐ (Best Practices) |
| Lab Alignment | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Production Ready | ⭐ | ⭐ | ⭐⭐⭐ |
| Risk of Failure | Low | Medium | Low |

---

## Next Steps

1. **Choose your approach** based on time available and learning goals
2. **Backup current files** before making changes
3. **Follow implementation steps** for chosen approach
4. **Test with simple GET request**: `curl http://localhost:8000/users/`
5. **Verify data alignment** with database using the check script
6. **Proceed to next lab** once GET requests return data successfully

---

*Generated: October 30, 2025*
*Context: Day 3 Lab 1 - AI-Driven Backend Development*
