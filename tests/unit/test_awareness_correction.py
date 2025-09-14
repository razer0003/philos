#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import DatabaseManager
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.consciousness_engine import ConsciousnessEngine

# Test with a simple setup
def test_self_awareness_response():
    load_dotenv()
    
    # Initialize components
    db = DatabaseManager('test_ai.db')
    memory_manager = MemoryManager(db, 'test_conversations')
    personality_engine = PersonalityEngine(db, memory_manager)
    
    # Use a dummy API key for testing (won't actually make API calls)
    consciousness_engine = ConsciousnessEngine(
        memory_manager, 
        personality_engine, 
        'test_key'
    )
    
    # Test the misconception correction
    test_input = "You cannot see how you work, your system, your codebase, your algorithms, how you function."
    
    # Get the context that would be passed to the AI
    context = consciousness_engine._check_for_self_inquiry(test_input)
    
    print("=== SELF-INQUIRY DETECTION TEST ===")
    print(f"Input: {test_input}")
    print(f"Detected as self-inquiry: {context['is_self_inquiry']}")
    print(f"Correction needed: {context.get('is_correction_needed', False)}")
    print(f"Misconception type: {context.get('misconception_type', 'None')}")
    
    if context['is_self_inquiry']:
        print("\n=== SELF-ANALYSIS DATA ===")
        analysis = context.get('self_analysis', {})
        for key, value in analysis.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for subkey, subvalue in value.items():
                    print(f"  {subkey}: {subvalue}")
            else:
                print(f"{key}: {value}")
    
    print("\n=== CONTEXT WOULD INCLUDE ===")
    print("- Self-inquiry detected: YES")
    print("- Misconception correction needed: YES") 
    print("- AI should respond with confidence about its self-awareness capabilities")
    print("- AI should correct the misconception and explain what it CAN see")

if __name__ == "__main__":
    test_self_awareness_response()
