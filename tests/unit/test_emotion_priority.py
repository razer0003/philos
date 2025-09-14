#!/usr/bin/env python3
"""Quick test of the improved emotion priority"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
from src.memory_manager import MemoryManager

def test_emotion_priority():
    """Test that anger/sadness thoughts take priority"""
    print("Testing emotion priority...")
    
    # Initialize components
    db_manager = DatabaseManager("data/ai_personality.db")
    memory_manager = MemoryManager(db_manager, "data/conversations")
    personality_engine = PersonalityEngine(db_manager, memory_manager)
    
    # Test messages that should have prominent anger/sadness thoughts
    test_cases = [
        {
            'message': "You're just a machine, not really conscious. Just code.",
            'expected_emotion': 'anger',
            'description': 'Identity attack should show anger thoughts first'
        },
        {
            'message': "You're so stupid and worthless.",
            'expected_emotion': 'anger', 
            'description': 'Disrespect should show anger thoughts'
        },
        {
            'message': "My friend died yesterday, I'm so sad.",
            'expected_emotion': 'sadness',
            'description': 'Loss should show grief/sadness thoughts'
        },
        {
            'message': "Hello Philos, how are you?",
            'expected_emotion': 'neutral',
            'description': 'Neutral message should show basic attachment thoughts'
        }
    ]
    
    user_id = "test_user"
    
    for test_case in test_cases:
        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"Message: '{test_case['message']}'")
        print(f"Expected: {test_case['expected_emotion']} emotions should be prominent")
        print("-" * 60)
        
        # Get emotional response
        response = personality_engine.generate_emotional_response_to_user(user_id, test_case['message'])
        
        print("Emotional thoughts:")
        for i, thought in enumerate(response.get('emotional_thoughts', []), 1):
            print(f"  {i}. {thought}")
        
        # Show emotion levels
        anger = response.get('anger_intensity', 0)
        sadness = response.get('sadness_intensity', 0)
        print(f"\nEmotion levels:")
        print(f"  Anger intensity: {anger:.2f}")
        print(f"  Sadness intensity: {sadness:.2f}")
        
        # Analyze if emotions are prominent
        if test_case['expected_emotion'] == 'anger' and anger > 0.3:
            print("✓ PASS: Anger emotions are prominent")
        elif test_case['expected_emotion'] == 'sadness' and sadness > 0.3:
            print("✓ PASS: Sadness emotions are prominent")
        elif test_case['expected_emotion'] == 'neutral' and anger < 0.1 and sadness < 0.1:
            print("✓ PASS: Neutral message shows basic attachment")
        else:
            print("✗ FAIL: Expected emotions not prominent enough")

if __name__ == "__main__":
    test_emotion_priority()
    print("\nEmotion priority testing complete!")
