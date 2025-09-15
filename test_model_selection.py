"""
Test script for model selection system
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the src directory to the path for imports
sys.path.append(str(Path(__file__).parent / 'src'))

from src.model_selector import get_model_for_task, get_task_config, TaskType

def test_model_selection():
    """Test the model selection functionality"""
    
    print("Testing Model Selection System")
    print("=" * 40)
    
    # Test nano tasks (should use gpt-5-nano)
    nano_tasks = [
        'emotional_processing',
        'memory_classification', 
        'personality_scoring',
        'simple_analysis',
        'sentiment_analysis'
    ]
    
    print("\nNano Model Tasks:")
    for task in nano_tasks:
        config = get_task_config(task)
        print(f"  {task}: {config['model']} (tokens: {config['max_tokens']}, temp: {config['temperature']})")
    
    # Test mini tasks (should use gpt-5-mini)
    mini_tasks = [
        'consciousness',
        'complex_reasoning',
        'personality_evolution',
        'creative_generation',
        'conversation_generation'
    ]
    
    print("\nMini Model Tasks:")
    for task in mini_tasks:
        config = get_task_config(task)
        print(f"  {task}: {config['model']} (tokens: {config['max_tokens']}, temp: {config['temperature']})")
    
    print("\nModel Configuration:")
    print(f"  Main Model: {os.getenv('GPT_MODEL', 'not set')}")
    print(f"  Nano Model: {os.getenv('GPT_NANO_MODEL', 'not set')}")
    print(f"  Use Nano Optimization: {os.getenv('USE_NANO_OPTIMIZATION', 'not set')}")

if __name__ == "__main__":
    test_model_selection()
