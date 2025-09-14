#!/usr/bin/env python3
"""
Test database and memory fixes
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_memory_database():
    """Test memory database with emotional_intensity field"""
    print("🧪 Testing Memory Database with Emotional Intensity")
    print("=" * 60)
    
    try:
        from src.database import DatabaseManager
        from src.models import Memory, MemoryType, MemorySource
        
        # Initialize database
        db = DatabaseManager("test_memories.db")
        db.init_database()
        print("✅ Database initialized")
        
        # Create memory with emotional_intensity
        memory = Memory(
            type=MemoryType.EXPERIENCE,
            content="Test memory with emotional intensity",
            importance=0.8,
            confidence=0.9,
            emotional_intensity=0.7,
            source=MemorySource.USER_INPUT
        )
        
        # Save memory
        success = db.save_memory(memory)
        if success:
            print("✅ Memory saved successfully")
        else:
            print("❌ Memory save failed")
            return False
        
        # Retrieve memory
        retrieved_memory = db.get_memory(memory.id)
        if retrieved_memory:
            print(f"✅ Memory retrieved: emotional_intensity = {retrieved_memory.emotional_intensity}")
        else:
            print("❌ Memory retrieval failed")
            return False
        
        # Test memory manager
        from src.memory_manager import MemoryManager
        memory_manager = MemoryManager(db, "conversations")
        
        memories = memory_manager.retrieve_relevant_memories("test", limit=3)
        print(f"✅ Memory manager retrieval: {len(memories)} memories found")
        
        # Test neural monitor memory activation
        from src.neural_monitor import NeuralStateMonitor
        neural_monitor = NeuralStateMonitor()
        
        if memories:
            for i, mem in enumerate(memories[:2]):
                try:
                    neural_monitor.log_memory_activation(
                        memory_id=str(mem.id),
                        similarity_score=0.8 - (i * 0.1),
                        emotional_weight=mem.emotional_intensity,
                        activation_strength=mem.importance * (0.9 - i * 0.1),
                        memory_age_factor=max(0.1, 1.0 - i * 0.01),  # Fixed version
                        content_preview=mem.content[:100]
                    )
                    print(f"✅ Neural memory activation logged for memory {i+1}")
                except Exception as e:
                    print(f"❌ Neural activation failed for memory {i+1}: {e}")
                    return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Memory database test PASSED!")
    return True

if __name__ == "__main__":
    success = test_memory_database()
    if not success:
        exit(1)
