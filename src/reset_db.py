import os
import sqlite3
from db import create_table
from data_generator import generate_synthetic_data

def reset_database(db_name="golfers.db"):
    # Remove existing database if it exists
    if os.path.exists(db_name):
        os.remove(db_name)
        print(f"Deleted old database: {db_name}")
    else:
        print("No existing database found — creating a new one.")

    # Recreate the database structure
    conn = sqlite3.connect(db_name)
    create_table()
    conn.close()
    print("Created new golfers table.")

    # Regenerate synthetic data
    generate_synthetic_data()
    print("Added new synthetic golfers (50 total).")

if __name__ == "__main__":
    reset_database()
