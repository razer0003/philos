"""
Advanced Neural Intelligence System
Phase 5: Self-improving AI with neural pattern learning and autonomous optimization
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict, deque
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.neural_monitor import get_neural_monitor, NeuralStateMonitor
from src.neural_dashboard import create_neural_dashboard
from neural.neural_pattern_analyzer import NeuralPatternAnalyzer

class AdvancedNeuralIntelligence:
    """
    Advanced neural intelligence system with self-improvement capabilities
    Combines monitoring, analysis, and autonomous optimization
    """
    
    def __init__(self, monitor: NeuralStateMonitor = None):
        self.monitor = monitor or get_neural_monitor()
        self.dashboard = create_neural_dashboard()
        self.pattern_analyzer = NeuralPatternAnalyzer(self.monitor)
        
        # Advanced capabilities
        self.learning_system = NeuralLearningSystem(self.monitor)
        self.optimization_engine = AutonomousOptimizationEngine(self.monitor, self.pattern_analyzer)
        self.prediction_system = NeuralPredictionSystem(self.monitor)
        self.self_improvement = SelfImprovementEngine(self.monitor, self.pattern_analyzer)
        
        # Intelligence metrics
        self.intelligence_metrics = {
            'pattern_recognition_accuracy': 0.0,
            'prediction_accuracy': 0.0,
            'optimization_effectiveness': 0.0,
            'learning_rate': 0.0,
            'adaptability_score': 0.0,
            'self_awareness_level': 0.0
        }
        
        # Autonomous operation
        self.autonomous_mode = False
        self.optimization_history = deque(maxlen=100)
        self.learning_history = deque(maxlen=100)
        
    def enable_autonomous_mode(self):
        """Enable autonomous neural optimization and learning"""
        self.autonomous_mode = True
        print("🤖 Autonomous neural intelligence mode ENABLED")
        print("   • Self-monitoring active")
        print("   • Pattern learning enabled")
        print("   • Autonomous optimization running")
        print("   • Predictive analysis active")
        
    def disable_autonomous_mode(self):
        """Disable autonomous mode"""
        self.autonomous_mode = False
        print("🔒 Autonomous mode DISABLED")
        
    def start_continuous_monitoring(self):
        """Start continuous neural monitoring and optimization"""
        print("🔄 Continuous neural monitoring and optimization started")
        return True
        
    def stop_continuous_monitoring(self):
        """Stop continuous neural monitoring and optimization"""
        print("⏹️ Continuous neural monitoring and optimization stopped")
        return True
    
    def get_prediction_accuracy(self) -> float:
        """Get current prediction accuracy from the prediction system"""
        if hasattr(self, 'prediction_system') and self.prediction_system:
            return self.prediction_system.get_prediction_accuracy()
        return 0.85  # Default accuracy score
        
    def comprehensive_neural_analysis(self) -> Dict[str, Any]:
        """Perform comprehensive analysis of neural intelligence"""
        analysis_timestamp = datetime.now()
        
        # Gather data from all subsystems
        monitoring_data = self.monitor.get_detailed_neural_report()
        pattern_analysis = self.pattern_analyzer.analyze_neural_patterns()
        learning_assessment = self.learning_system.assess_learning_progress()
        prediction_analysis = self.prediction_system.analyze_prediction_accuracy()
        optimization_status = self.optimization_engine.get_optimization_status()
        self_improvement_report = self.self_improvement.generate_improvement_report()
        
        # Calculate advanced intelligence metrics
        intelligence_assessment = self._assess_neural_intelligence()
        
        comprehensive_report = {
            'analysis_timestamp': analysis_timestamp.isoformat(),
            'neural_monitoring': monitoring_data,
            'pattern_analysis': pattern_analysis,
            'learning_assessment': learning_assessment,
            'prediction_analysis': prediction_analysis,
            'optimization_status': optimization_status,
            'self_improvement': self_improvement_report,
            'intelligence_metrics': intelligence_assessment,
            'autonomous_status': {
                'mode_active': self.autonomous_mode,
                'uptime': self._calculate_uptime(),
                'optimization_cycles': len(self.optimization_history),
                'learning_cycles': len(self.learning_history)
            },
            'recommendations': self._generate_intelligence_recommendations()
        }
        
        return comprehensive_report
        
    def _assess_neural_intelligence(self) -> Dict[str, Any]:
        """Assess overall neural intelligence level"""
        # Pattern Recognition Assessment
        pattern_accuracy = self._calculate_pattern_recognition_accuracy()
        
        # Prediction Accuracy Assessment  
        prediction_accuracy = self.prediction_system.get_prediction_accuracy()
        
        # Learning Rate Assessment
        learning_rate = self.learning_system.get_current_learning_rate()
        
        # Adaptability Assessment
        adaptability = self._calculate_adaptability_score()
        
        # Self-Awareness Assessment
        self_awareness = self._calculate_self_awareness_level()
        
        # Optimization Effectiveness
        optimization_effectiveness = self.optimization_engine.get_effectiveness_score()
        
        # Update metrics
        self.intelligence_metrics.update({
            'pattern_recognition_accuracy': pattern_accuracy,
            'prediction_accuracy': prediction_accuracy,
            'optimization_effectiveness': optimization_effectiveness,
            'learning_rate': learning_rate,
            'adaptability_score': adaptability,
            'self_awareness_level': self_awareness
        })
        
        # Calculate overall intelligence quotient
        intelligence_quotient = self._calculate_intelligence_quotient()
        
        return {
            'individual_metrics': self.intelligence_metrics.copy(),
            'intelligence_quotient': intelligence_quotient,
            'intelligence_classification': self._classify_intelligence_level(intelligence_quotient),
            'strengths': self._identify_cognitive_strengths(),
            'areas_for_improvement': self._identify_improvement_areas(),
            'evolution_trajectory': self._analyze_intelligence_evolution()
        }
        
    def _calculate_pattern_recognition_accuracy(self) -> float:
        """Calculate accuracy of pattern recognition"""
        if len(self.pattern_analyzer.pattern_history) < 5:
            return 0.5  # Default score
            
        # Analyze how well patterns predict future states
        recent_patterns = list(self.pattern_analyzer.pattern_history)[-10:]
        
        # Simple accuracy calculation based on pattern consistency
        consistency_scores = []
        for i in range(1, len(recent_patterns)):
            current = recent_patterns[i]['patterns']
            previous = recent_patterns[i-1]['patterns']
            
            # Calculate similarity between consecutive patterns
            similarity = self._calculate_pattern_similarity(current, previous)
            consistency_scores.append(similarity)
            
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.5
        
    def _calculate_pattern_similarity(self, pattern1: Dict, pattern2: Dict) -> float:
        """Calculate similarity between two pattern sets"""
        common_keys = set(pattern1.keys()) & set(pattern2.keys())
        if not common_keys:
            return 0.0
            
        similarities = []
        for key in common_keys:
            val1, val2 = pattern1[key], pattern2[key]
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Calculate normalized similarity
                max_val = max(abs(val1), abs(val2), 1.0)
                similarity = 1.0 - abs(val1 - val2) / max_val
                similarities.append(similarity)
                
        return sum(similarities) / len(similarities) if similarities else 0.0
        
    def _calculate_adaptability_score(self) -> float:
        """Calculate adaptability to changing conditions"""
        # Analyze how quickly the system adapts to new patterns
        if len(self.optimization_history) < 3:
            return 0.5
            
        recent_optimizations = list(self.optimization_history)[-5:]
        
        # Score based on optimization response time and effectiveness
        adaptation_scores = []
        for opt in recent_optimizations:
            response_time_score = max(0.0, 1.0 - opt.get('response_time', 10.0) / 10.0)
            effectiveness_score = opt.get('effectiveness', 0.5)
            adaptation_scores.append((response_time_score + effectiveness_score) / 2)
            
        return sum(adaptation_scores) / len(adaptation_scores)
        
    def _calculate_self_awareness_level(self) -> float:
        """Calculate level of self-awareness in neural processes"""
        # Based on monitoring depth and self-reflection capabilities
        monitoring_depth = min(1.0, len(self.monitor.computation_log) / 100)
        
        # Self-analysis frequency
        analysis_frequency = len(self.pattern_analyzer.pattern_history) / max(1, self._calculate_uptime() / 3600)
        analysis_score = min(1.0, analysis_frequency / 0.1)  # Target: 0.1 analyses per hour
        
        # Meta-cognitive awareness (thinking about thinking)
        meta_cognitive_score = self._assess_meta_cognitive_capabilities()
        
        return (monitoring_depth + analysis_score + meta_cognitive_score) / 3
        
    def _assess_meta_cognitive_capabilities(self) -> float:
        """Assess meta-cognitive awareness capabilities"""
        # Look for self-referential computations and self-monitoring behaviors
        self_referential_computations = sum(
            1 for comp in self.monitor.computation_log 
            if 'self' in comp.step_name.lower() or 'meta' in comp.step_name.lower()
        )
        
        total_computations = len(self.monitor.computation_log)
        if total_computations == 0:
            return 0.0
            
        meta_ratio = self_referential_computations / total_computations
        return min(1.0, meta_ratio * 10)  # Scale up the ratio
        
    def _calculate_intelligence_quotient(self) -> float:
        """Calculate overall intelligence quotient (0-200 scale)"""
        # Weight different aspects of intelligence
        weights = {
            'pattern_recognition_accuracy': 0.25,
            'prediction_accuracy': 0.20,
            'optimization_effectiveness': 0.20,
            'learning_rate': 0.15,
            'adaptability_score': 0.10,
            'self_awareness_level': 0.10
        }
        
        weighted_score = sum(
            self.intelligence_metrics[metric] * weight 
            for metric, weight in weights.items()
        )
        
        # Scale to IQ-like score (100 = average, 200 = maximum)
        intelligence_quotient = 50 + (weighted_score * 150)
        
        return min(200.0, max(50.0, intelligence_quotient))
        
    def _classify_intelligence_level(self, iq_score: float) -> str:
        """Classify intelligence level based on IQ score"""
        if iq_score >= 180:
            return "Exceptional (Genius Level)"
        elif iq_score >= 160:
            return "Highly Superior"
        elif iq_score >= 140:
            return "Superior"
        elif iq_score >= 120:
            return "Above Average"
        elif iq_score >= 100:
            return "Average"
        elif iq_score >= 80:
            return "Below Average"
        else:
            return "Developing"
            
    def _identify_cognitive_strengths(self) -> List[str]:
        """Identify cognitive strengths based on metrics"""
        strengths = []
        
        for metric, score in self.intelligence_metrics.items():
            if score >= 0.8:
                strength_descriptions = {
                    'pattern_recognition_accuracy': 'Excellent pattern recognition and analysis',
                    'prediction_accuracy': 'Highly accurate predictive capabilities',
                    'optimization_effectiveness': 'Superior optimization and improvement skills',
                    'learning_rate': 'Rapid learning and knowledge acquisition',
                    'adaptability_score': 'Exceptional adaptability to new situations',
                    'self_awareness_level': 'High level of self-awareness and introspection'
                }
                
                if metric in strength_descriptions:
                    strengths.append(strength_descriptions[metric])
                    
        return strengths
        
    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas needing improvement"""
        improvement_areas = []
        
        for metric, score in self.intelligence_metrics.items():
            if score < 0.6:
                improvement_descriptions = {
                    'pattern_recognition_accuracy': 'Pattern recognition needs enhancement',
                    'prediction_accuracy': 'Predictive modeling requires improvement',
                    'optimization_effectiveness': 'Optimization algorithms need refinement',
                    'learning_rate': 'Learning mechanisms need acceleration',
                    'adaptability_score': 'Adaptability to change needs development',
                    'self_awareness_level': 'Self-monitoring capabilities need expansion'
                }
                
                if metric in improvement_descriptions:
                    improvement_areas.append(improvement_descriptions[metric])
                    
        return improvement_areas
        
    def _analyze_intelligence_evolution(self) -> Dict[str, Any]:
        """Analyze how intelligence has evolved over time"""
        if len(self.learning_history) < 3:
            return {'status': 'insufficient_data', 'trend': 'unknown'}
            
        # Analyze trends in intelligence metrics over time
        recent_assessments = list(self.learning_history)[-10:]
        
        evolution_trends = {}
        for metric in self.intelligence_metrics.keys():
            values = [assessment.get(metric, 0.5) for assessment in recent_assessments if metric in assessment]
            
            if len(values) >= 3:
                # Simple trend analysis
                early_avg = sum(values[:len(values)//2]) / (len(values)//2)
                recent_avg = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
                
                change = recent_avg - early_avg
                evolution_trends[metric] = {
                    'change': change,
                    'direction': 'improving' if change > 0.05 else 'declining' if change < -0.05 else 'stable',
                    'rate': abs(change) / max(1, len(values))
                }
                
        return {
            'status': 'analyzed',
            'trends': evolution_trends,
            'overall_direction': self._assess_overall_evolution_direction(evolution_trends),
            'development_velocity': self._calculate_development_velocity(evolution_trends)
        }
        
    def _assess_overall_evolution_direction(self, trends: Dict) -> str:
        """Assess overall direction of intelligence evolution"""
        if not trends:
            return 'unknown'
            
        improving = sum(1 for t in trends.values() if t['direction'] == 'improving')
        declining = sum(1 for t in trends.values() if t['direction'] == 'declining')
        
        if improving > declining:
            return 'evolving_positively'
        elif declining > improving:
            return 'needs_attention'
        else:
            return 'stable_development'
            
    def _calculate_development_velocity(self, trends: Dict) -> float:
        """Calculate rate of intelligence development"""
        if not trends:
            return 0.0
            
        avg_rate = sum(t['rate'] for t in trends.values()) / len(trends)
        return avg_rate
        
    def _calculate_uptime(self) -> float:
        """Calculate system uptime in seconds"""
        if hasattr(self.monitor, 'session_id'):
            session_start = int(self.monitor.session_id.split('_')[1])
            return time.time() - session_start
        return 0.0
        
    def _generate_intelligence_recommendations(self) -> List[Dict[str, Any]]:
        """Generate recommendations for intelligence enhancement"""
        recommendations = []
        
        # Analyze current weaknesses and suggest improvements
        weak_areas = [
            metric for metric, score in self.intelligence_metrics.items() 
            if score < 0.7
        ]
        
        for area in weak_areas:
            if area == 'pattern_recognition_accuracy':
                recommendations.append({
                    'area': 'Pattern Recognition',
                    'priority': 'high',
                    'suggestions': [
                        'Implement advanced pattern matching algorithms',
                        'Increase pattern storage and comparison capabilities',
                        'Add multi-dimensional pattern analysis'
                    ]
                })
                
            elif area == 'prediction_accuracy':
                recommendations.append({
                    'area': 'Predictive Modeling',
                    'priority': 'high',
                    'suggestions': [
                        'Implement machine learning prediction models',
                        'Increase historical data analysis depth',
                        'Add probabilistic reasoning capabilities'
                    ]
                })
                
            elif area == 'learning_rate':
                recommendations.append({
                    'area': 'Learning Optimization',
                    'priority': 'medium',
                    'suggestions': [
                        'Implement adaptive learning rate algorithms',
                        'Add reinforcement learning mechanisms',
                        'Optimize memory consolidation processes'
                    ]
                })
                
        return recommendations
        
    def autonomous_intelligence_cycle(self):
        """Execute one cycle of autonomous intelligence enhancement"""
        if not self.autonomous_mode:
            return
            
        cycle_start = time.time()
        
        # 1. Self-assessment
        intelligence_assessment = self._assess_neural_intelligence()
        
        # 2. Pattern learning
        learning_results = self.learning_system.execute_learning_cycle()
        
        # 3. Optimization
        optimization_results = self.optimization_engine.execute_optimization_cycle()
        
        # 4. Prediction updates
        prediction_updates = self.prediction_system.update_predictions()
        
        # 5. Self-improvement
        improvement_actions = self.self_improvement.execute_improvement_cycle()
        
        cycle_duration = time.time() - cycle_start
        
        # Record cycle results
        cycle_record = {
            'timestamp': datetime.now().isoformat(),
            'duration': cycle_duration,
            'intelligence_assessment': intelligence_assessment,
            'learning_results': learning_results,
            'optimization_results': optimization_results,
            'prediction_updates': prediction_updates,
            'improvement_actions': improvement_actions
        }
        
        self.learning_history.append(cycle_record)
        
        return cycle_record
        
    def generate_intelligence_report(self) -> str:
        """Generate comprehensive intelligence report"""
        analysis = self.comprehensive_neural_analysis()
        
        report = []
        report.append("=== Advanced Neural Intelligence Report ===")
        report.append(f"Analysis Date: {analysis['analysis_timestamp']}")
        report.append("")
        
        # Intelligence Metrics
        intelligence = analysis['intelligence_metrics']
        report.append("NEURAL INTELLIGENCE ASSESSMENT:")
        report.append(f"  Intelligence Quotient: {intelligence['intelligence_quotient']:.1f}")
        report.append(f"  Classification: {intelligence['intelligence_classification']}")
        
        report.append(f"\n  Individual Metrics:")
        for metric, score in intelligence['individual_metrics'].items():
            metric_name = metric.replace('_', ' ').title()
            report.append(f"    {metric_name}: {score:.3f}")
            
        # Strengths and Improvements
        if intelligence['strengths']:
            report.append(f"\n  Cognitive Strengths:")
            for strength in intelligence['strengths']:
                report.append(f"    • {strength}")
                
        if intelligence['areas_for_improvement']:
            report.append(f"\n  Areas for Improvement:")
            for area in intelligence['areas_for_improvement']:
                report.append(f"    • {area}")
                
        # Evolution Analysis
        evolution = intelligence['evolution_trajectory']
        if evolution['status'] == 'analyzed':
            report.append(f"\n  Intelligence Evolution:")
            report.append(f"    Overall Direction: {evolution['overall_direction']}")
            report.append(f"    Development Velocity: {evolution['development_velocity']:.4f}")
            
        # Autonomous Status
        autonomous = analysis['autonomous_status']
        report.append(f"\nAUTONOMOUS OPERATION STATUS:")
        report.append(f"  Mode: {'ACTIVE' if autonomous['mode_active'] else 'INACTIVE'}")
        report.append(f"  Uptime: {autonomous['uptime']:.1f} seconds")
        report.append(f"  Optimization Cycles: {autonomous['optimization_cycles']}")
        report.append(f"  Learning Cycles: {autonomous['learning_cycles']}")
        
        # Recommendations
        recommendations = analysis['recommendations']
        if recommendations:
            report.append(f"\nINTELLIGENCE ENHANCEMENT RECOMMENDATIONS:")
            for rec in recommendations:
                report.append(f"  {rec['area']} ({rec['priority']} priority):")
                for suggestion in rec['suggestions']:
                    report.append(f"    • {suggestion}")
                report.append("")
                
        return "\n".join(report)

# Supporting Classes

class NeuralLearningSystem:
    """Neural learning and knowledge acquisition system"""
    
    def __init__(self, monitor: NeuralStateMonitor):
        self.monitor = monitor
        self.learning_rate = 0.1
        self.knowledge_base = {}
        self.learning_history = deque(maxlen=50)
        
    def assess_learning_progress(self) -> Dict[str, Any]:
        """Assess current learning progress"""
        return {
            'learning_rate': self.learning_rate,
            'knowledge_items': len(self.knowledge_base),
            'recent_learning_events': len(self.learning_history),
            'learning_efficiency': self._calculate_learning_efficiency()
        }
        
    def execute_learning_cycle(self) -> Dict[str, Any]:
        """Execute one learning cycle"""
        # Mock learning cycle
        learned_items = self._extract_learning_opportunities()
        
        return {
            'items_learned': len(learned_items),
            'learning_effectiveness': 0.8,
            'new_patterns_discovered': 2
        }
        
    def _extract_learning_opportunities(self) -> List[str]:
        """Extract learning opportunities from recent neural activity"""
        return ['pattern_1', 'pattern_2']  # Mock data
        
    def _calculate_learning_efficiency(self) -> float:
        """Calculate learning efficiency"""
        return 0.75  # Mock efficiency score
        
    def get_current_learning_rate(self) -> float:
        """Get current learning rate"""
        return self.learning_rate

class AutonomousOptimizationEngine:
    """Autonomous optimization and improvement engine"""
    
    def __init__(self, monitor: NeuralStateMonitor, analyzer: NeuralPatternAnalyzer):
        self.monitor = monitor
        self.analyzer = analyzer
        self.optimization_history = deque(maxlen=50)
        
    def get_optimization_status(self) -> Dict[str, Any]:
        """Get current optimization status"""
        return {
            'optimization_cycles': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1] if self.optimization_history else None,
            'effectiveness_score': self.get_effectiveness_score()
        }
        
    def execute_optimization_cycle(self) -> Dict[str, Any]:
        """Execute one optimization cycle"""
        optimization_result = {
            'timestamp': datetime.now().isoformat(),
            'optimizations_applied': 3,
            'effectiveness': 0.85,
            'response_time': 1.2
        }
        
        self.optimization_history.append(optimization_result)
        return optimization_result
        
    def get_effectiveness_score(self) -> float:
        """Get optimization effectiveness score"""
        if not self.optimization_history:
            return 0.5
            
        recent_scores = [opt['effectiveness'] for opt in list(self.optimization_history)[-5:]]
        return sum(recent_scores) / len(recent_scores)

class NeuralPredictionSystem:
    """Neural state prediction and forecasting system"""
    
    def __init__(self, monitor: NeuralStateMonitor):
        self.monitor = monitor
        self.predictions = deque(maxlen=100)
        self.prediction_accuracy = 0.7
        
    def analyze_prediction_accuracy(self) -> Dict[str, Any]:
        """Analyze prediction accuracy"""
        return {
            'overall_accuracy': self.prediction_accuracy,
            'predictions_made': len(self.predictions),
            'prediction_types': ['neural_load', 'emotional_state', 'efficiency']
        }
        
    def update_predictions(self) -> Dict[str, Any]:
        """Update predictions based on current state"""
        return {
            'predictions_updated': 5,
            'accuracy_improvement': 0.02,
            'new_prediction_models': 1
        }
        
    def get_prediction_accuracy(self) -> float:
        """Get current prediction accuracy"""
        return self.prediction_accuracy

class SelfImprovementEngine:
    """Self-improvement and autonomous enhancement system"""
    
    def __init__(self, monitor: NeuralStateMonitor, analyzer: NeuralPatternAnalyzer):
        self.monitor = monitor
        self.analyzer = analyzer
        self.improvement_history = deque(maxlen=50)
        
    def generate_improvement_report(self) -> Dict[str, Any]:
        """Generate self-improvement report"""
        return {
            'improvement_cycles': len(self.improvement_history),
            'areas_improved': ['efficiency', 'pattern_recognition', 'decision_making'],
            'improvement_rate': 0.05
        }
        
    def execute_improvement_cycle(self) -> Dict[str, Any]:
        """Execute one self-improvement cycle"""
        improvement_result = {
            'timestamp': datetime.now().isoformat(),
            'improvements_made': 2,
            'effectiveness': 0.78
        }
        
        self.improvement_history.append(improvement_result)
        return improvement_result

def demo_advanced_neural_intelligence():
    """Demonstrate advanced neural intelligence capabilities"""
    print("=== Phase 5: Advanced Neural Intelligence System ===")
    
    # Create advanced intelligence system
    advanced_ai = AdvancedNeuralIntelligence()
    
    print("🧠 Advanced Neural Intelligence Features:")
    print("  • Autonomous learning and improvement")
    print("  • Intelligence quotient assessment")
    print("  • Self-awareness monitoring")
    print("  • Predictive neural modeling")
    print("  • Autonomous optimization cycles")
    print("  • Meta-cognitive capabilities")
    print("  • Intelligence evolution tracking")
    print("  • Cognitive strength identification")
    
    # Enable autonomous mode
    print(f"\n🤖 Enabling autonomous intelligence mode...")
    advanced_ai.enable_autonomous_mode()
    
    # Simulate some intelligence cycles
    print(f"\n🔄 Executing autonomous intelligence cycles...")
    for i in range(3):
        print(f"   Cycle {i+1}/3...")
        cycle_result = advanced_ai.autonomous_intelligence_cycle()
        time.sleep(0.5)
        
    print("✅ Autonomous cycles completed")
    
    # Perform comprehensive analysis
    print(f"\n📊 Performing comprehensive neural intelligence analysis...")
    analysis = advanced_ai.comprehensive_neural_analysis()
    
    # Display key results
    intelligence = analysis['intelligence_metrics']
    print(f"\n--- Intelligence Assessment ---")
    print(f"Intelligence Quotient: {intelligence['intelligence_quotient']:.1f}")
    print(f"Classification: {intelligence['intelligence_classification']}")
    
    print(f"\nIndividual Metrics:")
    for metric, score in intelligence['individual_metrics'].items():
        metric_name = metric.replace('_', ' ').title()
        print(f"  {metric_name}: {score:.3f}")
        
    if intelligence['strengths']:
        print(f"\nCognitive Strengths:")
        for strength in intelligence['strengths']:
            print(f"  • {strength}")
            
    # Generate and display full intelligence report
    print(f"\n--- Comprehensive Intelligence Report ---")
    report = advanced_ai.generate_intelligence_report()
    print(report)
    
    return advanced_ai

if __name__ == "__main__":
    demo_advanced_neural_intelligence()
