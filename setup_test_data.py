"""
Setup script to ensure test data exists in the database.
This script adds roles to the roles table if they don't exist.
"""

import sqlite3
import os

DB_PATH = "artifacts/onboarding.db"

def setup_roles():
    """Ensure roles exist in the database."""
    print("Setting up test data...")
    
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if roles table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='roles'")
        if not cursor.fetchone():
            print("Error: roles table does not exist")
            return False
        
        # Check existing roles
        cursor.execute("SELECT role_id, role_name FROM roles")
        existing_roles = cursor.fetchall()
        
        if existing_roles:
            print("Existing roles:")
            for role_id, role_name in existing_roles:
                print(f"  - {role_id}: {role_name}")
        else:
            print("No roles found. Adding default roles...")
            
            # Insert default roles
            default_roles = [
                (1, "New Hire"),
                (2, "Manager"),
                (3, "HR Admin"),
                (4, "IT Support")
            ]
            
            for role_id, role_name in default_roles:
                try:
                    cursor.execute(
                        "INSERT INTO roles (role_id, role_name) VALUES (?, ?)",
                        (role_id, role_name)
                    )
                    print(f"  ✓ Added role: {role_id} - {role_name}")
                except sqlite3.IntegrityError:
                    print(f"  - Role {role_id} already exists")
            
            conn.commit()
            print("✓ Default roles added successfully")
        
        return True
        
    except Exception as e:
        print(f"Error setting up roles: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

def show_database_info():
    """Display information about the database."""
    print("\n" + "="*60)
    print("Database Information")
    print("="*60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables in database:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} rows")
    
    # Show users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count > 0:
        print(f"\nSample users:")
        cursor.execute("SELECT user_id, first_name, last_name, email FROM users LIMIT 3")
        for row in cursor.fetchall():
            print(f"  - ID {row[0]}: {row[1]} {row[2]} ({row[3]})")
    
    conn.close()
    print("="*60 + "\n")

if __name__ == "__main__":
    if setup_roles():
        show_database_info()
        print("✓ Setup complete! You can now run the tests.")
    else:
        print("✗ Setup failed. Please check the errors above.")
