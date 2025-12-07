#!/usr/bin/env python3
"""
Database initialization script for HonestBallot voting app
This script initializes the local SQLite database with demo data
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.storage.database import init_demo_data


def main():
    """Initialize the database"""
    print("Initializing HonestBallot Local Database...")
    print("-" * 50)
    
    db = init_demo_data()
    
    print("✅ Database initialized successfully!")
    print("\nDemo Users Created:")
    print("-" * 50)
    
    users = db.get_all_users()
    for user in users:
        print(f"  ID: {user[0]}")
        print(f"  Username: {user[1]}")
        print(f"  Email: {user[2]}")
        print(f"  Role: {user[3]}")
        print()
    
    print("-" * 50)
    print("✅ All 5 demo users created with password: password123")
    print("\nYou can now run: python main.py")
    
    db.close()


if __name__ == "__main__":
    main()
