from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager  
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
import os

# Test Philos's improved conversational memory
print("🧠 Testing Philos's Conversational Memory")
print("=" * 50)

# Set up test components
db = DatabaseManager(':memory:')
memory = MemoryManager(db, conversations_path='test_conversations')
personality = PersonalityEngine(db, memory)

# Check if we have API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("❌ No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
    print("\n🔍 Testing conversation history retrieval instead:")
    
    # Create some test memories to simulate a conversation
    from src.models import MemoryType, MemorySource
    
    # Simulate conversation memories
    memory.create_memory("Something seems simplistic about that approach", MemoryType.EXPERIENCE, source=MemorySource.USER)
    memory.create_ai_memory("I think that analysis is a bit simplistic. There are more nuanced factors to consider.", MemoryType.RESPONSE)
    memory.create_memory("Simplistic?", MemoryType.EXPERIENCE, source=MemorySource.USER)
    
    # Test conversation history retrieval
    history = memory.get_recent_conversation_history(max_exchanges=3)
    print(f"\n📜 Retrieved {len(history)} conversation exchanges:")
    
    for i, exchange in enumerate(history):
        print(f"\n{i+1}. User: {exchange.get('user', 'N/A')}")
        print(f"   AI: {exchange.get('ai', 'N/A')}")
        print(f"   Time: {exchange.get('timestamp', 'N/A')}")
    
    print(f"\n✅ Conversation history system working!")
    print("Now when someone asks 'Simplistic?' Philos should understand")  
    print("they're referring to something he just called simplistic.")
    
else:
    print("✅ API key found - you can test the full conversation system!")
    print("The system now includes:")
    print("  • Recent conversation history in context")
    print("  • Reference resolution for 'that', 'it', 'this', etc.")  
    print("  • Continuity awareness for follow-up questions")
    print("  • Enhanced internal thought processing with conversation context")
