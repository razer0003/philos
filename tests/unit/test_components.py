#!/usr/bin/env python3
"""
Test neural components integration
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_neural_components():
    """Test if neural components can be imported and instantiated"""
    print("🧪 Testing Neural Components Integration")
    print("=" * 50)
    
    # Test NeuralStateMonitor
    try:
        from src.neural_monitor import NeuralStateMonitor
        monitor = NeuralStateMonitor()
        print("✅ NeuralStateMonitor: WORKING")
    except Exception as e:
        print(f"❌ NeuralStateMonitor: FAILED - {e}")
    
    # Test NeuralPatternAnalyzer (in root directory)
    try:
        from neural.neural_pattern_analyzer import NeuralPatternAnalyzer
        analyzer = NeuralPatternAnalyzer()
        print("✅ NeuralPatternAnalyzer: WORKING")
    except Exception as e:
        print(f"❌ NeuralPatternAnalyzer: FAILED - {e}")
    
    # Test AdvancedNeuralIntelligence (in root directory)
    try:
        from advanced_neural_intelligence import AdvancedNeuralIntelligence
        ani = AdvancedNeuralIntelligence()
        print("✅ AdvancedNeuralIntelligence: WORKING")
    except Exception as e:
        print(f"❌ AdvancedNeuralIntelligence: FAILED - {e}")
    
    # Test Memory model with emotional_intensity
    try:
        from src.models import Memory, MemoryType, MemorySource
        memory = Memory(
            type=MemoryType.EXPERIENCE,  # Use correct enum value
            content="Test memory",
            importance=0.8,
            confidence=0.9,
            emotional_intensity=0.7,
            source=MemorySource.USER_INPUT
        )
        print(f"✅ Memory with emotional_intensity: WORKING - {memory.emotional_intensity}")
    except Exception as e:
        print(f"❌ Memory model: FAILED - {e}")
    
    print("\n🏁 Component testing complete!")

if __name__ == "__main__":
    test_neural_components()
