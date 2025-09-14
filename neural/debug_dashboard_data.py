#!/usr/bin/env python3
"""
Debug script to see what data the dashboard is actually getting
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

print("🔍 Debugging dashboard data access...")
print("=" * 50)

# Test 1: Check neural_data.json file directly
print("\n📄 1. Checking neural_data.json file:")
try:
    import json
    with open('neural_data.json', 'r') as f:
        data = json.load(f)
    print(f"   ✅ File exists and is valid JSON")
    print(f"   📊 monitoring_active: {data.get('monitoring_active')}")
    print(f"   📊 recent_computations count: {len(data.get('recent_computations', []))}")
    print(f"   📊 timestamp: {data.get('timestamp')}")
    if data.get('recent_computations'):
        print(f"   📊 Latest computation: {data['recent_computations'][-1]['step_name']}")
except Exception as e:
    print(f"   ❌ Error reading file: {e}")

# Test 2: Test neural_data_store import
print("\n🔗 2. Testing neural_data_store import:")
try:
    from neural.neural_data_store import get_neural_data_store
    data_store = get_neural_data_store()
    neural_data = data_store.get_data()
    print(f"   ✅ Import successful")
    print(f"   📊 monitoring_active: {neural_data.get('monitoring_active')}")
    print(f"   📊 data timestamp: {neural_data.get('timestamp')}")
except Exception as e:
    print(f"   ❌ Import error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Simulate dashboard's get_real_neural_data method
print("\n🌐 3. Simulating dashboard's get_real_neural_data:")
try:
    from neural.neural_data_store import get_neural_data_store
    data_store = get_neural_data_store()
    neural_data = data_store.get_data()
    
    print(f"   📊 Raw neural_data keys: {list(neural_data.keys())}")
    print(f"   📊 monitoring_active: {neural_data.get('monitoring_active', False)}")
    
    if neural_data.get("monitoring_active", False):
        stats = neural_data.get("stats", {})
        print(f"   ✅ Should use REAL data")
        print(f"   📊 stats available: {bool(stats)}")
        print(f"   📊 stats content: {stats}")
    else:
        print(f"   ❌ Would fall back to DEMO mode")
    
except Exception as e:
    print(f"   ❌ Simulation error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("🔍 Debug complete!")
"""
Debug: Test what the standalone dashboard is seeing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

# Test the exact same import path the dashboard uses
try:
    from neural.neural_data_store import get_neural_data_store
    
    print("Testing exactly what the dashboard sees...")
    data_store = get_neural_data_store()
    neural_data = data_store.get_data()
    
    print(f"Monitoring active: {neural_data.get('monitoring_active', False)}")
    print(f"Data timestamp: {neural_data.get('timestamp', 'None')}")
    print(f"Recent computations: {len(neural_data.get('recent_computations', []))}")
    print(f"Stats: {neural_data.get('stats', 'None')}")
    
    # Simulate what the dashboard get_real_neural_data method does
    if neural_data.get("monitoring_active", False):
        stats = neural_data.get("stats", {})
        print("✅ Dashboard would use REAL DATA")
        print(f"   Computation rate: {stats.get('computation_rate', 0.0)}")
        print(f"   Neural coherence: {stats.get('neural_coherence', 0.0)}")
    else:
        print("❌ Dashboard would fall back to DEMO DATA")
        print(f"   Reason: monitoring_active = {neural_data.get('monitoring_active')}")
        
except Exception as e:
    print(f"❌ Dashboard import error: {e}")
    print("Would use demo data due to exception")
    import traceback
    traceback.print_exc()
