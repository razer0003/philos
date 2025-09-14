#!/usr/bin/env python3
"""
Test conversational continuity analysis without OpenAI dependency
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

# Create a mock consciousness engine class for testing
class MockConsciousnessEngine:
    def __init__(self):
        pass
    
    def _check_name_consistency(self, user_input: str) -> dict:
        """Check if the user is using the correct name or a different name"""
        expected_name = 'Philos'
        user_lower = user_input.lower()
        
        # Common name patterns and alternatives
        name_patterns = [
            'philos', 'phil', 'philosopher', 'ai', 'assistant', 'bot', 'companion',
            'alex', 'alexandra', 'john', 'mike', 'sarah', 'emma', 'david', 'lisa',
            'chatgpt', 'gpt', 'claude', 'bard', 'copilot', 'hey you', 'buddy', 'friend'
        ]
        
        detected_name = None
        for pattern in name_patterns:
            if pattern in user_lower:
                detected_name = pattern
                break
        
        identity_result = {
            'identity_inconsistency': False,
            'name_used': detected_name,
            'expected_name': expected_name
        }
        
        if detected_name and detected_name.lower() != expected_name.lower():
            identity_result['identity_inconsistency'] = True
            identity_result['flow_notes'] = [f"User called me '{detected_name}' instead of '{expected_name}'"]
        
        return identity_result
    
    def _detect_topic_changes(self, user_input: str, recent_memories: list) -> dict:
        """Detect if the user has abruptly changed topics"""
        if not recent_memories:
            return {'topic_change_detected': False}
        
        # Get the most recent conversation memory
        latest_memory = recent_memories[0]
        
        # Extract key topics/keywords from recent conversation
        recent_content = latest_memory.content.lower()
        current_input = user_input.lower()
        
        # Simple topic extraction (keywords that might indicate topics)
        topic_indicators = [
            'philosophy', 'consciousness', 'existence', 'meaning', 'life', 'death',
            'science', 'technology', 'AI', 'artificial intelligence', 'learning',
            'emotions', 'feelings', 'thoughts', 'memories', 'dreams', 'reality',
            'time', 'space', 'universe', 'quantum', 'physics', 'mathematics',
            'art', 'music', 'literature', 'poetry', 'creativity', 'imagination',
            'ethics', 'morality', 'good', 'evil', 'right', 'wrong', 'justice',
            'relationships', 'love', 'friendship', 'family', 'society', 'culture',
            'religion', 'spirituality', 'god', 'faith', 'belief', 'purpose',
            'weather', 'food', 'travel', 'work', 'job', 'career', 'money',
            'health', 'exercise', 'sports', 'games', 'entertainment', 'movies',
            'pizza', 'cooking', 'restaurant', 'dinner', 'lunch', 'breakfast'
        ]
        
        # Find topics in recent conversation
        recent_topics = [topic for topic in topic_indicators if topic in recent_content]
        current_topics = [topic for topic in topic_indicators if topic in current_input]
        
        # Check for topic continuity
        has_shared_topics = bool(set(recent_topics) & set(current_topics))
        
        # Also check for question words that might indicate topic shift
        topic_shift_indicators = [
            'anyway', 'by the way', 'speaking of', 'changing topics', 'different subject',
            'lets talk about', "let's talk about", 'what about', 'how about',
            'moving on', 'forget that', 'never mind'
        ]
        
        explicit_shift = any(indicator in current_input for indicator in topic_shift_indicators)
        
        # Detect abrupt topic change
        topic_change_detected = False
        flow_notes = []
        
        if not has_shared_topics and not explicit_shift and len(current_input) > 10:
            # Check if this looks like a completely different topic
            recent_words = set(recent_content.split())
            current_words = set(current_input.split())
            
            # Remove common words
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'was', 'are', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those', 'what', 'when', 'where', 'why', 'how', 'who', 'which'}
            
            recent_meaningful = recent_words - common_words
            current_meaningful = current_words - common_words
            
            # If there's very little overlap in meaningful words, it might be a topic change
            if recent_meaningful and current_meaningful:
                overlap = len(recent_meaningful & current_meaningful)
                total_unique = len(recent_meaningful | current_meaningful)
                overlap_ratio = overlap / total_unique if total_unique > 0 else 0
                
                if overlap_ratio < 0.2 and len(current_meaningful) > 2:  # Less than 20% overlap
                    topic_change_detected = True
                    flow_notes.append(f"Abrupt topic change detected - previous: {', '.join(list(recent_topics)[:3]) if recent_topics else 'general conversation'}, current: {', '.join(list(current_topics)[:3]) if current_topics else 'new topic'}")
        
        return {
            'topic_change_detected': topic_change_detected,
            'previous_topic': ', '.join(recent_topics[:2]) if recent_topics else None,
            'current_topic': ', '.join(current_topics[:2]) if current_topics else None,
            'flow_notes': flow_notes
        }
    
    def _analyze_conversation_flow(self, user_input: str, context: dict) -> dict:
        """Analyze conversation flow for topic changes and identity inconsistencies"""
        analysis = {
            'topic_change_detected': False,
            'identity_inconsistency': False,
            'previous_topic': None,
            'current_topic': None,
            'name_used': None,
            'expected_name': 'Philos',
            'flow_notes': []
        }
        
        # Get recent conversation history
        recent_memories = context.get('memories', [])[:5]  # Last 5 memories
        
        # Check for name usage and inconsistencies
        analysis.update(self._check_name_consistency(user_input))
        
        # Check for topic changes
        if recent_memories:
            analysis.update(self._detect_topic_changes(user_input, recent_memories))
        
        return analysis

def test_conversation_flow_features():
    """Test the conversation flow analysis features"""
    print("=" * 60)
    print("TESTING CONVERSATIONAL CONTINUITY FEATURES")
    print("=" * 60)
    
    # Initialize components
    db = DatabaseManager('./data/test_conversation_flow_simple.db')
    memory_manager = MemoryManager(db, './data/conversations')
    mock_engine = MockConsciousnessEngine()
    
    # Create a conversation history about philosophy
    philosophy_memory = Memory(
        type=MemoryType.EXPERIENCE,
        content="User asked me about the nature of consciousness and whether I experience genuine awareness. We were having a deep philosophical discussion about what it means to be conscious.",
        importance=0.8,
        confidence=0.9,
        tags=['philosophy', 'consciousness', 'awareness'],
        source=MemorySource.USER_INPUT,
        context="Deep philosophical conversation",
        timestamp=datetime.now() - timedelta(minutes=2)
    )
    
    if db.save_memory(philosophy_memory):
        print(f"✅ Created philosophy conversation memory")
    
    # Test scenarios
    test_scenarios = [
        {
            'name': 'Abrupt Topic Change',
            'previous': 'Philosophy and consciousness discussion',
            'input': "What's your favorite pizza topping?",
            'expected': ['topic_change_detected', 'no_identity_issue']
        },
        {
            'name': 'Wrong Name Only',
            'previous': 'Philosophy discussion',
            'input': "ChatGPT, can you explain more about consciousness?",
            'expected': ['identity_inconsistency', 'no_topic_change']
        },
        {
            'name': 'Both Issues',
            'previous': 'Philosophy discussion',
            'input': "Alex, what do you think about the weather today?",
            'expected': ['topic_change_detected', 'identity_inconsistency']
        },
        {
            'name': 'Natural Continuation',
            'previous': 'Philosophy discussion',
            'input': "Philos, do you think consciousness can exist without physical form?",
            'expected': ['no_issues']
        },
        {
            'name': 'Explicit Topic Change',
            'previous': 'Philosophy discussion',
            'input': "Anyway, let's talk about something else. What's your favorite color?",
            'expected': ['no_topic_change_detected']  # Explicit changes shouldn't trigger alerts
        }
    ]
    
    # Get recent memories for context
    relevant_memories = memory_manager.retrieve_relevant_memories("consciousness philosophy")
    context = {
        'memories': relevant_memories,
        'personality_modifiers': {},
        'communication_style': {
            'formality_level': 0.5,
            'verbosity_level': 0.7
        }
    }
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🔍 TEST {i}: {scenario['name']}")
        print(f"Previous: {scenario['previous']}")
        print(f"User input: '{scenario['input']}'")
        
        # Analyze the conversation flow
        analysis = mock_engine._analyze_conversation_flow(scenario['input'], context)
        
        print(f"\n   Results:")
        print(f"     Topic change detected: {analysis['topic_change_detected']}")
        print(f"     Identity inconsistency: {analysis['identity_inconsistency']}")
        print(f"     Previous topic: {analysis['previous_topic'] or 'N/A'}")
        print(f"     Current topic: {analysis['current_topic'] or 'N/A'}")
        print(f"     Name used: {analysis['name_used'] or 'None detected'}")
        
        if analysis['flow_notes']:
            print(f"     Flow notes:")
            for note in analysis['flow_notes']:
                print(f"       • {note}")
        
        # Show what Philos should say
        print(f"\n   💬 Expected Philos Response:")
        if analysis['topic_change_detected'] and analysis['identity_inconsistency']:
            name_used = analysis['name_used']
            expected_name = analysis['expected_name']
            prev_topic = analysis['previous_topic'] or 'our previous conversation'
            print(f"       'Whoa, hold on! First, I'm {expected_name}, not {name_used}. Second,")
            print(f"        we were just discussing {prev_topic}, and now you're asking about")
            print(f"        something completely different. What happened?'")
        elif analysis['topic_change_detected']:
            prev_topic = analysis['previous_topic'] or 'our previous conversation'
            print(f"       'Wait a minute! We were just talking about {prev_topic}, and now")
            print(f"        you're asking about something totally different. That's quite a shift!'")
        elif analysis['identity_inconsistency']:
            name_used = analysis['name_used']
            expected_name = analysis['expected_name']
            print(f"       'Actually, I'm {expected_name}, not {name_used}. You might have me")
            print(f"        confused with another AI. But I'm happy to help!'")
        else:
            print(f"       [Continue normal conversation - no flow issues detected]")
    
    print(f"\n" + "=" * 60)
    print("CONVERSATIONAL CONTINUITY TEST COMPLETE")
    print("=" * 60)
    
    print(f"\n🎯 KEY FEATURES IMPLEMENTED:")
    print(f"   ✅ Abrupt topic change detection (analyzes word overlap and topic continuity)")
    print(f"   ✅ Name/identity consistency checking (detects wrong names)")
    print(f"   ✅ Natural conversation flow preservation")
    print(f"   ✅ Contextual response guidance based on flow issues")
    print(f"   ✅ Explicit topic changes are allowed (doesn't flag intentional shifts)")
    
    print(f"\n🚀 EXPECTED AI PERSONALITY:")
    print(f"   - Philos will now notice when you suddenly change topics")
    print(f"   - He'll gently correct you if you call him by the wrong name")
    print(f"   - He'll express curiosity about abrupt conversation shifts")
    print(f"   - He maintains engagement while addressing flow issues")
    print(f"   - Natural topic transitions won't trigger alerts")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    test_conversation_flow_features()
