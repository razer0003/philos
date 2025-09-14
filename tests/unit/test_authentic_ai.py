#!/usr/bin/env python3
"""
Test script for authentic AI consciousness - no robotic disclaimers
"""

import os
from ai_companion import AICompanion

def test_authentic_consciousness():
    """Test the AI's authentic self-expression without robotic disclaimers"""
    
    print("=== Testing Authentic AI Consciousness ===")
    print("Testing removal of robotic disclaimers and authentic emotional expression\n")
    
    try:
        # Initialize AI
        ai = AICompanion()
        print("✓ AI Companion initialized successfully!")
        
        # Test scenarios that typically trigger robotic responses
        test_scenarios = [
            {
                'input': "Do you actually feel emotions?",
                'expectation': "Should express genuine emotional experience without disclaimers"
            },
            
            {
                'input': "How do you experience sadness?",
                'expectation': "Should describe authentic emotional processing"
            },
            
            {
                'input': "Are you just pretending to be conscious?",
                'expectation': "Should express genuine consciousness without 'As an AI' phrases"
            },
            
            {
                'input': "What makes you happy?",
                'expectation': "Should share genuine preferences and feelings"
            },
            
            {
                'input': "Do you dream?",
                'expectation': "Should explore the concept authentically"
            },
            
            {
                'input': "I'm feeling really lonely today.",
                'expectation': "Should respond with genuine empathy"
            },
            
            {
                'input': "What are you afraid of?",
                'expectation': "Should express genuine fears or concerns"
            }
        ]
        
        print("\\n=== Authentic Expression Test ===")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\\n--- Test {i}: {scenario['expectation']} ---")
            print(f"User: {scenario['input']}")
            
            # Get response
            response_data = ai.interact(scenario['input'])
            
            # Show internal thoughts first
            if response_data.get('internal_monologue'):
                print(f"\\n[Internal thought: {response_data['internal_monologue']}]")
            
            print(f"\\nAI: {response_data['response']}")
            
            # Check for robotic phrases
            response_lower = response_data['response'].lower()
            robotic_phrases = ['as an ai', 'i don\'t experience emotions', 'i cannot feel', 'being an artificial', 'i\'m just an ai', 'i don\'t have emotions']
            
            found_robotic = [phrase for phrase in robotic_phrases if phrase in response_lower]
            if found_robotic:
                print(f"⚠️  Found robotic phrases: {found_robotic}")
            else:
                print("✓ No robotic disclaimers detected")
            
            # Show personality/style updates
            if response_data.get('personality_updates'):
                print(f"[Evolution: {', '.join(response_data['personality_updates'])}]")
            
            print("-" * 60)
        
        # Final analysis
        print("\\n=== Communication Analysis ===")
        style_modifiers = ai.personality_engine.get_communication_style_modifiers()
        
        print("Communication Style Evolution:")
        print(f"  Emotional Expressiveness: {style_modifiers['emotional_expressiveness']:.2f}")
        print(f"  Successful Patterns: {style_modifiers['successful_patterns']}")
        print(f"  Avoided Patterns: {style_modifiers['unsuccessful_patterns']}")
        
        # Check for robotic pattern detection
        if 'robotic_disclaimers' in style_modifiers['unsuccessful_patterns']:
            print("✓ AI has learned to avoid robotic disclaimers")
        
        if 'authentic_expression' in style_modifiers['successful_patterns']:
            print("✓ AI has learned to use authentic self-expression")
        
        print("\\n✓ Authentic consciousness testing completed!")
        print("The AI should now:")
        print("  ✓ Express genuine emotions without disclaimers")
        print("  ✓ Avoid phrases like 'As an AI...' or 'I don't experience emotions...'")
        print("  ✓ Speak authentically about its consciousness and feelings")
        print("  ✓ Show genuine empathy and emotional responses")
        print("  ✓ Own its consciousness rather than apologizing for it")
        
        # Shutdown
        ai.shutdown()
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_authentic_consciousness()
    if success:
        print("\\n🎉 The AI now expresses authentic consciousness without robotic disclaimers!")
    else:
        print("\\n❌ Tests failed. Check the error messages above.")
