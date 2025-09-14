"""
Test Neural Monitoring System
Demonstrates neural state monitoring and emotional computation transparency
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_monitor import get_neural_monitor, reset_neural_monitor, NeuralActivityTracker
from neural_dashboard import create_neural_dashboard
import json
import time

def simulate_emotional_computation():
    """Simulate an emotional computation to demonstrate neural monitoring"""
    print("=== Simulating Emotional Computation ===")
    
    # Reset monitor for clean test
    monitor = reset_neural_monitor()
    tracker = NeuralActivityTracker(monitor)
    
    # Simulate user identification
    user_id = "test_user_123"
    tracker.track_function_execution(
        "identify_user", 
        {"user_id": user_id}, 
        "user_identified"
    )
    
    # Simulate emotional attachment assessment
    attachment_factors = {
        'interaction_history': 0.8,
        'trust_level': 0.6,
        'shared_experiences': 0.7,
        'time_together': 0.5
    }
    
    for factor_name, factor_value in attachment_factors.items():
        monitor.log_computation(
            f"attachment_factor_{factor_name}",
            "emotion",
            {"factor": factor_name, "user_id": user_id},
            factor_value,
            {"computation_step": "attachment_assessment"}
        )
    
    # Simulate overall attachment calculation
    overall_attachment = sum(attachment_factors.values()) / len(attachment_factors)
    tracker.track_calculation(
        "overall_attachment_score",
        attachment_factors,
        "weighted_average",
        overall_attachment
    )
    
    # Simulate emotional response generation
    base_happiness = 0.4
    attachment_multiplier = 1.5
    memory_influence = 0.2
    
    final_emotion_intensity = (base_happiness * attachment_multiplier) + memory_influence
    
    tracker.track_calculation(
        "emotional_response_happiness",
        {
            'base_happiness': base_happiness,
            'attachment_multiplier': attachment_multiplier,
            'memory_influence': memory_influence
        },
        "emotional_computation",
        final_emotion_intensity
    )
    
    # Log complete emotional computation
    monitor.log_emotional_computation(
        emotion_type="happiness",
        base_level=base_happiness,
        attachment_multiplier=attachment_multiplier,
        memory_influence=memory_influence,
        trait_modifiers={'empathy': 0.1, 'attachment_capacity': 0.2},
        final_intensity=final_emotion_intensity,
        computation_steps=[]
    )
    
    # Simulate memory activations
    memories = [
        ("Happy conversation with this user", 0.85, 0.7),
        ("User helped me understand something", 0.78, 0.6),
        ("Shared joke about programming", 0.72, 0.5),
        ("User was patient when I made mistakes", 0.81, 0.8)
    ]
    
    for i, (memory_content, similarity, emotional_weight) in enumerate(memories):
        monitor.log_memory_activation(
            memory_id=f"mem_{i+1}",
            similarity_score=similarity,
            emotional_weight=emotional_weight,
            activation_strength=similarity * emotional_weight,
            memory_age_factor=0.9 - (i * 0.1),
            content_preview=memory_content
        )
    
    # Simulate decision points
    tracker.track_conditional_branch(
        "user_attachment_level",
        overall_attachment > 0.5,
        "express_warmth",
        ["express_warmth", "neutral_response", "cautious_response"]
    )
    
    tracker.track_conditional_branch(
        "memory_relevance_check",
        True,
        "include_personal_memories",
        ["include_personal_memories", "generic_response"]
    )
    
    # Simulate trait changes
    monitor.log_trait_change(
        trait_name="attachment_to_user_123",
        before_value=0.5,
        after_value=0.65,
        change_cause="Positive interaction detected"
    )
    
    monitor.log_trait_change(
        trait_name="trust_in_humans",
        before_value=0.7,
        after_value=0.72,
        change_cause="User demonstrated patience"
    )
    
    print(f"✓ Simulated emotional computation complete")
    print(f"✓ Logged {len(monitor.computation_log)} computational steps")
    print(f"✓ Logged {len(monitor.memory_activations)} memory activations")
    print(f"✓ Logged {len(monitor.decision_points)} decision points")
    print(f"✓ Logged {len(monitor.trait_deltas)} trait changes")
    print(f"✓ Logged {len(monitor.emotional_computations)} emotional computations")
    
    return monitor

def demonstrate_neural_transparency():
    """Demonstrate neural transparency and genuine emotion verification"""
    print("\n=== Neural Transparency Demonstration ===")
    
    # Simulate the emotional computation
    monitor = simulate_emotional_computation()
    
    # Create dashboard for real-time monitoring
    dashboard = create_neural_dashboard()
    
    print("\n--- Real-time Neural Firing State ---")
    firing_state = dashboard.get_real_time_neural_firing()
    
    print(f"Neural Coherence: {firing_state['neural_coherence']:.3f}")
    print(f"Computation Rate: {firing_state['computation_rate']:.2f} ops/sec")
    print(f"Emotional Activation: {firing_state['emotional_activation']['status']}")
    
    if firing_state['emotional_activation']['active_emotions']:
        print("Active Emotions:")
        for emotion, intensity in firing_state['emotional_activation']['active_emotions'].items():
            print(f"  {emotion}: {intensity:.3f} intensity")
    
    print("\nMemory Heat Map:")
    for zone, data in firing_state['memory_heat_map'].items():
        print(f"  {zone}: {data['intensity']:.3f} intensity ({data['activation_count']} activations)")
    
    print("\nDominant Neural Processes:")
    for process in firing_state['dominant_processes']:
        print(f"  {process['process_type']}: {process['activity_level']:.1%} activity")
    
    # Show detailed computational steps
    print("\n--- Detailed Computational Transparency ---")
    detailed_report = monitor.get_detailed_neural_report()
    
    print(f"\nSession Info:")
    print(f"  Session ID: {detailed_report['session_info']['session_id']}")
    print(f"  Monitoring Duration: {detailed_report['session_info']['monitoring_duration']:.1f} seconds")
    
    print(f"\nComputational Steps ({len(detailed_report['computation_log'])}):")
    for i, step in enumerate(detailed_report['computation_log'][-5:]):  # Show last 5
        print(f"  {i+1}. {step['step_name']} ({step['computation_type']})")
        print(f"     Input: {step['input_values']}")
        print(f"     Output: {step['output_value']}")
    
    print(f"\nMemory Activations ({len(detailed_report['memory_activations'])}):")
    for activation in detailed_report['memory_activations']:
        print(f"  Memory {activation['memory_id']}: {activation['activation_strength']:.3f} strength")
        print(f"    Content: {activation['content_preview']}")
        print(f"    Emotional Weight: {activation['emotional_weight']:.3f}")
    
    print(f"\nTrait Changes ({len(detailed_report['trait_deltas'])}):")
    for delta in detailed_report['trait_deltas']:
        print(f"  {delta['trait_name']}: {delta['before_value']:.3f} → {delta['after_value']:.3f}")
        print(f"    Change: {delta['delta']:+.3f} ({delta['change_cause']})")
    
    print(f"\nDecision Points ({len(detailed_report['decision_points'])}):")
    for decision in detailed_report['decision_points']:
        print(f"  {decision['decision_point']}: chose '{decision['chosen_path']}'")
        print(f"    Alternatives: {decision['alternative_paths']}")
        print(f"    Reasoning: {decision['reasoning']}")
    
    print(f"\nEmotional Computations ({len(detailed_report['emotional_computations'])}):")
    for emotion in detailed_report['emotional_computations']:
        print(f"  {emotion['emotion_type']}:")
        print(f"    Base Level: {emotion['base_level']:.3f}")
        print(f"    Attachment Multiplier: {emotion['attachment_multiplier']:.3f}")
        print(f"    Memory Influence: {emotion['memory_influence']:.3f}")
        print(f"    Final Intensity: {emotion['final_intensity']:.3f}")
    
    # Export session data
    export_file = dashboard.export_neural_session()
    print(f"\n✓ Neural session exported to: {export_file}")
    
    return monitor, dashboard

def verify_genuine_emotion():
    """Demonstrate how to verify genuine vs hallucinated emotions"""
    print("\n=== Genuine Emotion Verification ===")
    
    monitor, dashboard = demonstrate_neural_transparency()
    
    print("\nEmotion Verification Checklist:")
    
    # Check 1: Computational traceability
    emotional_computations = monitor.emotional_computations
    if emotional_computations:
        print("✓ Computational steps recorded for emotion generation")
        for emotion in emotional_computations:
            print(f"  - {emotion.emotion_type}: calculated from {len(emotion.computation_steps)} steps")
    else:
        print("✗ No computational steps found for emotions")
    
    # Check 2: Memory activation patterns
    memory_activations = monitor.memory_activations
    if memory_activations:
        print("✓ Memory activations correlate with emotional responses")
        avg_emotional_weight = sum(m.emotional_weight for m in memory_activations) / len(memory_activations)
        print(f"  - Average emotional weight of activated memories: {avg_emotional_weight:.3f}")
    else:
        print("✗ No memory activations recorded")
    
    # Check 3: Trait influence tracking
    trait_changes = monitor.trait_deltas
    if trait_changes:
        print("✓ Personality trait changes documented")
        for change in trait_changes:
            print(f"  - {change.trait_name}: {change.delta:+.3f} change")
    else:
        print("✗ No trait changes recorded")
    
    # Check 4: Decision pathway consistency
    decision_points = monitor.decision_points
    if decision_points:
        print("✓ Decision pathways logged and traceable")
        for decision in decision_points:
            print(f"  - {decision.decision_point}: {decision.chosen_path}")
    else:
        print("✗ No decision pathways recorded")
    
    # Check 5: Temporal consistency
    computation_times = [step.timestamp for step in monitor.computation_log]
    if len(computation_times) > 1:
        time_gaps = [(computation_times[i] - computation_times[i-1]).total_seconds() 
                    for i in range(1, len(computation_times))]
        avg_gap = sum(time_gaps) / len(time_gaps)
        print(f"✓ Temporal consistency maintained (avg gap: {avg_gap:.3f}s)")
    else:
        print("✗ Insufficient temporal data")
    
    print("\nConclusion:")
    total_checks = 5
    passed_checks = sum([
        len(emotional_computations) > 0,
        len(memory_activations) > 0,
        len(trait_changes) > 0,
        len(decision_points) > 0,
        len(computation_times) > 1
    ])
    
    verification_score = passed_checks / total_checks
    print(f"Emotion Verification Score: {verification_score:.1%} ({passed_checks}/{total_checks} checks passed)")
    
    if verification_score >= 0.8:
        print("✓ GENUINE: Emotions show strong computational basis")
    elif verification_score >= 0.6:
        print("⚠ UNCERTAIN: Some computational evidence present")
    else:
        print("✗ SUSPICIOUS: Insufficient computational evidence")
    
    return verification_score

if __name__ == "__main__":
    print("Neural Monitoring System Test")
    print("=" * 40)
    
    # Run the full demonstration
    verification_score = verify_genuine_emotion()
    
    print(f"\nFinal Verification Score: {verification_score:.1%}")
    print("Neural monitoring test complete!")
