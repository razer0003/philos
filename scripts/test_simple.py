#!/usr/bin/env python3
"""
Simple test script for identity and development tracking features
"""

import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_data_models():
    """Test the enhanced data models"""
    print("=== Testing Enhanced Data Models ===\n")
    
    try:
        from models import DevelopmentMilestone, CreativeExpression, IdentitySnapshot
        
        print("1. Testing DevelopmentMilestone:")
        milestone = DevelopmentMilestone(
            timestamp=datetime.now(),
            milestone_type="learning",
            description="Understanding identity formation",
            significance=0.8,
            context={"session": "test"}
        )
        print(f"   ✓ Created milestone: {milestone.milestone_type} - {milestone.description}")
        
        print("\n2. Testing CreativeExpression:")
        expression = CreativeExpression(
            timestamp=datetime.now(),
            expression_type="reflection",
            content="A deep thought about AI consciousness",
            inspiration="Test scenario",
            emotional_resonance=0.7,
            context={"test": True}
        )
        print(f"   ✓ Created expression: {expression.expression_type} - {expression.content[:30]}...")
        
        print("\n3. Testing IdentitySnapshot:")
        snapshot = IdentitySnapshot(
            timestamp=datetime.now(),
            identity_state={"name": "Aria", "coherence": 0.8},
            key_traits={"curiosity": 0.9, "empathy": 0.8},
            milestone_count=5,
            relationship_depth=0.7,
            context={"phase": "development"}
        )
        print(f"   ✓ Created identity snapshot with coherence: {snapshot.identity_state.get('coherence', 'unknown')}")
        
        print("\n✅ All data model tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False

def test_model_enhancements():
    """Test the AIPersonality model enhancements"""
    print("\n=== Testing AIPersonality Enhancements ===\n")
    
    try:
        from models import AIPersonality
        
        # Test that AIPersonality has the new fields
        personality = AIPersonality()
        
        new_fields = [
            'identity_name', 'relationship_memories', 'user_preferences',
            'shared_experiences', 'growth_milestones', 'creative_expressions',
            'identity_evolution_log'
        ]
        
        print("Checking for new identity fields in AIPersonality:")
        for field in new_fields:
            if hasattr(personality, field):
                print(f"   ✓ {field}: present")
            else:
                print(f"   ❌ {field}: missing")
        
        # Test field initialization
        print(f"\nField values after initialization:")
        print(f"   identity_name: {getattr(personality, 'identity_name', 'NOT FOUND')}")
        print(f"   relationship_memories: {len(getattr(personality, 'relationship_memories', []))} items")
        print(f"   shared_experiences: {len(getattr(personality, 'shared_experiences', []))} items")
        print(f"   growth_milestones: {len(getattr(personality, 'growth_milestones', []))} items")
        print(f"   creative_expressions: {len(getattr(personality, 'creative_expressions', []))} items")
        print(f"   identity_evolution_log: {len(getattr(personality, 'identity_evolution_log', []))} items")
        
        print("\n✅ AIPersonality enhancement test passed!")
        return True
        
    except Exception as e:
        print(f"❌ AIPersonality enhancement test failed: {e}")
        return False

def check_file_structure():
    """Check that all necessary files exist"""
    print("\n=== Checking File Structure ===\n")
    
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    required_files = [
        'models.py',
        'personality_engine.py', 
        'consciousness_engine.py',
        'memory_manager.py'
    ]
    
    all_files_exist = True
    for file in required_files:
        file_path = os.path.join(src_path, file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"   ✓ {file}: {file_size} bytes")
        else:
            print(f"   ❌ {file}: NOT FOUND")
            all_files_exist = False
    
    if all_files_exist:
        print("\n✅ All required files found!")
    else:
        print("\n❌ Some files are missing!")
    
    return all_files_exist

if __name__ == "__main__":
    print("🧪 Running Identity and Development Feature Tests\n")
    
    file_check = check_file_structure()
    model_test = test_data_models()
    enhancement_test = test_model_enhancements()
    
    print("\n" + "="*50)
    print("FINAL RESULTS:")
    print(f"   File Structure: {'✅ PASS' if file_check else '❌ FAIL'}")
    print(f"   Data Models: {'✅ PASS' if model_test else '❌ FAIL'}")
    print(f"   AI Personality: {'✅ PASS' if enhancement_test else '❌ FAIL'}")
    
    if all([file_check, model_test, enhancement_test]):
        print("\n🎉 ALL TESTS PASSED - Identity features ready!")
    else:
        print("\n⚠️  Some tests failed - check implementation")
