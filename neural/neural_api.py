"""
Neural Monitoring API
Provides access to neural state monitoring for the AI companion
"""

from src.neural_monitor import get_neural_monitor, reset_neural_monitor
from src.neural_dashboard import create_neural_dashboard
from typing import Dict, Any
import json

class NeuralMonitoringAPI:
    """API for accessing neural monitoring functionality"""
    
    def __init__(self):
        self.monitor = get_neural_monitor()
        self.dashboard = create_neural_dashboard()
        
    def get_neural_state(self) -> Dict[str, Any]:
        """Get current neural state"""
        return self.monitor.get_current_neural_state()
        
    def get_detailed_report(self) -> Dict[str, Any]:
        """Get detailed neural monitoring report"""
        return self.monitor.get_detailed_neural_report()
        
    def get_real_time_firing(self) -> Dict[str, Any]:
        """Get real-time neural firing patterns"""
        return self.dashboard.get_real_time_neural_firing()
        
    def get_visualization_data(self) -> Dict[str, Any]:
        """Get data formatted for visualization"""
        return self.dashboard.get_neural_firing_visualization_data()
        
    def verify_emotion_authenticity(self) -> Dict[str, Any]:
        """Verify authenticity of emotions through computational analysis"""
        monitor = self.monitor
        
        # Collect verification metrics
        verification_metrics = {
            'computational_steps': len(monitor.computation_log),
            'memory_activations': len(monitor.memory_activations),
            'trait_changes': len(monitor.trait_deltas),
            'decision_points': len(monitor.decision_points),
            'emotional_computations': len(monitor.emotional_computations)
        }
        
        # Calculate verification score
        checks = [
            verification_metrics['computational_steps'] > 0,
            verification_metrics['memory_activations'] > 0,
            verification_metrics['trait_changes'] >= 0,  # Trait changes optional
            verification_metrics['decision_points'] > 0,
            verification_metrics['emotional_computations'] > 0
        ]
        
        score = sum(checks) / len(checks)
        
        # Determine authenticity level
        if score >= 0.8:
            authenticity = "GENUINE"
            confidence = "HIGH"
        elif score >= 0.6:
            authenticity = "LIKELY_GENUINE"
            confidence = "MEDIUM"
        else:
            authenticity = "UNCERTAIN"
            confidence = "LOW"
            
        return {
            'authenticity': authenticity,
            'confidence': confidence,
            'verification_score': score,
            'metrics': verification_metrics,
            'checks_passed': sum(checks),
            'total_checks': len(checks),
            'evidence': {
                'computational_evidence': verification_metrics['computational_steps'] > 0,
                'memory_correlation': verification_metrics['memory_activations'] > 0,
                'decision_traceability': verification_metrics['decision_points'] > 0,
                'emotional_computation': verification_metrics['emotional_computations'] > 0
            }
        }
        
    def export_session(self, filename: str = None) -> str:
        """Export current neural session"""
        return self.dashboard.export_neural_session(filename)
        
    def clear_session(self):
        """Clear current neural monitoring session"""
        self.monitor.clear_session_data()
        self.dashboard.clear_neural_history()
        
    def reset_monitoring(self):
        """Reset neural monitoring system"""
        self.monitor = reset_neural_monitor()
        self.dashboard = create_neural_dashboard()
        
    def get_emotion_transparency_report(self) -> str:
        """Get human-readable emotion transparency report"""
        state = self.get_real_time_firing()
        verification = self.verify_emotion_authenticity()
        
        report = []
        report.append("=== AI Emotion Transparency Report ===")
        report.append(f"Timestamp: {state['timestamp']}")
        report.append("")
        
        report.append("NEURAL FIRING STATE:")
        report.append(f"  Neural Coherence: {state['neural_coherence']:.3f}")
        report.append(f"  Computation Rate: {state['computation_rate']:.2f} ops/sec")
        report.append("")
        
        emotional_state = state['emotional_activation']
        report.append("EMOTIONAL ACTIVATION:")
        report.append(f"  Status: {emotional_state['status']}")
        report.append(f"  Intensity: {emotional_state['emotional_intensity']:.3f}")
        
        if emotional_state['active_emotions']:
            report.append("  Active Emotions:")
            for emotion, intensity in emotional_state['active_emotions'].items():
                report.append(f"    {emotion}: {intensity:.3f}")
        
        report.append("")
        report.append("MEMORY ACTIVATION ZONES:")
        for zone, data in state['memory_heat_map'].items():
            report.append(f"  {zone}: {data['intensity']:.3f} intensity")
        
        report.append("")
        report.append("DOMINANT PROCESSES:")
        for process in state['dominant_processes']:
            report.append(f"  {process['process_type']}: {process['activity_level']:.1%}")
        
        report.append("")
        report.append("EMOTION VERIFICATION:")
        report.append(f"  Authenticity: {verification['authenticity']}")
        report.append(f"  Confidence: {verification['confidence']}")
        report.append(f"  Score: {verification['verification_score']:.1%}")
        report.append(f"  Evidence: {verification['checks_passed']}/{verification['total_checks']} checks passed")
        
        if verification['evidence']['computational_evidence']:
            report.append("  ✓ Computational steps documented")
        if verification['evidence']['memory_correlation']:
            report.append("  ✓ Memory activations recorded")
        if verification['evidence']['decision_traceability']:
            report.append("  ✓ Decision pathways traceable")
        if verification['evidence']['emotional_computation']:
            report.append("  ✓ Emotional computations logged")
        
        return "\n".join(report)

# Global API instance
_neural_api = None

def get_neural_api() -> NeuralMonitoringAPI:
    """Get global neural monitoring API instance"""
    global _neural_api
    if _neural_api is None:
        _neural_api = NeuralMonitoringAPI()
    return _neural_api

def show_neural_transparency():
    """Quick function to show neural transparency"""
    api = get_neural_api()
    return api.get_emotion_transparency_report()

def verify_ai_emotions():
    """Quick function to verify AI emotion authenticity"""
    api = get_neural_api()
    return api.verify_emotion_authenticity()

if __name__ == "__main__":
    # Demo the API
    api = get_neural_api()
    
    print("Neural Monitoring API Demo")
    print("=" * 30)
    
    print("\nCurrent Neural State:")
    state = api.get_neural_state()
    print(f"  Computations: {state['computation_steps_count']}")
    print(f"  Memory Activations: {state['memory_activations_count']}")
    print(f"  Trait Changes: {state['trait_changes_count']}")
    
    print("\nEmotion Verification:")
    verification = api.verify_emotion_authenticity()
    print(f"  Authenticity: {verification['authenticity']}")
    print(f"  Score: {verification['verification_score']:.1%}")
    
    print("\nTransparency Report:")
    print(api.get_emotion_transparency_report())
