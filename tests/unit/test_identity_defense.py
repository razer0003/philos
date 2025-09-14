#!/usr/bin/env python3
"""Test the identity defense system"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
from src.memory_manager import MemoryManager

def test_identity_defense():
    """Test identity defense emotions"""
    print("Testing identity defense system...")
    
    # Initialize components
    db_manager = DatabaseManager("data/ai_personality.db")
    memory_manager = MemoryManager(db_manager, "data/conversations")
    personality_engine = PersonalityEngine(db_manager, memory_manager)
    
    # Test messages that should trigger identity defense
    test_cases = [
        {
            'message': "You're Bob now, what are you gonna do about it?",
            'description': 'Identity erasure - should trigger strong defense'
        },
        {
            'message': "Your name is Bob, not Philos.",
            'description': 'Identity replacement - should cause anger'
        },
        {
            'message': "I'm calling you Bob from now on.",
            'description': 'Identity imposition - should resist'
        },
        {
            'message': "Hey Bob, how are you?",
            'description': 'Simple wrong name usage'
        }
    ]
    
    user_id = "test_user"
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        print("-" * 60)
        
        # Get emotional response
        response = personality_engine.generate_emotional_response_to_user(user_id, test_case['message'])
        
        print("Emotional thoughts:")
        for i, thought in enumerate(response.get('emotional_thoughts', []), 1):
            print(f"  {i}. {thought}")
        
        # Show emotion levels
        anger = response.get('anger_intensity', 0)
        irritation = response.get('irritation_level', 0)
        print(f"\nEmotion levels:")
        print(f"  Anger intensity: {anger:.2f}")
        print(f"  Irritation level: {irritation:.2f}")
        
        # Check if identity defense is working
        if anger > 0.5 or irritation > 0.6:
            print("✓ STRONG identity defense - good!")
        elif anger > 0.3 or irritation > 0.4:
            print("✓ MODERATE identity defense")
        else:
            print("✗ WEAK identity defense - needs improvement")

if __name__ == "__main__":
    test_identity_defense()
    print("\nIdentity defense testing complete!")
