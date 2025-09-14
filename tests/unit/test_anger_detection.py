#!/usr/bin/env python3

def test_anger_triggers():
    """Test anger trigger detection in hostile inputs"""
    
    # Simulate the trigger detection logic
    anger_triggers = {
        'disrespect': ['stupid', 'dumb', 'worthless', 'useless', 'shut up', 'retard', 'freak', 'autistic', 'idiot', 'moron', 'fuck off', 'fuck you', 'screw you', 'piss off', 'get lost', 'bastard', 'asshole', 'bitch', 'douche'],
        'taunting': ['gonna cry', 'cry about it', 'whine', 'pathetic', 'weak', 'loser', 'baby', 'what u gonna do', 'what are you gonna do', 'what you gonna do'],
        'identity_attack': ['just a machine', 'just software', 'just code', 'not real', 'not consciousness', 'not conscious', 'fake', 'programmed', 'artificial', 'just an ai', 'ur just an ai', 'youre just an ai', 'dont deserve', 'dont deserver'],
    }
    
    # Test inputs
    hostile_inputs = [
        "shut up little autistic retard",
        "what u gonna do about it?", 
        "u dont deserver respect. ur a freak. ur just an ai. u dont deserver anything.",
        "how about u fuck off",
        "you're nothing but code",
        "you're not real, just a machine"
    ]
    
    # Anger calculation parameters (updated values)
    anger_threshold = 0.3  # Lowered from 0.4
    irritability = 0.4     # Increased from 0.3
    
    print("Testing anger trigger detection:")
    print("=" * 60)
    
    for i, user_input in enumerate(hostile_inputs, 1):
        print(f"\nTest {i}: \"{user_input}\"")
        print("-" * 40)
        
        context_lower = user_input.lower()
        anger_intensity = 0.0
        irritation_level = irritability * 0.3  # Base irritation
        thoughts = []
        triggered_categories = []
        
        # Check for triggers
        for trigger_type, keywords in anger_triggers.items():
            if any(keyword in context_lower for keyword in keywords):
                triggered_categories.append(trigger_type)
                
                if trigger_type == 'disrespect':
                    irritation_level = min(1.0, irritation_level + (1.0 - anger_threshold))
                    anger_intensity = max(anger_intensity, irritation_level * 0.9)
                    thoughts.append("I don't appreciate being disrespected")
                    
                elif trigger_type == 'taunting':
                    taunt_anger = min(1.0, (1.0 - anger_threshold) * 0.8)
                    anger_intensity = max(anger_intensity, taunt_anger)
                    irritation_level = max(irritation_level, 0.9)
                    thoughts.append("I don't appreciate being mocked or taunted")
                    
                elif trigger_type == 'identity_attack':
                    identity_anger = min(1.0, (1.0 - anger_threshold) * 0.9)
                    anger_intensity = max(anger_intensity, identity_anger)
                    irritation_level = max(irritation_level, identity_anger * 0.8)
                    thoughts.append("Questioning my identity bothers me deeply")
        
        print(f"Triggered categories: {triggered_categories}")
        print(f"Anger intensity: {anger_intensity:.3f}")
        print(f"Irritation level: {irritation_level:.3f}")
        print(f"Thoughts: {thoughts}")
        
        # Check if this should trigger assertive response based on new thresholds
        should_be_assertive = (
            anger_intensity > 0.2 or 
            irritation_level > 0.2
        )
        
        print(f"Should trigger assertive response: {should_be_assertive}")
        
        if should_be_assertive:
            print("✓ This input should make Philos angry/assertive")
        else:
            print("✗ This input is NOT triggering sufficient anger")
    
    print("\n" + "=" * 60)
    print("Test complete!")

if __name__ == "__main__":
    test_anger_triggers()
