#!/usr/bin/env python3

from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager

# Test the self-inquiry detection
db = DatabaseManager(':memory:')
memory_mgr = MemoryManager(db, 'test_conversations')  # Use a temporary directory
personality = PersonalityEngine(db, memory_mgr)
consciousness = ConsciousnessEngine(memory_mgr, personality, 'dummy_key')

# Test input about AI limitations
test_input = 'You can not see how you work, your system, your codebase, your algorithms, how you function.'
result = consciousness._check_for_self_inquiry(test_input)

print('Self-inquiry detection result:')
print(f'Is self-inquiry: {result["is_self_inquiry"]}')
print(f'Aspect requested: {result.get("aspect_requested", "None")}')
print(f'Correction needed: {result.get("is_correction_needed", "False")}')
print(f'Misconception type: {result.get("misconception_type", "None")}')

# Test another query
test_input2 = 'How do you work?'
result2 = consciousness._check_for_self_inquiry(test_input2)

print('\nSecond test result:')
print(f'Is self-inquiry: {result2["is_self_inquiry"]}')
print(f'Aspect requested: {result2.get("aspect_requested", "None")}')
print(f'Self-analysis available: {bool(result2.get("self_analysis"))}')
