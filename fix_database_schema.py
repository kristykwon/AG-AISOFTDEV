"""
Fix the database schema to use proper SQLite autoincrement for primary keys.
SERIAL is not a native SQLite type, so we need to recreate tables with INTEGER PRIMARY KEY AUTOINCREMENT.
"""

import sqlite3
import os

DB_PATH = "artifacts/onboarding.db"

def fix_database():
    """Fix the database schema to properly handle autoincrement primary keys."""
    print("Backing up and fixing database schema...")
    
    # Backup the database first
    import shutil
    backup_path = "artifacts/onboarding_backup.db"
    if os.path.exists(DB_PATH):
        shutil.copy(DB_PATH, backup_path)
        print(f"✓ Database backed up to {backup_path}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Fix roles table
        print("\nFixing roles table...")
        
        # Get existing data
        cursor.execute("SELECT role_name FROM roles ORDER BY rowid")
        roles_data = cursor.fetchall()
        
        # Drop and recreate table
        cursor.execute("DROP TABLE IF EXISTS roles_old")
        cursor.execute("ALTER TABLE roles RENAME TO roles_old")
        
        cursor.execute("""
        CREATE TABLE roles (
            role_id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name VARCHAR(50) NOT NULL UNIQUE
        )
        """)
        
        # Reinsert data with proper IDs
        for idx, (role_name,) in enumerate(roles_data, 1):
            cursor.execute("INSERT INTO roles (role_id, role_name) VALUES (?, ?)", (idx, role_name))
        
        cursor.execute("DROP TABLE roles_old")
        print(f"✓ Roles table fixed with {len(roles_data)} roles")
        
        # Fix users table
        print("\nFixing users table...")
        
        # Get existing data (note: rowid is SQLite's internal ID)
        cursor.execute("""
        SELECT rowid, first_name, last_name, email, role_id, start_date 
        FROM users 
        ORDER BY rowid
        """)
        users_data = cursor.fetchall()
        
        # Drop foreign key constraints temporarily and recreate table
        cursor.execute("PRAGMA foreign_keys = OFF")
        
        cursor.execute("DROP TABLE IF EXISTS users_old")
        cursor.execute("ALTER TABLE users RENAME TO users_old")
        
        cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            role_id INTEGER NOT NULL,
            start_date DATE NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE CASCADE
        )
        """)
        
        # Reinsert data with proper IDs using the rowid as the new user_id
        for user_data in users_data:
            rowid, first_name, last_name, email, role_id, start_date = user_data
            cursor.execute("""
            INSERT INTO users (user_id, first_name, last_name, email, role_id, start_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (rowid, first_name, last_name, email, role_id, start_date))
        
        cursor.execute("DROP TABLE users_old")
        cursor.execute("PRAGMA foreign_keys = ON")
        print(f"✓ Users table fixed with {len(users_data)} users")
        
        # Fix other tables that reference users
        print("\nFixing task_assignments table...")
        cursor.execute("SELECT COUNT(*) FROM task_assignments")
        count = cursor.fetchone()[0]
        if count > 0:
            # This table references users, but since we preserved the user_ids using rowid, references should still work
            print(f"✓ Task assignments table has {count} records (preserved)")
        
        conn.commit()
        
        # Verify the fix
        print("\n" + "="*60)
        print("Verification:")
        print("="*60)
        
        cursor.execute("SELECT role_id, role_name FROM roles")
        print("\nRoles:")
        for role in cursor.fetchall():
            print(f"  - ID {role[0]}: {role[1]}")
        
        cursor.execute("SELECT user_id, first_name, last_name, email, role_id FROM users")
        print("\nUsers:")
        for user in cursor.fetchall():
            print(f"  - ID {user[0]}: {user[1]} {user[2]} (role_id={user[4]})")
        
        print("\n✓ Database schema fixed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing database: {str(e)}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if fix_database():
        print("\n✓ You can now start the API and run tests!")
    else:
        print("\n✗ Failed to fix database. Check the errors above.")
