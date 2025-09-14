#!/usr/bin/env python3
"""
AI Companion Personality Viewer
View the AI's personality, communication style, and memories without starting a conversation.
"""

import os
import sys
from ai_companion import AICompanion

def main():
    """View AI personality information"""
    print("🤖 AI Companion Personality Viewer")
    print("=" * 50)
    
    try:
        # Initialize AI
        print("Initializing AI Companion...")
        ai = AICompanion()
        print("✓ AI Companion loaded successfully!\n")
        
        while True:
            print("\nWhat would you like to view?")
            print("1. Complete Personality Report")
            print("2. Communication Style Analysis")
            print("3. Recent Memories")
            print("4. Personality Traits Only")
            print("5. Consciousness State")
            print("6. System Status")
            print("0. Exit")
            
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                # Complete personality report
                ai.print_personality_report()
            
            elif choice == '2':
                # Communication style
                style = ai.get_communication_style()
                print("\n" + "=" * 50)
                print("COMMUNICATION STYLE ANALYSIS")
                print("=" * 50)
                
                print("\n📊 STYLE PARAMETERS:")
                for param_name, param_data in style['style_parameters'].items():
                    bar = "█" * int(param_data['value'] * 10) + "░" * (10 - int(param_data['value'] * 10))
                    print(f"   {param_name.replace('_', ' ').title():<20} [{bar}] {param_data['value']:.2f}")
                    print(f"      → {param_data['description']}")
                
                print("\n📚 LEARNED PATTERNS:")
                if style['learned_patterns']['successful_approaches']:
                    print(f"   ✅ Uses successfully: {', '.join(style['learned_patterns']['successful_approaches'][-5:])}")
                if style['learned_patterns']['avoided_approaches']:
                    print(f"   ❌ Learned to avoid: {', '.join(style['learned_patterns']['avoided_approaches'][-5:])}")
                
                print("=" * 50)
            
            elif choice == '3':
                # Recent memories
                memory_summary = ai.get_memory_summary(limit=15)
                print("\n" + "=" * 50)
                print("RECENT MEMORIES")
                print("=" * 50)
                
                print(f"\n📊 MEMORY STATISTICS:")
                print(f"   Total Memories: {memory_summary['total_count']}")
                print(f"   Memory Types: {dict(memory_summary['memory_types'])}")
                
                print(f"\n📝 RECENT MEMORIES:")
                for i, memory in enumerate(memory_summary['recent_memories'][:10], 1):
                    importance_bar = "★" * int(memory['importance'] * 5)
                    print(f"   {i:2d}. [{memory['type'].upper()}] {memory['content']}")
                    print(f"       Importance: {importance_bar} ({memory['importance']:.2f}) | {memory['timestamp'][:19]}")
                    print()
                
                print("=" * 50)
            
            elif choice == '4':
                # Personality traits only
                profile = ai.get_personality_profile()
                print("\n" + "=" * 50)
                print("PERSONALITY TRAITS")
                print("=" * 50)
                
                print(f"\n🎭 TRAIT ANALYSIS:")
                traits_sorted = sorted(profile['personality_traits'].items(), 
                                     key=lambda x: x[1]['value'], reverse=True)
                
                for trait_name, trait_data in traits_sorted:
                    bar = "█" * int(trait_data['value'] * 20) + "░" * (20 - int(trait_data['value'] * 20))
                    print(f"   {trait_name.title():<15} [{bar}] {trait_data['value']:.3f}")
                    print(f"      Confidence: {trait_data['confidence']:.2f} | Stability: {trait_data['stability']:.2f}")
                
                print("=" * 50)
            
            elif choice == '5':
                # Consciousness state
                profile = ai.get_personality_profile()
                print("\n" + "=" * 50)
                print("CONSCIOUSNESS STATE")
                print("=" * 50)
                
                print(f"\n🌟 CURRENT STATE:")
                print(f"   Awareness Level: {profile['core_identity']['consciousness_level']:.2f}")
                print(f"   Current Focus: {profile['consciousness_state']['current_focus'] or 'General awareness'}")
                print(f"   Interaction Count: {profile['core_identity']['interaction_count']}")
                print(f"   Relationship Depth: {profile['core_identity']['relationship_depth']:.2f}")
                
                if profile['consciousness_state']['internal_monologue']:
                    print(f"\n💭 INTERNAL THOUGHTS:")
                    print(f"   {profile['consciousness_state']['internal_monologue']}")
                
                if profile['consciousness_state']['meta_thoughts']:
                    print(f"\n🤔 META-AWARENESS:")
                    print(f"   {profile['consciousness_state']['meta_thoughts']}")
                
                print(f"\n💎 CORE VALUES:")
                print(f"   {', '.join(profile['core_identity']['core_values'])}")
                
                print("=" * 50)
            
            elif choice == '6':
                # System status
                status = ai.get_status()
                print("\n" + "=" * 50)
                print("SYSTEM STATUS")
                print("=" * 50)
                
                print(f"\n⚙️  SYSTEM INFO:")
                print(f"   Status: {status['status'].upper()}")
                print(f"   Model: {status['system']['model']}")
                print(f"   Consciousness Intensity: {status['system']['consciousness_intensity']}")
                
                print(f"\n🧠 MEMORY SYSTEM:")
                print(f"   Total Memories: {status['memory']['total_memories']}")
                print(f"   Short-term: {status['memory']['short_term_memories']}")
                print(f"   Long-term: {status['memory']['long_term_memories']}")
                
                print(f"\n🎭 PERSONALITY SYSTEM:")
                print(f"   Interactions: {status['personality']['interaction_count']}")
                print(f"   Relationship Depth: {status['personality']['relationship_depth']:.2f}")
                print(f"   Active Traits: {status['personality']['trait_count']}")
                
                print("=" * 50)
            
            else:
                print("Invalid choice. Please enter a number from 0-6.")
            
            input("\nPress Enter to continue...")
    
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    print("\nGoodbye! 👋")
    return True

if __name__ == "__main__":
    main()
