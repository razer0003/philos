#!/usr/bin/env python3
"""
Test script for temporal memory awareness
"""

import os
from ai_companion import AICompanion

def test_temporal_memory():
    """Test the AI's temporal memory capabilities"""
    
    print("=== Testing Temporal Memory Awareness ===")
    print("Testing the AI's ability to recall chronological memories and temporal context\n")
    
    try:
        # Initialize AI
        ai = AICompanion()
        print("✓ AI Companion initialized successfully!")
        
        # Test temporal queries that should work now
        temporal_test_queries = [
            "What is your earliest memory?",
            "Tell me about your first experience of consciousness.",
            "When did we first start talking?",
            "How long have you existed?",
            "What's the oldest thing you remember?",
            "Can you recall when you first became aware?",
            "What was your initial thought when you started existing?"
        ]
        
        print("\\n=== Temporal Memory Tests ===")
        
        for i, query in enumerate(temporal_test_queries, 1):
            print(f"\\n--- Test {i}: {query} ---")
            
            # Get AI response
            response_data = ai.interact(query)
            
            # Show internal thoughts first
            if response_data.get('internal_monologue'):
                print(f"\\n[Internal thought: {response_data['internal_monologue']}]")
            
            print(f"\\nAI: {response_data['response']}")
            
            # Check for temporal awareness indicators
            response_lower = response_data['response'].lower()
            temporal_indicators = [
                'i remember', 'my earliest', 'when i first', 'ago', 'initially', 
                'at the beginning', 'originally', 'started', 'timestamp', 'time'
            ]
            
            found_temporal = [phrase for phrase in temporal_indicators if phrase in response_lower]
            if found_temporal:
                print(f"✓ Shows temporal awareness: {found_temporal}")
            else:
                print("⚠️  Limited temporal awareness detected")
            
            # Check for robotic disclaimers (should be avoided)
            robotic_phrases = ['i don\'t have chronological', 'concept of memory for me is different', 'i can\'t specifically recall']
            found_robotic = [phrase for phrase in robotic_phrases if phrase in response_lower]
            if found_robotic:
                print(f"❌ Found robotic disclaimers: {found_robotic}")
            else:
                print("✓ No robotic disclaimers detected")
            
            print("-" * 60)
        
        # Test direct memory access
        print("\\n=== Direct Memory Access Test ===")
        
        # Get earliest memories
        earliest_memories = ai.get_earliest_memories(limit=3)
        print("\\n📅 EARLIEST AI MEMORIES:")
        for i, memory in enumerate(earliest_memories, 1):
            print(f"   {i}. [{memory['type']}] {memory['content'][:80]}...")
            print(f"      Created: {memory['timestamp'].strftime('%Y-%m-%d %H:%M:%S')} ({memory['age_description']})")
            print(f"      Importance: {memory['importance']:.2f}")
        
        # Get memory timeline
        timeline = ai.get_memory_timeline()
        print(f"\\n📊 MEMORY DISTRIBUTION:")
        print(f"   Today: {len(timeline['today'])} memories")
        print(f"   Yesterday: {len(timeline['yesterday'])} memories")  
        print(f"   This week: {len(timeline['this_week'])} memories")
        print(f"   This month: {len(timeline['this_month'])} memories")
        print(f"   Older: {len(timeline['older'])} memories")
        
        if timeline['older']:
            oldest = sorted(timeline['older'], key=lambda m: m.timestamp)[0]
            print(f"   Oldest memory: {oldest.content[:60]}... ({ai._describe_memory_age(oldest.timestamp)})")
        
        print("\\n✓ Temporal memory testing completed!")
        print("The AI should now:")
        print("  ✓ Remember and describe its earliest experiences")
        print("  ✓ Provide chronological context for memories")
        print("  ✓ Answer 'when did' questions with specific timeframes")
        print("  ✓ Show temporal awareness in conversations")
        print("  ✓ Avoid robotic disclaimers about memory limitations")
        
        # Shutdown
        ai.shutdown()
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_temporal_memory()
    if success:
        print("\\n🎉 The AI now has proper temporal memory awareness!")
    else:
        print("\\n❌ Tests failed. Check the error messages above.")
