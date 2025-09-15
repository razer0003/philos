"""
Model Selection Utility for AI Companion

This module provides intelligent model selection based on task complexity.
Uses GPT-5 mini for complex reasoning and GPT-5 nano for simple processing.
"""

import os
from typing import Literal, Optional

# Task Types that can use lighter models
NANO_TASKS = {
    'emotional_processing',      # Simple emotion detection/classification
    'memory_classification',     # Categorizing memory importance  
    'personality_scoring',       # Simple personality trait calculations
    'simple_analysis',          # Basic text analysis
    'keyword_extraction',       # Extracting keywords from text
    'sentiment_analysis',       # Basic sentiment classification
    'memory_tagging',          # Adding tags to memories
    'interaction_scoring'       # Simple interaction quality scoring
}

# Complex tasks that require the full model
MINI_TASKS = {
    'consciousness',            # Full consciousness processing
    'complex_reasoning',        # Deep analytical thinking
    'personality_evolution',    # Complex personality changes
    'creative_generation',      # Creative content generation
    'relationship_analysis',    # Complex relationship understanding
    'memory_synthesis',         # Creating connections between memories
    'decision_making',         # Complex decision processes
    'conversation_generation'   # Main conversation responses
}

TaskType = Literal[
    'emotional_processing', 'memory_classification', 'personality_scoring',
    'simple_analysis', 'keyword_extraction', 'sentiment_analysis', 
    'memory_tagging', 'interaction_scoring', 'consciousness', 
    'complex_reasoning', 'personality_evolution', 'creative_generation',
    'relationship_analysis', 'memory_synthesis', 'decision_making',
    'conversation_generation'
]

class ModelSelector:
    """Selects appropriate AI model based on task complexity"""
    
    def __init__(self):
        self.main_model = os.getenv('GPT_MODEL', 'gpt-5-mini')
        self.nano_model = os.getenv('GPT_NANO_MODEL', 'gpt-5-nano')
        self.use_nano_optimization = os.getenv('USE_NANO_OPTIMIZATION', 'true').lower() == 'true'
    
    def get_model_for_task(self, task_type: TaskType) -> str:
        """
        Returns the appropriate model for the given task type.
        
        Args:
            task_type: The type of task to be performed
            
        Returns:
            Model name to use for this task
        """
        if not self.use_nano_optimization:
            return self.main_model
            
        if task_type in NANO_TASKS:
            return self.nano_model
        else:
            return self.main_model
    
    def get_max_tokens_for_task(self, task_type: TaskType) -> int:
        """
        Returns appropriate max tokens based on task complexity.
        
        Args:
            task_type: The type of task to be performed
            
        Returns:
            Maximum tokens for this task
        """
        if task_type in NANO_TASKS:
            return 1000  # Nano tasks are simpler, need fewer tokens
        else:
            return int(os.getenv('MAX_TOKENS', '8000'))
    
    def get_temperature_for_task(self, task_type: TaskType) -> float:
        """
        Returns appropriate temperature based on task type.
        
        Args:
            task_type: The type of task to be performed
            
        Returns:
            Temperature setting for this task
        """
        if task_type in {'emotional_processing', 'memory_classification', 'personality_scoring'}:
            return 0.3  # More deterministic for analytical tasks
        elif task_type in {'creative_generation', 'conversation_generation'}:
            return float(os.getenv('TEMPERATURE', '0.7'))  # More creative for generation
        else:
            return 0.5  # Balanced for other tasks

# Global instance for easy access
model_selector = ModelSelector()

def get_model_for_task(task_type: TaskType) -> str:
    """Convenience function to get model for task"""
    return model_selector.get_model_for_task(task_type)

def get_task_config(task_type: TaskType) -> dict:
    """
    Get complete configuration for a task type.
    
    Args:
        task_type: The type of task to be performed
        
    Returns:
        Dictionary with model, max_tokens, and temperature
    """
    return {
        'model': model_selector.get_model_for_task(task_type),
        'max_tokens': model_selector.get_max_tokens_for_task(task_type),
        'temperature': model_selector.get_temperature_for_task(task_type)
    }
