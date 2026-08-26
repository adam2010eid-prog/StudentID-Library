"""
Step 0: Explore the database structure before writing any queries.
Run this first so we know the table names and column names.
"""

import sqlite3

# Change this if your .db file has a different name
DB_PATH = "Library Database"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# List all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables found in the database:")
for table in tables:
    table_name = table[0]
    print(f"\n--- {table_name} ---")

    # Show column names and types for each table
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    for col in columns:
        # col format: (index, name, type, notnull, default_value, primary_key)
        print(f"  {col[1]} ({col[2]})")

    # Show a couple of sample rows so we understand the data shape
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
    sample_rows = cursor.fetchall()
    print("  Sample rows:")
    for row in sample_rows:
        print(f"    {row}")

conn.close()
