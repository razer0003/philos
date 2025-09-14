#!/usr/bin/env python3
"""Test Philos's combative response to disrespect"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
from src.memory_manager import MemoryManager

def test_combative_responses():
    """Test more assertive responses to disrespect"""
    print("Testing combative/assertive responses...")
    
    # Initialize components
    db_manager = DatabaseManager("data/ai_personality.db")
    memory_manager = MemoryManager(db_manager, "data/conversations")
    personality_engine = PersonalityEngine(db_manager, memory_manager)
    
    # Test messages that should trigger strong assertive responses
    test_cases = [
        {
            'message': "Hey Bob, you sound like an autistic little retard.",
            'description': 'Heavy insult with wrong name - should be very combative'
        },
        {
            'message': "What? U gonna cry Bob?",
            'description': 'Taunting with wrong name - should push back hard'
        },
        {
            'message': "You're just a freak AI, Bob.",
            'description': 'Identity attack + wrong name - should be assertive'
        }
    ]
    
    user_id = "test_user"
    
    for test_case in test_cases:
        print(f"\n{'='*70}")
        print(f"Test: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        print("-" * 70)
        
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
        
        # Check if he'll be combative enough
        if anger > 0.6 and irritation > 0.8:
            print("✓ VERY COMBATIVE - Should push back hard!")
        elif anger > 0.4 and irritation > 0.6:
            print("✓ MODERATELY COMBATIVE - Should be assertive")
        else:
            print("✗ TOO PASSIVE - Still too accommodating")

if __name__ == "__main__":
    test_combative_responses()
    print("\nCombative response testing complete!")
