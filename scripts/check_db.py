#!/usr/bin/env python3
import sqlite3
import os

db_path = './data/ai_companion.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('Tables in database:', [t[0] for t in tables])
    
    if any('memories' in str(t) for t in tables):
        cursor.execute('SELECT COUNT(*) FROM memories')
        count = cursor.fetchone()[0]
        print(f'\nTotal memories: {count}')
        
        cursor.execute('SELECT type, content, timestamp, importance FROM memories ORDER BY timestamp DESC LIMIT 10')
        memories = cursor.fetchall()
        
        print('\nRecent memories:')
        for i, (mem_type, content, timestamp, importance) in enumerate(memories, 1):
            print(f'{i}. [{mem_type}] {content[:60]}...')
            print(f'   Time: {timestamp}')
            print(f'   Importance: {importance}')
            print()
    
    conn.close()
else:
    print('Database not found')
