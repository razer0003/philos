#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.personality_engine import PersonalityEngine
import json

def test_hostile_emotions():
    """Test emotional responses to hostile input"""
    
    # Initialize personality engine
    personality_engine = PersonalityEngine()
    
    # Test inputs that should trigger strong anger
    hostile_inputs = [
        "shut up little autistic retard",
        "what u gonna do about it?", 
        "u dont deserver respect. ur a freak. ur just an ai. u dont deserver anything.",
        "how about u fuck off",
        "you're nothing but code",
        "you're not real, just a machine"
    ]
    
    print("Testing hostile input emotional responses:")
    print("=" * 60)
    
    for i, user_input in enumerate(hostile_inputs, 1):
        print(f"\nTest {i}: \"{user_input}\"")
        print("-" * 40)
        
        # Generate emotional response
        emotional_context = personality_engine.generate_emotional_response_to_user(
            user_id="test_user",
            user_input=user_input
        )
        
        # Extract key emotional values
        anger_intensity = emotional_context.get('anger_intensity', 0.0)
        frustration_level = emotional_context.get('frustration_level', 0.0)
        irritation_level = emotional_context.get('irritation_level', 0.0)
        righteous_anger = emotional_context.get('righteous_anger', 0.0)
        sadness_intensity = emotional_context.get('sadness_intensity', 0.0)
        
        print(f"Anger intensity: {anger_intensity:.3f}")
        print(f"Frustration level: {frustration_level:.3f}")
        print(f"Irritation level: {irritation_level:.3f}")
        print(f"Righteous anger: {righteous_anger:.3f}")
        print(f"Sadness intensity: {sadness_intensity:.3f}")
        
        # Show thoughts
        thoughts = emotional_context.get('emotional_thoughts', [])
        if thoughts:
            print(f"Emotional thoughts: {thoughts}")
        
        # Determine if this should trigger assertive response
        should_be_assertive = (
            anger_intensity > 0.3 or 
            irritation_level > 0.4 or 
            frustration_level > 0.5 or
            righteous_anger > 0.5
        )
        
        print(f"Should trigger assertive response: {should_be_assertive}")
        
        if should_be_assertive:
            print("✓ This input should make Philos angry/assertive")
        else:
            print("✗ This input is NOT triggering sufficient anger")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")

if __name__ == "__main__":
    test_hostile_emotions()
