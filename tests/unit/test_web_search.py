#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.web_search import WebSearchManager

def test_web_search():
    """Test the web search functionality"""
    
    search_manager = WebSearchManager()
    
    # Test queries
    test_queries = [
        "What is Python programming language",
        "Current weather in New York",
        "Who is the president of the United States",
        "What happened in 2025"
    ]
    
    print("Testing Web Search Functionality")
    print("=" * 50)
    
    for query in test_queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 30)
        
        # Test search
        result = search_manager.search_web(query, max_results=3)
        
        if result['success']:
            print(f"✅ Search successful!")
            print(f"Found {result['results_count']} results")
            print(f"Summary: {result['summary'][:200]}...")
            
            if result['results']:
                print("Results:")
                for i, res in enumerate(result['results'][:2], 1):
                    print(f"  {i}. {res['title']} ({res['type']})")
                    print(f"     {res['content'][:100]}...")
        else:
            print(f"❌ Search failed: {result.get('error', 'Unknown error')}")
        
        print()
    
    # Test search detection
    print("\nTesting Search Detection")
    print("=" * 30)
    
    test_cases = [
        ("What's the weather like?", "I don't know the current weather conditions"),
        ("Tell me about cats", "Cats are domestic animals that..."),
        ("Look up the latest news", "I'll help you find that information"),
        ("What happened today?", "I'm not sure what specific events you're referring to")
    ]
    
    for user_query, ai_response in test_cases:
        should_search = search_manager.should_search(user_query, ai_response)
        print(f"Query: '{user_query}'")
        print(f"AI Response: '{ai_response}'") 
        print(f"Should search: {'✅ Yes' if should_search else '❌ No'}")
        if should_search:
            extracted_query = search_manager.extract_search_query(user_query, ai_response)
            print(f"Extracted query: '{extracted_query}'")
        print()

if __name__ == "__main__":
    test_web_search()
