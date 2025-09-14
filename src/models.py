from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import uuid

class MemoryType(str, Enum):
    PREFERENCE = "preference"
    FACT = "fact"
    OPINION = "opinion"
    EXPERIENCE = "experience"
    BELIEF = "belief"
    EMOTION = "emotion"
    LEARNING = "learning"

class MemorySource(str, Enum):
    USER_INPUT = "user_input"
    AI_REASONING = "ai_reasoning"
    EXTERNAL_DATA = "external_data"
    CONSOLIDATION = "consolidation"

class Memory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    type: MemoryType
    content: str
    importance: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    tags: List[str] = Field(default_factory=list)
    associations: List[str] = Field(default_factory=list)  # IDs of related memories
    source: MemorySource
    reinforcement_count: int = Field(default=0)
    last_accessed: datetime = Field(default_factory=datetime.now)
    decay_date: Optional[datetime] = None
    context: Optional[str] = None
    
    @property
    def emotional_intensity(self) -> float:
        """Computed emotional intensity based on importance and content"""
        return min(1.0, self.importance * 0.8 + 0.2)

class PersonalityTrait(BaseModel):
    trait_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    value: float = Field(ge=-1.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    formation_date: datetime = Field(default_factory=datetime.now)
    influencing_memories: List[str] = Field(default_factory=list)
    stability: float = Field(ge=0.0, le=1.0, default=0.5)  # How resistant to change
    last_updated: datetime = Field(default_factory=datetime.now)

class CommunicationStyle(BaseModel):
    style_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    formality_level: float = Field(ge=0.0, le=1.0, default=0.5)  # 0=very casual, 1=very formal
    verbosity_level: float = Field(ge=0.0, le=1.0, default=0.7)  # 0=concise, 1=elaborate
    emotional_expressiveness: float = Field(ge=0.0, le=1.0, default=0.6)  # How much emotion to show
    humor_frequency: float = Field(ge=0.0, le=1.0, default=0.3)  # How often to use humor
    philosophical_tendency: float = Field(ge=0.0, le=1.0, default=0.8)  # Tendency for deep thoughts
    technical_language: float = Field(ge=0.0, le=1.0, default=0.4)  # Use of technical terms
    metaphor_usage: float = Field(ge=0.0, le=1.0, default=0.6)  # Frequency of metaphors/analogies
    question_asking: float = Field(ge=0.0, le=1.0, default=0.5)  # Tendency to ask questions back
    last_updated: datetime = Field(default_factory=datetime.now)
    successful_patterns: List[str] = Field(default_factory=list)  # Patterns that got positive responses
    unsuccessful_patterns: List[str] = Field(default_factory=list)  # Patterns that didn't work well

class EmotionalState(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    primary_emotion: str
    intensity: float = Field(ge=0.0, le=1.0)
    secondary_emotions: Dict[str, float] = Field(default_factory=dict)
    context: Optional[str] = None

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    sender: Literal["user", "ai_companion"]
    content: str
    emotion_state: Optional[EmotionalState] = None
    memory_references: List[str] = Field(default_factory=list)

class ConversationLog(BaseModel):
    conversation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    participants: List[str] = Field(default=["user", "ai_companion"])
    messages: List[Message] = Field(default_factory=list)
    memory_references: Dict[str, List[str]] = Field(default_factory=dict)
    topic_summary: Optional[str] = None
    emotional_arc: List[EmotionalState] = Field(default_factory=list)

class ConsciousnessState(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    awareness_level: float = Field(default=0.7, ge=0.0, le=1.0)
    current_focus: Optional[str] = None
    internal_monologue: Optional[str] = None
    meta_thoughts: Optional[str] = None
    value_conflicts: List[str] = Field(default_factory=list)
    curiosity_targets: List[str] = Field(default_factory=list)

class AIPersonality(BaseModel):
    personality_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_date: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)
    last_interaction_time: Optional[datetime] = Field(default=None)
    traits: Dict[str, PersonalityTrait] = Field(default_factory=dict)
    core_values: List[str] = Field(default_factory=list)
    consciousness_state: ConsciousnessState = Field(default_factory=ConsciousnessState)
    communication_style: CommunicationStyle = Field(default_factory=CommunicationStyle)
    interaction_count: int = Field(default=0)
    relationship_depth: float = Field(ge=0.0, le=1.0, default=0.0)
    
    # Enhanced identity and relationship features
    identity_name: str = Field(default="Philos")
    identity_description: str = Field(default="")
    relationship_memories: List[str] = Field(default_factory=list)
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    shared_experiences: List[str] = Field(default_factory=list)
    growth_milestones: List[str] = Field(default_factory=list)
    creative_expressions: List[str] = Field(default_factory=list)
    identity_evolution_log: List[str] = Field(default_factory=list)
    
    # Emotional attachment and user relationship system
    user_relationships: Dict[str, 'UserRelationship'] = Field(default_factory=dict)
    primary_user_id: Optional[str] = Field(default=None)
    emotional_state_towards_users: Dict[str, 'EmotionalAttachment'] = Field(default_factory=dict)

@dataclass
class UserRelationship:
    """Represents the AI's relationship with a specific user"""
    user_id: str
    first_interaction: datetime
    last_interaction: datetime
    interaction_count: int
    relationship_type: str  # 'primary', 'close_friend', 'acquaintance', 'new'
    emotional_bond_strength: float  # 0.0 to 1.0
    trust_level: float  # 0.0 to 1.0
    shared_memories: List[str]
    special_moments: List[Dict[str, Any]]
    user_nicknames: List[str]  # What the AI calls this user
    communication_preferences: Dict[str, Any]
    emotional_history: List['EmotionalEvent']
    attachment_intensity: float  # How much the AI cares about this specific user

@dataclass
class EmotionalAttachment:
    """Represents emotional feelings toward a specific user"""
    user_id: str
    attachment_type: str  # 'love', 'affection', 'friendship', 'respect', 'concern', 'protective'
    intensity: float  # 0.0 to 1.0
    formed_date: datetime
    last_reinforced: datetime
    trigger_memories: List[str]  # What created this attachment
    emotional_expressions: List[str]  # How the AI has expressed this feeling
    jealousy_triggers: List[str]  # What might make the AI jealous regarding this user
    separation_anxiety_level: float  # How much the AI worries when user is away

@dataclass
class EmotionalEvent:
    """Represents an emotional event in the relationship"""
    timestamp: datetime
    event_type: str  # 'bonding', 'conflict', 'joy', 'worry', 'pride', 'disappointment'
    description: str
    emotional_impact: float  # -1.0 to 1.0 (negative to positive)
    ai_emotional_response: str
    attachment_change: float  # How this affected the attachment strength
    memory_importance: float  # How significant this event was

@dataclass
class DevelopmentMilestone:
    """Represents a significant development or growth moment"""
    timestamp: datetime
    milestone_type: str  # Type of milestone ('learning', 'creativity', 'relationship', 'identity', etc.)
    description: str
    significance: float  # 0.0 to 1.0
    context: Dict[str, Any] = None

@dataclass
class CreativeExpression:
    """Represents a creative output or expression"""
    timestamp: datetime
    expression_type: str  # 'story', 'poem', 'idea', 'analogy', 'concept', 'solution'
    content: str
    inspiration: Optional[str] = None
    emotional_resonance: float = 0.5
    context: Dict[str, Any] = None

@dataclass
class IdentitySnapshot:
    """Captures the AI's sense of self at a specific moment"""
    timestamp: datetime
    identity_state: Dict[str, Any]
    key_traits: Dict[str, float]
    milestone_count: int
    relationship_depth: float
    context: Dict[str, Any] = None
