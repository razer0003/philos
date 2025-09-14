#!/usr/bin/env python3
"""
Test the memory system fixes for temporal queries
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.memory_manager import MemoryManager
from src.database import DatabaseManager

def test_memory_retrieval():
    """Test the enhanced memory retrieval for 'last discussion' queries"""
    
    print("=" * 60)
    print("TESTING MEMORY RETRIEVAL FIXES")
    print("=" * 60)
    
    # Initialize database and memory manager
    db = DatabaseManager('./data/ai_companion.db')
    memory_manager = MemoryManager(db, './data/conversations')
    
    # Test queries that should now work better
    test_queries = [
        "What's the last thing we talked about?",
        "What did we discuss most recently?", 
        "What was our last conversation about?",
        "What did we talk about before this?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: {query} ---")
        
        # Retrieve memories using the enhanced system
        memories = memory_manager.retrieve_relevant_memories(query, limit=5)
        
        print(f"Found {len(memories)} relevant memories:")
        for j, memory in enumerate(memories, 1):
            age_desc = describe_memory_age(memory.timestamp)
            print(f"  {j}. [{memory.type.value}] {memory.content[:70]}...")
            print(f"     Time: {age_desc} | Importance: {memory.importance:.2f}")
        
        print("-" * 40)

def describe_memory_age(timestamp):
    """Describe how old a memory is"""
    from datetime import datetime, timedelta
    
    age = datetime.now() - timestamp
    
    if age.total_seconds() < 60:
        return "just now"
    elif age.total_seconds() < 3600:
        minutes = int(age.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif age.days == 0:
        hours = int(age.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif age.days == 1:
        return "yesterday"
    elif age.days < 7:
        return f"{age.days} days ago"
    else:
        return f"{age.days} days ago"

if __name__ == "__main__":
    test_memory_retrieval()
