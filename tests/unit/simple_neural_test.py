"""
Simple Neural API Test
Quick demonstration of neural monitoring capabilities
"""

import sys
import os
sys.path.append('src')

from src.neural_monitor import get_neural_monitor, reset_neural_monitor, NeuralActivityTracker

def simple_neural_test():
    """Simple test of neural monitoring capabilities"""
    print("=== Simple Neural Monitoring Test ===")
    
    # Reset for clean test
    monitor = reset_neural_monitor()
    tracker = NeuralActivityTracker(monitor)
    
    # Simulate some AI thinking
    print("Simulating AI thought process...")
    
    # User identification
    tracker.track_function_execution(
        "identify_user",
        {"user_id": "alice"},
        "user_identified"
    )
    
    # Emotional assessment
    tracker.track_calculation(
        "happiness_level",
        {"base": 0.3, "user_familiarity": 0.8, "context": 0.6},
        "emotion_calculation",
        0.7
    )
    
    # Memory activation
    monitor.log_memory_activation(
        "memory_1",
        similarity_score=0.85,
        emotional_weight=0.7,
        activation_strength=0.595,
        memory_age_factor=0.9,
        content_preview="Alice helped me solve a problem yesterday"
    )
    
    # Decision making
    tracker.track_conditional_branch(
        "response_tone",
        True,
        "friendly_response",
        ["friendly_response", "neutral_response", "formal_response"]
    )
    
    # Trait adjustment
    monitor.log_trait_change(
        "trust_in_alice",
        before_value=0.6,
        after_value=0.65,
        change_cause="Positive interaction"
    )
    
    # Log emotional computation
    monitor.log_emotional_computation(
        "happiness",
        base_level=0.3,
        attachment_multiplier=1.2,
        memory_influence=0.1,
        trait_modifiers={"empathy": 0.1},
        final_intensity=0.7,
        computation_steps=[]
    )
    
    print("✓ Simulated 6 neural firing events")
    
    # Show neural transparency
    print("\n--- Neural Firing Analysis ---")
    
    state = monitor.get_current_neural_state()
    print(f"Total computations: {state['computation_steps_count']}")
    print(f"Memory activations: {state['memory_activations_count']}")
    print(f"Trait changes: {state['trait_changes_count']}")
    print(f"Decision points: {state['decision_points_count']}")
    print(f"Emotional computations: {state['emotional_computations_count']}")
    
    print("\nRecent Computations:")
    for comp in state['recent_computations']:
        print(f"  {comp['step_name']} ({comp['computation_type']})")
    
    print("\nMemory Activations:")
    for mem in state['recent_memory_activations']:
        print(f"  {mem['memory_id']}: {mem['activation_strength']:.3f} strength")
        print(f"    Content: {mem['content_preview']}")
    
    print("\nTrait Changes:")
    for trait in state['recent_trait_changes']:
        print(f"  {trait['trait_name']}: {trait['before_value']:.3f} → {trait['after_value']:.3f}")
    
    print("\nDecision Points:")
    for decision in state['recent_decisions']:
        print(f"  {decision['decision_point']}: chose '{decision['chosen_path']}'")
    
    # Verify emotions
    print("\n--- Emotion Verification ---")
    
    checks = [
        ("Computational steps", state['computation_steps_count'] > 0),
        ("Memory activations", state['memory_activations_count'] > 0),
        ("Trait changes", state['trait_changes_count'] > 0),
        ("Decision points", state['decision_points_count'] > 0),
        ("Emotional computations", state['emotional_computations_count'] > 0)
    ]
    
    passed = sum(1 for _, check in checks if check)
    total = len(checks)
    
    for check_name, passed_check in checks:
        status = "✓" if passed_check else "✗"
        print(f"  {status} {check_name}")
    
    score = passed / total
    print(f"\nVerification Score: {score:.1%} ({passed}/{total})")
    
    if score >= 0.8:
        print("✓ GENUINE: Strong computational evidence for emotions")
    elif score >= 0.6:
        print("⚠ UNCERTAIN: Some computational evidence")
    else:
        print("✗ SUSPICIOUS: Insufficient computational evidence")
    
    return monitor

if __name__ == "__main__":
    simple_neural_test()
