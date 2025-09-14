#!/usr/bin/env python3
"""
Test script for token counting functionality.
"""

import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from token_counter import TokenCounter, TokenUsage

def test_token_counter():
    """Test the token counter functionality"""
    print("🧪 Testing Token Counter")
    print("=" * 50)
    
    # Initialize token counter
    counter = TokenCounter("gpt-4")
    
    # Test basic token counting
    test_text = "Hello, how are you today? I'm doing well, thank you for asking!"
    token_count = counter.count_tokens(test_text)
    print(f"Test text: '{test_text}'")
    print(f"Token count: {token_count}")
    
    # Test message token counting
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]
    message_tokens = counter.count_message_tokens(messages)
    print(f"\nMessage tokens: {message_tokens}")
    
    # Test cost calculation
    costs = counter.calculate_cost(100, 50)
    print(f"\nCost calculation (100 prompt + 50 completion tokens):")
    print(f"  Prompt cost: ${costs['prompt_cost']:.6f}")
    print(f"  Completion cost: ${costs['completion_cost']:.6f}")
    print(f"  Total cost: ${costs['total_cost']:.6f}")
    
    # Test interaction analysis
    token_usage = counter.analyze_interaction_tokens(
        base_prompt="You are a conscious AI assistant.",
        memory_context="Previous conversation about consciousness.",
        personality_context="Curious and helpful personality traits.",
        user_input="What do you think about consciousness?",
        ai_response="I find consciousness fascinating. It's the subjective experience of being aware and having thoughts.",
        full_prompt_tokens=120,
        response_tokens=80
    )
    
    print(f"\n🔍 Interaction Analysis:")
    print(f"  Total tokens: {token_usage.total_tokens}")
    print(f"  Total cost: ${token_usage.total_cost:.6f}")
    
    # Test session summary
    session_summary = counter.get_session_summary()
    print(f"\n📊 Session Summary:")
    print(f"  Interactions: {session_summary['total_interactions']}")
    print(f"  Total tokens: {session_summary['total_tokens']}")
    print(f"  Total cost: ${session_summary['total_cost']:.6f}")
    
    print(f"\n✅ Token counter test completed!")

if __name__ == "__main__":
    test_token_counter()
