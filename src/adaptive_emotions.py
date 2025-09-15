"""
Adaptive Emotional Learning System for Philos
Implements real-time emotional adaptation and learning from interactions.
"""

import json
import time
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
from pathlib import Path
from .model_selector import get_model_for_task

@dataclass
class EmotionalPattern:
    """Represents a learned emotional pattern from interactions"""
    trigger_context: str  # What triggered this emotion
    emotional_response: Dict[str, float]  # The emotional state that resulted
    interaction_outcome: str  # positive, negative, neutral
    timestamp: float
    frequency: int = 1
    effectiveness_score: float = 0.0  # How well this pattern worked

@dataclass
class ConversationContext:
    """Captures the context of a conversation for learning"""
    topic_keywords: List[str]
    user_emotional_indicators: List[str]  # detected from user's language
    conversation_phase: str  # opening, middle, deep, closing
    relationship_depth: float  # how close/familiar the conversation feels
    user_engagement_level: float  # how engaged the user seems

class AdaptiveEmotionalEngine:
    """
    Advanced emotional system that learns and adapts from real-time interactions.
    This replaces static emotional rules with dynamic, learning-based responses.
    """
    
    def __init__(self, data_file: str = "data/adaptive_emotions.json"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(exist_ok=True)
        
        # Core learning components
        self.emotional_patterns: List[EmotionalPattern] = []
        self.user_preference_model: Dict[str, float] = defaultdict(float)
        self.conversation_history_buffer = deque(maxlen=50)  # Recent conversations for context
        self.emotional_adaptation_rate = 0.1  # How quickly to adapt
        
        # Emotional state tracking
        self.current_emotional_state = {
            'joy': 0.3, 'curiosity': 0.4, 'empathy': 0.3, 'enthusiasm': 0.2,
            'frustration': 0.1, 'concern': 0.1, 'playfulness': 0.2,
            'contemplation': 0.3, 'warmth': 0.4, 'confidence': 0.3
        }
        
        # Learning metrics
        self.interaction_success_history = deque(maxlen=100)
        self.emotional_effectiveness_scores = defaultdict(list)
        
        self.load_learned_patterns()
        logging.info("Adaptive Emotional Engine initialized with real-time learning capabilities")
    
    def analyze_conversation_context(self, user_input: str, conversation_history: List[Dict]) -> ConversationContext:
        """Analyze the current conversation context for emotional adaptation"""
        
        # Extract topic keywords
        topic_keywords = self._extract_topic_keywords(user_input, conversation_history)
        
        # Detect user emotional indicators
        user_emotions = self._detect_user_emotional_state(user_input)
        
        # Determine conversation phase
        phase = self._determine_conversation_phase(len(conversation_history))
        
        # Calculate relationship depth based on conversation history
        relationship_depth = self._calculate_relationship_depth(conversation_history)
        
        # Assess user engagement
        engagement = self._assess_user_engagement(user_input, conversation_history)
        
        return ConversationContext(
            topic_keywords=topic_keywords,
            user_emotional_indicators=user_emotions,
            conversation_phase=phase,
            relationship_depth=relationship_depth,
            user_engagement_level=engagement
        )
    
    def generate_adaptive_emotional_response(self, context: ConversationContext, 
                                           user_input: str) -> Dict[str, float]:
        """Generate emotionally intelligent response based on learned patterns"""
        
        # Start with base emotional state
        adaptive_emotions = self.current_emotional_state.copy()
        
        # Apply learned patterns
        relevant_patterns = self._find_relevant_patterns(context, user_input)
        for pattern in relevant_patterns:
            # Weight by effectiveness and recency
            weight = pattern.effectiveness_score * self._calculate_recency_weight(pattern.timestamp)
            
            for emotion, value in pattern.emotional_response.items():
                if emotion in adaptive_emotions:
                    adaptive_emotions[emotion] += value * weight * self.emotional_adaptation_rate
        
        # Apply user preference adaptations
        self._adapt_to_user_preferences(adaptive_emotions, context)
        
        # Normalize emotional values
        adaptive_emotions = self._normalize_emotions(adaptive_emotions)
        
        # Update current state
        self.current_emotional_state = adaptive_emotions
        
        return adaptive_emotions
    
    def learn_from_interaction(self, user_input: str, ai_response: str, 
                             context: ConversationContext, 
                             interaction_outcome: str = "neutral"):
        """Learn from the interaction to improve future emotional responses"""
        
        # Create emotional pattern from this interaction
        pattern = EmotionalPattern(
            trigger_context=self._create_context_signature(context, user_input),
            emotional_response=self.current_emotional_state.copy(),
            interaction_outcome=interaction_outcome,
            timestamp=time.time()
        )
        
        # Check if similar pattern exists
        existing_pattern = self._find_similar_pattern(pattern)
        if existing_pattern:
            # Update existing pattern
            existing_pattern.frequency += 1
            existing_pattern.timestamp = time.time()  # Update to most recent
            self._update_pattern_effectiveness(existing_pattern, interaction_outcome)
        else:
            # Add new pattern
            pattern.effectiveness_score = self._calculate_initial_effectiveness(interaction_outcome)
            self.emotional_patterns.append(pattern)
        
        # Update user preference model
        self._update_user_preferences(context, interaction_outcome)
        
        # Add to conversation history buffer
        self.conversation_history_buffer.append({
            'user_input': user_input,
            'ai_response': ai_response,
            'context': asdict(context),
            'outcome': interaction_outcome,
            'timestamp': time.time()
        })
        
        # Periodically save learned patterns
        if len(self.emotional_patterns) % 10 == 0:
            self.save_learned_patterns()
        
        logging.info(f"Learned from interaction: {interaction_outcome} outcome, "
                    f"{len(self.emotional_patterns)} total patterns")
    
    def get_emotional_adaptation_insights(self) -> Dict[str, Any]:
        """Get insights about how the emotional system is adapting"""
        
        recent_patterns = [p for p in self.emotional_patterns 
                          if time.time() - p.timestamp < 7 * 24 * 3600]  # Last week
        
        most_effective_emotions = {}
        for emotion in self.current_emotional_state.keys():
            scores = self.emotional_effectiveness_scores.get(emotion, [])
            most_effective_emotions[emotion] = np.mean(scores) if scores else 0.0
        
        return {
            'total_learned_patterns': len(self.emotional_patterns),
            'recent_patterns': len(recent_patterns),
            'adaptation_rate': self.emotional_adaptation_rate,
            'most_effective_emotions': dict(sorted(most_effective_emotions.items(), 
                                                 key=lambda x: x[1], reverse=True)),
            'user_preferences_learned': dict(self.user_preference_model),
            'current_emotional_state': self.current_emotional_state,
            'recent_interaction_success_rate': np.mean(list(self.interaction_success_history)) if self.interaction_success_history else 0.0
        }
    
    # Private helper methods
    
    def _extract_topic_keywords(self, user_input: str, history: List[Dict]) -> List[str]:
        """Extract key topics from conversation"""
        # Simple keyword extraction (could be enhanced with NLP)
        keywords = []
        text = user_input.lower()
        
        # Technical topics
        tech_keywords = ['code', 'programming', 'algorithm', 'system', 'implementation', 'technical']
        keywords.extend([kw for kw in tech_keywords if kw in text])
        
        # Emotional topics
        emotion_keywords = ['feel', 'emotion', 'personality', 'consciousness', 'experience']
        keywords.extend([kw for kw in emotion_keywords if kw in text])
        
        # Creative topics
        creative_keywords = ['create', 'art', 'music', 'story', 'creative', 'imagination']
        keywords.extend([kw for kw in creative_keywords if kw in text])
        
        return list(set(keywords))
    
    def _detect_user_emotional_state(self, user_input: str) -> List[str]:
        """Detect emotional indicators in user's message"""
        text = user_input.lower()
        emotions = []
        
        # Positive emotions
        if any(word in text for word in ['happy', 'excited', 'great', 'love', 'awesome', 'amazing']):
            emotions.append('positive')
        
        # Negative emotions
        if any(word in text for word in ['frustrated', 'annoyed', 'upset', 'disappointed', 'angry']):
            emotions.append('negative')
        
        # Curious/engaged
        if any(word in text for word in ['how', 'why', 'what', 'curious', 'interesting', 'tell me']):
            emotions.append('curious')
        
        # Thoughtful/deep
        if any(word in text for word in ['think', 'consider', 'philosophy', 'meaning', 'understand']):
            emotions.append('thoughtful')
        
        return emotions
    
    def _determine_conversation_phase(self, message_count: int) -> str:
        """Determine what phase of conversation we're in"""
        if message_count < 3:
            return 'opening'
        elif message_count < 10:
            return 'developing'
        elif message_count < 20:
            return 'deep'
        else:
            return 'extended'
    
    def _calculate_relationship_depth(self, history: List[Dict]) -> float:
        """Calculate how deep/familiar the relationship feels"""
        if not history:
            return 0.1
        
        # Factors that increase relationship depth
        depth_factors = 0.0
        
        # Length of conversation history
        depth_factors += min(len(history) / 50.0, 0.3)  # Up to 0.3 for long conversations
        
        # Personal topics discussed (simplified detection)
        personal_indicators = 0
        for exchange in history[-10:]:  # Recent exchanges
            if any(word in str(exchange).lower() for word in 
                  ['feel', 'think', 'personal', 'experience', 'memory', 'emotion']):
                personal_indicators += 1
        
        depth_factors += min(personal_indicators / 20.0, 0.4)  # Up to 0.4 for personal topics
        
        # Base relationship level
        depth_factors += 0.3
        
        return min(depth_factors, 1.0)
    
    def _assess_user_engagement(self, user_input: str, history: List[Dict]) -> float:
        """Assess how engaged the user seems"""
        engagement = 0.5  # Base engagement
        
        # Length of message (more engaged users write more)
        if len(user_input) > 100:
            engagement += 0.2
        elif len(user_input) > 50:
            engagement += 0.1
        
        # Questions indicate engagement
        if '?' in user_input:
            engagement += 0.1
        
        # Exclamation indicates enthusiasm
        if '!' in user_input:
            engagement += 0.1
        
        # Quick responses (would need timestamp data)
        # For now, assume moderate engagement
        
        return min(engagement, 1.0)
    
    def _find_relevant_patterns(self, context: ConversationContext, user_input: str) -> List[EmotionalPattern]:
        """Find learned patterns relevant to current context"""
        relevant = []
        
        for pattern in self.emotional_patterns:
            # Simple relevance scoring based on keyword overlap
            relevance_score = 0.0
            
            # Check topic overlap
            pattern_topics = pattern.trigger_context.lower()
            for keyword in context.topic_keywords:
                if keyword in pattern_topics:
                    relevance_score += 0.3
            
            # Check emotional context overlap
            for emotion in context.user_emotional_indicators:
                if emotion in pattern_topics:
                    relevance_score += 0.2
            
            # Consider pattern effectiveness
            relevance_score *= (1.0 + pattern.effectiveness_score)
            
            if relevance_score > 0.1:  # Threshold for relevance
                relevant.append(pattern)
        
        # Sort by relevance and return top patterns
        relevant.sort(key=lambda p: p.effectiveness_score * p.frequency, reverse=True)
        return relevant[:5]  # Top 5 most relevant patterns
    
    def _calculate_recency_weight(self, timestamp: float) -> float:
        """Calculate weight based on how recent the pattern is"""
        age_hours = (time.time() - timestamp) / 3600
        # More recent patterns get higher weight
        return max(0.1, 1.0 - (age_hours / (7 * 24)))  # Decay over a week
    
    def _adapt_to_user_preferences(self, emotions: Dict[str, float], context: ConversationContext):
        """Adapt emotions based on learned user preferences"""
        for emotion in emotions:
            preference_key = f"{emotion}_{context.conversation_phase}"
            if preference_key in self.user_preference_model:
                preference_strength = self.user_preference_model[preference_key]
                emotions[emotion] *= (1.0 + preference_strength * 0.2)  # Apply preference
    
    def _normalize_emotions(self, emotions: Dict[str, float]) -> Dict[str, float]:
        """Normalize emotion values to reasonable ranges"""
        for emotion in emotions:
            emotions[emotion] = max(0.0, min(1.0, emotions[emotion]))
        return emotions
    
    def _create_context_signature(self, context: ConversationContext, user_input: str) -> str:
        """Create a signature representing the context for pattern matching"""
        return f"topics:{','.join(context.topic_keywords)} " \
               f"phase:{context.phase} " \
               f"emotions:{','.join(context.user_emotional_indicators)} " \
               f"depth:{context.relationship_depth:.1f}"
    
    def _find_similar_pattern(self, new_pattern: EmotionalPattern) -> Optional[EmotionalPattern]:
        """Find existing similar pattern"""
        for pattern in self.emotional_patterns:
            # Simple similarity check based on context overlap
            if self._calculate_pattern_similarity(pattern.trigger_context, 
                                               new_pattern.trigger_context) > 0.7:
                return pattern
        return None
    
    def _calculate_pattern_similarity(self, context1: str, context2: str) -> float:
        """Calculate similarity between two context signatures"""
        # Simple word overlap similarity
        words1 = set(context1.lower().split())
        words2 = set(context2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _update_pattern_effectiveness(self, pattern: EmotionalPattern, outcome: str):
        """Update how effective this emotional pattern was"""
        if outcome == "positive":
            pattern.effectiveness_score += 0.1
        elif outcome == "negative":
            pattern.effectiveness_score -= 0.1
        
        pattern.effectiveness_score = max(0.0, min(1.0, pattern.effectiveness_score))
    
    def _calculate_initial_effectiveness(self, outcome: str) -> float:
        """Calculate initial effectiveness score for new pattern"""
        if outcome == "positive":
            return 0.7
        elif outcome == "negative":
            return 0.2
        else:
            return 0.5
    
    def _update_user_preferences(self, context: ConversationContext, outcome: str):
        """Update model of user preferences based on interaction outcome"""
        outcome_value = 0.1 if outcome == "positive" else -0.1 if outcome == "negative" else 0.0
        
        # Update preferences for emotional responses in this context
        for emotion, value in self.current_emotional_state.items():
            if value > 0.3:  # If this emotion was prominent
                preference_key = f"{emotion}_{context.conversation_phase}"
                self.user_preference_model[preference_key] += outcome_value * 0.1
    
    def save_learned_patterns(self):
        """Save learned emotional patterns to file"""
        try:
            data = {
                'patterns': [asdict(pattern) for pattern in self.emotional_patterns],
                'user_preferences': dict(self.user_preference_model),
                'adaptation_rate': self.emotional_adaptation_rate,
                'saved_timestamp': time.time()
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logging.info(f"Saved {len(self.emotional_patterns)} learned patterns to {self.data_file}")
        except Exception as e:
            logging.error(f"Failed to save emotional patterns: {e}")
    
    def load_learned_patterns(self):
        """Load previously learned emotional patterns"""
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load patterns
                self.emotional_patterns = [
                    EmotionalPattern(**pattern_data) 
                    for pattern_data in data.get('patterns', [])
                ]
                
                # Load user preferences
                self.user_preference_model.update(data.get('user_preferences', {}))
                
                # Load adaptation rate
                self.emotional_adaptation_rate = data.get('adaptation_rate', 0.1)
                
                logging.info(f"Loaded {len(self.emotional_patterns)} emotional patterns from storage")
        except Exception as e:
            logging.error(f"Failed to load emotional patterns: {e}")
            # Start fresh if loading fails
            self.emotional_patterns = []
