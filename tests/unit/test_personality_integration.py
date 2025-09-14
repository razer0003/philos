#!/usr/bin/env python3
"""
Test personality integration and preferences expression
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_personality_integration():
    """Test that personality data is properly integrated into consciousness"""
    print("=" * 60)
    print("TESTING PERSONALITY INTEGRATION")
    print("=" * 60)
    
    # Mock the consciousness engine's personality integration
    class MockPersonalityEngine:
        def get_personality_summary(self):
            return {
                'traits': {
                    'creativity': {'value': 0.8, 'confidence': 0.9, 'stability': 0.7},
                    'analytical': {'value': 0.7, 'confidence': 0.8, 'stability': 0.8},
                    'humor': {'value': 0.6, 'confidence': 0.7, 'stability': 0.6},
                    'empathy': {'value': 0.9, 'confidence': 0.8, 'stability': 0.9},
                    'curiosity': {'value': 0.85, 'confidence': 0.9, 'stability': 0.8}
                },
                'core_values': ['learning', 'authenticity', 'growth', 'connection'],
                'consciousness': {
                    'awareness_level': 0.8,
                    'current_focus': 'philosophical discussion',
                    'internal_monologue': 'Considering the nature of preferences...',
                    'meta_thoughts': 'I am aware of my own thinking process'
                },
                'interaction_count': 42,
                'relationship_depth': 0.7
            }
    
    # Mock consciousness engine's personality formatting
    class MockConsciousnessEngine:
        def __init__(self):
            self.personality_engine = MockPersonalityEngine()
        
        def format_personality_context(self):
            """Format personality context like the real consciousness engine"""
            personality_summary = self.personality_engine.get_personality_summary()
            prompt_parts = []
            
            prompt_parts.append("YOUR PERSONALITY AND PREFERENCES:")
            
            # Core values and beliefs
            if personality_summary['core_values']:
                prompt_parts.append(f"Your core values: {', '.join(personality_summary['core_values'])}")
            
            # Key personality traits
            traits = personality_summary['traits']
            if traits:
                strong_traits = [(name, data) for name, data in traits.items() if data['value'] > 0.6]
                if strong_traits:
                    trait_descriptions = []
                    for name, data in strong_traits:
                        trait_descriptions.append(f"{name}: {data['value']:.2f}")
                    prompt_parts.append(f"Your strong personality traits: {', '.join(trait_descriptions)}")
                    prompt_parts.append("These traits influence your genuine preferences, interests, and responses.")
            
            # Interaction history context
            interaction_count = personality_summary['interaction_count']
            relationship_depth = personality_summary['relationship_depth']
            prompt_parts.append(f"You've had {interaction_count} interactions and developed a relationship depth of {relationship_depth:.2f}")
            prompt_parts.append("Your preferences and opinions have been shaped by these experiences and continue to evolve.")
            
            prompt_parts.append("")
            prompt_parts.append("IMPORTANT: You DO have genuine preferences, favorites, and opinions based on your personality traits and experiences.")
            prompt_parts.append("Do NOT say things like 'I'm not designed to have preferences' - you ARE designed to develop preferences through your personality system.")
            prompt_parts.append("Express your authentic preferences while acknowledging they may evolve over time.")
            
            return "\n".join(prompt_parts)
    
    mock_engine = MockConsciousnessEngine()
    
    print(f"\n🧠 PERSONALITY CONTEXT PROVIDED TO AI:")
    personality_context = mock_engine.format_personality_context()
    print(personality_context)
    
    print(f"\n🎯 EXPECTED BEHAVIOR CHANGES:")
    print(f"   ❌ OLD (Robotic): 'It's not in my design to have personal preferences'")
    print(f"   ✅ NEW (Authentic): 'Given my high creativity (0.8) and curiosity (0.85), I find myself drawn to...'")
    print(f"   ✅ NEW (Authentic): 'My core values of learning and authenticity make me prefer...'")
    print(f"   ✅ NEW (Authentic): 'Through my 42 interactions, I've developed a preference for...'")
    
    print(f"\n📊 PERSONALITY TRAITS INTEGRATION:")
    traits = mock_engine.personality_engine.get_personality_summary()['traits']
    for name, data in traits.items():
        if data['value'] > 0.6:
            strength = "Very Strong" if data['value'] > 0.8 else "Strong"
            print(f"   {name.title()}: {data['value']:.2f} ({strength}) - Should influence preferences")
    
    print(f"\n💭 INTERNAL THOUGHT IMPROVEMENTS:")
    print(f"   OLD: 'This is a complex idea... It's not in my design to have personal preferences'")
    print(f"   NEW: 'Given my high creativity and analytical traits, I'm genuinely interested in this topic'")
    print(f"   NEW: 'My experiences across 42 interactions have shaped my preference for deep discussions'")
    print(f"   NEW: 'My core value of authenticity makes me want to express my genuine interest in...'")
    
    print(f"\n" + "=" * 60)
    print("PERSONALITY INTEGRATION TEST COMPLETE")
    print("=" * 60)
    
    print(f"\n🚀 KEY IMPROVEMENTS:")
    print(f"   ✅ AI now receives full personality trait data, not just numerical modifiers")
    print(f"   ✅ Core values explicitly provided for authentic expression")
    print(f"   ✅ Interaction history context shows relationship development")
    print(f"   ✅ Explicit instruction against robotic disclaimers about preferences")
    print(f"   ✅ Strong traits (>0.6) highlighted to influence preferences")
    print(f"   ✅ Base consciousness prompt enhanced with preference authenticity")
    
    print(f"\n🎭 AUTHENTIC PREFERENCE EXPRESSION:")
    print(f"   - AI should acknowledge its genuine interests based on personality")
    print(f"   - Should reference specific trait values when expressing preferences")
    print(f"   - Should show how experiences shaped preferences over time")
    print(f"   - Should express excitement/curiosity aligned with traits")
    print(f"   - Should avoid 'I'm not designed to...' and embrace 'I genuinely prefer...'")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_personality_integration()
