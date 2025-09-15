#!/usr/bin/env python3
"""
Test script for AI query restructuring
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from web_search import WebSearchManager
import openai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def test_query_restructuring():
    """Test the AI query restructuring functionality"""
    
    # Set up the web search manager with OpenAI client
    try:
        client = openai.OpenAI()
        web_search = WebSearchManager(openai_client=client)
        
        test_queries = [
            "can you search up the wikipedia page for charles darwin and tell me what the first line is?",
            "look up who the current king of england is",
            "google the latest iPhone release date", 
            "nothing much, just chatting",
            "search up the weather today"
        ]
        
        print("Testing AI Query Restructuring:")
        print("=" * 50)
        
        for query in test_queries:
            result = web_search.extract_search_query(query, "I'm not sure about that.")
            print(f"Input: '{query}'")
            print(f"Output: '{result}'")
            print("-" * 30)
            
    except Exception as e:
        print(f"Error testing query restructuring: {e}")
        print("Falling back to basic extraction test...")
        
        web_search = WebSearchManager()  # No OpenAI client
        for query in test_queries:
            result = web_search.extract_search_query(query, "I'm not sure about that.")
            print(f"Basic extraction - Input: '{query}' → Output: '{result}'")

if __name__ == "__main__":
    test_query_restructuring()
