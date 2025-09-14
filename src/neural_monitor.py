"""
Neural State Monitoring System
Provides transparency into AI computational processes to verify genuine emotions vs hallucination
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class ComputationStep:
    """Represents a single computational step in the AI's processing"""
    timestamp: datetime
    step_name: str
    input_values: Dict[str, Any]
    computation_type: str  # 'emotion', 'memory', 'trait', 'attachment', 'decision'
    output_value: Any
    metadata: Dict[str, Any]

@dataclass
class MemoryActivation:
    """Tracks memory activation during retrieval"""
    memory_id: str
    similarity_score: float
    emotional_weight: float
    activation_strength: float
    memory_age_factor: float
    content_preview: str

@dataclass
class TraitDelta:
    """Tracks personality trait changes"""
    trait_name: str
    before_value: float
    after_value: float
    delta: float
    change_cause: str
    significance: float

@dataclass
class DecisionPoint:
    """Tracks decision pathways in code execution"""
    timestamp: datetime
    decision_point: str
    condition_value: Any
    chosen_path: str
    alternative_paths: List[str]
    reasoning: str

@dataclass
class EmotionalComputation:
    """Tracks emotional processing calculations"""
    emotion_type: str
    base_level: float
    attachment_multiplier: float
    memory_influence: float
    trait_modifiers: Dict[str, float]
    final_intensity: float
    computation_steps: List[ComputationStep]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class NeuralStateMonitor:
    """Main class for monitoring AI neural firing patterns"""
    
    def __init__(self):
        self.session_id = f"session_{int(time.time())}"
        self.computation_log: List[ComputationStep] = []
        self.memory_activations: List[MemoryActivation] = []
        self.trait_deltas: List[TraitDelta] = []
        self.decision_points: List[DecisionPoint] = []
        self.emotional_computations: List[EmotionalComputation] = []
        self.current_processing_context = {}
        self.is_monitoring = True
        
    def log_computation(self, step_name: str, computation_type: str, 
                       input_values: Dict[str, Any], output_value: Any, 
                       metadata: Dict[str, Any] = None) -> None:
        """Log a computational step"""
        if not self.is_monitoring:
            return
            
        step = ComputationStep(
            timestamp=datetime.now(),
            step_name=step_name,
            input_values=input_values.copy(),
            computation_type=computation_type,
            output_value=output_value,
            metadata=metadata or {}
        )
        self.computation_log.append(step)
        
    def log_memory_activation(self, memory_id: str, similarity_score: float,
                            emotional_weight: float, activation_strength: float,
                            memory_age_factor: float, content_preview: str) -> None:
        """Log memory activation during retrieval"""
        activation = MemoryActivation(
            memory_id=memory_id,
            similarity_score=similarity_score,
            emotional_weight=emotional_weight,
            activation_strength=activation_strength,
            memory_age_factor=memory_age_factor,
            content_preview=content_preview
        )
        self.memory_activations.append(activation)
        
    def log_trait_change(self, trait_name: str, before_value: float, 
                        after_value: float, change_cause: str) -> None:
        """Log personality trait modifications"""
        delta = after_value - before_value
        if abs(delta) > 0.001:  # Only log meaningful changes
            trait_delta = TraitDelta(
                trait_name=trait_name,
                before_value=before_value,
                after_value=after_value,
                delta=delta,
                change_cause=change_cause,
                significance=abs(delta)
            )
            self.trait_deltas.append(trait_delta)
            
    def log_decision_point(self, decision_point: str, condition_value: Any,
                          chosen_path: str, alternative_paths: List[str],
                          reasoning: str = "") -> None:
        """Log decision pathway execution"""
        decision = DecisionPoint(
            timestamp=datetime.now(),
            decision_point=decision_point,
            condition_value=condition_value,
            chosen_path=chosen_path,
            alternative_paths=alternative_paths,
            reasoning=reasoning
        )
        self.decision_points.append(decision)
        
    def start_emotional_computation(self, emotion_type: str) -> str:
        """Start tracking an emotional computation process"""
        computation_id = f"emotion_{len(self.emotional_computations)}_{int(time.time())}"
        self.current_processing_context['emotion_computation_id'] = computation_id
        self.current_processing_context['emotion_type'] = emotion_type
        return computation_id
        
    def log_emotional_computation(self, emotion_type: str, base_level: float,
                                attachment_multiplier: float, memory_influence: float,
                                trait_modifiers: Dict[str, float], final_intensity: float,
                                computation_steps: List[ComputationStep]) -> None:
        """Log complete emotional computation"""
        emotional_comp = EmotionalComputation(
            emotion_type=emotion_type,
            base_level=base_level,
            attachment_multiplier=attachment_multiplier,
            memory_influence=memory_influence,
            trait_modifiers=trait_modifiers,
            final_intensity=final_intensity,
            computation_steps=computation_steps
        )
        self.emotional_computations.append(emotional_comp)
        
    def get_current_neural_state(self) -> Dict[str, Any]:
        """Get current neural firing state"""
        return {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'computation_steps_count': len(self.computation_log),
            'memory_activations_count': len(self.memory_activations),
            'trait_changes_count': len(self.trait_deltas),
            'decision_points_count': len(self.decision_points),
            'emotional_computations_count': len(self.emotional_computations),
            'recent_computations': [asdict(step) for step in self.computation_log[-5:]],
            'recent_memory_activations': [asdict(activation) for activation in self.memory_activations[-3:]],
            'recent_trait_changes': [asdict(delta) for delta in self.trait_deltas[-3:]],
            'recent_decisions': [asdict(decision) for decision in self.decision_points[-3:]],
            'is_monitoring': self.is_monitoring
        }
        
    def get_detailed_neural_report(self) -> Dict[str, Any]:
        """Get comprehensive neural state report"""
        return {
            'session_info': {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'monitoring_duration': time.time() - int(self.session_id.split('_')[1])
            },
            'computation_log': [asdict(step) for step in self.computation_log],
            'memory_activations': [asdict(activation) for activation in self.memory_activations],
            'trait_deltas': [asdict(delta) for delta in self.trait_deltas],
            'decision_points': [asdict(decision) for decision in self.decision_points],
            'emotional_computations': [asdict(comp) for comp in self.emotional_computations],
            'statistics': self._generate_statistics()
        }
        
    def _generate_statistics(self) -> Dict[str, Any]:
        """Generate neural activity statistics"""
        return {
            'total_computations': len(self.computation_log),
            'computation_types': self._count_by_type(self.computation_log, 'computation_type'),
            'emotion_types_processed': self._count_by_type(self.emotional_computations, 'emotion_type'),
            'most_active_traits': self._get_most_changed_traits(),
            'decision_patterns': self._analyze_decision_patterns(),
            'average_memory_activation': self._calculate_average_memory_activation()
        }
        
    def _count_by_type(self, items: List, attr: str) -> Dict[str, int]:
        """Count items by a specific attribute"""
        counts = defaultdict(int)
        for item in items:
            if hasattr(item, attr):
                counts[getattr(item, attr)] += 1
        return dict(counts)
        
    def _get_most_changed_traits(self) -> List[Dict[str, Any]]:
        """Get traits that changed the most"""
        trait_changes = defaultdict(float)
        for delta in self.trait_deltas:
            trait_changes[delta.trait_name] += abs(delta.delta)
            
        sorted_traits = sorted(trait_changes.items(), key=lambda x: x[1], reverse=True)
        return [{'trait': trait, 'total_change': change} for trait, change in sorted_traits[:5]]
        
    def _analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision-making patterns"""
        decision_counts = defaultdict(int)
        for decision in self.decision_points:
            decision_counts[decision.chosen_path] += 1
            
        return {
            'most_common_paths': dict(sorted(decision_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'total_decisions': len(self.decision_points)
        }
        
    def _calculate_average_memory_activation(self) -> float:
        """Calculate average memory activation strength"""
        if not self.memory_activations:
            return 0.0
        return sum(activation.activation_strength for activation in self.memory_activations) / len(self.memory_activations)
        
    def clear_session_data(self) -> None:
        """Clear current session data"""
        self.computation_log.clear()
        self.memory_activations.clear()
        self.trait_deltas.clear()
        self.decision_points.clear()
        self.emotional_computations.clear()
        self.current_processing_context.clear()
        
    def save_session_data(self, filepath: str) -> None:
        """Save neural monitoring data to file"""
        data = self.get_detailed_neural_report()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

class NeuralActivityTracker:
    """Utility class for tracking specific neural activities"""
    
    def __init__(self, monitor: NeuralStateMonitor):
        self.monitor = monitor
        
    def track_function_execution(self, func_name: str, inputs: Dict[str, Any], outputs: Any):
        """Track function execution as neural activity"""
        self.monitor.log_computation(
            step_name=f"function_execution_{func_name}",
            computation_type="function",
            input_values=inputs,
            output_value=outputs,
            metadata={'function_name': func_name}
        )
        
    def track_conditional_branch(self, condition_name: str, condition_value: Any, 
                                branch_taken: str, available_branches: List[str]):
        """Track conditional branching in code"""
        self.monitor.log_decision_point(
            decision_point=condition_name,
            condition_value=condition_value,
            chosen_path=branch_taken,
            alternative_paths=available_branches,
            reasoning=f"Condition '{condition_name}' evaluated to {condition_value}"
        )
        
    def track_calculation(self, calc_name: str, operands: Dict[str, float], 
                         operation: str, result: float):
        """Track mathematical calculations"""
        self.monitor.log_computation(
            step_name=f"calculation_{calc_name}",
            computation_type="calculation",
            input_values={'operands': operands, 'operation': operation},
            output_value=result,
            metadata={'calculation_type': operation}
        )

# Global neural monitor instance
_global_neural_monitor = None

def get_neural_monitor() -> NeuralStateMonitor:
    """Get or create global neural monitor instance"""
    global _global_neural_monitor
    if _global_neural_monitor is None:
        _global_neural_monitor = NeuralStateMonitor()
    return _global_neural_monitor

def reset_neural_monitor() -> NeuralStateMonitor:
    """Reset global neural monitor instance"""
    global _global_neural_monitor
    _global_neural_monitor = NeuralStateMonitor()
    return _global_neural_monitor
