#!/usr/bin/env python3
"""
Test to check if neural dashboard is getting real data
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

try:
    from neural.neural_data_store import get_neural_data_store
    
    print("Testing neural data store connection...")
    data_store = get_neural_data_store()
    neural_data = data_store.get_data()
    
    print(f"✅ Neural data store accessible")
    print(f"Monitoring active: {neural_data.get('monitoring_active', False)}")
    print(f"Data source test: {'REAL DATA' if neural_data.get('monitoring_active') else 'DEMO MODE'}")
    print(f"Recent computations count: {len(neural_data.get('recent_computations', []))}")
    
    if neural_data.get('recent_computations'):
        print("Recent computations:")
        for comp in neural_data['recent_computations'][:3]:
            print(f"  - {comp.get('step_name', 'unknown')}")
    
    print(f"Stats: {neural_data.get('stats', {})}")
    
except Exception as e:
    print(f"❌ Error accessing neural data store: {e}")
    print("Dashboard would fall back to demo mode")
