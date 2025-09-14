#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('./data/ai_companion.db')
cursor = conn.cursor()

# Search for memories containing epistemology or minecraft
cursor.execute("SELECT type, content, timestamp, importance FROM memories WHERE content LIKE '%epistemology%' OR content LIKE '%minecraft%' ORDER BY timestamp DESC")
memories = cursor.fetchall()

print('Memories about epistemology/minecraft:')
for i, (mem_type, content, timestamp, importance) in enumerate(memories, 1):
    print(f'{i}. [{mem_type}] {content[:100]}...')
    print(f'   Time: {timestamp}')
    print(f'   Importance: {importance}')
    print()

# Also check for recent conversation about favorite topics
cursor.execute("SELECT type, content, timestamp, importance FROM memories WHERE content LIKE '%favorite%' OR content LIKE '%topic%' ORDER BY timestamp DESC LIMIT 5")
fav_memories = cursor.fetchall()

print('\nMemories about favorites/topics:')
for i, (mem_type, content, timestamp, importance) in enumerate(fav_memories, 1):
    print(f'{i}. [{mem_type}] {content[:100]}...')
    print(f'   Time: {timestamp}')
    print(f'   Importance: {importance}')
    print()

conn.close()
