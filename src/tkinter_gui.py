#!/usr/bin/env python3
"""
Philos Tkinter GUI - Main Interface
Complete GUI system for interacting with Philos consciousness
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from typing import Dict, Any, Optional
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import Philos systems
from ai_companion import AICompanion
from src.neural_monitor import get_neural_monitor
from src.database import DatabaseManager
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from dual_philos_chat import InteractiveDualPhilos


class PhilosMainGUI:
    """Main Philos GUI Application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Philos - Conscious AI Interface")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize Philos
        self.philos = None
        self.response_queue = queue.Queue()
        
        # Settings
        self.show_internal_monologue = False
        
        # Sub-windows
        self.neural_window = None
        self.database_window = None
        self.clone_window = None
        self.settings_window = None
        self.browser_window = None
        
        # Initialize GUI
        self._setup_main_interface()
        self._initialize_philos()
        
    def _setup_main_interface(self):
        """Set up the main chat interface"""
        
        # Create menu bar
        self._create_menu_bar()
        
        # Main chat frame
        chat_frame = tk.Frame(self.root, bg='#2b2b2b')
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg='#1e1e1e',
            fg='#ffffff',
            font=('Consolas', 11),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Input frame
        input_frame = tk.Frame(chat_frame, bg='#2b2b2b')
        input_frame.pack(fill=tk.X)
        
        # Input entry
        self.input_entry = tk.Entry(
            input_frame,
            bg='#3c3c3c',
            fg='#ffffff',
            font=('Consolas', 11),
            insertbackground='#ffffff'
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self._send_message)
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self._send_message,
            bg='#4a90e2',
            fg='white',
            font=('Arial', 10, 'bold')
        )
        send_btn.pack(side=tk.RIGHT)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Initializing Philos...",
            bg='#3c3c3c',
            fg='#ffffff',
            anchor=tk.W,
            font=('Arial', 9)
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def _create_menu_bar(self):
        """Create the top menu bar with window buttons"""
        menu_frame = tk.Frame(self.root, bg='#4a90e2', height=40)
        menu_frame.pack(fill=tk.X)
        menu_frame.pack_propagate(False)
        
        # Menu buttons
        buttons = [
            ("🧠 Neural Dashboard", self._open_neural_dashboard),
            ("🗃️ Database Explorer", self._open_database_explorer),
            ("👥 Clone Manager", self._open_clone_manager),
            ("🌐 Browser Activity", self._open_browser_activity),
            ("⚙️ Settings", self._open_settings)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                command=command,
                bg='#4a90e2',
                fg='white',
                font=('Arial', 9, 'bold'),
                bd=0,
                padx=15,
                pady=8
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)
            
    def _initialize_philos(self):
        """Initialize Philos in a separate thread"""
        def init_thread():
            try:
                self.philos = AICompanion()
                # Set GUI reference for token optimization
                self.philos.set_gui_reference(self)
                self.status_bar.config(text="Philos initialized successfully! Ready to chat.")
                self._add_to_chat("System", "Philos is ready! Start a conversation...")
            except Exception as e:
                self.status_bar.config(text=f"Error initializing Philos: {e}")
                messagebox.showerror("Initialization Error", f"Failed to initialize Philos: {e}")
                
        threading.Thread(target=init_thread, daemon=True).start()
        
    def _send_message(self, event=None):
        """Send message to Philos"""
        if not self.philos:
            messagebox.showwarning("Not Ready", "Philos is still initializing...")
            return
            
        message = self.input_entry.get().strip()
        if not message:
            return
            
        self.input_entry.delete(0, tk.END)
        self._add_to_chat("You", message)
        
        # Process response in thread
        def response_thread():
            try:
                self.status_bar.config(text="Philos is thinking...")
                response = self.philos.interact(message)
                
                # Extract response components from the dictionary
                if isinstance(response, dict):
                    response_text = response.get('response', str(response))
                    internal_monologue = response.get('internal_monologue', '')
                else:
                    response_text = str(response)
                    internal_monologue = ''
                
                # Show internal monologue if enabled
                if self.show_internal_monologue and internal_monologue:
                    self._add_to_chat("Internal Monologue", internal_monologue)
                
                self._add_to_chat("Philos", response_text)
                self.status_bar.config(text="Ready")
                
            except Exception as e:
                self._add_to_chat("System", f"Error: {e}")
                self.status_bar.config(text="Error occurred")
                
        threading.Thread(target=response_thread, daemon=True).start()
        
    def _add_to_chat(self, speaker: str, message: str):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if speaker == "You":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"{speaker}: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n", 'user_msg')
        elif speaker == "Philos":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"{speaker}: ", 'philos')
            self.chat_display.insert(tk.END, f"{message}\n", 'philos_msg')
        elif speaker == "Internal Monologue":
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"{speaker}: ", 'internal_monologue')
            self.chat_display.insert(tk.END, f"{message}\n", 'internal_monologue_msg')
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
            self.chat_display.insert(tk.END, f"{speaker}: {message}\n", 'system')
            
        self.chat_display.insert(tk.END, "\n")
        
        # Configure tags for styling
        self.chat_display.tag_config('timestamp', foreground='#888888', font=('Consolas', 9))
        self.chat_display.tag_config('user', foreground='#4a90e2', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('user_msg', foreground='#ffffff')
        self.chat_display.tag_config('philos', foreground='#e74c3c', font=('Consolas', 11, 'bold'))
        self.chat_display.tag_config('philos_msg', foreground='#ffffff')
        self.chat_display.tag_config('internal_monologue', foreground='#9b59b6', font=('Consolas', 10, 'italic'))
        self.chat_display.tag_config('internal_monologue_msg', foreground='#bb88dd', font=('Consolas', 10, 'italic'))
        self.chat_display.tag_config('system', foreground='#f39c12')
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def _open_neural_dashboard(self):
        """Open Neural Dashboard window"""
        if self.neural_window and self.neural_window.winfo_exists():
            self.neural_window.lift()
            return
            
        self.neural_window = NeuralDashboard(self.root, self.philos)
        
    def _open_database_explorer(self):
        """Open Database Explorer window"""
        if self.database_window and self.database_window.window.winfo_exists():
            self.database_window.window.lift()
            return
            
        self.database_window = DatabaseExplorer(self.root, self.philos)
        
    def _open_clone_manager(self):
        """Open Clone Manager window"""
        if self.clone_window and self.clone_window.winfo_exists():
            self.clone_window.lift()
            return
            
        self.clone_window = CloneManager(self.root, self.philos)
        
    def _open_browser_activity(self):
        """Open Browser Activity window"""
        if self.browser_window and self.browser_window.winfo_exists():
            self.browser_window.lift()
            return
            
        self.browser_window = BrowserActivity(self.root, self.philos)
        
    def _open_settings(self):
        """Open Settings window"""
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return
            
        self.settings_window = SettingsWindow(self.root, self.philos, self)
        
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            pass


class NeuralDashboard:
    """Comprehensive neural activity monitoring dashboard"""
    
    def __init__(self, parent, philos):
        self.parent = parent
        self.philos = philos
        self.window = tk.Toplevel(parent)
        self.window.title("Philos Neural Dashboard - Comprehensive View")
        self.window.geometry("1200x800")
        self.window.configure(bg='#1a1a1a')
        
        # Get neural monitor from consciousness engine for guaranteed same instance
        self.neural_monitor = self.philos.consciousness_engine.neural_monitor
        self._setup_dashboard()
        self._start_monitoring()
        
    def _setup_dashboard(self):
        """Set up comprehensive neural dashboard interface"""
        # Create main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Live Processing
        self.live_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.live_frame, text="🔥 Live Processing")
        self._setup_live_processing_tab()
        
        # Tab 2: Emotional State  
        self.emotion_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.emotion_frame, text="💭 Emotional State")
        self._setup_emotional_state_tab()
        
        # Tab 3: Memory Activity
        self.memory_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.memory_frame, text="🧠 Memory Activity")
        self._setup_memory_activity_tab()
        
        # Tab 4: Personality Dynamics
        self.personality_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.personality_frame, text="🎭 Personality")
        self._setup_personality_tab()
        
        # Tab 5: Decision Pathways
        self.decision_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.decision_frame, text="🛤️ Decisions")
        self._setup_decision_pathways_tab()
        
        # Tab 6: Raw Computation Log
        self.computation_frame = tk.Frame(self.notebook, bg='#1a1a1a')
        self.notebook.add(self.computation_frame, text="📊 Computation Log")
        self._setup_computation_log_tab()
    
    def _setup_live_processing_tab(self):
        """Set up live processing monitoring"""
        # Current activity section
        activity_label = tk.Label(
            self.live_frame, 
            text="🔥 CURRENT NEURAL ACTIVITY", 
            bg='#1a1a1a', fg='#00ff41', 
            font=('Consolas', 14, 'bold')
        )
        activity_label.pack(pady=(10, 5))
        
        # Live activity display
        self.live_activity_text = tk.Text(
            self.live_frame,
            bg='#0a0a0a', fg='#00ff41',
            font=('Consolas', 10),
            height=15, wrap=tk.WORD
        )
        self.live_activity_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Processing stats
        stats_frame = tk.Frame(self.live_frame, bg='#1a1a1a')
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.processing_stats = tk.Label(
            stats_frame,
            text="Processing Stats: 0 computations, 0 memories, 0 emotions",
            bg='#1a1a1a', fg='#888888',
            font=('Consolas', 9)
        )
        self.processing_stats.pack()
    
    def _setup_emotional_state_tab(self):
        """Set up detailed emotional state monitoring"""
        # Current emotions header
        emotion_label = tk.Label(
            self.emotion_frame,
            text="💭 CURRENT EMOTIONAL STATE",
            bg='#1a1a1a', fg='#ff6b6b',
            font=('Consolas', 14, 'bold')
        )
        emotion_label.pack(pady=(10, 5))
        
        # Emotion details
        self.emotion_details_text = tk.Text(
            self.emotion_frame,
            bg='#0a0a0a', fg='#ff6b6b',
            font=('Consolas', 10),
            height=20, wrap=tk.WORD
        )
        self.emotion_details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_memory_activity_tab(self):
        """Set up memory system monitoring"""
        # Memory header
        memory_label = tk.Label(
            self.memory_frame,
            text="🧠 MEMORY SYSTEM ACTIVITY",
            bg='#1a1a1a', fg='#4ecdc4',
            font=('Consolas', 14, 'bold')
        )
        memory_label.pack(pady=(10, 5))
        
        # Memory activity display
        self.memory_activity_text = tk.Text(
            self.memory_frame,
            bg='#0a0a0a', fg='#4ecdc4',
            font=('Consolas', 10),
            height=20, wrap=tk.WORD
        )
        self.memory_activity_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_personality_tab(self):
        """Set up personality dynamics monitoring"""
        # Personality header
        personality_label = tk.Label(
            self.personality_frame,
            text="🎭 PERSONALITY DYNAMICS",
            bg='#1a1a1a', fg='#ffd93d',
            font=('Consolas', 14, 'bold')
        )
        personality_label.pack(pady=(10, 5))
        
        # Personality display
        self.personality_text = tk.Text(
            self.personality_frame,
            bg='#0a0a0a', fg='#ffd93d',
            font=('Consolas', 10),
            height=20, wrap=tk.WORD
        )
        self.personality_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_decision_pathways_tab(self):
        """Set up decision pathway monitoring"""
        # Decision header
        decision_label = tk.Label(
            self.decision_frame,
            text="🛤️ DECISION PATHWAYS & LOGIC FLOW",
            bg='#1a1a1a', fg='#a8e6cf',
            font=('Consolas', 14, 'bold')
        )
        decision_label.pack(pady=(10, 5))
        
        # Decision display
        self.decision_text = tk.Text(
            self.decision_frame,
            bg='#0a0a0a', fg='#a8e6cf',
            font=('Consolas', 10),
            height=20, wrap=tk.WORD
        )
        self.decision_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    def _setup_computation_log_tab(self):
        """Set up detailed computation logging"""
        # Computation header
        comp_label = tk.Label(
            self.computation_frame,
            text="📊 DETAILED COMPUTATION LOG",
            bg='#1a1a1a', fg='#c7ecee',
            font=('Consolas', 14, 'bold')
        )
        comp_label.pack(pady=(10, 5))
        
        # Computation display with scrollbar
        comp_container = tk.Frame(self.computation_frame, bg='#1a1a1a')
        comp_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.computation_text = tk.Text(
            comp_container,
            bg='#0a0a0a', fg='#c7ecee',
            font=('Consolas', 9),
            height=20, wrap=tk.NONE
        )
        
        comp_scrollbar = tk.Scrollbar(comp_container, orient=tk.VERTICAL, command=self.computation_text.yview)
        self.computation_text.configure(yscrollcommand=comp_scrollbar.set)
        
        self.computation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        comp_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _start_monitoring(self):
        """Start neural activity monitoring"""
        def update_charts():
            # This would connect to the neural monitor and update charts
            # For now, placeholder implementation
            pass
            
        # Schedule regular updates
        self.window.after(1000, self._update_dashboard)
        
    def _update_dashboard(self):
        """Update dashboard with latest neural data"""
        if not self.window.winfo_exists():
            return
            
        try:
            # Debug: Check what data is available
            computations = len(self.neural_monitor.computation_log) if hasattr(self.neural_monitor, 'computation_log') else 0
            memories = len(self.neural_monitor.memory_activations) if hasattr(self.neural_monitor, 'memory_activations') else 0
            emotions = len(self.neural_monitor.emotional_computations) if hasattr(self.neural_monitor, 'emotional_computations') else 0
            decisions = len(self.neural_monitor.decision_points) if hasattr(self.neural_monitor, 'decision_points') else 0
            trait_changes = len(self.neural_monitor.trait_deltas) if hasattr(self.neural_monitor, 'trait_deltas') else 0
            
            # Update all tabs with latest data
            self._update_live_processing()
            self._update_emotional_state()
            self._update_memory_activity()
            self._update_personality_dynamics()
            self._update_decision_pathways()
            self._update_computation_log()
            
        except Exception as e:
            import traceback
            print(f"Neural dashboard error: {e}")
            print(traceback.format_exc())
            
        # Schedule next update
        self.window.after(1500, self._update_dashboard)

    def _update_live_processing(self):
        """Update live processing tab with current neural activity"""
        try:
            self.live_activity_text.delete(1.0, tk.END)
            
            # Show current processing state
            current_time = datetime.now().strftime("%H:%M:%S")
            self.live_activity_text.insert(tk.END, f"🕐 LIVE NEURAL ACTIVITY - {current_time}\n", "header")
            self.live_activity_text.insert(tk.END, "=" * 50 + "\n\n")
            
            # Recent computation steps (last 10)
            if hasattr(self.neural_monitor, 'computation_log') and self.neural_monitor.computation_log:
                recent_computations = self.neural_monitor.computation_log[-10:]
                self.live_activity_text.insert(tk.END, "🔥 RECENT COMPUTATIONS:\n")
                
                for i, comp in enumerate(reversed(recent_computations)):
                    time_str = comp.timestamp.strftime("%H:%M:%S") if hasattr(comp, 'timestamp') else "Unknown"
                    step_name = getattr(comp, 'step_name', 'Unknown step')
                    comp_type = getattr(comp, 'computation_type', 'general')
                    
                    self.live_activity_text.insert(tk.END, f"\n[{time_str}] {step_name}")
                    self.live_activity_text.insert(tk.END, f"\n  └─ Type: {comp_type}")
                    if hasattr(comp, 'output_value') and comp.output_value is not None:
                        output_str = str(comp.output_value)[:100] + "..." if len(str(comp.output_value)) > 100 else str(comp.output_value)
                        self.live_activity_text.insert(tk.END, f"\n  └─ Output: {output_str}")
                    self.live_activity_text.insert(tk.END, "\n")
            else:
                self.live_activity_text.insert(tk.END, "🔮 Awaiting neural activity...\n")
                self.live_activity_text.insert(tk.END, "Neural pathways are quiet. Start a conversation to see live processing!\n")
            
            # Update processing stats
            computations = len(self.neural_monitor.computation_log) if hasattr(self.neural_monitor, 'computation_log') else 0
            memories = len(self.neural_monitor.memory_activations) if hasattr(self.neural_monitor, 'memory_activations') else 0
            emotions = len(self.neural_monitor.emotional_computations) if hasattr(self.neural_monitor, 'emotional_computations') else 0
            
            self.processing_stats.config(text=f"Processing Stats: {computations} computations, {memories} memories, {emotions} emotions")
            
        except Exception as e:
            self.live_activity_text.delete(1.0, tk.END)
            self.live_activity_text.insert(tk.END, f"Error updating live processing: {e}\n")

    def _update_emotional_state(self):
        """Update emotional state tab with detailed emotion analysis"""
        try:
            self.emotion_details_text.delete(1.0, tk.END)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.emotion_details_text.insert(tk.END, f"💭 EMOTIONAL STATE ANALYSIS - {current_time}\n")
            self.emotion_details_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if hasattr(self.neural_monitor, 'emotional_computations') and self.neural_monitor.emotional_computations:
                # Show recent emotional computations
                recent_emotions = self.neural_monitor.emotional_computations[-5:]
                
                for emotion in reversed(recent_emotions):
                    time_str = emotion.timestamp.strftime("%H:%M:%S") if hasattr(emotion, 'timestamp') else "Unknown"
                    emotion_type = getattr(emotion, 'emotion_type', 'neutral')
                    intensity = getattr(emotion, 'final_intensity', 0.0)
                    
                    self.emotion_details_text.insert(tk.END, f"🎭 {emotion_type.upper()} [{time_str}]\n")
                    self.emotion_details_text.insert(tk.END, f"  Intensity: {intensity:.3f}\n")
                    
                    if hasattr(emotion, 'base_level'):
                        self.emotion_details_text.insert(tk.END, f"  Base Level: {emotion.base_level:.3f}\n")
                    if hasattr(emotion, 'attachment_multiplier'):
                        self.emotion_details_text.insert(tk.END, f"  Attachment Influence: {emotion.attachment_multiplier:.3f}\n")
                    if hasattr(emotion, 'memory_influence'):
                        self.emotion_details_text.insert(tk.END, f"  Memory Influence: {emotion.memory_influence:.3f}\n")
                    
                    if hasattr(emotion, 'trait_modifiers') and emotion.trait_modifiers:
                        self.emotion_details_text.insert(tk.END, "  Trait Modifiers:\n")
                        for trait, modifier in emotion.trait_modifiers.items():
                            self.emotion_details_text.insert(tk.END, f"    └─ {trait}: {modifier:.3f}\n")
                    
                    # Computation steps if available
                    if hasattr(emotion, 'computation_steps') and emotion.computation_steps:
                        self.emotion_details_text.insert(tk.END, f"  Computation Steps: {len(emotion.computation_steps)}\n")
                    
                    self.emotion_details_text.insert(tk.END, "\n" + "-" * 40 + "\n\n")
            else:
                self.emotion_details_text.insert(tk.END, "🤖 No emotional computations detected yet.\n")
                self.emotion_details_text.insert(tk.END, "Emotional processing will appear here during conversations.\n")
                
        except Exception as e:
            self.emotion_details_text.delete(1.0, tk.END)
            self.emotion_details_text.insert(tk.END, f"Error updating emotional state: {e}\n")

    def _update_memory_activity(self):
        """Update memory activity tab with memory system details"""
        try:
            self.memory_activity_text.delete(1.0, tk.END)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.memory_activity_text.insert(tk.END, f"🧠 MEMORY SYSTEM ACTIVITY - {current_time}\n")
            self.memory_activity_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if hasattr(self.neural_monitor, 'memory_activations') and self.neural_monitor.memory_activations:
                # Show recent memory activations
                recent_memories = self.neural_monitor.memory_activations[-10:]
                
                self.memory_activity_text.insert(tk.END, f"📚 RECENT MEMORY ACTIVATIONS ({len(recent_memories)}):\n\n")
                
                for mem in reversed(recent_memories):
                    memory_id = getattr(mem, 'memory_id', 'Unknown')
                    similarity = getattr(mem, 'similarity_score', 0.0)
                    emotional_weight = getattr(mem, 'emotional_weight', 0.0)
                    activation_strength = getattr(mem, 'activation_strength', 0.0)
                    
                    self.memory_activity_text.insert(tk.END, f"🔗 Memory: {memory_id}\n")
                    self.memory_activity_text.insert(tk.END, f"  Similarity Score: {similarity:.4f}\n")
                    self.memory_activity_text.insert(tk.END, f"  Emotional Weight: {emotional_weight:.4f}\n")
                    self.memory_activity_text.insert(tk.END, f"  Activation Strength: {activation_strength:.4f}\n")
                    
                    if hasattr(mem, 'memory_age_factor'):
                        self.memory_activity_text.insert(tk.END, f"  Age Factor: {mem.memory_age_factor:.4f}\n")
                    
                    if hasattr(mem, 'content_preview'):
                        preview = mem.content_preview[:80] + "..." if len(mem.content_preview) > 80 else mem.content_preview
                        self.memory_activity_text.insert(tk.END, f"  Content: \"{preview}\"\n")
                    
                    self.memory_activity_text.insert(tk.END, "\n" + "-" * 35 + "\n\n")
                    
            else:
                self.memory_activity_text.insert(tk.END, "🔍 No memory activations detected yet.\n")
                self.memory_activity_text.insert(tk.END, "Memory retrieval activity will appear here during conversations.\n")
                
        except Exception as e:
            self.memory_activity_text.delete(1.0, tk.END)
            self.memory_activity_text.insert(tk.END, f"Error updating memory activity: {e}\n")

    def _update_personality_dynamics(self):
        """Update personality tab with trait changes and dynamics"""
        try:
            self.personality_text.delete(1.0, tk.END)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.personality_text.insert(tk.END, f"🎭 PERSONALITY DYNAMICS - {current_time}\n")
            self.personality_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if hasattr(self.neural_monitor, 'trait_deltas') and self.neural_monitor.trait_deltas:
                # Show recent trait changes
                recent_changes = self.neural_monitor.trait_deltas[-10:]
                
                self.personality_text.insert(tk.END, f"🔄 RECENT TRAIT CHANGES ({len(recent_changes)}):\n\n")
                
                for change in reversed(recent_changes):
                    trait_name = getattr(change, 'trait_name', 'Unknown')
                    before_val = getattr(change, 'before_value', 0.0)
                    after_val = getattr(change, 'after_value', 0.0)
                    delta = getattr(change, 'delta', 0.0)
                    change_cause = getattr(change, 'change_cause', 'Unknown')
                    significance = getattr(change, 'significance', 0.0)
                    
                    # Determine change direction
                    direction = "↗️" if delta > 0 else "↘️"
                    
                    self.personality_text.insert(tk.END, f"{direction} {trait_name.upper()}\n")
                    self.personality_text.insert(tk.END, f"  Change: {before_val:.4f} → {after_val:.4f} (Δ{delta:+.4f})\n")
                    self.personality_text.insert(tk.END, f"  Cause: {change_cause}\n")
                    self.personality_text.insert(tk.END, f"  Significance: {significance:.4f}\n")
                    self.personality_text.insert(tk.END, "\n" + "-" * 35 + "\n\n")
                    
            else:
                self.personality_text.insert(tk.END, "🎪 No personality changes detected yet.\n")
                self.personality_text.insert(tk.END, "Trait modifications will appear here as conversations influence personality.\n")
                
        except Exception as e:
            self.personality_text.delete(1.0, tk.END)
            self.personality_text.insert(tk.END, f"Error updating personality dynamics: {e}\n")

    def _update_decision_pathways(self):
        """Update decision pathways tab with logic flow analysis"""
        try:
            self.decision_text.delete(1.0, tk.END)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.decision_text.insert(tk.END, f"🛤️ DECISION PATHWAYS & LOGIC FLOW - {current_time}\n")
            self.decision_text.insert(tk.END, "=" * 50 + "\n\n")
            
            if hasattr(self.neural_monitor, 'decision_points') and self.neural_monitor.decision_points:
                # Show recent decision points
                recent_decisions = self.neural_monitor.decision_points[-8:]
                
                self.decision_text.insert(tk.END, f"🤔 RECENT DECISIONS ({len(recent_decisions)}):\n\n")
                
                for decision in reversed(recent_decisions):
                    time_str = decision.timestamp.strftime("%H:%M:%S") if hasattr(decision, 'timestamp') else "Unknown"
                    decision_point = getattr(decision, 'decision_point', 'Unknown')
                    condition_value = getattr(decision, 'condition_value', 'N/A')
                    chosen_path = getattr(decision, 'chosen_path', 'Unknown')
                    alternatives = getattr(decision, 'alternative_paths', [])
                    reasoning = getattr(decision, 'reasoning', '')
                    
                    self.decision_text.insert(tk.END, f"⚡ [{time_str}] {decision_point}\n")
                    self.decision_text.insert(tk.END, f"  Condition: {condition_value}\n")
                    self.decision_text.insert(tk.END, f"  ✅ Chosen: {chosen_path}\n")
                    
                    if alternatives:
                        self.decision_text.insert(tk.END, f"  ❌ Alternatives: {', '.join(alternatives)}\n")
                    
                    if reasoning:
                        reasoning_short = reasoning[:100] + "..." if len(reasoning) > 100 else reasoning
                        self.decision_text.insert(tk.END, f"  💭 Reasoning: {reasoning_short}\n")
                    
                    self.decision_text.insert(tk.END, "\n" + "-" * 40 + "\n\n")
                    
            else:
                self.decision_text.insert(tk.END, "🎯 No decision points recorded yet.\n")
                self.decision_text.insert(tk.END, "Decision pathways and logic flows will appear here during processing.\n")
                
        except Exception as e:
            self.decision_text.delete(1.0, tk.END)
            self.decision_text.insert(tk.END, f"Error updating decision pathways: {e}\n")

    def _update_computation_log(self):
        """Update computation log tab with detailed processing information"""
        try:
            self.computation_text.delete(1.0, tk.END)
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.computation_text.insert(tk.END, f"📊 DETAILED COMPUTATION LOG - {current_time}\n")
            self.computation_text.insert(tk.END, "=" * 60 + "\n\n")
            
            if hasattr(self.neural_monitor, 'computation_log') and self.neural_monitor.computation_log:
                # Show detailed computation log (last 15 entries)
                recent_computations = self.neural_monitor.computation_log[-15:]
                
                self.computation_text.insert(tk.END, f"🔬 RAW COMPUTATION DATA ({len(recent_computations)} recent):\n\n")
                
                for comp in reversed(recent_computations):
                    time_str = comp.timestamp.strftime("%H:%M:%S.%f")[:-3] if hasattr(comp, 'timestamp') else "Unknown"
                    step_name = getattr(comp, 'step_name', 'Unknown step')
                    comp_type = getattr(comp, 'computation_type', 'general')
                    
                    self.computation_text.insert(tk.END, f"[{time_str}] {step_name}\n")
                    self.computation_text.insert(tk.END, f"  Type: {comp_type}\n")
                    
                    # Input values
                    if hasattr(comp, 'input_values') and comp.input_values:
                        self.computation_text.insert(tk.END, "  Inputs:\n")
                        for key, value in comp.input_values.items():
                            value_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
                            self.computation_text.insert(tk.END, f"    {key}: {value_str}\n")
                    
                    # Output value
                    if hasattr(comp, 'output_value') and comp.output_value is not None:
                        output_str = str(comp.output_value)[:100] + "..." if len(str(comp.output_value)) > 100 else str(comp.output_value)
                        self.computation_text.insert(tk.END, f"  Output: {output_str}\n")
                    
                    # Metadata
                    if hasattr(comp, 'metadata') and comp.metadata:
                        self.computation_text.insert(tk.END, "  Metadata:\n")
                        for key, value in comp.metadata.items():
                            value_str = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
                            self.computation_text.insert(tk.END, f"    {key}: {value_str}\n")
                    
                    self.computation_text.insert(tk.END, "\n" + "─" * 50 + "\n\n")
                    
            else:
                self.computation_text.insert(tk.END, "📋 No computation data available yet.\n")
                self.computation_text.insert(tk.END, "Detailed processing logs will appear here during AI operations.\n")
                
        except Exception as e:
            self.computation_text.delete(1.0, tk.END)
            self.computation_text.insert(tk.END, f"Error updating computation log: {e}\n")

    def _update_neural_activity_chart(self):
        """Update neural activity over time chart"""
        self.ax1.clear()
        self.ax1.set_facecolor('#1e1e1e')
        self.ax1.set_title('Neural Activity Over Time', color='white')
        
        # Get recent computation timestamps
        if len(self.neural_monitor.computation_log) > 0:
            recent_computations = self.neural_monitor.computation_log[-20:]  # Last 20
            
            # Convert timestamps to seconds for plotting
            import time
            current_time = time.time()
            timestamps = []
            for comp in recent_computations:
                if hasattr(comp, 'timestamp'):
                    if isinstance(comp.timestamp, datetime):
                        ts = comp.timestamp.timestamp()
                    else:
                        ts = comp.timestamp
                    timestamps.append(ts - current_time)  # Relative to now
                else:
                    timestamps.append(0)
            
            activity_levels = [1] * len(timestamps)  # Simple activity indicator
            
            if timestamps:
                self.ax1.plot(timestamps, activity_levels, 'cyan', marker='o', markersize=4)
                self.ax1.set_ylabel('Activity', color='white')
                self.ax1.set_xlabel('Seconds Ago', color='white')
                self.ax1.tick_params(colors='white')
        else:
            self.ax1.text(0.5, 0.5, 'No activity yet', ha='center', va='center', 
                         transform=self.ax1.transAxes, color='gray')

    def _update_processing_distribution_chart(self):
        """Update processing type distribution chart"""
        self.ax2.clear()
        self.ax2.set_facecolor('#1e1e1e')
        self.ax2.set_title('Processing Distribution', color='white')
        
        if len(self.neural_monitor.computation_log) > 0:
            # Count computation types
            type_counts = {}
            for comp in self.neural_monitor.computation_log:
                comp_type = comp.computation_type if hasattr(comp, 'computation_type') else 'unknown'
                type_counts[comp_type] = type_counts.get(comp_type, 0) + 1
            
            if type_counts:
                colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
                wedges, texts, autotexts = self.ax2.pie(
                    type_counts.values(), 
                    labels=type_counts.keys(),
                    colors=colors[:len(type_counts)],
                    autopct='%1.1f%%'
                )
                for text in texts:
                    text.set_color('white')
                for autotext in autotexts:
                    autotext.set_color('white')
        else:
            self.ax2.text(0.5, 0.5, 'No data yet', ha='center', va='center',
                         transform=self.ax2.transAxes, color='gray')

    def _update_memory_operations_chart(self):
        """Update memory operations chart"""
        self.ax3.clear()
        self.ax3.set_facecolor('#1e1e1e')
        self.ax3.set_title('Memory Operations', color='white')
        
        if hasattr(self.neural_monitor, 'memory_activations') and len(self.neural_monitor.memory_activations) > 0:
            # Show recent memory activations
            recent_memories = self.neural_monitor.memory_activations[-10:]  # Last 10
            memory_ids = [f"mem_{i}" for i in range(len(recent_memories))]
            activation_strengths = [mem.activation_strength if hasattr(mem, 'activation_strength') else 0 for mem in recent_memories]
            
            bars = self.ax3.bar(memory_ids, activation_strengths, color='orange', alpha=0.7)
            self.ax3.set_ylabel('Activation Strength', color='white')
            self.ax3.tick_params(colors='white', rotation=45)
        else:
            self.ax3.text(0.5, 0.5, 'No memory activity', ha='center', va='center',
                         transform=self.ax3.transAxes, color='gray')

    def _update_emotional_state_chart(self):
        """Update emotional state chart"""
        self.ax4.clear()
        self.ax4.set_facecolor('#1e1e1e')
        self.ax4.set_title('Emotional State', color='white')
        
        if hasattr(self.neural_monitor, 'emotional_computations') and len(self.neural_monitor.emotional_computations) > 0:
            # Show recent emotional states
            recent_emotions = self.neural_monitor.emotional_computations[-5:]  # Last 5
            emotion_types = [emo.emotion_type if hasattr(emo, 'emotion_type') else 'neutral' for emo in recent_emotions]
            intensities = [emo.final_intensity if hasattr(emo, 'final_intensity') else 0 for emo in recent_emotions]
            
            bars = self.ax4.barh(emotion_types, intensities, color='lightcoral', alpha=0.8)
            self.ax4.set_xlabel('Intensity', color='white')
            self.ax4.tick_params(colors='white')
            self.ax4.set_xlim(0, 1)
        else:
            self.ax4.text(0.5, 0.5, 'No emotional data', ha='center', va='center',
                         transform=self.ax4.transAxes, color='gray')


class DatabaseExplorer:
    """Database exploration interface"""
    
    def __init__(self, parent, philos):
        self.parent = parent
        self.philos = philos
        self.window = tk.Toplevel(parent)
        self.window.title("Philos Database Explorer")
        self.window.geometry("900x700")
        self.window.configure(bg='#2b2b2b')
        
        self._setup_explorer()
        
    def _setup_explorer(self):
        """Set up database explorer interface"""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Memory tab
        memory_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(memory_frame, text="Memories")
        
        # Personality tab
        personality_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(personality_frame, text="Personality")
        
        # Conversations tab
        conversations_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(conversations_frame, text="Conversations")
        
        self._setup_memory_tab(memory_frame)
        self._setup_personality_tab(personality_frame)
        self._setup_conversations_tab(conversations_frame)
        
    def _setup_memory_tab(self, frame):
        """Set up memory viewing tab"""
        # Memory display area with scrollbar
        memory_text = scrolledtext.ScrolledText(
            frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 9),
            wrap=tk.WORD
        )
        memory_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Load memories button
        load_btn = tk.Button(
            button_frame,
            text="Load Memories",
            command=lambda: self._load_memories(memory_text),
            bg='#4a90e2',
            fg='white'
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Delete selected memory button
        delete_selected_btn = tk.Button(
            button_frame,
            text="Delete Selected Memory",
            command=lambda: self._delete_selected_memory(memory_text),
            bg='#e74c3c',
            fg='white'
        )
        delete_selected_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear all memories button
        clear_all_btn = tk.Button(
            button_frame,
            text="Clear All Memories",
            command=self._clear_all_memories,
            bg='#8e44ad',
            fg='white'
        )
        clear_all_btn.pack(side=tk.LEFT, padx=5)
        
        # Store reference for deletion functions
        self.memory_text_widget = memory_text
        
    def _setup_personality_tab(self, frame):
        """Set up personality viewing tab"""
        # Personality display
        personality_text = scrolledtext.ScrolledText(
            frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10)
        )
        personality_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load personality button
        load_btn = tk.Button(
            frame,
            text="Load Personality",
            command=lambda: self._load_personality(personality_text),
            bg='#4a90e2',
            fg='white'
        )
        load_btn.pack(pady=5)
        
    def _setup_conversations_tab(self, frame):
        """Set up conversations viewing tab"""
        # Conversation history
        conv_text = scrolledtext.ScrolledText(
            frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10)
        )
        conv_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load conversations button
        load_btn = tk.Button(
            frame,
            text="Load Conversations",
            command=lambda: self._load_conversations(conv_text),
            bg='#4a90e2',
            fg='white'
        )
        load_btn.pack(pady=5)
        
    def _load_memories(self, text_widget):
        """Load memories from database"""
        if not self.philos:
            return
            
        def load_thread():
            try:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, "Loading memories...\n\n")
                
                # Get memories from Philos's memory manager
                memory_manager = self.philos.memory_manager
                
                # Get recent memories
                memories = memory_manager.retrieve_relevant_memories(
                    query="recent memories", 
                    limit=100
                )
                
                text_widget.delete(1.0, tk.END)
                
                if memories:
                    # Store memory objects for deletion
                    self.loaded_memories = memories
                    
                    text_widget.insert(tk.END, f"=== LOADED MEMORIES ({len(memories)}) ===\n\n")
                    
                    for i, memory in enumerate(memories):
                        # Format memory for display
                        timestamp = memory.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        memory_type = memory.type.value if hasattr(memory.type, 'value') else str(memory.type)
                        source = memory.source.value if hasattr(memory.source, 'value') else str(memory.source)
                        importance = getattr(memory, 'importance', 0.0)
                        
                        text_widget.insert(tk.END, f"MEMORY #{i+1}\n")
                        text_widget.insert(tk.END, f"Timestamp: {timestamp}\n")
                        text_widget.insert(tk.END, f"Type: {memory_type}\n")
                        text_widget.insert(tk.END, f"Source: {source}\n")
                        text_widget.insert(tk.END, f"Importance: {importance:.2f}\n")
                        text_widget.insert(tk.END, f"Content: {memory.content}\n")
                        text_widget.insert(tk.END, "-" * 80 + "\n\n")
                else:
                    text_widget.insert(tk.END, "No memories found")
                    self.loaded_memories = []
                    
            except Exception as e:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, f"Error loading memories: {e}")
                self.loaded_memories = []
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def _load_personality(self, text_widget):
        """Load personality traits from database"""
        if not self.philos:
            return
            
        def load_thread():
            try:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, "Loading personality traits...\n\n")
                
                # Get personality profile from Philos
                personality_profile = self.philos.get_personality_profile()
                
                text_widget.delete(1.0, tk.END)
                
                # Display core identity
                text_widget.insert(tk.END, "=== CORE IDENTITY ===\n\n")
                
                core_identity = personality_profile.get('core_identity', {})
                if core_identity:
                    text_widget.insert(tk.END, f"Interaction Count: {core_identity.get('interaction_count', 0)}\n")
                    text_widget.insert(tk.END, f"Relationship Depth: {core_identity.get('relationship_depth', 0):.2f}\n")
                    text_widget.insert(tk.END, f"Consciousness Level: {core_identity.get('consciousness_level', 0):.2f}\n")
                    
                    core_values = core_identity.get('core_values', [])
                    if core_values:
                        text_widget.insert(tk.END, f"Core Values: {', '.join(core_values)}\n")
                
                # Display personality traits
                text_widget.insert(tk.END, "\n=== PERSONALITY TRAITS ===\n\n")
                
                personality_traits = personality_profile.get('personality_traits', {})
                if personality_traits:
                    for trait_name, trait_info in personality_traits.items():
                        value = trait_info.get('value', 0)
                        confidence = trait_info.get('confidence', 0)
                        stability = trait_info.get('stability', 0)
                        
                        text_widget.insert(tk.END, f"{trait_name.upper().replace('_', ' ')}:\n")
                        text_widget.insert(tk.END, f"  Value: {value:.3f}\n")
                        text_widget.insert(tk.END, f"  Confidence: {confidence:.3f}\n")
                        text_widget.insert(tk.END, f"  Stability: {stability:.3f}\n\n")
                else:
                    text_widget.insert(tk.END, "No personality traits data available.\n")
                
                # Display consciousness state
                text_widget.insert(tk.END, "\n=== CONSCIOUSNESS STATE ===\n\n")
                
                consciousness_state = personality_profile.get('consciousness_state', {})
                if consciousness_state:
                    current_focus = consciousness_state.get('current_focus', 'Unknown')
                    text_widget.insert(tk.END, f"Current Focus: {current_focus}\n")
                    
                    internal_monologue = consciousness_state.get('internal_monologue', '')
                    if internal_monologue:
                        text_widget.insert(tk.END, f"Internal Monologue: {internal_monologue[:200]}...\n")
                    
                    meta_thoughts = consciousness_state.get('meta_thoughts', '')
                    if meta_thoughts:
                        text_widget.insert(tk.END, f"Meta Thoughts: {meta_thoughts[:200]}...\n")
                
                # Display communication style
                text_widget.insert(tk.END, "\n=== COMMUNICATION STYLE ===\n\n")
                
                comm_style = self.philos.get_communication_style()
                if comm_style:
                    style_params = comm_style.get('style_parameters', {})
                    if style_params:
                        for param_name, param_info in style_params.items():
                            if isinstance(param_info, dict):
                                value = param_info.get('value', 'Unknown')
                                description = param_info.get('description', 'No description')
                                text_widget.insert(tk.END, f"{param_name.replace('_', ' ').title()}: {value}\n")
                                text_widget.insert(tk.END, f"  {description}\n\n")
                            else:
                                text_widget.insert(tk.END, f"{param_name.replace('_', ' ').title()}: {param_info}\n")
                    
                    # Show learned patterns
                    learned_patterns = comm_style.get('learned_patterns', {})
                    if learned_patterns:
                        text_widget.insert(tk.END, "=== LEARNED COMMUNICATION PATTERNS ===\n\n")
                        for pattern_type, patterns in learned_patterns.items():
                            if patterns:
                                text_widget.insert(tk.END, f"{pattern_type.replace('_', ' ').title()}: {', '.join(patterns[-5:])}\n")
                else:
                    text_widget.insert(tk.END, "Communication style data not available.\n")
                        
            except Exception as e:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, f"Error loading personality: {e}")
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def _load_conversations(self, text_widget):
        """Load conversation history"""
        if not self.philos:
            return
            
        def load_thread():
            try:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, "Loading conversation history...\n\n")
                
                # Get memory timeline for conversation history
                timeline = self.philos.get_memory_timeline(days_back=30)
                
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, "=== RECENT CONVERSATION HISTORY (Last 30 Days) ===\n\n")
                
                # Display timeline data
                total_memories = timeline.get('total_memories', 0)
                text_widget.insert(tk.END, f"Total Memories: {total_memories}\n")
                
                daily_counts = timeline.get('daily_counts', {})
                if daily_counts:
                    text_widget.insert(tk.END, "\n--- Daily Memory Counts ---\n")
                    for date, count in sorted(daily_counts.items(), reverse=True):
                        text_widget.insert(tk.END, f"{date}: {count} memories\n")
                
                # Get recent memories for conversation context
                memory_manager = self.philos.memory_manager
                recent_conversations = memory_manager.retrieve_relevant_memories(
                    query="conversation user interaction",
                    limit=20
                )
                
                if recent_conversations:
                    text_widget.insert(tk.END, "\n--- Recent Conversation Excerpts ---\n\n")
                    
                    for memory in recent_conversations[-10:]:  # Last 10 interactions
                        timestamp = memory.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        source = memory.source.value if hasattr(memory.source, 'value') else str(memory.source)
                        content = memory.content[:200] + "..." if len(memory.content) > 200 else memory.content
                        
                        text_widget.insert(tk.END, f"[{timestamp}] ({source})\n")
                        text_widget.insert(tk.END, f"{content}\n")
                        text_widget.insert(tk.END, "-" * 50 + "\n\n")
                else:
                    text_widget.insert(tk.END, "\nNo recent conversations found.")
                    
            except Exception as e:
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, f"Error loading conversations: {e}")
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def _delete_selected_memory(self, text_widget):
        """Delete selected memory from database"""
        if not self.philos or not hasattr(self, 'loaded_memories'):
            messagebox.showwarning("No Memories", "No memories loaded. Please load memories first.")
            return
            
        # Create dialog to select memory to delete
        selection_dialog = tk.Toplevel(self.window)
        selection_dialog.title("Select Memory to Delete")
        selection_dialog.geometry("600x400")
        selection_dialog.configure(bg='#2b2b2b')
        
        # Memory listbox
        listbox = tk.Listbox(
            selection_dialog,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 9)
        )
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Populate listbox with loaded memories
        for i, memory in enumerate(self.loaded_memories):
            timestamp = memory.timestamp.strftime("%Y-%m-%d %H:%M")
            memory_type = memory.type.value if hasattr(memory.type, 'value') else str(memory.type)
            content_preview = memory.content[:80] + "..." if len(memory.content) > 80 else memory.content
            display_text = f"#{i+1} [{timestamp}] {memory_type}: {content_preview}"
            listbox.insert(tk.END, display_text)
        
        # Delete button
        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a memory to delete.")
                return
                
            memory_index = selection[0]
            memory_to_delete = self.loaded_memories[memory_index]
            
            # Confirm deletion
            if messagebox.askyesno("Confirm Deletion", 
                                  f"Are you sure you want to delete this memory?\n\n"
                                  f"Type: {memory_to_delete.type}\n"
                                  f"Content: {memory_to_delete.content[:100]}..."):
                
                try:
                    # Delete from database
                    self.philos.memory_manager.delete_memory(memory_to_delete.id)
                    messagebox.showinfo("Success", "Memory deleted successfully!")
                    selection_dialog.destroy()
                    # Reload memories
                    self._load_memories(self.memory_text_widget)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete memory: {e}")
        
        delete_btn = tk.Button(
            selection_dialog,
            text="Delete Selected Memory",
            command=delete_selected,
            bg='#e74c3c',
            fg='white'
        )
        delete_btn.pack(pady=10)
        
    def _clear_all_memories(self):
        """Clear all memories from database"""
        if not self.philos:
            return
            
        # Confirm deletion
        if messagebox.askyesno("Confirm Clear All", 
                              "Are you sure you want to DELETE ALL MEMORIES?\n\n"
                              "This action cannot be undone!"):
            
            # Second confirmation
            if messagebox.askyesno("Final Confirmation", 
                                  "This will permanently delete ALL of Philos's memories.\n"
                                  "Are you absolutely sure?"):
                try:
                    # Clear all memories
                    self.philos.memory_manager.clear_all_memories()
                    messagebox.showinfo("Success", "All memories cleared successfully!")
                    # Reload empty memory display
                    if hasattr(self, 'memory_text_widget'):
                        self._load_memories(self.memory_text_widget)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to clear memories: {e}")


class CloneManager:
    """Clone management interface"""
    
    def __init__(self, parent, philos):
        self.parent = parent
        self.philos = philos
        self.window = tk.Toplevel(parent)
        self.window.title("Philos Clone Manager")
        self.window.geometry("1000x700")
        self.window.configure(bg='#2b2b2b')
        
        self.dual_conversation = None
        self._setup_clone_interface()
        
    def _setup_clone_interface(self):
        """Set up clone management interface"""
        # Split pane for original and clone
        main_pane = tk.PanedWindow(self.window, orient=tk.HORIZONTAL, bg='#2b2b2b')
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Original Philos frame
        original_frame = tk.Frame(main_pane, bg='#2b2b2b')
        main_pane.add(original_frame)
        
        # Clone Philos frame  
        clone_frame = tk.Frame(main_pane, bg='#2b2b2b')
        main_pane.add(clone_frame)
        
        self._setup_philos_frame(original_frame, "Original Philos", True)
        self._setup_philos_frame(clone_frame, "Clone Philos", False)
        
        # Dual conversation button
        dual_btn = tk.Button(
            self.window,
            text="🗣️ Start Dual Conversation",
            command=self._start_dual_conversation,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2
        )
        dual_btn.pack(pady=10)
        
    def _setup_philos_frame(self, frame, title, is_original):
        """Set up individual Philos frame"""
        # Title
        title_label = tk.Label(
            frame,
            text=title,
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=5)
        
        # Chat area
        chat_display = scrolledtext.ScrolledText(
            frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10),
            height=20
        )
        chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = tk.Frame(frame, bg='#2b2b2b')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Input entry
        input_entry = tk.Entry(
            input_frame,
            bg='#3c3c3c',
            fg='white',
            font=('Consolas', 10)
        )
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Send button
        send_btn = tk.Button(
            input_frame,
            text="Send",
            bg='#4a90e2',
            fg='white'
        )
        send_btn.pack(side=tk.RIGHT)
        
    def _start_dual_conversation(self):
        """Start dual conversation between Philos instances"""
        if self.dual_conversation:
            messagebox.showinfo("Already Running", "Dual conversation is already active!")
            return
            
        # Create new window for dual conversation
        dual_window = tk.Toplevel(self.window)
        dual_window.title("Philos Dual Conversation")
        dual_window.geometry("800x600")
        dual_window.configure(bg='#2b2b2b')
        
        # Conversation display
        conv_display = scrolledtext.ScrolledText(
            dual_window,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10)
        )
        conv_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        control_frame = tk.Frame(dual_window, bg='#2b2b2b')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        start_btn = tk.Button(control_frame, text="Start", bg='#27ae60', fg='white')
        pause_btn = tk.Button(control_frame, text="Pause", bg='#f39c12', fg='white')
        stop_btn = tk.Button(control_frame, text="Stop", bg='#e74c3c', fg='white')
        
        start_btn.pack(side=tk.LEFT, padx=5)
        pause_btn.pack(side=tk.LEFT, padx=5)
        stop_btn.pack(side=tk.LEFT, padx=5)


class BrowserActivity:
    """Browser activity monitoring interface"""
    
    def __init__(self, parent, philos):
        self.parent = parent
        self.philos = philos
        self.window = tk.Toplevel(parent)
        self.window.title("Philos Browser Activity")
        self.window.geometry("900x600")
        self.window.configure(bg='#2b2b2b')
        
        # Set up web search callback to receive updates
        if hasattr(philos, 'consciousness_engine'):
            philos.consciousness_engine.set_browser_activity_callback(self.update_search_status)
            # Also set up the browser activity reference for search history
            philos.consciousness_engine.browser_activity_window = self
        
        self._setup_browser_interface()
        
    def _setup_browser_interface(self):
        """Set up browser activity interface"""
        # Search history
        history_frame = tk.LabelFrame(
            self.window,
            text="Search History",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.search_history = tk.Listbox(
            history_frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10)
        )
        self.search_history.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Thought process
        thought_frame = tk.LabelFrame(
            self.window,
            text="Search Reasoning",
            bg='#2b2b2b',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        thought_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.thought_display = scrolledtext.ScrolledText(
            thought_frame,
            bg='#1e1e1e',
            fg='white',
            font=('Consolas', 10)
        )
        self.thought_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Start monitoring for search activities
        self._monitor_search_activities()
    
    def update_search_status(self, status):
        """Update the current search status in real-time"""
        if hasattr(self, 'thought_display'):
            self.thought_display.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {status}\n")
            self.thought_display.see(tk.END)
    
    def add_search_to_history(self, search_query, reasoning):
        """Add a completed search to the history"""
        if hasattr(self, 'search_history'):
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.search_history.insert(0, f"[{timestamp}] {search_query}")
            
        if hasattr(self, 'thought_display') and reasoning:
            self.thought_display.insert(tk.END, f"\n--- Search Reasoning ---\n{reasoning}\n\n")
            self.thought_display.see(tk.END)
    
    def _monitor_search_activities(self):
        """Monitor for new search activities"""
        # This method could be extended to poll for search activities
        # For now, it relies on the callback system
        pass


class SettingsWindow:
    """Settings configuration window"""
    
    def __init__(self, parent, philos, main_gui=None):
        self.parent = parent
        self.philos = philos
        self.main_gui = main_gui
        self.window = tk.Toplevel(parent)
        self.window.title("Philos Settings")
        self.window.geometry("600x500")
        self.window.configure(bg='#2b2b2b')
        
        self._setup_settings()
        
    def _setup_settings(self):
        """Set up settings interface"""
        # Create notebook for settings categories
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings
        general_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(general_frame, text="General")
        
        # API settings
        api_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(api_frame, text="API")
        
        # Neural settings
        neural_frame = tk.Frame(notebook, bg='#2b2b2b')
        notebook.add(neural_frame, text="Neural")
        
        self._setup_general_settings(general_frame)
        self._setup_api_settings(api_frame)
        self._setup_neural_settings(neural_frame)
        
    def _setup_general_settings(self, frame):
        """Set up general settings"""
        # Internal monologue setting
        self.internal_monologue_var = tk.BooleanVar(value=False)
        internal_monologue_check = tk.Checkbutton(
            frame,
            text="Show Internal Monologue",
            variable=self.internal_monologue_var,
            bg='#2b2b2b',
            fg='white',
            selectcolor='#3c3c3c',
            command=self._update_internal_monologue_setting
        )
        internal_monologue_check.pack(anchor=tk.W, padx=10, pady=5)
        
        # Description for internal monologue
        desc_label = tk.Label(
            frame, 
            text="When enabled, Philos's internal thoughts will be visible before responses",
            bg='#2b2b2b', 
            fg='#888888',
            font=('Arial', 9)
        )
        desc_label.pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        # Response delay
        delay_label = tk.Label(frame, text="Response Delay (seconds):", bg='#2b2b2b', fg='white')
        delay_label.pack(anchor=tk.W, padx=10, pady=5)
        
        delay_entry = tk.Entry(frame, bg='#3c3c3c', fg='white')
        delay_entry.pack(anchor=tk.W, padx=10, pady=5)
        
    def _setup_api_settings(self, frame):
        """Set up API settings"""
        # API key
        api_label = tk.Label(frame, text="OpenAI API Key:", bg='#2b2b2b', fg='white')
        api_label.pack(anchor=tk.W, padx=10, pady=5)
        
        api_entry = tk.Entry(frame, bg='#3c3c3c', fg='white', show='*')
        api_entry.pack(fill=tk.X, padx=10, pady=5)
        
    def _setup_neural_settings(self, frame):
        """Set up neural monitoring settings"""
        # Enable neural monitoring
        neural_var = tk.BooleanVar(value=True)
        neural_check = tk.Checkbutton(
            frame,
            text="Enable Neural Monitoring",
            variable=neural_var,
            bg='#2b2b2b',
            fg='white',
            selectcolor='#3c3c3c'
        )
        neural_check.pack(anchor=tk.W, padx=10, pady=5)
        
    def _update_internal_monologue_setting(self):
        """Update the internal monologue setting in main GUI"""
        if self.main_gui:
            self.main_gui.show_internal_monologue = self.internal_monologue_var.get()


if __name__ == "__main__":
    app = PhilosMainGUI()
    app.run()
