"""
Neural Web Dashboard
Real-time web interface for visualizing AI neural firing patterns
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import json
import time
import threading
from datetime import datetime
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.neural_monitor import get_neural_monitor
from neural_dashboard import create_neural_dashboard

app = Flask(__name__)
app.config['SECRET_KEY'] = 'neural_monitoring_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global dashboard instance
neural_dashboard = None
neural_monitor = None
monitoring_active = False

def initialize_dashboard():
    """Initialize the neural dashboard"""
    global neural_dashboard, neural_monitor
    neural_monitor = get_neural_monitor()
    neural_dashboard = create_neural_dashboard()
    print("🌐 Neural web dashboard initialized")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('neural_dashboard.html')

@app.route('/api/neural_state')
def get_neural_state():
    """Get current neural state"""
    if not neural_dashboard:
        return jsonify({'error': 'Dashboard not initialized'})
    
    try:
        state = neural_dashboard.get_real_time_neural_firing()
        return jsonify(state)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/visualization_data')
def get_visualization_data():
    """Get data for visualization"""
    if not neural_dashboard:
        return jsonify({'error': 'Dashboard not initialized'})
    
    try:
        data = neural_dashboard.get_neural_firing_visualization_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/neural_report')
def get_neural_report():
    """Get detailed neural report"""
    if not neural_monitor:
        return jsonify({'error': 'Monitor not initialized'})
    
    try:
        report = neural_monitor.get_detailed_neural_report()
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('👤 Client connected to neural dashboard')
    emit('status', {'message': 'Connected to neural monitoring system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('👤 Client disconnected from neural dashboard')

@socketio.on('start_monitoring')
def handle_start_monitoring():
    """Start real-time monitoring"""
    global monitoring_active
    monitoring_active = True
    emit('monitoring_started', {'status': 'active'})
    print('🔄 Real-time monitoring started')

@socketio.on('stop_monitoring')
def handle_stop_monitoring():
    """Stop real-time monitoring"""
    global monitoring_active
    monitoring_active = False
    emit('monitoring_stopped', {'status': 'inactive'})
    print('⏹️ Real-time monitoring stopped')

def background_monitoring():
    """Background thread for sending real-time updates"""
    while True:
        if monitoring_active and neural_dashboard:
            try:
                # Get current neural state
                state = neural_dashboard.get_real_time_neural_firing()
                
                # Send update to all connected clients
                socketio.emit('neural_update', state)
                
                # Check for new neural activity
                current_state = neural_monitor.get_current_neural_state()
                if current_state['computation_steps_count'] > 0:
                    socketio.emit('neural_activity', {
                        'timestamp': datetime.now().isoformat(),
                        'activity_detected': True,
                        'recent_computations': current_state['recent_computations']
                    })
                
            except Exception as e:
                print(f"Error in background monitoring: {e}")
        
        time.sleep(1)  # Update every second

def start_web_dashboard(host='127.0.0.1', port=5000, debug=False):
    """Start the web dashboard server"""
    initialize_dashboard()
    
    # Start background monitoring thread
    monitoring_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitoring_thread.start()
    
    print(f"🌐 Starting neural web dashboard at http://{host}:{port}")
    print("📊 Real-time neural firing visualization available")
    
    # Run the Flask-SocketIO server
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    start_web_dashboard(debug=True)
