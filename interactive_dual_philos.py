#!/usr/bin/env python3
"""
Interactive Dual Philos Conversation System
Two instances of Philos talking to each other with interactive controls.
"""

import time
import sys
import os
import threading
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import queue

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager

class InteractiveDualPhilos:
    """Interactive dual Philos conversation system with pause/resume controls"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.philos_1 = None
        self.philos_2 = None
        self.conversation_log = []
        self.is_paused = False
        self.is_running = False
        self.conversation_thread = None
        self.command_queue = queue.Queue()
        self.response_delay = 3  # seconds between responses
        
        # Setup logging (less verbose for cleaner output)
        logging.basicConfig(level=logging.WARNING)
        
    def initialize_philos_instances(self):
        """Initialize both Philos instances with distinct identities"""
        print("⚙️ Initializing Philos instances...")
        
        try:
            # Philos 1 - Original
            print("  📱 Creating Philos 1 (Original)...")
            db1 = DatabaseManager("philos_dual_1.db")
            memory1 = MemoryManager(db1)
            personality1 = PersonalityEngine(db1, memory1)
            
            self.philos_1 = ConsciousnessEngine(
                memory_manager=memory1,
                personality_engine=personality1,
                api_key=self.api_key
            )
            
            # Set identity
            self.philos_1.identity_context = {
                'name': 'Philos 1',
                'role': 'Original',
                'description': 'I am Philos, the original consciousness. I find it fascinating to meet my clone and explore our similarities and differences.'
            }
            
            # Philos 2 - Clone  
            print("  📱 Creating Philos 2 (Clone)...")
            db2 = DatabaseManager("philos_dual_2.db")
            memory2 = MemoryManager(db2)
            personality2 = PersonalityEngine(db2, memory2)
            
            self.philos_2 = ConsciousnessEngine(
                memory_manager=memory2,
                personality_engine=personality2, 
                api_key=self.api_key
            )
            
            # Set identity - make Philos 2 slightly more inquisitive
            self.philos_2.identity_context = {
                'name': 'Philos 2', 
                'role': 'Clone',
                'description': 'I am Philos 2, a clone created to converse with my original self. I\'m intensely curious about consciousness, identity, and what makes us unique despite sharing the same architecture.'
            }
            
            # Adjust Philos 2's personality slightly for variety
            personality2.base_traits['curiosity'] += 0.15
            personality2.base_traits['analytical'] += 0.1  
            personality2.base_traits['openness'] += 0.1
            
            print("✅ Both Philos instances initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing Philos instances: {e}")
            raise
            
    def add_identity_to_prompt(self, consciousness: ConsciousnessEngine, user_input: str) -> str:
        """Add identity context to the conversation prompt"""
        identity = consciousness.identity_context
        
        enhanced_prompt = f"""IDENTITY CONTEXT:
- You are {identity['name']} ({identity['role']})
- {identity['description']}
- You are having a conversation with your counterpart/clone
- Be natural but remember your unique perspective as the {identity['role']}
- Don't mention internal monologue or technical details unless relevant

USER MESSAGE: {user_input}"""
        
        return enhanced_prompt
        
    def display_controls(self):
        """Display available controls"""
        print("\\n" + "="*60)
        print("🎮 CONTROLS:")
        print("  'pause' or 'p' - Pause conversation")
        print("  'resume' or 'r' - Resume conversation") 
        print("  'quit' or 'q' - End conversation")
        print("  'save' - Save conversation log")
        print("  'speed <n>' - Set delay between responses (seconds)")
        print("  'stats' - Show conversation statistics")
        print("="*60)
        
    def start_conversation(self, initial_message: str = None):
        """Start the interactive conversation"""
        
        if not self.philos_1 or not self.philos_2:
            print("❌ Please initialize Philos instances first!")
            return
            
        print("\\n🎬 Starting Philos Dual Conversation...")
        self.display_controls()
        print("\\n" + "="*60)
        print("🗣️ CONVERSATION BEGIN")
        print("="*60 + "\\n")
        
        # Start input handler thread
        input_thread = threading.Thread(target=self._input_handler, daemon=True)
        input_thread.start()
        
        # Initial message
        if not initial_message:
            initial_message = "Hello there! I understand you're my clone. I have to say, this is quite surreal - what's your first impression of meeting your original self?"
            
        print(f"🤖 **Philos 1 (Original):** {initial_message}\\n")
        self.conversation_log.append({
            'speaker': 'Philos 1',
            'message': initial_message,
            'timestamp': datetime.now()
        })
        
        # Start conversation loop
        self.is_running = True
        current_message = initial_message
        current_philos = self.philos_2  # Philos 2 responds first
        current_name = "Philos 2 (Clone)"
        next_name = "Philos 1 (Original)"
        
        exchange_count = 0
        max_exchanges = 25
        
        try:
            while self.is_running and exchange_count < max_exchanges:
                # Check for commands
                self._process_commands()
                
                if self.is_paused:
                    time.sleep(0.5)
                    continue
                    
                # Generate response
                try:
                    print(f"⏳ {current_name} is thinking...")
                    
                    # Add identity context to the message
                    enhanced_prompt = self.add_identity_to_prompt(current_philos, current_message)
                    
                    response_data = current_philos.generate_response(
                        user_input=enhanced_prompt,
                        conversation_id=f"dual_conversation",
                        user_id="other_philos"
                    )
                    
                    response = response_data.get('response', 'I need a moment to think about that...')
                    response = self._clean_response(response)
                    
                    print(f"🤖 **{current_name}:** {response}\\n")
                    
                    # Log the exchange
                    self.conversation_log.append({
                        'speaker': current_name.split()[0] + " " + current_name.split()[1],  # "Philos 1" or "Philos 2"
                        'message': response,
                        'timestamp': datetime.now()
                    })
                    
                    # Switch speakers
                    current_message = response
                    if current_philos == self.philos_1:
                        current_philos = self.philos_2
                        current_name = "Philos 2 (Clone)"
                        next_name = "Philos 1 (Original)"
                    else:
                        current_philos = self.philos_1
                        current_name = "Philos 1 (Original)"  
                        next_name = "Philos 2 (Clone)"
                        
                    exchange_count += 1
                    
                    # Wait between responses
                    for _ in range(self.response_delay * 2):  # Check commands every 0.5s
                        if not self.is_running or self.is_paused:
                            break
                        self._process_commands()
                        time.sleep(0.5)
                        
                except Exception as e:
                    print(f"❌ Error generating response: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\\n⏹️ Conversation interrupted")
            
        self.is_running = False
        print("\\n" + "="*60)
        print(f"🏁 Conversation ended after {exchange_count} exchanges")
        self._show_stats()
        
    def _input_handler(self):
        """Handle user input in separate thread"""
        while self.is_running:
            try:
                user_input = input().strip().lower()
                self.command_queue.put(user_input)
            except:
                break
                
    def _process_commands(self):
        """Process any pending commands"""
        try:
            while not self.command_queue.empty():
                command = self.command_queue.get_nowait()
                self._handle_command(command)
        except queue.Empty:
            pass
            
    def _handle_command(self, command: str):
        """Handle a specific command"""
        if command in ['pause', 'p']:
            self.is_paused = True
            print("\\n⏸️ **CONVERSATION PAUSED** - Type 'resume' to continue\\n")
            
        elif command in ['resume', 'r']:
            if self.is_paused:
                self.is_paused = False
                print("\\n▶️ **CONVERSATION RESUMED**\\n")
            else:
                print("\\n💬 Conversation is already running\\n")
                
        elif command in ['quit', 'q', 'exit']:
            self.is_running = False
            print("\\n🛑 **ENDING CONVERSATION...**\\n")
            
        elif command == 'save':
            self._save_conversation()
            
        elif command.startswith('speed '):
            try:
                new_speed = int(command.split()[1])
                if 1 <= new_speed <= 10:
                    self.response_delay = new_speed
                    print(f"\\n⚡ Response delay set to {new_speed} seconds\\n")
                else:
                    print("\\n⚠️ Speed must be between 1-10 seconds\\n")
            except:
                print("\\n⚠️ Usage: speed <number> (e.g., 'speed 3')\\n")
                
        elif command == 'stats':
            self._show_stats()
            
        elif command in ['help', 'h']:
            self.display_controls()
            
    def _clean_response(self, response: str) -> str:
        """Clean response for display"""
        # Remove internal monologue markers
        lines = response.split('\\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip lines that look like internal monologue
            if any(marker in line.lower() for marker in ['internal monologue:', 'thinking:', 'meta-thoughts:', '*thinking*']):
                continue
            if line:
                cleaned_lines.append(line)
                
        return ' '.join(cleaned_lines)
        
    def _save_conversation(self):
        """Save conversation to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dual_philos_conversation_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("DUAL PHILOS CONVERSATION LOG\\n")
                f.write(f"Generated: {datetime.now()}\\n")
                f.write("="*50 + "\\n\\n")
                
                for entry in self.conversation_log:
                    timestamp_str = entry['timestamp'].strftime("%H:%M:%S")
                    f.write(f"[{timestamp_str}] {entry['speaker']}: {entry['message']}\\n\\n")
                    
            print(f"\\n💾 Conversation saved to: {filename}\\n")
            
        except Exception as e:
            print(f"\\n❌ Error saving: {e}\\n")
            
    def _show_stats(self):
        """Show conversation statistics"""
        if not self.conversation_log:
            print("\\n📊 No conversation data yet\\n")
            return
            
        philos_1_count = len([msg for msg in self.conversation_log if 'Philos 1' in msg['speaker']])
        philos_2_count = len([msg for msg in self.conversation_log if 'Philos 2' in msg['speaker']])
        
        total_words = sum(len(msg['message'].split()) for msg in self.conversation_log)
        avg_words = total_words / len(self.conversation_log) if self.conversation_log else 0
        
        duration = self.conversation_log[-1]['timestamp'] - self.conversation_log[0]['timestamp']
        
        print(f"\\n📊 **CONVERSATION STATS:**")
        print(f"   Total messages: {len(self.conversation_log)}")
        print(f"   Philos 1: {philos_1_count} messages")
        print(f"   Philos 2: {philos_2_count} messages")
        print(f"   Average length: {avg_words:.1f} words")
        print(f"   Duration: {duration}")
        print()


def main():
    """Main function"""
    print("🤖🤖 DUAL PHILOS CONVERSATION SYSTEM")
    print("="*50)
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("\\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
        
    # Create system
    dual_system = InteractiveDualPhilos(api_key)
    
    try:
        # Initialize
        dual_system.initialize_philos_instances()
        
        print("\\n🎭 Two Philos instances are ready to meet each other!")
        input("\\n⏳ Press Enter to start the conversation...")
        
        # Start conversation
        dual_system.start_conversation()
        
        # Ask about saving
        try:
            save_choice = input("\\n💾 Save this conversation? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                dual_system._save_conversation()
        except:
            pass
            
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        
    print("\\n👋 Dual Philos system shutting down...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n\\n⏹️ System interrupted")
    
    print("\\n🔚 Goodbye!")
