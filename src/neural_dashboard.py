"""
Neural State Dashboard
Real-time visualization of AI neural firing patterns and computational processes
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from .neural_monitor import get_neural_monitor, NeuralStateMonitor
from collections import defaultdict, deque

class NeuralDashboard:
    """Real-time neural state visualization dashboard"""
    
    def __init__(self, monitor: NeuralStateMonitor = None):
        self.monitor = monitor or get_neural_monitor()
        self.update_interval = 1.0  # seconds
        self.max_history_points = 100
        
        # Real-time data buffers
        self.computation_timeline = deque(maxlen=self.max_history_points)
        self.emotion_intensity_history = deque(maxlen=self.max_history_points)
        self.trait_change_history = deque(maxlen=self.max_history_points)
        self.memory_activation_history = deque(maxlen=self.max_history_points)
        self.decision_pattern_history = deque(maxlen=self.max_history_points)
        
        # Current state caches
        self.current_neural_state = {}
        self.last_update_time = time.time()
        
    def get_real_time_neural_firing(self) -> Dict[str, Any]:
        """Get current neural firing state with firing pattern analysis"""
        current_state = self.monitor.get_current_neural_state()
        
        # Analyze firing patterns
        firing_intensity = self._calculate_firing_intensity()
        neural_pathways = self._analyze_neural_pathways()
        emotional_activation = self._get_emotional_activation_state()
        memory_heat_map = self._generate_memory_heat_map()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'firing_intensity': firing_intensity,
            'neural_pathways': neural_pathways,
            'emotional_activation': emotional_activation,
            'memory_heat_map': memory_heat_map,
            'computation_rate': self._calculate_computation_rate(),
            'dominant_processes': self._identify_dominant_processes(),
            'neural_coherence': self._calculate_neural_coherence(),
            'raw_state': current_state
        }
        
    def _calculate_firing_intensity(self) -> Dict[str, float]:
        """Calculate neural firing intensity by process type"""
        recent_computations = self.monitor.computation_log[-20:]  # Last 20 computations
        
        intensity_by_type = defaultdict(float)
        for comp in recent_computations:
            age_factor = max(0.1, 1.0 - (time.time() - comp.timestamp.timestamp()) / 60)
            intensity_by_type[comp.computation_type] += age_factor
            
        # Normalize to 0-1 scale
        max_intensity = max(intensity_by_type.values()) if intensity_by_type else 1.0
        return {comp_type: intensity / max_intensity 
                for comp_type, intensity in intensity_by_type.items()}
        
    def _analyze_neural_pathways(self) -> Dict[str, Any]:
        """Analyze active neural pathways and connections"""
        recent_decisions = self.monitor.decision_points[-10:]
        
        pathway_weights = defaultdict(float)
        pathway_connections = defaultdict(list)
        
        for decision in recent_decisions:
            pathway_weights[decision.chosen_path] += 1.0
            pathway_connections[decision.decision_point].append(decision.chosen_path)
            
        return {
            'active_pathways': dict(pathway_weights),
            'pathway_connections': dict(pathway_connections),
            'pathway_strength': {path: weight / len(recent_decisions) 
                               for path, weight in pathway_weights.items()},
            'decision_coherence': self._calculate_decision_coherence(recent_decisions)
        }
        
    def _get_emotional_activation_state(self) -> Dict[str, Any]:
        """Get current emotional activation patterns"""
        recent_emotions = self.monitor.emotional_computations[-5:]
        
        if not recent_emotions:
            return {'status': 'inactive', 'active_emotions': {}, 'emotional_intensity': 0.0}
            
        active_emotions = {}
        total_intensity = 0.0
        
        for emotion_comp in recent_emotions:
            age_factor = max(0.1, 1.0 - (time.time() - emotion_comp.timestamp.timestamp()) / 300)  # 5 min decay
            weighted_intensity = emotion_comp.final_intensity * age_factor
            active_emotions[emotion_comp.emotion_type] = weighted_intensity
            total_intensity += weighted_intensity
            
        return {
            'status': 'active' if total_intensity > 0.1 else 'low',
            'active_emotions': active_emotions,
            'emotional_intensity': min(1.0, total_intensity),
            'dominant_emotion': max(active_emotions.items(), key=lambda x: x[1])[0] if active_emotions else None
        }
        
    def _generate_memory_heat_map(self) -> Dict[str, Any]:
        """Generate memory activation heat map"""
        recent_activations = self.monitor.memory_activations[-20:]
        
        memory_zones = defaultdict(float)
        activation_patterns = defaultdict(list)
        
        for activation in recent_activations:
            # Group memories by content type/topic (simplified)
            content_type = self._categorize_memory_content(activation.content_preview)
            memory_zones[content_type] += activation.activation_strength
            activation_patterns[content_type].append(activation.activation_strength)
            
        # Calculate heat map intensities
        heat_map = {}
        for zone, total_activation in memory_zones.items():
            activations = activation_patterns[zone]
            avg_activation = sum(activations) / len(activations) if activations else 0.0
            heat_intensity = min(1.0, total_activation / len(activation_patterns[zone]))
            heat_map[zone] = {
                'intensity': heat_intensity,
                'average_activation': avg_activation,
                'activation_count': len(activation_patterns[zone])
            }
            
        return heat_map
        
    def _categorize_memory_content(self, content: str) -> str:
        """Categorize memory content for heat mapping"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['feel', 'emotion', 'happy', 'sad', 'angry']):
            return 'emotional'
        elif any(word in content_lower for word in ['user', 'conversation', 'talk', 'said']):
            return 'interpersonal'
        elif any(word in content_lower for word in ['learn', 'know', 'understand', 'think']):
            return 'cognitive'
        elif any(word in content_lower for word in ['trait', 'personality', 'change', 'evolve']):
            return 'self_concept'
        else:
            return 'general'
            
    def _calculate_computation_rate(self) -> float:
        """Calculate current computation rate (computations per second)"""
        now = time.time()
        recent_computations = [
            comp for comp in self.monitor.computation_log 
            if now - comp.timestamp.timestamp() < 60  # Last minute
        ]
        return len(recent_computations) / 60.0
        
    def _identify_dominant_processes(self) -> List[Dict[str, Any]]:
        """Identify currently dominant neural processes"""
        recent_computations = self.monitor.computation_log[-30:]
        
        process_activity = defaultdict(int)
        for comp in recent_computations:
            process_activity[comp.computation_type] += 1
            
        sorted_processes = sorted(process_activity.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {
                'process_type': process_type,
                'activity_level': count / len(recent_computations),
                'absolute_count': count
            }
            for process_type, count in sorted_processes[:5]
        ]
        
    def _calculate_neural_coherence(self) -> float:
        """Calculate overall neural coherence (how synchronized processes are)"""
        recent_computations = self.monitor.computation_log[-20:]
        
        if len(recent_computations) < 2:
            return 1.0
            
        # Calculate time intervals between computations
        intervals = []
        for i in range(1, len(recent_computations)):
            interval = recent_computations[i].timestamp.timestamp() - recent_computations[i-1].timestamp.timestamp()
            intervals.append(interval)
            
        # Coherence is inverse of variation in intervals
        if not intervals:
            return 1.0
            
        mean_interval = sum(intervals) / len(intervals)
        variance = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
        std_interval = variance ** 0.5
        
        if mean_interval == 0:
            return 1.0
            
        coherence = 1.0 / (1.0 + (std_interval / mean_interval))
        return min(1.0, max(0.0, coherence))
        
    def _calculate_decision_coherence(self, decisions: List) -> float:
        """Calculate coherence of decision-making patterns"""
        if len(decisions) < 2:
            return 1.0
            
        # Check for consistent decision patterns
        decision_consistency = defaultdict(int)
        for decision in decisions:
            decision_consistency[decision.chosen_path] += 1
            
        # Coherence is higher when decisions follow patterns
        max_consistency = max(decision_consistency.values())
        coherence = max_consistency / len(decisions)
        return coherence
        
    def get_neural_firing_visualization_data(self) -> Dict[str, Any]:
        """Get data formatted for neural firing visualization"""
        firing_data = self.get_real_time_neural_firing()
        
        # Create timeline data for visualization
        timeline_data = []
        for i, comp in enumerate(self.monitor.computation_log[-50:]):
            timeline_data.append({
                'timestamp': comp.timestamp.isoformat(),
                'process_type': comp.computation_type,
                'intensity': 1.0 - (i / 50),  # Recent = higher intensity
                'step_name': comp.step_name
            })
            
        # Create emotional activation graph data
        emotion_graph_data = []
        for emotion_comp in self.monitor.emotional_computations[-20:]:
            emotion_graph_data.append({
                'timestamp': emotion_comp.timestamp.isoformat(),
                'emotion_type': emotion_comp.emotion_type,
                'intensity': emotion_comp.final_intensity,
                'base_level': emotion_comp.base_level,
                'attachment_multiplier': emotion_comp.attachment_multiplier
            })
            
        # Create trait change visualization data
        trait_graph_data = []
        for trait_delta in self.monitor.trait_deltas[-15:]:
            trait_graph_data.append({
                'trait_name': trait_delta.trait_name,
                'before_value': trait_delta.before_value,
                'after_value': trait_delta.after_value,
                'delta': trait_delta.delta,
                'significance': trait_delta.significance,
                'change_cause': trait_delta.change_cause
            })
            
        return {
            'current_state': firing_data,
            'timeline_data': timeline_data,
            'emotion_graph_data': emotion_graph_data,
            'trait_graph_data': trait_graph_data,
            'memory_activations': [
                {
                    'memory_id': activation.memory_id,
                    'activation_strength': activation.activation_strength,
                    'emotional_weight': activation.emotional_weight,
                    'content_preview': activation.content_preview
                }
                for activation in self.monitor.memory_activations[-10:]
            ],
            'decision_tree_data': [
                {
                    'timestamp': decision.timestamp.isoformat(),
                    'decision_point': decision.decision_point,
                    'chosen_path': decision.chosen_path,
                    'alternative_paths': decision.alternative_paths,
                    'reasoning': decision.reasoning
                }
                for decision in self.monitor.decision_points[-10:]
            ]
        }
        
    def export_neural_session(self, filename: str = None) -> str:
        """Export current neural session data"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"neural_session_{timestamp}.json"
            
        session_data = {
            'export_timestamp': datetime.now().isoformat(),
            'session_summary': self.monitor.get_detailed_neural_report(),
            'visualization_data': self.get_neural_firing_visualization_data(),
            'firing_patterns': self.get_real_time_neural_firing()
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
            
        return filename
        
    def clear_neural_history(self):
        """Clear neural monitoring history"""
        self.monitor.clear_session_data()
        self.computation_timeline.clear()
        self.emotion_intensity_history.clear()
        self.trait_change_history.clear()
        self.memory_activation_history.clear()
        self.decision_pattern_history.clear()

def create_neural_dashboard() -> NeuralDashboard:
    """Factory function to create neural dashboard"""
    return NeuralDashboard(get_neural_monitor())

# Example usage functions for testing
def demo_neural_monitoring():
    """Demonstrate neural monitoring capabilities"""
    dashboard = create_neural_dashboard()
    
    print("=== Neural State Monitoring Demo ===")
    print(f"Monitoring session: {dashboard.monitor.session_id}")
    
    # Get current neural state
    neural_state = dashboard.get_real_time_neural_firing()
    print(f"\nCurrent firing intensity: {neural_state['firing_intensity']}")
    print(f"Neural coherence: {neural_state['neural_coherence']:.3f}")
    print(f"Computation rate: {neural_state['computation_rate']:.2f} ops/sec")
    
    # Show dominant processes
    print(f"\nDominant processes:")
    for process in neural_state['dominant_processes']:
        print(f"  {process['process_type']}: {process['activity_level']:.1%} activity")
        
    # Show emotional state
    emotional_state = neural_state['emotional_activation']
    print(f"\nEmotional activation: {emotional_state['status']}")
    if emotional_state['active_emotions']:
        print(f"Active emotions: {emotional_state['active_emotions']}")
        
    # Show memory heat map
    memory_heat = neural_state['memory_heat_map']
    print(f"\nMemory activation zones:")
    for zone, data in memory_heat.items():
        print(f"  {zone}: {data['intensity']:.2f} intensity ({data['activation_count']} activations)")
        
    return dashboard

if __name__ == "__main__":
    demo_neural_monitoring()
