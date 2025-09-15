#!/usr/bin/env python3

from src.web_search import WebSearchManager

def debug_search_triggers():
    """Debug which triggers are firing inappropriately"""
    
    web_search = WebSearchManager()
    
    test_input = "i haven't actually watched or heard of them until you now just brought them up"
    test_response = "If I had to pick franchises that feel like my 'favorites'..."
    
    query_lower = test_input.lower()
    response_lower = test_response.lower()
    
    print(f"Testing: '{test_input}'")
    print(f"Response: '{test_response}'")
    print()
    
    # Check explicit search triggers
    search_triggers = [
        # Direct search commands
        'search for', 'search up', 'look up', 'google', 'bing',
        'find information about', 'find out about',
        'can you search', 'look it up', 'find out',
        'search it up', 'look this up', 'google it',
        'check online', 'find online', 'search online',
        
        # Question patterns that imply searching
        'what\'s the latest', 'current information', 'recent news',
        'who is the current', 'what is the current',
        'who\'s the', 'what\'s the', 'when did',
        
        # Uncertainty + request patterns
        'do you know who', 'do you know what', 'do you know when'
    ]
    
    triggered_search = [trigger for trigger in search_triggers if trigger in query_lower]
    if triggered_search:
        print(f"❌ Explicit search triggers: {triggered_search}")
    else:
        print("✓ No explicit search triggers")
    
    # Check uncertainty indicators
    uncertainty_indicators = [
        "i don't know", "i'm not sure", "i don't have information",
        "i'm not certain", "i don't have current data",
        "i'm not familiar", "i don't recall", "i'm unsure",
        "no information", "not sure about", "don't have details"
    ]
    
    triggered_uncertainty = [indicator for indicator in uncertainty_indicators if indicator in response_lower]
    if triggered_uncertainty:
        print(f"❌ Uncertainty indicators: {triggered_uncertainty}")
    else:
        print("✓ No uncertainty indicators")
    
    # Check current indicators
    current_indicators = [
        'today', 'this year', 'recently', 'latest', 'current',
        'what\'s happening now', 'right now', '2025', 'newest', 'updated', 'breaking'
    ]
    
    triggered_current = [indicator for indicator in current_indicators if indicator in query_lower]
    if triggered_current:
        print(f"❌ Current indicators: {triggered_current}")
    else:
        print("✓ No current indicators")
    
    # Check contextual follow-up
    followup_result = web_search._is_contextual_followup(test_input, test_response)
    if followup_result:
        print(f"❌ Contextual follow-up detected: {followup_result}")
    else:
        print("✓ No contextual follow-up")
    
    print()
    print(f"Final result: {web_search.should_search(test_input, test_response)}")

if __name__ == "__main__":
    debug_search_triggers()