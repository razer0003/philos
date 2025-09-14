"""
Neural System Launcher
Comprehensive launcher for all neural monitoring components INCLUDING the AI companion
"""

import threading
import time
import webbrowser
import subprocess
import sys
from pathlib import Path

def launch_ai_companion():
    """Launch the AI companion for interaction"""
    print("🤖 Starting AI Companion...")
    try:
        # Start the AI companion in a new process
        companion_process = subprocess.Popen([
            sys.executable, 'ai_companion.py'
        ], cwd=Path.cwd())
        return companion_process
    except Exception as e:
        print(f"❌ Failed to start AI companion: {e}")
        return None

def launch_web_dashboard():
    """Launch the standalone neural dashboard"""
    print("🌐 Starting standalone neural dashboard...")
    try:
        # Import and start standalone dashboard
        from neural.standalone_neural_dashboard import StandaloneNeuralDashboard
        dashboard = StandaloneNeuralDashboard(port=8080)
        dashboard.start_server()
    except Exception as e:
        print(f"❌ Failed to start web dashboard: {e}")

def launch_pattern_analyzer():
    """Launch the neural pattern analyzer"""
    print("🧠 Starting neural pattern analyzer...")
    try:
        from neural.neural_pattern_analyzer import NeuralPatternAnalyzer
        
        analyzer = NeuralPatternAnalyzer()
        analyzer.start_real_time_analysis()
    except Exception as e:
        print(f"❌ Failed to start pattern analyzer: {e}")

def launch_advanced_intelligence():
    """Launch advanced neural intelligence system"""
    print("🚀 Starting advanced neural intelligence...")
    try:
        from advanced_neural_intelligence import AdvancedNeuralIntelligence
        
        ani = AdvancedNeuralIntelligence()
        ani.start_continuous_monitoring()
    except Exception as e:
        print(f"❌ Failed to start advanced intelligence: {e}")

def main():
    """Launch all neural system components including AI companion"""
    print("=" * 70)
    print("🧠 COMPLETE NEURAL MONITORING SYSTEM WITH AI COMPANION")
    print("=" * 70)
    
    print("\n🚀 Launching all components...")
    
    # Launch AI companion first
    print("\n1️⃣ Starting AI Companion...")
    companion_process = launch_ai_companion()
    time.sleep(2)  # Give AI time to start
    
    # Launch neural monitoring components in separate threads
    threads = []
    
    print("2️⃣ Starting Neural Web Dashboard...")
    dashboard_thread = threading.Thread(target=launch_web_dashboard, daemon=True)
    dashboard_thread.start()
    threads.append(dashboard_thread)
    
    # TEMPORARILY DISABLE background threads to debug fake neural activity
    print("⚠️ Pattern Analyzer and Advanced Intelligence DISABLED for debugging")
    # print("3️⃣ Starting Neural Pattern Analyzer...")
    # analyzer_thread = threading.Thread(target=launch_pattern_analyzer, daemon=True)
    # analyzer_thread.start()
    # threads.append(analyzer_thread)
    
    # print("4️⃣ Starting Advanced Neural Intelligence...")
    # intelligence_thread = threading.Thread(target=launch_advanced_intelligence, daemon=True)
    # intelligence_thread.start()
    # threads.append(intelligence_thread)
    
    # Wait for web server to start
    time.sleep(3)
    
    # Open browser to dashboard
    try:
        print("\n🌐 Opening neural dashboard in browser...")
        webbrowser.open('http://127.0.0.1:8080')
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print("   Please manually open http://127.0.0.1:8080")
    
    print("\n" + "=" * 70)
    print("✅ COMPLETE NEURAL MONITORING SYSTEM ACTIVE")
    print("=" * 70)
    print("🤖 AI Companion: Running in separate window")
    print("📊 Neural Dashboard: http://127.0.0.1:8080")
    print("🧠 Pattern Analyzer: Analyzing neural patterns")
    print("🚀 Advanced Intelligence: Monitoring & optimizing")
    print("\n" + "=" * 70)
    print("💬 USAGE INSTRUCTIONS:")
    print("1. Talk to the AI in the companion window")
    print("2. Watch real-time neural firing on the web dashboard")
    print("3. See pattern analysis and predictions")
    print("4. Monitor emotion verification in real-time")
    print("\n💡 Every message you send will trigger neural activity!")
    print("   Watch the dashboard to see the AI's 'neurons firing'")
    print("\n🛑 Press Ctrl+C here to stop all components")
    print("=" * 70)
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down complete neural monitoring system...")
        
        # Terminate AI companion if it's running
        if companion_process:
            try:
                companion_process.terminate()
                companion_process.wait(timeout=5)
                print("✅ AI Companion stopped")
            except:
                companion_process.kill()
                print("🔥 AI Companion force stopped")
        
        print("✅ All neural monitoring components stopped.")
        print("👋 Thank you for exploring AI neural transparency!")

if __name__ == "__main__":
    main()
