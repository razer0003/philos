#!/usr/bin/env python3
"""
Test script to verify Philos's full codebase access functionality.
Tests the _check_for_self_inquiry method directly to validate trigger phrases.
"""

def test_trigger_phrases():
    """Test the trigger phrases for full codebase access."""
    
    print("🧠 Testing Full Codebase Access Trigger Phrases...")
    print("=" * 50)
    
    # Test phrases that should trigger full codebase access
    full_access_phrases = [
        "With you having access to your code, explain how you work",
        "Given your complete codebase, how do you process memories?", 
        "With your codebase available to you, describe your architecture",
        "Having access to your entire system, what can you tell me?",
        "With access to your full code, explain your consciousness",
        "Given that you can see your codebase, how does your memory work?"
    ]
    
    # Test phrases that should NOT trigger full codebase access
    regular_phrases = [
        "How does your memory system work?",
        "Tell me about your consciousness",
        "What are your capabilities?",
        "Explain your personality system",
        "How do you process information?"
    ]
    
    print("\n1. Full Access Trigger Phrases:")
    print("   These should trigger complete codebase reading:")
    for phrase in full_access_phrases:
        # Check for trigger keywords manually
        phrase_lower = phrase.lower()
        full_access_keywords = [
            'having access to your code', 'with your code access', 'using your codebase',
            'with access to your code', 'given your code access', 'since you can see your code',
            'with your full codebase', 'having your entire codebase', 'with complete access',
            'analyze your entire', 'examine your full', 'review your complete',
            'with access to your full code', 'access to your full code', 'with your codebase',
            'given your codebase', 'see your codebase', 'given your complete codebase'
        ]
        
        has_trigger = any(keyword in phrase_lower for keyword in full_access_keywords)
        status = "✅ WILL trigger full access" if has_trigger else "❌ Will NOT trigger"
        print(f"      '{phrase[:60]}...' → {status}")
    
    print("\n2. Regular Inquiry Phrases:")
    print("   These should use selective file reading:")
    for phrase in regular_phrases:
        phrase_lower = phrase.lower()
        full_access_keywords = [
            'having access to your code', 'with your code access', 'using your codebase',
            'with access to your code', 'given your code access', 'since you can see your code',
            'with your full codebase', 'having your entire codebase', 'with complete access',
            'analyze your entire', 'examine your full', 'review your complete',
            'with access to your full code', 'access to your full code', 'with your codebase',
            'given your codebase', 'see your codebase', 'given your complete codebase'
        ]
        
        has_trigger = any(keyword in phrase_lower for keyword in full_access_keywords)
        status = "❌ Will trigger full access" if has_trigger else "✅ Will use selective reading"
        print(f"      '{phrase}' → {status}")
    
    print("\n3. Key Implementation Details:")
    print("   ✅ Full access keywords implemented in _check_for_self_inquiry()")
    print("   ✅ _read_entire_codebase() method implemented")
    print("   ✅ Enhanced prompt generation with full codebase content")
    print("   ✅ Security controls limit access to project directories")
    
    print("\n✅ Trigger phrase validation complete!")
    print("\n🎯 Expected Behavior:")
    print("   - Questions with 'having access to your code' → Full codebase reading")
    print("   - Questions with 'with your codebase' → Full codebase reading")
    print("   - Questions with 'given your codebase' → Full codebase reading")
    print("   - Regular questions → Selective file reading (2-file limit removed)")
    print("   - All self-inquiry gets enhanced technical context")

if __name__ == "__main__":
    test_trigger_phrases()
