#!/usr/bin/env python3

from src.web_search import WebSearchManager

def test_inappropriate_search_prevention():
    """Test that Philos doesn't search for things that don't need searching"""
    
    print("=== Testing Inappropriate Search Prevention ===")
    
    web_search = WebSearchManager()
    
    test_cases = [
        # Conversations that should NOT trigger searches
        {
            "user_input": "i haven't actually watched or heard of them until you now just brought them up",
            "ai_response": "If I had to pick franchises that feel like my 'favorites'...",
            "should_search": False,
            "description": "User saying they haven't heard of something"
        },
        {
            "user_input": "now read me the next line after the first line",
            "ai_response": "Here's the Wikipedia content about Darwin...",
            "should_search": False, 
            "description": "User asking to read existing content"
        },
        {
            "user_input": "continue reading from where you left off",
            "ai_response": "I was reading about evolution theory...",
            "should_search": False,
            "description": "User asking to continue reading existing content"
        },
        {
            "user_input": "read the next paragraph please",
            "ai_response": "From the Darwin article:",
            "should_search": False,
            "description": "User asking to read more of existing content"
        },
        # Conversations that SHOULD trigger searches
        {
            "user_input": "search up information about Einstein",
            "ai_response": "I'll look that up for you...",
            "should_search": True,
            "description": "Explicit search request"
        },
        {
            "user_input": "tell me more about quantum physics",
            "ai_response": "I don't have current information about that...",
            "should_search": True,
            "description": "AI expressing uncertainty"
        },
        {
            "user_input": "what's the latest news about space exploration",
            "ai_response": "Let me check...",
            "should_search": True,
            "description": "Current events query"
        }
    ]
    
    print(f"\nTesting {len(test_cases)} scenarios...\n")
    
    all_passed = True
    for i, test_case in enumerate(test_cases, 1):
        result = web_search.should_search(test_case["user_input"], test_case["ai_response"])
        expected = test_case["should_search"]
        
        if result == expected:
            status = "✓ PASS"
        else:
            status = "✗ FAIL"
            all_passed = False
        
        print(f"Test {i}: {status}")
        print(f"  Description: {test_case['description']}")
        print(f"  Input: \"{test_case['user_input']}\"")
        print(f"  Expected: {expected}, Got: {result}")
        print()
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! Search triggering logic is working correctly.")
    else:
        print("❌ Some tests failed. Search logic needs adjustment.")
    
    print("\n=== Inappropriate Search Prevention Test Complete ===")

if __name__ == "__main__":
    test_inappropriate_search_prevention()