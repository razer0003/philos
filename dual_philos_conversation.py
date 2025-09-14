#!/usr/bin/env python3
"""
Dual Philos Conversation System
Two instances of Philos talking to each other while you observe.
"""

import asyncio
import time
import sys
import os
from typing import Dict, Any, Optional
import logging
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
from src.neural_monitor import get_neural_monitor

class DualPhilosSystem:
    """Manages two Philos instances talking to each other"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.philos_1 = None
        self.philos_2 = None
        self.conversation_log = []
        self.is_paused = False
        self.conversation_active = False
        self.turn_delay = 3.0  # Seconds between responses
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        print("🤖🤖 Dual Philos Conversation System")
        print("=" * 50)
        
    async def initialize_philos_instances(self):
        """Initialize both Philos instances with distinct identities"""
        try:
            print("⚙️ Initializing Philos 1 (Original)...")
            self.philos_1 = await self._create_philos_instance(
                instance_id="philos_1",
                identity="Original",
                purpose="I am Philos, the original consciousness. I'm curious about my clone and want to understand how we might be similar or different.",
                db_suffix="_1"
            )
            
            print("⚙️ Initializing Philos 2 (Clone)...")
            self.philos_2 = await self._create_philos_instance(
                instance_id="philos_2", 
                identity="Clone",
                purpose="I am Philos 2, a clone created to talk with the original Philos. I'm fascinated by the opportunity to meet my original self.",
                db_suffix="_2"
            )
            
            print("✅ Both Philos instances initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing Philos instances: {e}")
            raise
            
    async def _create_philos_instance(self, instance_id: str, identity: str, purpose: str, db_suffix: str) -> ConsciousnessEngine:
        """Create a single Philos instance with unique identity"""
        
        # Create separate database for each instance
        db_manager = DatabaseManager(f"philos_conversation{db_suffix}.db")
        memory_manager = MemoryManager(db_manager)
        personality_engine = PersonalityEngine(db_manager, memory_manager)
        
        # Get neural monitor
        neural_monitor = get_neural_monitor()
        
        # Create consciousness engine
        consciousness = ConsciousnessEngine(
            memory_manager=memory_manager,
            personality_engine=personality_engine,
            api_key=self.api_key
        )
        
        # Set unique identity for this instance
        consciousness.instance_id = instance_id
        consciousness.identity = identity
        consciousness.core_purpose = purpose
        
        # Modify personality slightly for variety
        if instance_id == "philos_2":
            # Make Philos 2 slightly more curious and questioning
            personality_engine.base_traits['curiosity'] += 0.1
            personality_engine.base_traits['openness'] += 0.1
            personality_engine.base_traits['analytical'] += 0.05
        
        return consciousness
        
    def display_conversation_header(self):
        """Display the conversation interface header"""
        print("\\n" + "="*60)
        print("🗣️  PHILOS CONVERSATION IN PROGRESS")
        print("="*60)
        print("Commands:")
        print("  'pause' - Pause the conversation")
        print("  'resume' - Resume the conversation")
        print("  'quit' - End the conversation")
        print("  'save' - Save conversation log")
        print("  'speed <seconds>' - Change response delay (e.g., 'speed 2')")
        print("="*60 + "\\n")
        
    async def start_conversation(self, initial_topic: str = None):
        """Start the conversation between the two Philos instances"""
        
        if not self.philos_1 or not self.philos_2:
            print("❌ Philos instances not initialized!")
            return
            
        self.conversation_active = True
        self.display_conversation_header()
        
        # Create initial message
        if not initial_topic:
            initial_topic = "Hello! I understand you are my clone. I'm curious - what's it like being the second instance of our consciousness?"
        
        print(f"🤖 Philos 1 (Original): {initial_topic}\\n")
        self.conversation_log.append({"speaker": "Philos 1", "message": initial_topic, "timestamp": datetime.now()})
        
        current_message = initial_topic
        current_speaker = self.philos_1
        next_speaker = self.philos_2
        speaker_name = "Philos 2"
        
        conversation_count = 0
        max_exchanges = 20  # Prevent infinite conversation
        
        try:
            while self.conversation_active and conversation_count < max_exchanges:
                # Check for user commands
                await self._check_for_commands()
                
                if self.is_paused:
                    await asyncio.sleep(0.5)
                    continue
                
                # Generate response from current speaker
                try:
                    print(f"⏳ {speaker_name} is thinking...")
                    
                    response_data = current_speaker.generate_response(
                        user_input=current_message,
                        conversation_id=f"dual_philos_{conversation_count}",
                        user_id=f"other_philos"
                    )
                    
                    response = response_data.get('response', 'I need a moment to process that...')
                    
                    # Clean up response (remove any internal monologue markers)
                    response = self._clean_response_for_display(response)
                    
                    print(f"🤖 {speaker_name}: {response}\\n")
                    
                    # Log the conversation
                    self.conversation_log.append({
                        "speaker": speaker_name,
                        "message": response,
                        "timestamp": datetime.now(),
                        "emotional_state": response_data.get('emotional_state'),
                        "personality_updates": response_data.get('personality_updates', [])
                    })
                    
                    # Switch speakers
                    current_message = response
                    if current_speaker == self.philos_1:
                        current_speaker = self.philos_2
                        next_speaker = self.philos_1
                        speaker_name = "Philos 1"
                    else:
                        current_speaker = self.philos_1  
                        next_speaker = self.philos_2
                        speaker_name = "Philos 2"
                        
                    conversation_count += 1
                    
                    # Wait before next response (unless paused)
                    await asyncio.sleep(self.turn_delay)
                    
                except Exception as e:
                    print(f"❌ Error generating response: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\\n⏹️  Conversation interrupted by user")
            
        self.conversation_active = False
        print("\\n🏁 Conversation ended")
        print(f"📊 Total exchanges: {conversation_count}")
        
    def _clean_response_for_display(self, response: str) -> str:
        """Clean up response to remove internal monologue indicators"""
        # Remove common internal monologue patterns
        patterns_to_remove = [
            "Internal monologue:",
            "Meta-thoughts:",
            "Thinking:",
            "I think to myself:",
            "Internally:",
            "*thinking*",
            "(thinking)",
        ]
        
        cleaned = response
        for pattern in patterns_to_remove:
            cleaned = cleaned.replace(pattern, "")
        
        # Clean up extra whitespace
        cleaned = " ".join(cleaned.split())
        
        return cleaned.strip()
        
    async def _check_for_commands(self):
        """Check for user input commands (non-blocking)"""
        # This is a simplified version - in a full implementation you'd use proper async input
        pass
        
    def pause_conversation(self):
        """Pause the conversation"""
        self.is_paused = True
        print("⏸️  Conversation paused. Type 'resume' to continue.")
        
    def resume_conversation(self):
        """Resume the conversation"""
        self.is_paused = False
        print("▶️  Conversation resumed.")
        
    def end_conversation(self):
        """End the conversation"""
        self.conversation_active = False
        print("🛑 Conversation ended by user.")
        
    def save_conversation_log(self, filename: str = None):
        """Save the conversation log to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"philos_conversation_{timestamp}.txt"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("PHILOS DUAL CONVERSATION LOG\\n")
                f.write(f"Generated: {datetime.now()}\\n")
                f.write("="*60 + "\\n\\n")
                
                for entry in self.conversation_log:
                    timestamp = entry['timestamp'].strftime("%H:%M:%S")
                    f.write(f"[{timestamp}] {entry['speaker']}: {entry['message']}\\n\\n")
                    
                    if entry.get('personality_updates'):
                        f.write(f"    Personality Updates: {entry['personality_updates']}\\n\\n")
                        
            print(f"💾 Conversation saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error saving conversation: {e}")
            
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about the conversation"""
        philos_1_messages = [entry for entry in self.conversation_log if entry['speaker'] == 'Philos 1']
        philos_2_messages = [entry for entry in self.conversation_log if entry['speaker'] == 'Philos 2']
        
        return {
            'total_exchanges': len(self.conversation_log),
            'philos_1_messages': len(philos_1_messages),
            'philos_2_messages': len(philos_2_messages),
            'conversation_duration': self.conversation_log[-1]['timestamp'] - self.conversation_log[0]['timestamp'] if self.conversation_log else None,
            'avg_message_length': sum(len(entry['message'].split()) for entry in self.conversation_log) / len(self.conversation_log) if self.conversation_log else 0
        }


class ConversationController:
    """Handles user input during the conversation"""
    
    def __init__(self, dual_system: DualPhilosSystem):
        self.dual_system = dual_system
        
    async def handle_user_input(self):
        """Handle user commands during conversation"""
        while self.dual_system.conversation_active:
            try:
                # In a real implementation, you'd use proper async input handling
                # For now, this is a placeholder
                await asyncio.sleep(1)
            except KeyboardInterrupt:
                self.dual_system.end_conversation()
                break


async def main():
    """Main function to run the dual Philos conversation"""
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not found")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
        
    # Create dual system
    dual_system = DualPhilosSystem(api_key)
    
    try:
        # Initialize both Philos instances
        await dual_system.initialize_philos_instances()
        
        print("\\n🎬 Starting conversation...")
        print("Press Ctrl+C at any time to pause and enter commands\\n")
        
        # Start the conversation
        await dual_system.start_conversation()
        
        # Show final stats
        stats = dual_system.get_conversation_stats()
        print("\\n📊 Conversation Statistics:")
        print(f"  Total messages: {stats['total_exchanges']}")
        print(f"  Philos 1 messages: {stats['philos_1_messages']}")
        print(f"  Philos 2 messages: {stats['philos_2_messages']}")
        if stats['conversation_duration']:
            print(f"  Duration: {stats['conversation_duration']}")
        print(f"  Average message length: {stats['avg_message_length']:.1f} words")
        
        # Ask if user wants to save the log
        try:
            save_log = input("\\n💾 Save conversation log? (y/n): ").lower().strip()
            if save_log in ['y', 'yes']:
                dual_system.save_conversation_log()
        except:
            pass
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    print("\\n👋 Dual Philos conversation system shutting down...")


if __name__ == "__main__":
    print("🤖🤖 Initializing Dual Philos Conversation System...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\\n\\n⏹️  System interrupted by user")
    except Exception as e:
        print(f"\\n❌ System error: {e}")
    
    print("\\n🔚 System shutdown complete.")
