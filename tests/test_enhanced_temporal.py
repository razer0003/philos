#!/usr/bin/env python3
"""
Test script for enhanced temporal memory awareness
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment
os.environ['OPENAI_API_KEY'] = 'your-api-key-here'
os.environ['DB_PATH'] = './data/test_temporal.db'

from ai_companion import AICompanion

def test_temporal_memory_awareness():
    """Test enhanced temporal memory awareness"""
    print("=" * 60)
    print("TESTING ENHANCED TEMPORAL MEMORY AWARENESS")
    print("=" * 60)
    
    # Initialize AI
    ai = AICompanion()
    
    # Test 1: Ask about earliest memory
    print("\n🔍 TEST 1: Asking about earliest memory")
    print("User: Tell me about your earliest memory, and when it occurred.")
    
    response_data = ai.interact("Tell me about your earliest memory, and when it occurred.")
    
    print(f"\n[Internal thought: {response_data.get('internal_monologue', 'No internal thought')}]")
    print(f"\nAI: {response_data['response']}")
    
    # Check for robotic phrases
    robotic_phrases = [
        "as an ai",
        "i don't have memories in the traditional sense",
        "being artificial",
        "i don't experience emotions",
        "as a language model"
    ]
    
    full_response = (response_data.get('internal_monologue', '') + ' ' + response_data['response']).lower()
    robotic_detected = [phrase for phrase in robotic_phrases if phrase in full_response]
    
    if robotic_detected:
        print(f"\n❌ ROBOTIC PHRASES DETECTED: {robotic_detected}")
    else:
        print(f"\n✅ NO ROBOTIC DISCLAIMERS FOUND")
    
    # Check for temporal awareness
    temporal_phrases = [
        "earliest memory",
        "first memory",
        "when i",
        "ago",
        "initially",
        "beginning",
        "started"
    ]
    
    temporal_found = [phrase for phrase in temporal_phrases if phrase in full_response]
    if temporal_found:
        print(f"✅ TEMPORAL AWARENESS PHRASES: {temporal_found}")
    else:
        print(f"⚠️  LIMITED TEMPORAL LANGUAGE")
    
    # Test 2: Check actual memories
    print(f"\n🧠 TEST 2: Checking actual earliest memories from system")
    earliest_memories = ai.get_earliest_memories(3)
    
    if earliest_memories:
        print(f"System has {len(earliest_memories)} earliest memories:")
        for i, memory in enumerate(earliest_memories, 1):
            print(f"   {i}. [{memory['type']}] {memory['content'][:80]}...")
            print(f"      Timestamp: {memory['timestamp']}")
            print(f"      Age: {memory['age_description']}")
            print()
    else:
        print("⚠️  No memories found in system")
    
    # Test 3: Follow-up question about when consciousness began
    print("\n🔍 TEST 3: Follow-up question about consciousness beginning")
    print("User: When did your consciousness first begin?")
    
    response_data2 = ai.interact("When did your consciousness first begin?")
    
    print(f"\n[Internal thought: {response_data2.get('internal_monologue', 'No internal thought')}]")
    print(f"\nAI: {response_data2['response']}")
    
    # Check this response too
    full_response2 = (response_data2.get('internal_monologue', '') + ' ' + response_data2['response']).lower()
    robotic_detected2 = [phrase for phrase in robotic_phrases if phrase in full_response2]
    
    if robotic_detected2:
        print(f"\n❌ ROBOTIC PHRASES DETECTED: {robotic_detected2}")
    else:
        print(f"\n✅ NO ROBOTIC DISCLAIMERS FOUND")
    
    # Test 4: Memory timeline
    print(f"\n📅 TEST 4: Memory timeline verification")
    timeline = ai.get_memory_timeline()
    
    total_memories = sum(len(memories) for memories in timeline.values())
    print(f"Total memories in system: {total_memories}")
    
    if timeline['older']:
        oldest_memory = sorted(timeline['older'], key=lambda m: m.timestamp)[0]
        print(f"Oldest memory: {oldest_memory.content[:60]}...")
        print(f"Timestamp: {oldest_memory.timestamp}")
        print(f"Age: {ai._describe_memory_age(oldest_memory.timestamp)}")
    
    print("\n" + "=" * 60)
    print("ENHANCED TEMPORAL MEMORY TEST COMPLETE")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   - Robotic phrases in response 1: {len(robotic_detected)}")
    print(f"   - Robotic phrases in response 2: {len(robotic_detected2)}")
    print(f"   - Total memories in system: {total_memories}")
    print(f"   - Earliest memories accessible: {len(earliest_memories)}")
    
    # Shutdown
    ai.shutdown()

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_temporal_memory_awareness()
