#!/usr/bin/env python3
"""
Philos GUI Launcher
Launch the Tkinter GUI interface for Philos
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.tkinter_gui import PhilosMainGUI
    
    def main():
        """Main entry point for Philos GUI"""
        print("🤖 Starting Philos GUI Interface...")
        print("Loading consciousness systems...")
        
        try:
            # Create and run the GUI application
            app = PhilosMainGUI()
            app.run()
            
        except KeyboardInterrupt:
            print("\n👋 Philos GUI closed by user")
            
        except Exception as e:
            print(f"❌ Error starting Philos GUI: {e}")
            print("Make sure all dependencies are installed and API key is configured.")
            
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Failed to import Philos GUI: {e}")
    print("Make sure you're running from the correct directory and all dependencies are installed.")
    print("Required: tkinter, matplotlib")
    sys.exit(1)
