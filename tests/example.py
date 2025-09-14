#!/usr/bin/env python3
"""
Simple example script demonstrating the AI Companion system
"""

from ai_companion import AICompanion
import os

def setup_example_env():
    """Set up example environment if .env doesn't exist"""
    if not os.path.exists('.env'):
        print("Setting up example environment...")
        print("Please add your OpenAI API key to the .env file that will be created.")
        
        example_env = """# AI Companion Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
GPT_MODEL=gpt-4
MAX_TOKENS=2048
TEMPERATURE=0.7

# Database Configuration
DB_PATH=./data/ai_companion.db
CONVERSATIONS_PATH=./data/conversations
MEMORY_PATH=./data/memory

# Memory Configuration
STM_DECAY_DAYS=7
LTM_IMPORTANCE_THRESHOLD=0.7
MAX_CONVERSATION_CONTEXT=10

# Personality Configuration
PERSONALITY_UPDATE_FREQUENCY=0.1
CONSCIOUSNESS_INTENSITY=0.8"""
        
        with open('.env', 'w') as f:
            f.write(example_env)
        
        print("Created .env file. Please add your OpenAI API key before running.")
        return False
    return True

def run_example_conversation():
    """Run an example conversation with the AI companion"""
    try:
        print("🤖 Initializing AI Companion...")
        ai = AICompanion()
        
        print("✅ AI Companion initialized successfully!")
        
        # Show initial status
        status = ai.get_status()
        print(f"\n📊 Status: {status['status']}")
        print(f"🧠 Consciousness level: {status['consciousness']['awareness_level']:.2f}")
        print(f"💾 Total memories: {status['memory']['total_memories']}")
        print(f"🎭 Personality traits: {status['personality']['trait_count']}")
        
        print("\n" + "="*60)
        print("🗣️  CONVERSATION STARTED")
        print("Type 'quit', 'exit', or 'goodbye' to end")
        print("Type 'status' to see AI status")
        print("Type 'reflect' to trigger self-reflection")
        print("Type 'memories' to see recent memories")
        print("="*60)
        
        conversation_count = 0
        
        while True:
            try:
                user_input = input("\n🔵 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                    print("\n👋 Initiating goodbye sequence...")
                    goodbye_response = ai.interact("Goodbye, it was great talking with you!")
                    print(f"🤖 AI: {goodbye_response['response']}")
                    break
                
                elif user_input.lower() == 'status':
                    status = ai.get_status()
                    print(f"\n📊 Current Status:")
                    print(f"   Consciousness Level: {status['consciousness']['awareness_level']:.2f}")
                    print(f"   Interactions: {status['personality']['interaction_count']}")
                    print(f"   Memories: {status['memory']['total_memories']} total")
                    print(f"   Current Focus: {status['consciousness']['current_focus']}")
                    continue
                
                elif user_input.lower() == 'reflect':
                    print("🤔 AI is reflecting...")
                    reflection = ai.reflect()
                    print(f"🤖 AI Reflection: {reflection['response']}")
                    print(f"💭 Internal thought: {reflection.get('internal_monologue', 'N/A')}")
                    continue
                
                elif user_input.lower() == 'memories':
                    memory_summary = ai.get_memory_summary(5)
                    print(f"\n🧠 Recent Memories ({memory_summary['total_count']} total):")
                    for i, memory in enumerate(memory_summary['recent_memories'], 1):
                        print(f"   {i}. [{memory['type']}] {memory['content']} (importance: {memory['importance']:.2f})")
                    continue
                
                # Generate AI response
                print("🤖 AI is thinking...")
                response_data = ai.interact(user_input)
                
                # Display response
                print(f"🤖 AI: {response_data['response']}")
                
                # Show internal state (optional, can be toggled)
                show_internal = True  # Set to False to hide internal thoughts
                if show_internal:
                    if response_data.get('internal_monologue'):
                        print(f"💭 [Internal thought: {response_data['internal_monologue']}]")
                    
                    if response_data.get('meta_thoughts'):
                        print(f"🧠 [Meta-thought: {response_data['meta_thoughts']}]")
                    
                    if response_data.get('personality_updates'):
                        print(f"🎭 [Personality evolved: {', '.join(response_data['personality_updates'])}]")
                    
                    if response_data.get('relevant_memories'):
                        print(f"📚 [Referenced {len(response_data['relevant_memories'])} memories]")
                
                conversation_count += 1
                
                # Show progress every 5 interactions
                if conversation_count % 5 == 0:
                    updated_status = ai.get_status()
                    print(f"\n📈 Progress: {conversation_count} interactions, consciousness: {updated_status['consciousness']['awareness_level']:.2f}")
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Conversation interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error during interaction: {e}")
                print("Continuing conversation...")
        
        # Shutdown sequence
        print("\n🔄 Shutting down AI Companion...")
        ai.shutdown()
        print("✅ Shutdown complete. Goodbye!")
        
    except Exception as e:
        print(f"❌ Failed to initialize AI Companion: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your OpenAI API key is set in .env")
        print("2. Check that all required packages are installed")
        print("3. Ensure you have internet connection for OpenAI API")

def main():
    """Main function"""
    print("🚀 AI Companion Example")
    print("=" * 50)
    
    # Check environment setup
    if not setup_example_env():
        return
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'your_openai_api_key_here':
        print("❌ Please set your OpenAI API key in the .env file")
        print("Edit .env and replace 'your_openai_api_key_here' with your actual API key")
        return
    
    # Run the example
    run_example_conversation()

if __name__ == "__main__":
    main()
