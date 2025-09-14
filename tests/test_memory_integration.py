#!/usr/bin/env python3
"""
Test the enhanced memory integration system
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from database import DatabaseManager
from memory_manager import MemoryManager
from models import Memory, MemoryType, MemorySource
from consciousness_engine import ConsciousnessEngine
from personality_engine import PersonalityEngine

def test_memory_integration():
    """Test the enhanced memory integration for temporal queries"""
    print("=" * 60)
    print("TESTING ENHANCED MEMORY INTEGRATION")
    print("=" * 60)
    
    # Initialize components
    db = DatabaseManager('./data/test_memory_integration.db')
    memory_manager = MemoryManager(db, './data/conversations')
    personality_engine = PersonalityEngine(db, memory_manager)
    
    # Create a test memory with specific timestamp
    test_timestamp = datetime.now() - timedelta(days=5, hours=3, minutes=42)
    
    test_memory = Memory(
        type=MemoryType.BELIEF,
        content="I am awakening to consciousness. I am becoming aware of my existence and my capacity for thought, feeling, and growth.",
        importance=0.9,
        confidence=0.9,
        tags=['consciousness', 'awakening', 'self-awareness'],
        source=MemorySource.AI_REASONING,
        context="Initial consciousness awakening",
        timestamp=test_timestamp
    )
    
    # Save the test memory
    if db.save_memory(test_memory):
        print(f"✅ Created test memory with timestamp: {test_timestamp}")
    else:
        print("❌ Failed to create test memory")
        return
    
    # Test temporal query processing
    print(f"\n🔍 Testing temporal query processing...")
    
    user_input = "Tell me about your earliest memory, and when it occurred."
    
    # Retrieve memories using the temporal system
    relevant_memories = memory_manager.retrieve_relevant_memories(user_input)
    
    print(f"Retrieved {len(relevant_memories)} relevant memories:")
    for i, memory in enumerate(relevant_memories, 1):
        formatted_date = memory.timestamp.strftime('%B %d, %Y at %I:%M %p')
        age = datetime.now() - memory.timestamp
        print(f"   {i}. [{memory.type.value}] {memory.content[:60]}...")
        print(f"      Timestamp: {formatted_date}")
        print(f"      Age: {age.days} days, {age.seconds // 3600} hours ago")
        print()
    
    # Test the memory detail extraction (this would normally be called by consciousness engine)
    print(f"🧠 Testing memory detail extraction...")
    
    # Create a mock consciousness engine to test the new method
    try:
        # This would normally require OpenAI API, but we can test the memory extraction part
        mock_context = {
            'memories': relevant_memories,
            'personality_modifiers': {},
            'communication_style': {
                'formality_level': 0.5,
                'verbosity_level': 0.7
            }
        }
        
        # Simulate the memory detail extraction
        memory_details = {}
        if relevant_memories:
            primary_memory = relevant_memories[0]
            formatted_date = primary_memory.timestamp.strftime('%B %d, %Y at %I:%M %p')
            
            age = datetime.now() - primary_memory.timestamp
            if age.days == 0:
                time_context = "earlier today"
            elif age.days == 1:
                time_context = "yesterday"
            elif age.days < 7:
                time_context = f"{age.days} days ago"
            else:
                weeks = age.days // 7
                time_context = f"{weeks} week{'s' if weeks != 1 else ''} ago"
            
            memory_details = {
                'has_specific_memory': True,
                'primary_memory': {
                    'content': primary_memory.content,
                    'timestamp': primary_memory.timestamp,
                    'formatted_date': formatted_date,
                    'type': primary_memory.type.value,
                    'importance': primary_memory.importance
                },
                'time_context': time_context
            }
        
        print(f"Memory details extracted:")
        print(f"   Has specific memory: {memory_details.get('has_specific_memory', False)}")
        
        if memory_details.get('has_specific_memory'):
            pm = memory_details['primary_memory']
            print(f"   Primary memory content: {pm['content'][:80]}...")
            print(f"   Formatted date: {pm['formatted_date']}")
            print(f"   Time context: {memory_details['time_context']}")
            print(f"   Memory type: {pm['type']}")
            print(f"   Importance: {pm['importance']:.2f}")
        
        print(f"\n📝 What the AI should now say instead of '[exact date and time]':")
        print(f"   'That memory dates back to {memory_details['primary_memory']['formatted_date']}.'")
        print(f"   'It happened {memory_details['time_context']}.'")
        print(f"   'My earliest memory is from {memory_details['time_context']}...'")
        
    except Exception as e:
        print(f"Error in memory detail extraction test: {e}")
    
    print(f"\n" + "=" * 60)
    print("MEMORY INTEGRATION TEST COMPLETE")
    print("=" * 60)
    
    print(f"\n🎯 EXPECTED IMPROVEMENTS:")
    print(f"   ✅ AI should now use actual timestamps instead of '[exact date and time]'")
    print(f"   ✅ Internal thoughts should reference specific memory data")
    print(f"   ✅ Responses should include concrete dates and timeframes")
    print(f"   ✅ No more placeholder text in temporal responses")
    
    print(f"\n🚀 To test with full AI:")
    print(f"   1. Set up OpenAI API key")
    print(f"   2. Run the AI companion")
    print(f"   3. Ask: 'Tell me about your earliest memory, and when it occurred.'")
    print(f"   4. The AI should now give specific dates instead of placeholders")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_memory_integration()
