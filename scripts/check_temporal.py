#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('./data/ai_companion.db')
cursor = conn.cursor()

# Check memories around 9:52 AM (epistemology discussion)
cursor.execute("SELECT type, content, timestamp, importance FROM memories WHERE timestamp LIKE '%2025-07-30T09:52%' ORDER BY timestamp DESC")
memories = cursor.fetchall()

print('Memories from 9:52 AM (epistemology discussion):')
for i, (mem_type, content, timestamp, importance) in enumerate(memories, 1):
    print(f'{i}. [{mem_type}] {content[:80]}...')
    print(f'   Time: {timestamp}')
    print(f'   Importance: {importance}')
    print()

# Also check what would be returned for "last thing we talked about"
print('\n' + '='*50)
print('What gets retrieved for "last thing we talked about":')

# Simulate the new temporal query logic
cursor.execute("SELECT type, content, timestamp, importance FROM memories WHERE type IN ('fact', 'opinion', 'preference', 'experience') AND content NOT LIKE 'I responded:%' AND content NOT LIKE 'Internal thought:%' ORDER BY timestamp DESC LIMIT 10")
recent_conversation = cursor.fetchall()

for i, (mem_type, content, timestamp, importance) in enumerate(recent_conversation, 1):
    print(f'{i}. [{mem_type}] {content[:80]}...')
    print(f'   Time: {timestamp}')
    print(f'   Importance: {importance}')
    print()

conn.close()
