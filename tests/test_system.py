#!/usr/bin/env python3
"""
Test script to verify AI Companion components work
"""

import tempfile
import os
import sys
from pathlib import Path

def test_models():
    """Test data models"""
    print("Testing models...")
    from models import Memory, PersonalityTrait, MemoryType, MemorySource
    
    # Test memory creation
    memory = Memory(
        type=MemoryType.PREFERENCE,
        content="Test memory content",
        importance=0.7,
        confidence=0.8,
        tags=["test"],
        source=MemorySource.USER_INPUT
    )
    
    assert memory.content == "Test memory content"
    assert memory.type == MemoryType.PREFERENCE
    print("✅ Models test passed")

def test_database():
    """Test database functionality"""
    print("Testing database...")
    from database import DatabaseManager
    from models import Memory, MemoryType, MemorySource
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_path = tmp.name
    
    try:
        db = DatabaseManager(tmp_path)
        
        # Test memory save/retrieve
        memory = Memory(
            type=MemoryType.FACT,
            content="Database test memory",
            importance=0.6,
            confidence=0.9,
            tags=["database", "test"],
            source=MemorySource.USER_INPUT
        )
        
        success = db.save_memory(memory)
        assert success, "Failed to save memory"
        
        retrieved = db.get_memory(memory.id)
        assert retrieved is not None, "Failed to retrieve memory"
        assert retrieved.content == memory.content
        
        print("✅ Database test passed")
    
    finally:
        try:
            os.unlink(tmp_path)
        except PermissionError:
            pass  # Windows sometimes locks the file

def test_memory_manager():
    """Test memory manager"""
    print("Testing memory manager...")
    from database import DatabaseManager
    from memory_manager import MemoryManager
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name
    
    tmp_conv_dir = tempfile.mkdtemp()
    
    try:
        db = DatabaseManager(tmp_db)
        mm = MemoryManager(db, tmp_conv_dir)
        
        # Test input processing
        memories = mm.process_input("I love programming in Python")
        assert len(memories) > 0, "No memories created from input"
        
        # Test memory retrieval
        relevant = mm.retrieve_relevant_memories("programming")
        assert len(relevant) > 0, "No relevant memories found"
        
        print("✅ Memory manager test passed")
    
    finally:
        try:
            os.unlink(tmp_db)
        except PermissionError:
            pass  # Windows sometimes locks the file
        import shutil
        shutil.rmtree(tmp_conv_dir)

def test_personality_engine():
    """Test personality engine"""
    print("Testing personality engine...")
    from database import DatabaseManager
    from memory_manager import MemoryManager
    from personality_engine import PersonalityEngine
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        tmp_db = tmp.name
    
    tmp_conv_dir = tempfile.mkdtemp()
    
    try:
        db = DatabaseManager(tmp_db)
        mm = MemoryManager(db, tmp_conv_dir)
        pe = PersonalityEngine(db, mm)
        
        # Test personality initialization
        assert pe.personality is not None
        assert len(pe.personality.traits) > 0
        
        # Test personality update
        updates = pe.update_personality_from_interaction(
            "I'm curious about AI", 
            "That's fascinating! I share your curiosity."
        )
        
        # Should have some form of response
        assert isinstance(updates, list)
        
        print("✅ Personality engine test passed")
    
    finally:
        try:
            os.unlink(tmp_db)
        except PermissionError:
            pass  # Windows sometimes locks the file
        import shutil
        shutil.rmtree(tmp_conv_dir)

def main():
    """Run all tests"""
    print("🧪 Running AI Companion Tests")
    print("=" * 40)
    
    try:
        test_models()
        test_database()
        test_memory_manager()
        test_personality_engine()
        
        print("\n🎉 All tests passed!")
        print("\nThe AI Companion system is working correctly.")
        print("You can now:")
        print("1. Add your OpenAI API key to .env")
        print("2. Run 'python example.py' for a full demo")
        print("3. Run 'python ai_companion.py' for direct usage")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
