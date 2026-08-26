"""
Task 1 - Part 1: Five business questions about members and checkouts.
Each answer is printed with a short label so it can be copied into the write-up file.
"""

import sqlite3

DB_PATH = "Library Database"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("Q1: How much is each member borrowing? (per-member checkout count, including zero)")
print("=" * 60)
query1 = """
SELECT m.member_id, m.first_name, m.last_name, COUNT(c.checkout_id) AS total_checkouts
FROM members m
LEFT JOIN checkouts c ON m.member_id = c.member_id
GROUP BY m.member_id, m.first_name, m.last_name
ORDER BY total_checkouts DESC;
"""
cursor.execute(query1)
rows1 = cursor.fetchall()
for row in rows1:
    print(row)
print(f"Total members: {len(rows1)}")

print("\n" + "=" * 60)
print("Q2: Which books match a chosen author pattern?")
print("=" * 60)
# Pattern chosen: authors whose name starts with 'A'
# Change AUTHOR_PATTERN below if you want a different letter/pattern
AUTHOR_PATTERN = "A%"
query2 = """
SELECT book_id, title, author
FROM books
WHERE author LIKE ?;
"""
cursor.execute(query2, (AUTHOR_PATTERN,))
rows2 = cursor.fetchall()
for row in rows2:
    print(row)
print(f"Pattern used: author LIKE '{AUTHOR_PATTERN}'")

print("\n" + "=" * 60)
print("Q3: What are the 5 most popular books (most-borrowed titles)?")
print("=" * 60)
query3 = """
SELECT b.book_id, b.title, b.author, COUNT(c.checkout_id) AS times_borrowed
FROM checkouts c
JOIN books b ON c.book_id = b.book_id
GROUP BY b.book_id, b.title, b.author
ORDER BY times_borrowed DESC
LIMIT 5;
"""
cursor.execute(query3)
rows3 = cursor.fetchall()
for row in rows3:
    print(row)

print("\n" + "=" * 60)
print("Q4: Who are the 10 most active readers (most books borrowed)?")
print("=" * 60)
query4 = """
SELECT m.member_id, m.first_name, m.last_name, COUNT(c.checkout_id) AS total_checkouts
FROM members m
JOIN checkouts c ON m.member_id = c.member_id
GROUP BY m.member_id, m.first_name, m.last_name
ORDER BY total_checkouts DESC
LIMIT 10;
"""
cursor.execute(query4)
rows4 = cursor.fetchall()
for row in rows4:
    print(row)

print("\n" + "=" * 60)
print("Q5: Neighborhood activity further back in time (skip the 10 most recent)")
print("=" * 60)
# Neighborhood chosen: Maadi
# Change NEIGHBORHOOD below if you want a different one
NEIGHBORHOOD = "Maadi"
query5 = """
SELECT c.checkout_id, m.member_id, m.first_name, m.last_name, m.neighborhood,
       c.book_id, c.checkout_date
FROM checkouts c
JOIN members m ON c.member_id = m.member_id
WHERE m.neighborhood = ?
ORDER BY c.checkout_date DESC
LIMIT -1 OFFSET 10;
"""
cursor.execute(query5, (NEIGHBORHOOD,))
rows5 = cursor.fetchall()
for row in rows5:
    print(row)
print(f"Neighborhood used: {NEIGHBORHOOD}")

conn.close()
