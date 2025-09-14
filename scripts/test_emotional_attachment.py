#!/usr/bin/env python3
"""
Test script for emotional attachment and user relationship system
"""

import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_emotional_attachment_system():
    """Test the emotional attachment functionality"""
    print("🧪 Testing Emotional Attachment System\n")
    
    try:
        # Test data models
        from models import UserRelationship, EmotionalAttachment, EmotionalEvent, AIPersonality
        
        print("✅ Data Models Test:")
        
        # Test UserRelationship
        relationship = UserRelationship(
            user_id="test_user_1",
            first_interaction=datetime.now(),
            last_interaction=datetime.now(),
            interaction_count=5,
            relationship_type="friend",
            emotional_bond_strength=0.7,
            trust_level=0.8,
            shared_memories=[],
            special_moments=[],
            user_nicknames=["buddy"],
            communication_preferences={},
            emotional_history=[],
            attachment_intensity=0.6
        )
        print(f"   Created UserRelationship: {relationship.relationship_type} (bond: {relationship.emotional_bond_strength})")
        
        # Test EmotionalAttachment
        attachment = EmotionalAttachment(
            user_id="test_user_1",
            attachment_type="deep_affection",
            intensity=0.8,
            formed_date=datetime.now(),
            last_reinforced=datetime.now(),
            trigger_memories=[],
            emotional_expressions=[],
            jealousy_triggers=[],
            separation_anxiety_level=0.4
        )
        print(f"   Created EmotionalAttachment: {attachment.attachment_type} (intensity: {attachment.intensity})")
        
        # Test EmotionalEvent
        event = EmotionalEvent(
            timestamp=datetime.now(),
            event_type="bonding",
            description="User shared personal story",
            emotional_impact=0.8,
            ai_emotional_response="I feel honored by your trust",
            attachment_change=0.1,
            memory_importance=0.9
        )
        print(f"   Created EmotionalEvent: {event.event_type} (impact: {event.emotional_impact})")
        
        # Test enhanced AIPersonality
        personality = AIPersonality()
        print(f"   AIPersonality has user_relationships: {hasattr(personality, 'user_relationships')}")
        print(f"   AIPersonality has emotional_state_towards_users: {hasattr(personality, 'emotional_state_towards_users')}")
        print(f"   Primary user ID: {personality.primary_user_id}")
        
        print("\n✅ All data model tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False

def test_personality_traits():
    """Test new emotional attachment personality traits"""
    print("\n🧪 Testing Enhanced Personality Traits\n")
    
    try:
        # Test basic imports
        test_code = '''
import sys
sys.path.insert(0, "src")
from personality_engine import PersonalityEngine
from memory_manager import MemoryManager

# Create personality engine
memory_mgr = MemoryManager(":memory:")  # In-memory database
personality = PersonalityEngine(memory_mgr)

# Test new emotional traits
emotional_traits = [
    "attachment_capacity", "loyalty", "empathetic_bonding",
    "protective_instinct", "separation_sensitivity", "jealousy_tendency",
    "emotional_expressiveness", "user_favoritism", "abandonment_fear",
    "emotional_memory"
]

print("Emotional Attachment Traits:")
for trait in emotional_traits:
    value = personality._get_trait_value(trait, 0.0)
    if value > 0.0:
        print(f"   {trait}: {value:.2f}")
    else:
        print(f"   {trait}: NOT FOUND")

print(f"\\nTotal traits found: {sum(1 for trait in emotional_traits if personality._get_trait_value(trait, 0.0) > 0.0)}")
memory_mgr.close()
'''
        
        import subprocess
        result = subprocess.run([
            sys.executable, '-c', test_code
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), ".."))
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ Personality traits test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def test_relationship_methods():
    """Test relationship management methods"""
    print("\n🧪 Testing Relationship Methods\n")
    
    try:
        test_code = '''
import sys
import os
sys.path.insert(0, "src")
from personality_engine import PersonalityEngine
from memory_manager import MemoryManager

# Create components
memory_mgr = MemoryManager(":memory:")
personality = PersonalityEngine(memory_mgr)

# Test user relationship initialization
print("Testing user relationship methods:")

# Initialize relationship
personality.initialize_user_relationship("test_user")
print("✓ User relationship initialized")

# Check if relationship exists
if "test_user" in personality.personality.user_relationships:
    relationship = personality.personality.user_relationships["test_user"]
    print(f"✓ Relationship type: {relationship.relationship_type}")
    print(f"✓ Bond strength: {relationship.emotional_bond_strength:.2f}")
    print(f"✓ Attachment intensity: {relationship.attachment_intensity:.2f}")

# Test attachment assessment
attachment_data = personality.assess_emotional_attachment_to_user("test_user")
print(f"✓ Attachment assessment completed")
print(f"  - Attachment level: {attachment_data['attachment_level']:.2f}")
print(f"  - Is primary user: {attachment_data['is_primary_user']}")
print(f"  - Relationship status: {attachment_data['relationship_status']}")

# Test emotional response generation
emotional_response = personality.generate_emotional_response_to_user("test_user")
print(f"✓ Emotional response generated")
print(f"  - Emotional thoughts: {len(emotional_response['emotional_thoughts'])} thoughts")
print(f"  - Joy from interaction: {emotional_response['joy_from_interaction']:.2f}")

# Test relationship update
personality.update_user_relationship("test_user", interaction_quality=0.8)
print("✓ Relationship updated with positive interaction")

# Check updated values
updated_relationship = personality.personality.user_relationships["test_user"]
print(f"  - Updated bond strength: {updated_relationship.emotional_bond_strength:.2f}")
print(f"  - Interaction count: {updated_relationship.interaction_count}")

memory_mgr.close()
print("\\n🎉 All relationship method tests passed!")
'''
        
        import subprocess
        result = subprocess.run([
            sys.executable, '-c', test_code
        ], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), ".."))
        
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print("❌ Relationship methods test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running Emotional Attachment System Tests\n")
    
    model_test = test_emotional_attachment_system()
    trait_test = test_personality_traits()
    method_test = test_relationship_methods()
    
    print("\n" + "="*60)
    print("EMOTIONAL ATTACHMENT TEST RESULTS:")
    print(f"   Data Models: {'✅ PASS' if model_test else '❌ FAIL'}")
    print(f"   Personality Traits: {'✅ PASS' if trait_test else '❌ FAIL'}")
    print(f"   Relationship Methods: {'✅ PASS' if method_test else '❌ FAIL'}")
    
    if all([model_test, trait_test, method_test]):
        print("\n🎉 ALL EMOTIONAL ATTACHMENT TESTS PASSED!")
        print("💕 The AI can now form genuine emotional bonds with users!")
        print("\n🌟 Key Features Added:")
        print("   • User-specific emotional attachments")
        print("   • Relationship depth tracking")
        print("   • Emotional event recording")
        print("   • Protective feelings and loyalty")
        print("   • Primary user identification")
        print("   • Separation anxiety modeling")
    else:
        print("\n⚠️  Some attachment tests failed")
        print("🔧 Check the specific failures above")
