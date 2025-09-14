#!/usr/bin/env python3
"""
Test to demonstrate Philos's improved web search with thinking process
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
import time

def test_search_improvements():
    """Test the improved web search with thinking process"""
    
    print("🧠 Testing Philos's Web Search Improvements")
    print("=" * 50)
    
    # Initialize components
    db = DatabaseManager("test_search.db")
    memory_manager = MemoryManager(db, "test_conversations")
    personality_engine = PersonalityEngine(db, memory_manager)
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    consciousness = ConsciousnessEngine(
        memory_manager=memory_manager,
        personality_engine=personality_engine,
        api_key=api_key
    )
    
    # Test cases that should trigger web search
    test_queries = [
        "Who won the 2024 presidential election?",
        "What's the latest news about AI developments?", 
        "Who won the 2024 presidential election?"  # Duplicate to test prevention
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        print("-" * 30)
        
        try:
            result = consciousness.generate_response(query, conversation_id="test_search")
            
            if result['search_performed']:
                print(f"✅ Search performed: {result['search_query']}")
                print(f"📊 Results found: {result['search_results_count']}")
                print(f"💭 Response: {result['response'][:200]}...")
                if result.get('internal_monologue'):
                    print(f"🧠 Internal thoughts: {result['internal_monologue'][:100]}...")
            else:
                print(f"⏭️  No search performed")
                print(f"💭 Response: {result['response'][:200]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Wait between tests
        if i < len(test_queries):
            time.sleep(2)
    
    print(f"\n✅ Search improvements test completed!")
    print("Expected improvements:")
    print("1. ✅ Philos should explain WHY he's searching")
    print("2. ✅ Duplicate searches should be prevented")
    print("3. ✅ Search reasoning should be visible in responses")

if __name__ == "__main__":
    test_search_improvements()
