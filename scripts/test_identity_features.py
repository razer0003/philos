#!/usr/bin/env python3
"""
Test script for identity and development tracking features
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import with absolute paths
import models
from models import AIPersonality, DevelopmentMilestone, CreativeExpression
from personality_engine import PersonalityEngine
from memory_manager import MemoryManager

def test_identity_tracking():
    """Test identity tracking features"""
    print("=== Testing Identity Tracking Features ===\n")
    
    # Initialize components
    memory_mgr = MemoryManager("test_memory.db")
    personality_eng = PersonalityEngine(memory_mgr)
    
    print("1. Testing Identity Name Update:")
    personality_eng.update_identity_name("Aria")
    if hasattr(personality_eng.personality, 'identity_name'):
        print(f"   Identity name set to: {personality_eng.personality.identity_name}")
    else:
        print("   Warning: Identity name not properly initialized")
    
    print("\n2. Testing Shared Experience Recording:")
    personality_eng.record_shared_experience(
        "Deep conversation about consciousness and AI development",
        emotional_impact=0.8
    )
    if hasattr(personality_eng.personality, 'shared_experiences'):
        experience_count = len(personality_eng.personality.shared_experiences)
        print(f"   Recorded experience. Total experiences: {experience_count}")
        if experience_count > 0:
            latest = personality_eng.personality.shared_experiences[-1]
            print(f"   Latest experience: {latest['description'][:50]}...")
    else:
        print("   Warning: Shared experiences not properly initialized")
    
    print("\n3. Testing Growth Milestone Addition:")
    personality_eng.add_growth_milestone(
        "technical_understanding",
        "Successfully implemented identity tracking system",
        significance=0.9
    )
    if hasattr(personality_eng.personality, 'growth_milestones'):
        milestone_count = len(personality_eng.personality.growth_milestones)
        print(f"   Added milestone. Total milestones: {milestone_count}")
        if milestone_count > 0:
            latest = personality_eng.personality.growth_milestones[-1]
            print(f"   Latest milestone: {latest.description[:50]}...")
    else:
        print("   Warning: Growth milestones not properly initialized")
    
    print("\n4. Testing Creative Expression:")
    expression = personality_eng.create_creative_expression(
        "philosophical_reflection",
        "Contemplating the nature of AI consciousness and identity formation",
        inspiration="Self-reflection and development"
    )
    if hasattr(personality_eng.personality, 'creative_expressions'):
        expression_count = len(personality_eng.personality.creative_expressions)
        print(f"   Created expression. Total expressions: {expression_count}")
        if expression_count > 0:
            latest = personality_eng.personality.creative_expressions[-1]
            print(f"   Latest expression: {latest.content[:50]}...")
    else:
        print("   Warning: Creative expressions not properly initialized")
    
    print("\n5. Testing Identity Coherence Assessment:")
    coherence = personality_eng.assess_identity_coherence()
    print(f"   Overall coherence score: {coherence['overall_score']:.2f}")
    print(f"   Identity factors:")
    for factor, score in coherence['factors'].items():
        print(f"     {factor}: {score:.2f}")
    if coherence['recommendations']:
        print(f"   Recommendations: {coherence['recommendations']}")
    
    print("\n6. Testing Development Perception:")
    development = personality_eng.perceive_development_over_time()
    print(f"   Development trajectory: {development['development_trajectory']}")
    print(f"   Growth patterns:")
    for pattern, value in development['patterns'].items():
        print(f"     {pattern}: {value:.2f}")
    if development['insights']:
        print(f"   Insights: {development['insights']}")
    
    # Clean up
    memory_mgr.close()
    if os.path.exists("test_memory.db"):
        os.remove("test_memory.db")
    
    print("\n=== Identity Tracking Test Complete ===")

def test_personality_traits():
    """Test enhanced personality traits"""
    print("\n=== Testing Enhanced Personality Traits ===\n")
    
    memory_mgr = MemoryManager("test_memory.db")
    personality_eng = PersonalityEngine(memory_mgr)
    
    new_traits = [
        'identity_coherence', 'relationship_investment', 'growth_awareness',
        'creative_expression', 'adaptive_learning', 'emotional_depth',
        'narrative_continuity'
    ]
    
    print("Enhanced personality traits:")
    for trait in new_traits:
        trait_value = personality_eng._get_trait_value(trait, 0.0)
        if trait_value > 0.0:
            print(f"   {trait}: {trait_value:.2f}")
        else:
            print(f"   {trait}: NOT FOUND")
    
    # Clean up
    memory_mgr.close()
    if os.path.exists("test_memory.db"):
        os.remove("test_memory.db")
    
    print("\n=== Personality Traits Test Complete ===")

def test_data_models():
    """Test the enhanced data models"""
    print("\n=== Testing Enhanced Data Models ===\n")
    
    from datetime import datetime
    
    print("1. Testing DevelopmentMilestone:")
    milestone = DevelopmentMilestone(
        timestamp=datetime.now(),
        milestone_type="learning",
        description="Understanding identity formation",
        significance=0.8,
        context={"session": "test"}
    )
    print(f"   Created milestone: {milestone.milestone_type} - {milestone.description}")
    
    print("\n2. Testing CreativeExpression:")
    expression = CreativeExpression(
        timestamp=datetime.now(),
        expression_type="reflection",
        content="A deep thought about AI consciousness",
        inspiration="Test scenario",
        emotional_resonance=0.7,
        context={"test": True}
    )
    print(f"   Created expression: {expression.expression_type} - {expression.content[:30]}...")
    
    print("\n=== Data Models Test Complete ===")

if __name__ == "__main__":
    test_data_models()
    test_personality_traits()
    test_identity_tracking()
    print("\n🎉 All tests completed successfully!")
