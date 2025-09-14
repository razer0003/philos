"""
Test Neural Monitoring with AI Interaction
Quick test to verify neural monitoring works with the AI companion
"""

import sys
sys.path.append('src')

from src.neural_monitor import get_neural_monitor
from src.personality_engine import PersonalityEngine
from src.consciousness_engine import ConsciousnessEngine
from src.database import DatabaseManager
from src.memory_manager import MemoryManager
import os
from dotenv import load_dotenv

def test_neural_monitoring_with_ai():
    """Test neural monitoring integration with actual AI components"""
    print("🧪 Testing Neural Monitoring Integration")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Initialize components (minimal setup for testing)
    try:
        # Setup components
        db_manager = DatabaseManager('./data/test_ai_companion.db')
        memory_manager = MemoryManager(db_manager, './data/conversations')
        personality_engine = PersonalityEngine(db_manager, memory_manager)
        
        # Get neural monitor
        monitor = get_neural_monitor()
        
        print("✅ AI components initialized with neural monitoring")
        
        # Test 1: Personality assessment with neural monitoring
        print("\n🧠 Test 1: Emotional attachment assessment...")
        test_user_id = "test_user_neural"
        
        # This should trigger neural monitoring
        attachment_data = personality_engine.assess_emotional_attachment_to_user(test_user_id)
        
        print(f"   Attachment level: {attachment_data['attachment_level']:.3f}")
        print(f"   Relationship type: {attachment_data['relationship_status']}")
        
        # Check neural activity
        neural_state = monitor.get_current_neural_state()
        print(f"\n📊 Neural Activity Recorded:")
        print(f"   Computations: {neural_state['computation_steps_count']}")
        print(f"   Memory activations: {neural_state['memory_activations_count']}")
        print(f"   Decision points: {neural_state['decision_points_count']}")
        print(f"   Emotional computations: {neural_state['emotional_computations_count']}")
        
        if neural_state['recent_computations']:
            print(f"\n🔥 Recent Neural Firing:")
            for comp in neural_state['recent_computations'][-5:]:
                print(f"     • {comp['step_name']} ({comp['computation_type']})")
        
        # Test 2: Trait modification with neural monitoring
        print(f"\n🧠 Test 2: Trait modification with monitoring...")
        
        # Simulate interaction that should modify traits
        personality_engine.update_personality_from_interaction(
            user_input="I really appreciate how patient you are with me",
            ai_response="Thank you! I try my best to be helpful and understanding.",
            context={"emotional_valence": "positive"}
        )
        
        # Check for new neural activity
        updated_state = monitor.get_current_neural_state()
        new_computations = updated_state['computation_steps_count'] - neural_state['computation_steps_count']
        new_trait_changes = updated_state['trait_changes_count'] - neural_state['trait_changes_count']
        
        print(f"   New computations: {new_computations}")
        print(f"   New trait changes: {new_trait_changes}")
        
        if updated_state['recent_trait_changes']:
            print(f"\n📈 Recent Trait Changes:")
            for trait in updated_state['recent_trait_changes'][-3:]:
                print(f"     • {trait['trait_name']}: {trait['before_value']:.3f} → {trait['after_value']:.3f}")
        
        # Test 3: Export neural session
        print(f"\n💾 Test 3: Neural session export...")
        filename = monitor.save_session_data("test_neural_session.json")
        print(f"   Neural session saved to: test_neural_session.json")
        
        # Summary
        final_state = monitor.get_current_neural_state()
        print(f"\n🎯 Final Neural State Summary:")
        print(f"   Total computations logged: {final_state['computation_steps_count']}")
        print(f"   Total memory activations: {final_state['memory_activations_count']}")
        print(f"   Total trait changes: {final_state['trait_changes_count']}")
        print(f"   Total decision points: {final_state['decision_points_count']}")
        print(f"   Total emotional computations: {final_state['emotional_computations_count']}")
        
        # Verification
        has_computations = final_state['computation_steps_count'] > 0
        has_decisions = final_state['decision_points_count'] > 0
        has_monitoring = final_state['is_monitoring']
        
        checks_passed = sum([has_computations, has_decisions, has_monitoring])
        total_checks = 3
        
        print(f"\n✅ Verification: {checks_passed}/{total_checks} checks passed")
        if checks_passed == total_checks:
            print("🎉 SUCCESS: Neural monitoring fully integrated with AI components!")
        else:
            print("⚠️  WARNING: Some neural monitoring features may not be working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in neural monitoring test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_neural_monitoring_with_ai()
