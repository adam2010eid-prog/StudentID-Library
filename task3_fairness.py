"""
Task 3 - Step 1: Compare neighborhoods by member count and checkout count.
This is exploratory - it prints the numbers we need to write the Fairness Reflection.
"""

import pandas as pd
import sqlite3

# Member counts per neighborhood come from the ORIGINAL members table
# (every registered member, regardless of whether they've ever checked out a book)
conn = sqlite3.connect("Library Database")
members_df = pd.read_sql_query("SELECT * FROM members;", conn)
conn.close()

# Normalize neighborhood text the same way Task 2 did, so comparisons are fair.
# Also collapse any internal double spaces (e.g. "Nasr  City" -> "Nasr City"),
# which is a separate small inconsistency found while building this comparison.
members_df["neighborhood"] = (
    members_df["neighborhood"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

member_counts = members_df.groupby("neighborhood")["member_id"].count()
print("Members per neighborhood:")
print(member_counts)

# Checkout counts come from the CLEANED dataset from Task 2
checkouts_df = pd.read_csv("task2_cleaned_data.csv")
checkout_counts = checkouts_df.groupby("neighborhood")["checkout_id"].count()
print("\nCheckouts per neighborhood:")
print(checkout_counts)

# Combine into one side-by-side table
comparison = pd.DataFrame({
    "member_count": member_counts,
    "checkout_count": checkout_counts,
})
comparison["checkouts_per_member"] = (comparison["checkout_count"] / comparison["member_count"]).round(2)
comparison = comparison.sort_values("checkouts_per_member")

print("\n" + "=" * 60)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 60)
print(comparison)
