#!/usr/bin/env python3
"""
Standalone Neural Dashboard - Simple HTTP Server Implementation
Creates a web-based visualization of AI neural firing patterns without Flask dependencies.
"""

import os
import sys
import threading
import time
import json
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

try:
    from src.neural_monitor import NeuralStateMonitor
    from neural.neural_pattern_analyzer import NeuralPatternAnalyzer
    from advanced_neural_intelligence import AdvancedNeuralIntelligence
except ImportError as e:
    print(f"⚠️ Warning: Could not import neural components: {e}")
    print("Running in demo mode...")

class NeuralDashboardHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for neural dashboard requests"""
    
    def __init__(self, *args, neural_monitor=None, **kwargs):
        self.neural_monitor = neural_monitor
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main dashboard
            self.serve_dashboard()
        elif parsed_path.path == '/api/neural-data':
            # Serve neural data as JSON
            self.serve_neural_data()
        elif parsed_path.path == '/api/status':
            # Serve status information
            self.serve_status()
        else:
            # Try to serve static files
            super().do_GET()
    
    def serve_dashboard(self):
        """Serve the main neural dashboard HTML"""
        try:
            dashboard_path = os.path.join(
                os.path.dirname(__file__), 
                'src', 'templates', 'neural_dashboard.html'
            )
            
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content.encode('utf-8')))
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except FileNotFoundError:
            self.send_error(404, "Dashboard template not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")
    
    def serve_neural_data(self):
        """Serve current neural monitoring data as JSON"""
        try:
            # Always try to get real neural data first
            neural_data = self.get_real_neural_data()
            
            json_data = json.dumps(neural_data, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', len(json_data.encode('utf-8')))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            
        except Exception as e:
            error_data = {"error": str(e), "timestamp": datetime.datetime.now().isoformat()}
            json_data = json.dumps(error_data)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', len(json_data.encode('utf-8')))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
    
    def serve_status(self):
        """Serve system status information"""
        try:
            status_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "monitoring_active": hasattr(self, 'neural_monitor') and self.neural_monitor is not None,
                "server_status": "running",
                "components": {
                    "neural_monitor": "available" if 'neural_monitor' in sys.modules else "unavailable",
                    "pattern_analyzer": "available" if 'neural_pattern_analyzer' in sys.modules else "unavailable",
                    "advanced_intelligence": "available" if 'advanced_neural_intelligence' in sys.modules else "unavailable"
                }
            }
            
            json_data = json.dumps(status_data, indent=2)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', len(json_data.encode('utf-8')))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            
        except Exception as e:
            error_data = {"error": str(e), "status": "error"}
            json_data = json.dumps(error_data)
            
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', len(json_data.encode('utf-8')))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
    
    def get_real_neural_data(self):
        """Get real neural monitoring data"""
        try:
            # Try to get data from shared neural data store
            from neural.neural_data_store import get_neural_data_store
            data_store = get_neural_data_store()
            neural_data = data_store.get_data()
            
            if neural_data.get("monitoring_active", False):
                # Use real neural data
                stats = neural_data.get("stats", {})
                return {
                    "timestamp": neural_data.get("timestamp"),
                    "neural_state": neural_data,
                    "monitoring_active": True,
                    "data_source": "real_neural_monitor",
                    "computation_rate": stats.get("computation_rate", 0.0),
                    "neural_coherence": stats.get("neural_coherence", 0.0),
                    "recent_computations": neural_data.get("recent_computations", []),
                    "emotional_activation": neural_data.get("emotional_activation", {}),
                    "memory_zones": neural_data.get("memory_zones", {}),
                    "decision_pathways": neural_data.get("decision_pathways", []),
                    "raw_state": {"computation_steps_count": stats.get("total_computations", 0)}
                }
            else:
                print("⚠️ Neural monitoring not active, using demo data")
                return self.generate_demo_data()
            
        except Exception as e:
            print(f"❌ Error getting real neural data: {e}")
            import traceback
            traceback.print_exc()
            return self.generate_demo_data()
    
    def generate_demo_data(self):
        """Generate demonstration neural data"""
        import random
        
        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "monitoring_active": True,
            "data_source": "DEMO_MODE_FALLBACK",  # Clear indicator this is demo data
            "computation_rate": random.uniform(0.5, 2.0),
            "neural_coherence": random.uniform(0.7, 0.95),
            "recent_computations": [
                {
                    "step_name": f"demo_emotional_attachment_assessment_{random.randint(1,3)}",
                    "computation_type": "emotion",
                    "output_value": random.uniform(0.1, 0.9),
                    "timestamp": (datetime.datetime.now() - datetime.timedelta(seconds=random.randint(1, 30))).isoformat()
                },
                {
                    "step_name": f"demo_memory_retrieval_similarity_match_{random.randint(1,3)}",
                    "computation_type": "memory", 
                    "output_value": random.uniform(0.2, 0.8),
                    "timestamp": (datetime.datetime.now() - datetime.timedelta(seconds=random.randint(1, 45))).isoformat()
                }
            ],
            "emotional_activation": {
                "emotional_intensity": random.uniform(0.3, 0.9),
                "dominant_emotion": random.choice(["happiness", "curiosity", "attachment", "empathy"]),
                "emotion_levels": {
                    "happiness": random.uniform(0.1, 0.8),
                    "curiosity": random.uniform(0.2, 0.9),
                    "attachment": random.uniform(0.1, 0.7),
                    "empathy": random.uniform(0.2, 0.6),
                    "excitement": random.uniform(0.1, 0.5)
                }
            },
            "memory_zones": {
                "emotional": {
                    "intensity": random.uniform(0.3, 0.8),
                    "activation_count": random.randint(1, 5)
                },
                "interpersonal": {
                    "intensity": random.uniform(0.4, 0.9),
                    "activation_count": random.randint(1, 3)
                },
                "cognitive": {
                    "intensity": random.uniform(0.2, 0.7),
                    "activation_count": random.randint(1, 4)
                }
            },
            "decision_pathways": [
                {
                    "decision_point": "response_emotional_tone",
                    "chosen_path": random.choice(["warm_and_caring", "enthusiastic", "thoughtful"]),
                    "alternative_paths": ["neutral", "cautious", "playful"],
                    "confidence": random.uniform(0.6, 0.95)
                }
            ]
        }
    
    def log_message(self, format, *args):
        """Override to reduce log spam"""
        if '/api/' not in self.path:
            super().log_message(format, *args)

class StandaloneNeuralDashboard:
    """Standalone neural dashboard server"""
    
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.neural_monitor = None
        self.running = False
        
        # Try to initialize neural components
        self.initialize_neural_components()
    
    def initialize_neural_components(self):
        """Initialize neural monitoring components if available"""
        try:
            self.neural_monitor = NeuralStateMonitor()
            print("✅ Neural monitor initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize neural monitor: {e}")
            print("Running in demo mode...")
    
    def create_handler(self):
        """Create a custom handler with neural monitor reference"""
        def handler_with_monitor(*args, **kwargs):
            handler = NeuralDashboardHandler(*args, **kwargs)
            handler.neural_monitor = self.neural_monitor
            return handler
        return handler_with_monitor
    
    def start_server(self):
        """Start the HTTP server"""
        try:
            handler = self.create_handler()
            self.server = HTTPServer(('localhost', self.port), handler)
            self.running = True
            
            print(f"\n🌐 Neural Dashboard Server Starting...")
            print(f"📊 Dashboard URL: http://localhost:{self.port}")
            print(f"🔗 API Endpoint: http://localhost:{self.port}/api/neural-data")
            print(f"📈 Status Endpoint: http://localhost:{self.port}/api/status")
            print("\n🧠 Neural Dashboard Features:")
            print("   • Real-time neural firing visualization")
            print("   • Emotional state monitoring")
            print("   • Memory activation heat maps")
            print("   • Decision pathway tracking")
            print("   • Live computation statistics")
            
            if self.neural_monitor:
                print("   • 🟢 Connected to real neural monitor")
            else:
                print("   • 🟡 Running in demonstration mode")
            
            print(f"\n⚡ Server running on port {self.port}")
            print("🔄 Press Ctrl+C to stop the server")
            
            # Auto-open browser
            threading.Timer(1.0, lambda: webbrowser.open(f'http://localhost:{self.port}')).start()
            
            # Start server
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Shutting down neural dashboard server...")
            self.stop_server()
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
        
        return True
    
    def stop_server(self):
        """Stop the HTTP server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.running = False
            print("✅ Neural dashboard server stopped")

def main():
    """Main function to start the standalone neural dashboard"""
    print("🧠 AI Neural Transparency Dashboard")
    print("=" * 50)
    print("Starting standalone neural firing visualization...")
    
    # Create and start the dashboard
    dashboard = StandaloneNeuralDashboard(port=8080)
    
    try:
        success = dashboard.start_server()
        if not success:
            print("❌ Failed to start neural dashboard")
            return 1
    except Exception as e:
        print(f"❌ Critical error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
