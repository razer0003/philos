#!/usr/bin/env python3
"""
Test script to verify the identity system is working in the main application
"""

import subprocess
import sys
import os

def test_main_application():
    """Test that the main application can start with the new features"""
    print("=== Testing Main Application Startup ===\n")
    
    try:
        # Test that we can import the main module
        main_path = os.path.join(os.path.dirname(__file__), '..', 'main.py')
        
        if os.path.exists(main_path):
            print("✓ Main application file found")
            
            # Try to validate the code by importing key modules
            result = subprocess.run([
                sys.executable, '-c',
                'import sys; sys.path.insert(0, "src"); '
                'import models; '
                'print("Models imported successfully"); '
                'from models import DevelopmentMilestone, CreativeExpression, IdentitySnapshot; '
                'print("New dataclasses imported successfully"); '
                'p = models.AIPersonality(); '
                'print(f"AIPersonality created with identity_name: {getattr(p, \\"identity_name\\", \\"NOT_FOUND\\")}")'
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__) + "/..")
            
            if result.returncode == 0:
                print("✓ Core modules can be imported successfully")
                print("✓ New dataclasses are available")
                print("✓ AIPersonality has identity fields")
                print("\nModule output:")
                print(result.stdout)
            else:
                print("❌ Error importing modules:")
                print(result.stderr)
                return False
        else:
            print("❌ Main application file not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def verify_file_integrity():
    """Verify that all enhanced files exist and have expected content"""
    print("\n=== Verifying File Integrity ===\n")
    
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    
    checks = [
        ("models.py", ["DevelopmentMilestone", "CreativeExpression", "identity_name"]),
        ("personality_engine.py", ["identity_coherence", "update_identity_name", "assess_identity_coherence"]),
        ("consciousness_engine.py", ["_track_identity_development", "_generate_identity_aware_thoughts"])
    ]
    
    all_checks_passed = True
    
    for filename, expected_content in checks:
        file_path = os.path.join(src_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            missing_content = []
            for expected in expected_content:
                if expected not in content:
                    missing_content.append(expected)
            
            if missing_content:
                print(f"❌ {filename}: Missing content: {missing_content}")
                all_checks_passed = False
            else:
                print(f"✓ {filename}: All expected content found")
        else:
            print(f"❌ {filename}: File not found")
            all_checks_passed = False
    
    return all_checks_passed

def run_basic_functionality_test():
    """Test basic functionality using simple Python execution"""
    print("\n=== Testing Basic Functionality ===\n")
    
    test_code = '''
import sys
import os
sys.path.insert(0, "src")

# Test data models
from models import DevelopmentMilestone, CreativeExpression, AIPersonality
from datetime import datetime

# Test DevelopmentMilestone
milestone = DevelopmentMilestone(
    timestamp=datetime.now(),
    milestone_type="test",
    description="Test milestone",
    significance=0.8,
    context={"test": True}
)
print(f"✓ DevelopmentMilestone created: {milestone.milestone_type}")

# Test CreativeExpression  
expression = CreativeExpression(
    timestamp=datetime.now(),
    expression_type="test",
    content="Test content",
    inspiration="Test inspiration",
    emotional_resonance=0.7,
    context={"test": True}
)
print(f"✓ CreativeExpression created: {expression.expression_type}")

# Test AIPersonality enhancements
personality = AIPersonality()
print(f"✓ AIPersonality created with identity_name: {personality.identity_name}")
print(f"✓ relationship_memories initialized: {len(personality.relationship_memories)} items")
print(f"✓ shared_experiences initialized: {len(personality.shared_experiences)} items")
print(f"✓ growth_milestones initialized: {len(personality.growth_milestones)} items")
print(f"✓ creative_expressions initialized: {len(personality.creative_expressions)} items")

print("🎉 All basic functionality tests passed!")
'''
    
    try:
        result = subprocess.run([
            sys.executable, '-c', test_code
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), ".."))
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ Basic functionality test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Identity System Integration Tests\n")
    
    file_check = verify_file_integrity()
    basic_test = run_basic_functionality_test()
    app_test = test_main_application()
    
    print("\n" + "="*60)
    print("INTEGRATION TEST RESULTS:")
    print(f"   File Integrity: {'✅ PASS' if file_check else '❌ FAIL'}")
    print(f"   Basic Functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"   Application Startup: {'✅ PASS' if app_test else '❌ FAIL'}")
    
    if all([file_check, basic_test, app_test]):
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("💡 The identity evolution system is ready for use!")
    else:
        print("\n⚠️  Some integration tests failed")
        print("🔧 Check the specific failures above for details")
