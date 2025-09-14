#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('./data/ai_companion.db')
cursor = conn.cursor()

# Get column info
cursor.execute("PRAGMA table_info(memories)")
columns = cursor.fetchall()
print("Column info (cid, name, type, notnull, dflt_value, pk):")
for col in columns:
    print(f"  {col}")

# Get a sample row to see the actual data structure
cursor.execute("SELECT * FROM memories LIMIT 1")
sample = cursor.fetchone()
if sample:
    print(f"\nSample row ({len(sample)} columns):")
    for i, value in enumerate(sample):
        col_name = columns[i][1] if i < len(columns) else f"col_{i}"
        print(f"  {i}: {col_name} = {type(value).__name__}({repr(value)})")

conn.close()
