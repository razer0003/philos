#!/usr/bin/env python3
"""
Test the neural data sharing fixes
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

def test_neural_data_sharing():
    """Test neural data sharing between components"""
    print("🧪 Testing Neural Data Sharing")
    print("=" * 50)
    
    try:
        # Test neural data store
        from neural.neural_data_store import get_neural_data_store
        data_store = get_neural_data_store()
        
        # Test updating computation data
        data_store.update_computation({
            "step_name": "test_computation",
            "computation_type": "test",
            "output_value": "test_output",
            "metadata": {"test": True}
        })
        print("✅ Computation data updated")
        
        # Test updating emotional state
        data_store.update_emotional_state({
            "happiness": 0.7,
            "curiosity": 0.8,
            "attachment": 0.6
        })
        print("✅ Emotional state updated")
        
        # Test getting data
        neural_data = data_store.get_data()
        print(f"✅ Neural data retrieved: {len(neural_data['recent_computations'])} computations")
        
        # Test database fixes
        from src.database import DatabaseManager
        from src.models import Memory, MemoryType, MemorySource
        
        db = DatabaseManager("test_neural.db")
        db.init_database()
        
        # Create and save memory
        memory = Memory(
            type=MemoryType.EXPERIENCE,
            content="Test memory for neural system",
            importance=0.8,
            confidence=0.9,
            emotional_intensity=0.7,
            source=MemorySource.USER_INPUT
        )
        
        success = db.save_memory(memory)
        if success:
            print("✅ Memory with emotional_intensity saved")
        else:
            print("❌ Memory save failed")
            return False
        
        # Test memory retrieval
        retrieved = db.get_memory(memory.id)
        if retrieved and retrieved.emotional_intensity == 0.7:
            print("✅ Memory with emotional_intensity retrieved correctly")
        else:
            print("❌ Memory retrieval failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Neural data sharing test PASSED!")
    return True

if __name__ == "__main__":
    success = test_neural_data_sharing()
    if not success:
        exit(1)
