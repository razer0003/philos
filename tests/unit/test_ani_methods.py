#!/usr/bin/env python3
"""
Test if AdvancedNeuralIntelligence methods are working
"""

import sys
sys.path.append('src')

# Force reimport
if 'advanced_neural_intelligence' in sys.modules:
    del sys.modules['advanced_neural_intelligence']

from advanced_neural_intelligence import AdvancedNeuralIntelligence

# Create instance and test methods
print("Testing AdvancedNeuralIntelligence methods...")

ani = AdvancedNeuralIntelligence()

print(f"Class type: {type(ani)}")
print(f"All methods: {[m for m in dir(ani) if not m.startswith('_')]}")

# Test specific methods
methods_to_test = [
    'start_continuous_monitoring',
    'stop_continuous_monitoring',
    'get_prediction_accuracy',
    'comprehensive_neural_analysis'
]

for method_name in methods_to_test:
    has_method = hasattr(ani, method_name)
    print(f"Method '{method_name}': {'✅' if has_method else '❌'}")
    
    if has_method:
        try:
            method = getattr(ani, method_name)
            print(f"  Type: {type(method)}")
            # Try to call it if it's a simple method
            if method_name in ['start_continuous_monitoring', 'stop_continuous_monitoring']:
                result = method()
                print(f"  Result: {result}")
        except Exception as e:
            print(f"  Error calling method: {e}")

print("\nDone!")
