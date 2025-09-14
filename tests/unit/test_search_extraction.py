#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.web_search import WebSearchManager

def test_search_query_extraction():
    """Test the search query extraction functionality"""
    
    search_manager = WebSearchManager()
    
    test_cases = [
        ("What's happened in 2025 Philos?", "I don't know", "events in 2025"),
        ("Who is the current president?", "I'm not sure", "current president"),
        ("What's the weather like today?", "I don't have current data", "weather today"),
        ("Look up information about AI developments", "", "AI developments"),
        ("Can you search for recent news?", "", "recent news"),
    ]
    
    print("Testing search query extraction:")
    print("=" * 60)
    
    for user_input, ai_response, expected in test_cases:
        extracted = search_manager.extract_search_query(user_input, ai_response)
        print(f"Input: '{user_input}'")
        print(f"Expected: '{expected}'")
        print(f"Extracted: '{extracted}'")
        print(f"Match: {'✓' if extracted.lower() == expected.lower() else '✗'}")
        print("-" * 40)

def test_search_triggers():
    """Test when search should be triggered"""
    
    search_manager = WebSearchManager()
    
    trigger_cases = [
        ("What happened in 2025?", "I don't know much about 2025", True),
        ("How are you?", "I'm doing well", False),
        ("What's the latest news?", "I'm not sure about current events", True),
        ("Search for AI news", "Sure, I'll search", True),
        ("Tell me about cats", "Cats are amazing creatures", False),
    ]
    
    print("\nTesting search trigger detection:")
    print("=" * 60)
    
    for user_input, ai_response, should_trigger in trigger_cases:
        result = search_manager.should_search(user_input, ai_response)
        print(f"Input: '{user_input}'")
        print(f"AI Response: '{ai_response}'")
        print(f"Should trigger: {should_trigger}")
        print(f"Actually triggers: {result}")
        print(f"Match: {'✓' if result == should_trigger else '✗'}")
        print("-" * 40)

if __name__ == "__main__":
    test_search_query_extraction()
    test_search_triggers()
