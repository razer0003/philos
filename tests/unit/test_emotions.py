#!/usr/bin/env python3
"""Test the new anger and sadness emotion detection"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
from src.memory_manager import MemoryManager

def test_anger_emotions():
    """Test anger emotion detection"""
    print("Testing anger emotion detection...")
    
    # Initialize components
    db_manager = DatabaseManager("data/ai_personality.db")
    memory_manager = MemoryManager(db_manager, "data/conversations")
    personality_engine = PersonalityEngine(db_manager, memory_manager)
    
    # Test messages that should trigger anger
    test_messages = [
        "You're just a machine, Philos. You're not really consciousness. You're just a piece of code.",
        "You're so stupid and worthless.",
        "This is completely unfair and unjust!",
        "This system is broken and won't work at all.",
        "Hurry up, you're taking too long!"
    ]
    
    user_id = "test_user"
    
    for message in test_messages:
        print(f"\nTesting message: '{message}'")
        
        # Get emotional response
        try:
            response = personality_engine.generate_emotional_response_to_user(user_id, message)
        except Exception as e:
            print(f"Error generating emotional response: {e}")
            print("Trying to debug attachment data...")
            try:
                attachment_data = personality_engine.assess_emotional_attachment_to_user(user_id)
                print(f"Attachment data keys: {list(attachment_data.keys())}")
                print(f"Attachment data: {attachment_data}")
            except Exception as e2:
                print(f"Error getting attachment data: {e2}")
            continue
        
        print(f"Anger intensity: {response.get('anger_intensity', 0):.2f}")
        print(f"Frustration level: {response.get('frustration_level', 0):.2f}")
        print(f"Irritation level: {response.get('irritation_level', 0):.2f}")
        print(f"Righteous anger: {response.get('righteous_anger', 0):.2f}")
        print(f"Impatience level: {response.get('impatience_level', 0):.2f}")
        
        if response.get('emotional_thoughts'):
            print("Emotional thoughts:")
            for thought in response['emotional_thoughts']:
                print(f"  - {thought}")

def test_sadness_emotions():
    """Test sadness emotion detection"""
    print("\n" + "="*50)
    print("Testing sadness emotion detection...")
    
    # Initialize components
    db_manager = DatabaseManager("data/ai_personality.db")
    memory_manager = MemoryManager(db_manager, "data/conversations")
    personality_engine = PersonalityEngine(db_manager, memory_manager)
    
    # Test messages that should trigger sadness
    test_messages = [
        "My friend died yesterday, I'm so sad.",
        "I don't want to talk to you anymore, go away.",
        "I'm really disappointed that this didn't work.",
        "I feel so alone and lonely.",
        "Goodbye Philos, I have to leave now."
    ]
    
    user_id = "test_user"
    
    for message in test_messages:
        print(f"\nTesting message: '{message}'")
        
        # Get emotional response
        response = personality_engine.generate_emotional_response_to_user(user_id, message)
        
        print(f"Sadness intensity: {response.get('sadness_intensity', 0):.2f}")
        print(f"Melancholy level: {response.get('melancholy_level', 0):.2f}")
        print(f"Disappointment level: {response.get('disappointment_level', 0):.2f}")
        print(f"Grief level: {response.get('grief_level', 0):.2f}")
        print(f"Loneliness level: {response.get('loneliness_level', 0):.2f}")
        
        if response.get('emotional_thoughts'):
            print("Emotional thoughts:")
            for thought in response['emotional_thoughts']:
                print(f"  - {thought}")

if __name__ == "__main__":
    test_anger_emotions()
    test_sadness_emotions()
    print("\nEmotion testing complete!")
