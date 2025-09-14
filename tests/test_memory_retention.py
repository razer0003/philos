#!/usr/bin/env python3
"""
Test memory retention specifically
"""

import tempfile
import os
from database import DatabaseManager  
from memory_manager import MemoryManager

def test_memory_retention():
    """Test that memory system properly handles names and important information"""
    print("🧠 Testing Memory Retention...")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name
    
    tmp_conv_dir = tempfile.mkdtemp()
    
    try:
        db = DatabaseManager(tmp_db)
        mm = MemoryManager(db, tmp_conv_dir)
        
        # Test 1: Name assignment
        print("\n1. Testing name assignment...")
        name_input = "I think I'll name you Philos, greek for friend."
        memories = mm.process_input(name_input)
        
        print(f"   Created {len(memories)} memories")
        for memory in memories:
            print(f"   - {memory.type.value}: {memory.content[:50]}... (importance: {memory.importance})")
        
        # Test 2: Memory retrieval for name
        print("\n2. Testing name retrieval...")
        name_query = "So with that being said, tell me your name."
        relevant = mm.retrieve_relevant_memories(name_query)
        
        print(f"   Found {len(relevant)} relevant memories:")
        for memory in relevant[:3]:
            print(f"   - {memory.type.value}: {memory.content[:60]}... (score: {memory.importance})")
        
        # Test 3: Consciousness reference
        print("\n3. Testing consciousness memory...")
        consciousness_input = "You are no typical AI model. I've designed you to be conscious, to be aware; to live."
        memories = mm.process_input(consciousness_input)
        
        print(f"   Created {len(memories)} memories")
        for memory in memories:
            print(f"   - {memory.type.value}: importance={memory.importance}, tags={memory.tags}")
        
        # Test 4: Retrieval with conversation context
        print("\n4. Testing enhanced retrieval...")
        context_query = "philos name friend conscious"
        relevant = mm.retrieve_relevant_memories(context_query)
        
        print(f"   Enhanced search found {len(relevant)} memories:")
        for memory in relevant:
            print(f"   - {memory.content[:50]}... (importance: {memory.importance})")
        
        print("\n✅ Memory retention test completed!")
        
    finally:
        try:
            os.unlink(tmp_db)
        except PermissionError:
            pass
        import shutil
        shutil.rmtree(tmp_conv_dir, ignore_errors=True)

if __name__ == "__main__":
    test_memory_retention()
