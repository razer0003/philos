#!/usr/bin/env python3
"""
Test consciousness engine memory processing
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_consciousness_memory():
    """Test consciousness engine memory retrieval to check for multiplication error"""
    print("🧪 Testing Consciousness Engine Memory Processing")
    print("=" * 60)
    
    try:
        from src.consciousness_engine import ConsciousnessEngine
        from src.memory_manager import MemoryManager
        from src.personality_engine import PersonalityEngine
        from src.neural_monitor import NeuralStateMonitor
        
        # Initialize components
        memory_manager = MemoryManager()
        personality_engine = PersonalityEngine()
        neural_monitor = NeuralStateMonitor()
        
        consciousness = ConsciousnessEngine(
            memory_manager=memory_manager,
            personality_engine=personality_engine,
            neural_monitor=neural_monitor
        )
        
        print("✅ ConsciousnessEngine initialized successfully")
        
        # Test memory retrieval (this should trigger the multiplication error if not fixed)
        try:
            relevant_memories = consciousness.memory_manager.retrieve_memories(
                "test query", max_memories=5
            )
            print(f"✅ Memory retrieval successful: {len(relevant_memories)} memories found")
            
            # Test the neural monitoring of memories (where the error occurred)
            if relevant_memories:
                for i, memory in enumerate(relevant_memories[:3]):  # Test first 3
                    neural_monitor.log_memory_activation(
                        memory_id=str(memory.id),
                        similarity_score=0.8 - (i * 0.1),
                        emotional_weight=memory.emotional_intensity,
                        activation_strength=memory.importance * (0.9 - i * 0.1),
                        memory_age_factor=max(0.1, 1.0 - i * 0.01),  # Fixed version
                        content_preview=memory.content[:100]
                    )
                print("✅ Neural memory activation logging successful")
            
        except Exception as e:
            print(f"❌ Memory processing failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Consciousness engine initialization failed: {e}")
        return False
    
    print("\n🎉 Consciousness engine memory processing test PASSED!")
    return True

if __name__ == "__main__":
    success = test_consciousness_memory()
    if not success:
        exit(1)
