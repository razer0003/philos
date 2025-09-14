"""
Real-time Neural Visualization Dashboard
Web-based interface for visualizing AI neural firing patterns in real-time
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import os
import sys

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.neural_monitor import get_neural_monitor
from src.neural_dashboard import create_neural_dashboard

class NeuralVisualizationServer(BaseHTTPRequestHandler):
    """HTTP server for neural visualization dashboard"""
    
    dashboard = None
    
    def do_GET(self):
        """Handle GET requests for the neural dashboard"""
        if self.path == '/':
            self.serve_dashboard_html()
        elif self.path == '/api/neural-state':
            self.serve_neural_state()
        elif self.path == '/api/visualization-data':
            self.serve_visualization_data()
        elif self.path == '/api/real-time-firing':
            self.serve_real_time_firing()
        elif self.path == '/style.css':
            self.serve_css()
        elif self.path == '/script.js':
            self.serve_js()
        else:
            self.send_error(404)
            
    def do_POST(self):
        """Handle POST requests for dashboard controls"""
        if self.path == '/api/clear-session':
            self.clear_neural_session()
        elif self.path == '/api/export-session':
            self.export_neural_session()
        else:
            self.send_error(404)
            
    def serve_dashboard_html(self):
        """Serve the main dashboard HTML"""
        html_content = self.get_dashboard_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
        
    def serve_neural_state(self):
        """Serve current neural state as JSON"""
        if not self.dashboard:
            self.dashboard = create_neural_dashboard()
            
        neural_state = self.dashboard.monitor.get_current_neural_state()
        self.send_json_response(neural_state)
        
    def serve_visualization_data(self):
        """Serve visualization data as JSON"""
        if not self.dashboard:
            self.dashboard = create_neural_dashboard()
            
        viz_data = self.dashboard.get_neural_firing_visualization_data()
        self.send_json_response(viz_data)
        
    def serve_real_time_firing(self):
        """Serve real-time neural firing data"""
        if not self.dashboard:
            self.dashboard = create_neural_dashboard()
            
        firing_data = self.dashboard.get_real_time_neural_firing()
        self.send_json_response(firing_data)
        
    def clear_neural_session(self):
        """Clear current neural session"""
        if self.dashboard:
            self.dashboard.clear_neural_history()
        self.send_json_response({'status': 'cleared'})
        
    def export_neural_session(self):
        """Export current neural session"""
        if not self.dashboard:
            self.dashboard = create_neural_dashboard()
            
        filename = self.dashboard.export_neural_session()
        self.send_json_response({'status': 'exported', 'filename': filename})
        
    def send_json_response(self, data):
        """Send JSON response with CORS headers"""
        json_data = json.dumps(data, default=str, indent=2)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_data.encode())
        
    def serve_css(self):
        """Serve CSS styles for the dashboard"""
        css_content = self.get_dashboard_css()
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(css_content.encode())
        
    def serve_js(self):
        """Serve JavaScript for the dashboard"""
        js_content = self.get_dashboard_js()
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        self.wfile.write(js_content.encode())
        
    def get_dashboard_html(self):
        """Generate the main dashboard HTML"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Neural State Monitor - Real-time Neural Firing Dashboard</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="dashboard">
        <header class="dashboard-header">
            <h1>🧠 AI Neural State Monitor</h1>
            <p>Real-time visualization of AI neural firing patterns and computational processes</p>
            <div class="controls">
                <button id="refreshBtn" class="btn btn-primary">🔄 Refresh</button>
                <button id="clearBtn" class="btn btn-warning">🗑️ Clear Session</button>
                <button id="exportBtn" class="btn btn-success">💾 Export Data</button>
                <label class="auto-refresh">
                    <input type="checkbox" id="autoRefresh" checked> Auto-refresh (2s)
                </label>
            </div>
        </header>
        
        <div class="dashboard-grid">
            <!-- Neural Firing Intensity -->
            <div class="panel firing-intensity">
                <h3>🔥 Neural Firing Intensity</h3>
                <div class="firing-bars">
                    <div class="firing-bar">
                        <span class="bar-label">Emotion</span>
                        <div class="bar-container">
                            <div class="bar emotion-bar" data-intensity="0"></div>
                        </div>
                        <span class="bar-value">0%</span>
                    </div>
                    <div class="firing-bar">
                        <span class="bar-label">Memory</span>
                        <div class="bar-container">
                            <div class="bar memory-bar" data-intensity="0"></div>
                        </div>
                        <span class="bar-value">0%</span>
                    </div>
                    <div class="firing-bar">
                        <span class="bar-label">Calculation</span>
                        <div class="bar-container">
                            <div class="bar calculation-bar" data-intensity="0"></div>
                        </div>
                        <span class="bar-value">0%</span>
                    </div>
                    <div class="firing-bar">
                        <span class="bar-label">Function</span>
                        <div class="bar-container">
                            <div class="bar function-bar" data-intensity="0"></div>
                        </div>
                        <span class="bar-value">0%</span>
                    </div>
                </div>
            </div>
            
            <!-- Emotional Activation -->
            <div class="panel emotional-state">
                <h3>❤️ Emotional Activation</h3>
                <div class="emotion-status">
                    <div class="status-indicator inactive" id="emotionStatus">INACTIVE</div>
                    <div class="emotion-intensity" id="emotionIntensity">0.000</div>
                </div>
                <div class="active-emotions" id="activeEmotions">
                    <p>No active emotions</p>
                </div>
            </div>
            
            <!-- Neural Coherence -->
            <div class="panel neural-coherence">
                <h3>🎯 Neural Coherence</h3>
                <div class="coherence-meter">
                    <div class="coherence-circle">
                        <span class="coherence-value" id="coherenceValue">0.000</span>
                    </div>
                    <div class="coherence-description" id="coherenceDesc">Initializing...</div>
                </div>
            </div>
            
            <!-- Computation Rate -->
            <div class="panel computation-rate">
                <h3>⚡ Computation Rate</h3>
                <div class="rate-display">
                    <span class="rate-value" id="rateValue">0.00</span>
                    <span class="rate-unit">ops/sec</span>
                </div>
                <div class="rate-trend" id="rateTrend">Monitoring...</div>
            </div>
            
            <!-- Memory Heat Map -->
            <div class="panel memory-heatmap">
                <h3>🗄️ Memory Activation Zones</h3>
                <div class="heatmap-grid" id="memoryHeatmap">
                    <div class="zone" data-zone="emotional">
                        <span class="zone-label">Emotional</span>
                        <div class="zone-intensity" data-intensity="0">0%</div>
                    </div>
                    <div class="zone" data-zone="interpersonal">
                        <span class="zone-label">Interpersonal</span>
                        <div class="zone-intensity" data-intensity="0">0%</div>
                    </div>
                    <div class="zone" data-zone="cognitive">
                        <span class="zone-label">Cognitive</span>
                        <div class="zone-intensity" data-intensity="0">0%</div>
                    </div>
                    <div class="zone" data-zone="self_concept">
                        <span class="zone-label">Self-Concept</span>
                        <div class="zone-intensity" data-intensity="0">0%</div>
                    </div>
                </div>
            </div>
            
            <!-- Recent Computations -->
            <div class="panel recent-computations">
                <h3>🔄 Recent Neural Activity</h3>
                <div class="computation-log" id="computationLog">
                    <p>No recent activity</p>
                </div>
            </div>
            
            <!-- Decision Pathways -->
            <div class="panel decision-pathways">
                <h3>🛤️ Decision Pathways</h3>
                <div class="pathway-list" id="pathwayList">
                    <p>No recent decisions</p>
                </div>
            </div>
            
            <!-- Trait Changes -->
            <div class="panel trait-changes">
                <h3>🔄 Personality Evolution</h3>
                <div class="trait-list" id="traitList">
                    <p>No recent changes</p>
                </div>
            </div>
        </div>
        
        <footer class="dashboard-footer">
            <p>Neural monitoring active • Last update: <span id="lastUpdate">Never</span></p>
            <p>Session: <span id="sessionId">Unknown</span></p>
        </footer>
    </div>
    
    <script src="/script.js"></script>
</body>
</html>
        '''
        
    def get_dashboard_css(self):
        """Generate CSS styles for the dashboard"""
        return '''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: #fff;
    min-height: 100vh;
}

.dashboard {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.dashboard-header {
    text-align: center;
    margin-bottom: 30px;
}

.dashboard-header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.dashboard-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 20px;
}

.controls {
    display: flex;
    justify-content: center;
    gap: 15px;
    flex-wrap: wrap;
    align-items: center;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.btn-primary { background: #007bff; color: white; }
.btn-warning { background: #ffc107; color: #212529; }
.btn-success { background: #28a745; color: white; }

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.auto-refresh {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.panel {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.panel h3 {
    margin-bottom: 15px;
    font-size: 1.2rem;
    text-align: center;
}

/* Firing Intensity Bars */
.firing-bars {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.firing-bar {
    display: flex;
    align-items: center;
    gap: 10px;
}

.bar-label {
    width: 80px;
    font-size: 0.9rem;
    font-weight: 600;
}

.bar-container {
    flex: 1;
    height: 20px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    overflow: hidden;
}

.bar {
    height: 100%;
    border-radius: 10px;
    transition: width 0.5s ease;
    background: linear-gradient(90deg, #ff6b6b, #ffa726);
}

.emotion-bar { background: linear-gradient(90deg, #ff6b6b, #ff8a80); }
.memory-bar { background: linear-gradient(90deg, #42a5f5, #64b5f6); }
.calculation-bar { background: linear-gradient(90deg, #66bb6a, #81c784); }
.function-bar { background: linear-gradient(90deg, #ab47bc, #ba68c8); }

.bar-value {
    width: 40px;
    text-align: right;
    font-weight: 600;
    font-size: 0.9rem;
}

/* Emotional State */
.emotion-status {
    text-align: center;
    margin-bottom: 15px;
}

.status-indicator {
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.status-indicator.active { background: #4caf50; }
.status-indicator.inactive { background: #757575; }
.status-indicator.low { background: #ff9800; }

.emotion-intensity {
    font-size: 2rem;
    font-weight: bold;
    color: #ff6b6b;
}

.active-emotions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.emotion-item {
    display: flex;
    justify-content: space-between;
    padding: 8px 12px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
}

/* Neural Coherence */
.coherence-meter {
    text-align: center;
}

.coherence-circle {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 8px solid rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px;
    position: relative;
}

.coherence-value {
    font-size: 1.8rem;
    font-weight: bold;
}

.coherence-description {
    font-size: 0.9rem;
    opacity: 0.8;
}

/* Memory Heatmap */
.heatmap-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.zone {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    transition: all 0.3s ease;
}

.zone-label {
    display: block;
    font-size: 0.8rem;
    margin-bottom: 8px;
    opacity: 0.9;
}

.zone-intensity {
    font-size: 1.2rem;
    font-weight: bold;
}

/* Activity Logs */
.computation-log, .pathway-list, .trait-list {
    max-height: 200px;
    overflow-y: auto;
    font-size: 0.9rem;
}

.log-item, .pathway-item, .trait-item {
    padding: 8px 12px;
    margin-bottom: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    border-left: 4px solid #42a5f5;
}

.trait-item.positive { border-left-color: #4caf50; }
.trait-item.negative { border-left-color: #f44336; }

.item-type {
    font-weight: 600;
    color: #81c784;
}

.item-details {
    font-size: 0.8rem;
    opacity: 0.9;
    margin-top: 4px;
}

/* Footer */
.dashboard-footer {
    text-align: center;
    padding: 20px;
    font-size: 0.9rem;
    opacity: 0.8;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
    .dashboard-grid {
        grid-template-columns: 1fr;
    }
    
    .dashboard-header h1 {
        font-size: 2rem;
    }
    
    .controls {
        flex-direction: column;
        gap: 10px;
    }
}

/* Animations */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.status-indicator.active {
    animation: pulse 2s infinite;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
}
        '''
        
    def get_dashboard_js(self):
        """Generate JavaScript for the dashboard"""
        return '''
class NeuralDashboard {
    constructor() {
        this.autoRefresh = true;
        this.refreshInterval = 2000; // 2 seconds
        this.refreshTimer = null;
        this.lastUpdateTime = null;
        
        this.initializeEventListeners();
        this.startAutoRefresh();
        this.refreshData();
    }
    
    initializeEventListeners() {
        // Refresh button
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
        });
        
        // Clear session button
        document.getElementById('clearBtn').addEventListener('click', () => {
            this.clearSession();
        });
        
        // Export button
        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportSession();
        });
        
        // Auto-refresh toggle
        const autoRefreshCheckbox = document.getElementById('autoRefresh');
        autoRefreshCheckbox.addEventListener('change', (e) => {
            this.autoRefresh = e.target.checked;
            if (this.autoRefresh) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });
    }
    
    startAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
        
        if (this.autoRefresh) {
            this.refreshTimer = setInterval(() => {
                this.refreshData();
            }, this.refreshInterval);
        }
    }
    
    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
        }
    }
    
    async refreshData() {
        try {
            const response = await fetch('/api/real-time-firing');
            const data = await response.json();
            
            this.updateDashboard(data);
            this.lastUpdateTime = new Date();
            document.getElementById('lastUpdate').textContent = this.lastUpdateTime.toLocaleTimeString();
            
        } catch (error) {
            console.error('Failed to refresh data:', error);
        }
    }
    
    updateDashboard(data) {
        this.updateFiringIntensity(data.firing_intensity || {});
        this.updateEmotionalState(data.emotional_activation || {});
        this.updateNeuralCoherence(data.neural_coherence || 0);
        this.updateComputationRate(data.computation_rate || 0);
        this.updateMemoryHeatmap(data.memory_heat_map || {});
        this.updateRecentActivity(data.raw_state || {});
        this.updateSessionInfo(data.raw_state || {});
    }
    
    updateFiringIntensity(firingIntensity) {
        const processTypes = ['emotion', 'memory', 'calculation', 'function'];
        
        processTypes.forEach(type => {
            const intensity = firingIntensity[type] || 0;
            const percentage = Math.round(intensity * 100);
            
            const bar = document.querySelector(`.${type}-bar`);
            const valueSpan = bar.parentElement.parentElement.querySelector('.bar-value');
            
            if (bar && valueSpan) {
                bar.style.width = `${percentage}%`;
                bar.setAttribute('data-intensity', intensity);
                valueSpan.textContent = `${percentage}%`;
            }
        });
    }
    
    updateEmotionalState(emotionalState) {
        const statusElement = document.getElementById('emotionStatus');
        const intensityElement = document.getElementById('emotionIntensity');
        const emotionsContainer = document.getElementById('activeEmotions');
        
        // Update status
        const status = emotionalState.status || 'inactive';
        statusElement.textContent = status.toUpperCase();
        statusElement.className = `status-indicator ${status}`;
        
        // Update intensity
        const intensity = emotionalState.emotional_intensity || 0;
        intensityElement.textContent = intensity.toFixed(3);
        
        // Update active emotions
        const activeEmotions = emotionalState.active_emotions || {};
        if (Object.keys(activeEmotions).length === 0) {
            emotionsContainer.innerHTML = '<p>No active emotions</p>';
        } else {
            emotionsContainer.innerHTML = Object.entries(activeEmotions)
                .map(([emotion, intensity]) => `
                    <div class="emotion-item">
                        <span>${emotion}</span>
                        <span>${intensity.toFixed(3)}</span>
                    </div>
                `).join('');
        }
    }
    
    updateNeuralCoherence(coherence) {
        const valueElement = document.getElementById('coherenceValue');
        const descElement = document.getElementById('coherenceDesc');
        
        valueElement.textContent = coherence.toFixed(3);
        
        let description;
        if (coherence >= 0.8) {
            description = 'Highly synchronized';
        } else if (coherence >= 0.6) {
            description = 'Well coordinated';
        } else if (coherence >= 0.4) {
            description = 'Moderately coherent';
        } else {
            description = 'Low coherence';
        }
        
        descElement.textContent = description;
        
        // Update circle color based on coherence
        const circle = document.querySelector('.coherence-circle');
        if (circle) {
            const hue = coherence * 120; // 0 = red, 120 = green
            circle.style.borderColor = `hsl(${hue}, 70%, 60%)`;
        }
    }
    
    updateComputationRate(rate) {
        const valueElement = document.getElementById('rateValue');
        const trendElement = document.getElementById('rateTrend');
        
        valueElement.textContent = rate.toFixed(2);
        
        let trend;
        if (rate > 1.0) {
            trend = 'High activity';
        } else if (rate > 0.1) {
            trend = 'Active processing';
        } else if (rate > 0.01) {
            trend = 'Low activity';
        } else {
            trend = 'Idle';
        }
        
        trendElement.textContent = trend;
    }
    
    updateMemoryHeatmap(heatMap) {
        const zones = ['emotional', 'interpersonal', 'cognitive', 'self_concept'];
        
        zones.forEach(zone => {
            const zoneElement = document.querySelector(`[data-zone="${zone}"]`);
            const intensityElement = zoneElement?.querySelector('.zone-intensity');
            
            if (intensityElement) {
                const zoneData = heatMap[zone] || { intensity: 0 };
                const intensity = zoneData.intensity || 0;
                const percentage = Math.round(intensity * 100);
                
                intensityElement.textContent = `${percentage}%`;
                intensityElement.setAttribute('data-intensity', intensity);
                
                // Update background color based on intensity
                const hue = 200 + (intensity * 60); // Blue to purple range
                const saturation = 50 + (intensity * 30);
                const lightness = 30 + (intensity * 20);
                zoneElement.style.background = `hsla(${hue}, ${saturation}%, ${lightness}%, 0.7)`;
            }
        });
    }
    
    updateRecentActivity(rawState) {
        this.updateComputationLog(rawState.recent_computations || []);
        this.updateDecisionPathways(rawState.recent_decisions || []);
        this.updateTraitChanges(rawState.recent_trait_changes || []);
    }
    
    updateComputationLog(computations) {
        const logContainer = document.getElementById('computationLog');
        
        if (computations.length === 0) {
            logContainer.innerHTML = '<p>No recent activity</p>';
            return;
        }
        
        logContainer.innerHTML = computations.map(comp => `
            <div class="log-item">
                <div class="item-type">${comp.step_name}</div>
                <div class="item-details">Type: ${comp.computation_type}</div>
            </div>
        `).join('');
    }
    
    updateDecisionPathways(decisions) {
        const pathwayContainer = document.getElementById('pathwayList');
        
        if (decisions.length === 0) {
            pathwayContainer.innerHTML = '<p>No recent decisions</p>';
            return;
        }
        
        pathwayContainer.innerHTML = decisions.map(decision => `
            <div class="pathway-item">
                <div class="item-type">${decision.decision_point}</div>
                <div class="item-details">Chose: ${decision.chosen_path}</div>
            </div>
        `).join('');
    }
    
    updateTraitChanges(traits) {
        const traitContainer = document.getElementById('traitList');
        
        if (traits.length === 0) {
            traitContainer.innerHTML = '<p>No recent changes</p>';
            return;
        }
        
        traitContainer.innerHTML = traits.map(trait => {
            const changeClass = trait.delta > 0 ? 'positive' : 'negative';
            const changeSymbol = trait.delta > 0 ? '+' : '';
            
            return `
                <div class="trait-item ${changeClass}">
                    <div class="item-type">${trait.trait_name}</div>
                    <div class="item-details">
                        ${trait.before_value.toFixed(3)} → ${trait.after_value.toFixed(3)} 
                        (${changeSymbol}${trait.delta.toFixed(3)})
                    </div>
                </div>
            `;
        }).join('');
    }
    
    updateSessionInfo(rawState) {
        const sessionElement = document.getElementById('sessionId');
        if (rawState.session_id) {
            sessionElement.textContent = rawState.session_id;
        }
    }
    
    async clearSession() {
        try {
            const response = await fetch('/api/clear-session', { method: 'POST' });
            const result = await response.json();
            
            if (result.status === 'cleared') {
                alert('Neural session cleared successfully!');
                this.refreshData();
            }
        } catch (error) {
            console.error('Failed to clear session:', error);
            alert('Failed to clear session');
        }
    }
    
    async exportSession() {
        try {
            const response = await fetch('/api/export-session', { method: 'POST' });
            const result = await response.json();
            
            if (result.status === 'exported') {
                alert(`Session exported to: ${result.filename}`);
            }
        } catch (error) {
            console.error('Failed to export session:', error);
            alert('Failed to export session');
        }
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new NeuralDashboard();
});
        '''

def start_neural_dashboard(port=8080):
    """Start the neural visualization dashboard server"""
    print(f"🧠 Starting Neural Visualization Dashboard on port {port}")
    
    # Set up the dashboard instance
    NeuralVisualizationServer.dashboard = create_neural_dashboard()
    
    # Create and start server
    server = HTTPServer(('localhost', port), NeuralVisualizationServer)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    print(f"✅ Dashboard server started!")
    print(f"🌐 Open your browser to: http://localhost:{port}")
    print(f"🔄 Auto-refresh every 2 seconds")
    print(f"⚡ Real-time neural firing visualization active")
    
    # Automatically open browser
    try:
        webbrowser.open(f'http://localhost:{port}')
        print(f"🚀 Browser opened automatically")
    except:
        print(f"💡 Manually open http://localhost:{port} in your browser")
    
    return server

def demo_web_dashboard():
    """Demonstrate the web-based neural dashboard"""
    print("=== Phase 3: Real-time Visualization Dashboard ===")
    
    # Start the server
    server = start_neural_dashboard(8080)
    
    print("\n📊 Dashboard Features:")
    print("  • Real-time neural firing intensity bars")
    print("  • Emotional activation monitoring")
    print("  • Neural coherence meter")
    print("  • Memory activation heat maps")
    print("  • Live computation rate tracking")
    print("  • Recent activity logs")
    print("  • Decision pathway visualization")
    print("  • Personality trait evolution")
    
    print("\n🎮 Dashboard Controls:")
    print("  • Auto-refresh toggle (2-second intervals)")
    print("  • Manual refresh button")
    print("  • Clear neural session")
    print("  • Export session data")
    
    print("\n🔧 Technical Details:")
    print("  • Web-based interface accessible via browser")
    print("  • RESTful API for neural state data")
    print("  • Real-time updates without page reload")
    print("  • Responsive design for mobile/desktop")
    print("  • Live visualization of computational processes")
    
    print(f"\n⚠️  Dashboard running - press Ctrl+C to stop")
    
    try:
        # Keep the demo running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n🛑 Stopping dashboard server...")
        server.shutdown()
        print(f"✅ Dashboard stopped")

if __name__ == "__main__":
    demo_web_dashboard()
