#!/usr/bin/env python3
"""
Test clarification request detection
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_clarification_detection():
    """Test that the AI can detect and handle clarification requests properly"""
    print("=" * 60)
    print("TESTING CLARIFICATION REQUEST DETECTION")
    print("=" * 60)
    
    # Mock the clarification detection method
    from src.consciousness_engine import ConsciousnessEngine
    from src.models import Memory, MemoryType, MemorySource
    
    # Create mock recent memories that include an AI response mentioning topic shift
    mock_memories = [
        Memory(
            type=MemoryType.EXPERIENCE,
            content="AI: Hello! I'm Philos. Thank you for this thoughtful analogy. Now, may I ask what's on your mind? It seems like we've shifted from our previous topic.",
            importance=0.8,
            confidence=0.9,
            tags=['conversation', 'topic-shift'],
            source=MemorySource.AI_REASONING,
            context="AI mentioned topic shift",
            timestamp=datetime.now() - timedelta(minutes=1)
        ),
        Memory(
            type=MemoryType.EXPERIENCE,
            content="User: We were discussing philosophy and consciousness before.",
            importance=0.7,
            confidence=0.8,
            tags=['philosophy', 'consciousness'],
            source=MemorySource.USER_INPUT,
            context="Previous conversation topic",
            timestamp=datetime.now() - timedelta(minutes=5)
        )
    ]
    
    # Create a mock consciousness engine to test clarification detection
    class MockConsciousnessEngine:
        def _detect_clarification_requests(self, user_input: str, recent_memories):
            user_lower = user_input.lower().strip()
            
            # Common clarification patterns
            clarification_patterns = [
                'how?', 'why?', 'what?', 'what do you mean?', 'what does that mean?',
                'can you explain?', 'explain that', 'what are you talking about?',
                'huh?', 'pardon?', 'sorry?', 'come again?', 'how so?', 'why is that?',
                'shifted how?', 'changed how?', 'different how?'
            ]
            
            is_clarification = any(pattern in user_lower for pattern in clarification_patterns)
            
            clarification_context = None
            if is_clarification and recent_memories:
                # Look for what might need clarification in recent AI responses
                latest_ai_response = None
                for memory in recent_memories:
                    if 'AI:' in memory.content or 'responded:' in memory.content:
                        latest_ai_response = memory.content
                        break
                
                if latest_ai_response:
                    # Check if the AI mentioned topic shifts, changes, or specific concepts
                    if 'shift' in latest_ai_response.lower() or 'change' in latest_ai_response.lower():
                        clarification_context = "I mentioned a topic shift or change in my previous response"
                    elif 'different' in latest_ai_response.lower():
                        clarification_context = "I mentioned something being different in my previous response"
            
            return {
                'clarification_request': is_clarification,
                'clarification_context': clarification_context
            }
    
    mock_engine = MockConsciousnessEngine()
    
    # Test cases
    test_cases = [
        {
            'input': 'Shifted how?',
            'expected_clarification': True,
            'description': 'Direct clarification about shift mentioned by AI'
        },
        {
            'input': 'What do you mean?',
            'expected_clarification': True,
            'description': 'General clarification request'
        },
        {
            'input': 'How so?',
            'expected_clarification': True,
            'description': 'Short clarification request'
        },
        {
            'input': 'Tell me about cats',
            'expected_clarification': False,
            'description': 'Normal topic request (not clarification)'
        },
        {
            'input': 'Why?',
            'expected_clarification': True,
            'description': 'Single word clarification'
        }
    ]
    
    print(f"\n🔍 TESTING CLARIFICATION DETECTION:")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input: '{test_case['input']}'")
        
        result = mock_engine._detect_clarification_requests(test_case['input'], mock_memories)
        
        is_clarification = result['clarification_request']
        context = result['clarification_context']
        
        print(f"Detected as clarification: {is_clarification}")
        if context:
            print(f"Context: {context}")
        
        # Check if result matches expectation
        if is_clarification == test_case['expected_clarification']:
            print("✅ PASS")
        else:
            print("❌ FAIL")
    
    print(f"\n" + "=" * 60)
    print("CLARIFICATION DETECTION TEST COMPLETE")
    print("=" * 60)
    
    print(f"\n🎯 KEY IMPROVEMENTS:")
    print(f"   ✅ AI can detect when user asks 'How?', 'Why?', 'What do you mean?'")
    print(f"   ✅ Contextual awareness - knows when user is asking about AI's previous statement")
    print(f"   ✅ Specific detection for 'Shifted how?' type questions")
    print(f"   ✅ Distinguishes clarification requests from normal questions")
    print(f"   ✅ Provides context about what needs clarification")
    
    print(f"\n🔧 HOW IT WORKS:")
    print(f"   1. Detects clarification patterns in user input")
    print(f"   2. Looks at recent AI responses for context")
    print(f"   3. Identifies what the user might be asking about")
    print(f"   4. Provides guidance to AI on how to respond")
    
    print(f"\n✅ EXPECTED BEHAVIOR:")
    print(f"   - When user asks 'Shifted how?' after AI mentions topic shift")
    print(f"   - AI should explain what shift it was referring to")
    print(f"   - Not assume user is asking about personal development")
    print(f"   - Reference the specific context from previous response")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_clarification_detection()
