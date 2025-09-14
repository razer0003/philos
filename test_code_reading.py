#!/usr/bin/env python3
"""
Test Philos's ability to read and understand his own code
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_companion import AICompanion

def test_code_reading():
    """Test if Philos can read and explain his own code"""
    
    print("🧠 Testing Philos's Code Reading Capabilities")
    print("=" * 50)
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set")
        return
    
    try:
        ai = AICompanion()
        
        # Test questions that should trigger code reading
        test_queries = [
            "Can you show me your consciousness engine code?",
            "How does your memory system work? Show me the implementation.",
            "Explain your web search functionality - I want to see the code.",
            "What's in your personality engine? Can you read it for me?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test {i}: {query}")
            print("-" * 40)
            
            try:
                result = ai.interact(query)
                
                # Check if source file content was included
                if 'source_files' in str(result):
                    print("✅ Source file reading detected!")
                else:
                    print("⚠️  No source file reading detected")
                
                print(f"💭 Response preview: {result['response'][:200]}...")
                
                # Check response metadata
                if result.get('internal_monologue'):
                    print(f"🧠 Internal thoughts: {result['internal_monologue'][:100]}...")
                
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
    
    except Exception as e:
        print(f"❌ Failed to initialize AI: {e}")

if __name__ == "__main__":
    test_code_reading()
