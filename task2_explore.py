"""
Task 2 - Step 1: Explore the four data quality problems before fixing anything.
This script does NOT modify the data - it only reports what's wrong, where,
and how much, so we can decide how to handle each issue.
"""

import pandas as pd
import sqlite3

INPUT_PATH = "task1_combined_data.csv"

df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df)} rows, {len(df.columns)} columns.\n")

# -----------------------------------------------------------------
# Problem 1: Missing values, column by column
# -----------------------------------------------------------------
print("=" * 60)
print("PROBLEM 1: Missing values per column")
print("=" * 60)
missing_counts = df.isnull().sum()
missing_counts = missing_counts[missing_counts > 0]
print(missing_counts)
print()

# -----------------------------------------------------------------
# Problem 2: Duplicate records
# -----------------------------------------------------------------
print("=" * 60)
print("PROBLEM 2: Duplicate records")
print("=" * 60)
# True duplicates: every column matches exactly
exact_dupes = df[df.duplicated(keep=False)]
print(f"Exact full-row duplicates: {len(exact_dupes)} rows involved")
if len(exact_dupes) > 0:
    print(exact_dupes.sort_values(by=list(df.columns)).head(10))

# Also check duplicates based only on checkout_id (should be unique)
checkout_id_dupes = df[df.duplicated(subset=["checkout_id"], keep=False)]
print(f"\nRows sharing the same checkout_id: {len(checkout_id_dupes)}")
if len(checkout_id_dupes) > 0:
    print(checkout_id_dupes.sort_values(by="checkout_id").head(10))
print()

# -----------------------------------------------------------------
# Problem 3: Inconsistent text values
# -----------------------------------------------------------------
print("=" * 60)
print("PROBLEM 3: Inconsistent text values")
print("=" * 60)
print("Unique values in 'neighborhood':")
print(df["neighborhood"].dropna().unique())
print("\nUnique values in 'membership_status':")
print(df["membership_status"].dropna().unique())
print("\nUnique values in 'genre' (checking just in case):")
print(df["genre"].dropna().unique())
print()

# -----------------------------------------------------------------
# Problem 4: member_id values that don't exist among registered members
# -----------------------------------------------------------------
print("=" * 60)
print("PROBLEM 4: Checkouts referencing a non-existent member_id")
print("=" * 60)
conn = sqlite3.connect("Library Database")
real_members = pd.read_sql_query("SELECT member_id FROM members;", conn)
conn.close()

real_member_ids = set(real_members["member_id"])
invalid_rows = df[~df["member_id"].isin(real_member_ids)]
print(f"Rows with a member_id not found in the members table: {len(invalid_rows)}")
if len(invalid_rows) > 0:
    print(invalid_rows[["checkout_id", "member_id", "first_name", "last_name", "source"]])
