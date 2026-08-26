"""
Task 2 - Step 2: Resolve the four data quality problems and save the cleaned dataset.
"""

import pandas as pd

INPUT_PATH = "task1_combined_data.csv"
OUTPUT_PATH = "task2_cleaned_data.csv"

df = pd.read_csv(INPUT_PATH)
print(f"Starting rows: {len(df)}")

# -----------------------------------------------------------------
# Problem 2: Remove true duplicate records (exact full-row matches)
# -----------------------------------------------------------------
before = len(df)
df = df.drop_duplicates(keep="first")
print(f"Removed {before - len(df)} true duplicate rows. Rows now: {len(df)}")

# -----------------------------------------------------------------
# Problem 4: Remove checkouts referencing a member_id that doesn't exist
# -----------------------------------------------------------------
import sqlite3
conn = sqlite3.connect("Library Database")
real_members = pd.read_sql_query("SELECT member_id FROM members;", conn)
conn.close()
real_member_ids = set(real_members["member_id"])

before = len(df)
df = df[df["member_id"].isin(real_member_ids)]
print(f"Removed {before - len(df)} rows with a non-existent member_id. Rows now: {len(df)}")

# -----------------------------------------------------------------
# Problem 3: Standardize inconsistent text values
# -----------------------------------------------------------------
# Neighborhood: strip whitespace and fix casing (Title Case)
df["neighborhood"] = df["neighborhood"].str.strip().str.title()

# Membership status: fix casing (Title Case) so Active/active become the same value
df["membership_status"] = df["membership_status"].str.strip().str.title()

print("\nNeighborhood values after cleanup:", sorted(df["neighborhood"].dropna().unique()))
print("Membership status values after cleanup:", sorted(df["membership_status"].dropna().unique()))

# -----------------------------------------------------------------
# Problem 1: Missing values, handled column by column
# -----------------------------------------------------------------
# grade: left as missing - no other source can tell us a member's real grade,
# so guessing a value would introduce false information.
#
# return_date: left as missing on purpose - a missing return_date means the
# book simply hasn't been returned yet (it's still checked out). This is
# meaningful information, not an error, so it must NOT be dropped or filled.
#
# publication_year: left as missing - the Book Catalog itself has gaps for
# some books, and there's no reliable way to recover the real year.
#
# first_name / last_name / neighborhood / membership_status: these were only
# missing for the 5 rows removed in Problem 4 (invalid member_id), so they
# should now show 0 missing values.

print("\nRemaining missing values per column after all fixes:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# -----------------------------------------------------------------
# Save the cleaned dataset
# -----------------------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)
print(f"\nSaved cleaned dataset to {OUTPUT_PATH}")
print(f"Final row count: {len(df)}")
