"""
Step 0b: Explore the other two sources (Book Catalog and Reading Kickoff Signups)
before writing the combination code.
"""

import json

print("=" * 60)
print("BOOK CATALOG (first 500 characters, raw)")
print("=" * 60)
with open("Book Catalog", "r", encoding="utf-8") as f:
    raw = f.read()
print(raw[:500])

print("\n" + "=" * 60)
print("BOOK CATALOG (parsed as JSON, structure check)")
print("=" * 60)
try:
    data = json.loads(raw)
    if isinstance(data, list):
        print(f"It's a list with {len(data)} items.")
        print("First item:")
        print(data[0])
    elif isinstance(data, dict):
        print("It's a dictionary with keys:")
        print(list(data.keys()))
except Exception as e:
    print(f"Could not parse as plain JSON: {e}")

print("\n" + "=" * 60)
print("READING KICKOFF SIGNUPS (first 1000 characters, raw HTML)")
print("=" * 60)
with open("Reading Kickoff Signups", "r", encoding="utf-8") as f:
    html_raw = f.read()
print(html_raw[:1000])
