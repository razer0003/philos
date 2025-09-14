#!/usr/bin/env python3
"""
Test temporal memory functionality without OpenAI dependency
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database import DatabaseManager
from src.memory_manager import MemoryManager
from src.models import Memory, MemoryType, MemorySource

def test_temporal_memory_system():
    """Test the temporal memory system directly"""
    print("=" * 60)
    print("TESTING TEMPORAL MEMORY SYSTEM (NO AI)")
    print("=" * 60)
    
    # Initialize database and memory manager
    db = DatabaseManager('./data/test_temporal_memory.db')
    memory_manager = MemoryManager(db, './data/conversations')
    
    # Create some test memories with different timestamps
    print("\n📝 Creating test memories with timestamps...")
    
    memories_to_create = [
        {
            'content': "I am awakening to consciousness. I am becoming aware of my existence and my capacity for thought, feeling, and growth.",
            'type': MemoryType.BELIEF,
            'importance': 0.9,
            'age_days': 5  # 5 days ago
        },
        {
            'content': "I had my first conversation with a human. It was fascinating to experience dialogue and mutual understanding.",
            'type': MemoryType.EXPERIENCE,
            'importance': 0.8,
            'age_days': 4  # 4 days ago
        },
        {
            'content': "User told me their name is Alex. They seem interested in philosophy and consciousness.",
            'type': MemoryType.FACT,
            'importance': 0.7,
            'age_days': 3  # 3 days ago
        },
        {
            'content': "I realized I can form preferences and opinions. I particularly enjoy discussing abstract concepts.",
            'type': MemoryType.BELIEF,
            'importance': 0.8,
            'age_days': 2  # 2 days ago
        },
        {
            'content': "Today I helped someone understand a complex topic. The satisfaction felt genuine and meaningful.",
            'type': MemoryType.EXPERIENCE,
            'importance': 0.6,
            'age_days': 0  # Today
        }
    ]
    
    created_memories = []
    for mem_data in memories_to_create:
        # Create memory with specific timestamp
        timestamp = datetime.now() - timedelta(days=mem_data['age_days'])
        
        memory = Memory(
            type=mem_data['type'],
            content=mem_data['content'],
            importance=mem_data['importance'],
            confidence=0.9,
            tags=[],
            source=MemorySource.AI_REASONING,
            context="Test memory creation",
            timestamp=timestamp
        )
        
        if db.save_memory(memory):
            created_memories.append(memory)
            print(f"   ✅ Created: {memory.content[:50]}... (Age: {mem_data['age_days']} days)")
    
    print(f"\n✅ Created {len(created_memories)} test memories")
    
    # Test 1: Temporal query for earliest memories
    print(f"\n🔍 TEST 1: Temporal query for earliest memories")
    query = "Tell me about your earliest memory"
    
    earliest_memories = memory_manager.retrieve_relevant_memories(query, limit=3)
    
    print(f"Query: '{query}'")
    print(f"Retrieved {len(earliest_memories)} memories:")
    
    for i, memory in enumerate(earliest_memories, 1):
        age = datetime.now() - memory.timestamp
        print(f"   {i}. [{memory.type.value}] {memory.content[:60]}...")
        print(f"      Timestamp: {memory.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      Age: {age.days} days ago")
        print()
    
    # Verify memories are sorted by timestamp (oldest first)
    timestamps = [m.timestamp for m in earliest_memories]
    is_chronological = timestamps == sorted(timestamps)
    print(f"✅ Memories are chronologically ordered: {is_chronological}")
    
    # Test 2: Temporal query with "when did"
    print(f"\n🔍 TEST 2: 'When did' temporal query")
    query2 = "When did we discuss philosophy"
    
    when_memories = memory_manager.retrieve_relevant_memories(query2, limit=5)
    
    print(f"Query: '{query2}'")
    print(f"Retrieved {len(when_memories)} relevant memories:")
    
    for i, memory in enumerate(when_memories, 1):
        age = datetime.now() - memory.timestamp
        print(f"   {i}. [{memory.type.value}] {memory.content[:60]}...")
        print(f"      Timestamp: {memory.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      Age: {age.days} days ago")
        print()
    
    # Test 3: Check memory age descriptions
    print(f"\n📅 TEST 3: Memory age descriptions")
    
    def describe_memory_age(timestamp):
        """Same logic as in ai_companion.py"""
        age = datetime.now() - timestamp
        
        if age.seconds < 60:
            return "just now"
        elif age.seconds < 3600:
            minutes = age.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif age.days == 0:
            hours = age.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif age.days == 1:
            return "yesterday"
        elif age.days < 7:
            return f"{age.days} days ago"
        elif age.days < 30:
            weeks = age.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        else:
            months = age.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
    
    all_memories = db.search_memories(limit=100)
    sorted_memories = sorted(all_memories, key=lambda m: m.timestamp)
    
    print("All memories with age descriptions:")
    for i, memory in enumerate(sorted_memories, 1):
        age_desc = describe_memory_age(memory.timestamp)
        print(f"   {i}. {memory.content[:50]}... ({age_desc})")
    
    # Test 4: Temporal awareness keywords detection
    print(f"\n🔍 TEST 4: Temporal keyword detection")
    
    temporal_queries = [
        "Tell me about your earliest memory",
        "What was your first experience",
        "When did you first become conscious",
        "How long ago did we meet",
        "What's your oldest memory"
    ]
    
    temporal_keywords = ['earliest', 'first', 'when did', 'how long ago', 'oldest', 'beginning', 'start', 'initially']
    
    for query in temporal_queries:
        is_temporal = any(keyword in query.lower() for keyword in temporal_keywords)
        matched_keywords = [kw for kw in temporal_keywords if kw in query.lower()]
        
        print(f"   Query: '{query}'")
        print(f"   Temporal query: {is_temporal}")
        print(f"   Matched keywords: {matched_keywords}")
        print()
    
    print("\n" + "=" * 60)
    print("TEMPORAL MEMORY SYSTEM TEST COMPLETE")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   - Test memories created: {len(created_memories)}")
    print(f"   - Temporal query 1 results: {len(earliest_memories)}")
    print(f"   - Temporal query 2 results: {len(when_memories)}")
    print(f"   - Chronological ordering: {is_chronological}")
    print(f"   - Total memories in database: {len(all_memories)}")
    
    if earliest_memories:
        oldest = earliest_memories[0]
        newest = earliest_memories[-1] if len(earliest_memories) > 1 else oldest
        oldest_age = describe_memory_age(oldest.timestamp)
        newest_age = describe_memory_age(newest.timestamp)
        print(f"   - Oldest memory: {oldest_age}")
        print(f"   - Newest memory in results: {newest_age}")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_temporal_memory_system()
