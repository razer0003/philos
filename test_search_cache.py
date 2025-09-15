#!/usr/bin/env python3

import time
from src.web_search import WebSearchManager

def test_search_cache_fixes():
    """Test that search cache fixes prevent cross-conversation contamination"""
    
    print("=== Testing Search Cache Fixes ===")
    
    # Create web search manager
    web_search = WebSearchManager()
    
    print("\nTest 1: Search cache expiration")
    
    # Simulate a search from a previous conversation
    web_search.last_search_query = "Charles Darwin Wikipedia"
    web_search.last_search_time = time.time() - 150  # 2.5 minutes ago (should expire)
    
    # Test contextual followup with expired cache
    result = web_search._is_contextual_followup(
        "i haven't actually watched or heard of them until you now just brought them up",
        "Hey — that's a cool trigger. The Hobbit pulling that thread makes sense..."
    )
    
    if not result:
        print("✓ SUCCESS: Expired cache correctly ignored")
    else:
        print("✗ FAILED: Expired cache still being used")
    
    # Verify cache was cleared
    if not web_search.last_search_query:
        print("✓ SUCCESS: Cache automatically cleared on expiration")
    else:
        print("✗ FAILED: Cache not cleared after expiration")
    
    print("\nTest 2: Recent cache with unrelated context")
    
    # Set up a recent search
    web_search.last_search_query = "Charles Darwin Wikipedia"  
    web_search.last_search_time = time.time() - 30  # 30 seconds ago (should be valid)
    
    # Test with completely unrelated conversation
    result2 = web_search._is_contextual_followup(
        "i haven't actually watched or heard of them until you now just brought them up",
        "If I had to pick franchises that feel like my 'favorites,' these would be the top contenders..."
    )
    
    print(f"Recent cache with unrelated context: {result2}")
    print(f"Cache query: {web_search.last_search_query}")
    
    print("\nTest 3: Manual cache clearing")
    
    # Test manual cache clearing
    web_search.last_search_query = "Some test query"
    web_search.last_search_time = time.time()
    
    print(f"Before clear: {web_search.last_search_query}")
    web_search.clear_search_cache()
    print(f"After clear: {web_search.last_search_query}")
    
    if not web_search.last_search_query:
        print("✓ SUCCESS: Manual cache clearing works")
    else:
        print("✗ FAILED: Manual cache clearing failed")
    
    print("\n=== Search Cache Test Complete ===")

if __name__ == "__main__":
    test_search_cache_fixes()