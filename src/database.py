import sqlite3
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from .models import Memory, PersonalityTrait, ConversationLog, MemoryType, MemorySource, Message, EmotionalState, AIPersonality

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
        
    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Memory table (original schema - don't break existing memories)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance REAL NOT NULL,
                    confidence REAL NOT NULL,
                    tags TEXT,
                    associations TEXT,
                    source TEXT NOT NULL,
                    reinforcement_count INTEGER DEFAULT 0,
                    last_accessed TEXT NOT NULL,
                    decay_date TEXT,
                    context TEXT
                )
            ''')
            
            # Personality traits table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personality_traits (
                    trait_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    value REAL NOT NULL,
                    confidence REAL NOT NULL,
                    formation_date TEXT NOT NULL,
                    influencing_memories TEXT,
                    stability REAL NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # AI Personality table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_personality (
                    personality_id TEXT PRIMARY KEY,
                    created_date TEXT NOT NULL,
                    last_updated TEXT NOT NULL,
                    core_values TEXT,
                    consciousness_state TEXT,
                    interaction_count INTEGER DEFAULT 0,
                    relationship_depth REAL DEFAULT 0.0
                )
            ''')
            
            conn.commit()
    
    def save_memory(self, memory: Memory) -> bool:
        """Save a memory to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO memories 
                    (id, timestamp, type, content, importance, confidence, tags, 
                     associations, source, reinforcement_count, last_accessed, 
                     decay_date, context)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    memory.id,
                    memory.timestamp.isoformat(),
                    memory.type.value,
                    memory.content,
                    memory.importance,
                    memory.confidence,
                    json.dumps(memory.tags),
                    json.dumps(memory.associations),
                    memory.source.value,
                    memory.reinforcement_count,
                    memory.last_accessed.isoformat(),
                    memory.decay_date.isoformat() if memory.decay_date else None,
                    memory.context
                ))
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error saving memory: {e}")
            return False
    
    def get_memory(self, memory_id: str) -> Optional[Memory]:
        """Retrieve a specific memory by ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
                row = cursor.fetchone()
                
                if row:
                    return self._row_to_memory(row)
                return None
        except Exception as e:
            logging.error(f"Error retrieving memory: {e}")
            return None
    
    def search_memories(self, query: str = None, memory_type: MemoryType = None, 
                       tags: List[str] = None, limit: int = 50) -> List[Memory]:
        """Search memories based on various criteria"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                where_clauses = []
                params = []
                
                if query:
                    where_clauses.append("content LIKE ?")
                    params.append(f"%{query}%")
                
                if memory_type:
                    where_clauses.append("type = ?")
                    params.append(memory_type.value)
                
                if tags:
                    for tag in tags:
                        where_clauses.append("tags LIKE ?")
                        params.append(f"%{tag}%")
                
                where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
                
                cursor.execute(f'''
                    SELECT * FROM memories 
                    WHERE {where_clause}
                    ORDER BY importance DESC, last_accessed DESC
                    LIMIT ?
                ''', params + [limit])
                
                rows = cursor.fetchall()
                return [self._row_to_memory(row) for row in rows]
        except Exception as e:
            logging.error(f"Error searching memories: {e}")
            return []
    
    def update_memory_access(self, memory_id: str):
        """Update the last accessed time and reinforcement count"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE memories 
                    SET last_accessed = ?, reinforcement_count = reinforcement_count + 1
                    WHERE id = ?
                ''', (datetime.now().isoformat(), memory_id))
                conn.commit()
        except Exception as e:
            logging.error(f"Error updating memory access: {e}")
    
    def save_personality_trait(self, trait: PersonalityTrait) -> bool:
        """Save a personality trait"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO personality_traits
                    (trait_id, name, value, confidence, formation_date, 
                     influencing_memories, stability, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    trait.trait_id,
                    trait.name,
                    trait.value,
                    trait.confidence,
                    trait.formation_date.isoformat(),
                    json.dumps(trait.influencing_memories),
                    trait.stability,
                    trait.last_updated.isoformat()
                ))
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error saving personality trait: {e}")
            return False
    
    def get_personality_traits(self) -> List[PersonalityTrait]:
        """Get all personality traits"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personality_traits')
                rows = cursor.fetchall()
                return [self._row_to_personality_trait(row) for row in rows]
        except Exception as e:
            logging.error(f"Error retrieving personality traits: {e}")
            return []
    
    def save_ai_personality(self, personality: AIPersonality) -> bool:
        """Save AI personality data"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO ai_personality
                    (personality_id, created_date, last_updated, core_values,
                     consciousness_state, interaction_count, relationship_depth)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    personality.personality_id,
                    personality.created_date.isoformat(),
                    personality.last_updated.isoformat(),
                    json.dumps(personality.core_values),
                    personality.consciousness_state.model_dump_json(),
                    personality.interaction_count,
                    personality.relationship_depth
                ))
                conn.commit()
                return True
        except Exception as e:
            logging.error(f"Error saving AI personality: {e}")
            return False
    
    def _safe_json_loads(self, data, default=None):
        """Safely parse JSON data with fallback"""
        if not data:
            return default or []
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return default or []
    
    def _safe_datetime_parse(self, date_value):
        """Safely parse datetime with fallback"""
        if not date_value:
            return datetime.now()
        try:
            if isinstance(date_value, str):
                return datetime.fromisoformat(date_value)
            elif isinstance(date_value, (int, float)):
                return datetime.fromtimestamp(date_value)
            else:
                return datetime.now()
        except (ValueError, TypeError):
            return datetime.now()
    
    def _row_to_memory(self, row) -> Memory:
        """Convert database row to Memory object"""
        # The actual database has these columns in order:
        # 0: id, 1: timestamp, 2: type, 3: content, 4: importance, 5: confidence, 
        # 6: tags, 7: associations, 8: source, 9: reinforcement_count, 
        # 10: last_accessed, 11: decay_date, 12: context, 13: emotional_intensity
        
        # Convert old numeric source values to new string enum values
        source_value = row[8]
        if isinstance(source_value, (int, str)) and str(source_value).isdigit():
            numeric_source = int(source_value)
            if numeric_source == 0:
                source_value = "user_input"
            elif numeric_source == 1:
                source_value = "ai_reasoning"
            elif numeric_source == 2:
                source_value = "external_data"
            elif numeric_source == 3:
                source_value = "consolidation"
            elif numeric_source == 4:
                source_value = "user_input"
            elif numeric_source == 5:
                source_value = "ai_reasoning"
            elif numeric_source == 6:
                source_value = "consolidation"
            elif numeric_source == 7:
                source_value = "external_data"
            elif numeric_source == 8:
                source_value = "user_input"
            elif numeric_source == 9:
                source_value = "ai_reasoning"
            elif numeric_source == 10:
                source_value = "consolidation"
            elif numeric_source == 75:
                source_value = "user_input"
            else:
                source_value = "user_input"  # Default fallback
        
        # Handle case where emotional_intensity might be missing (though it should exist)
        emotional_intensity = row[13] if len(row) > 13 else 0.5
        
        return Memory(
            id=row[0],
            timestamp=self._safe_datetime_parse(row[1]),
            type=MemoryType(row[2]),
            content=row[3],
            importance=row[4],
            confidence=row[5],
            tags=self._safe_json_loads(row[6]),
            associations=self._safe_json_loads(row[7]),
            source=MemorySource(source_value),
            reinforcement_count=row[9],
            last_accessed=self._safe_datetime_parse(row[10]),
            decay_date=self._safe_datetime_parse(row[11]) if row[11] else None,
            context=row[12],
            emotional_intensity=emotional_intensity
        )
    
    def _row_to_personality_trait(self, row) -> PersonalityTrait:
        """Convert database row to PersonalityTrait object"""
        return PersonalityTrait(
            trait_id=row[0],
            name=row[1],
            value=row[2],
            confidence=row[3],
            formation_date=self._safe_datetime_parse(row[4]),
            influencing_memories=self._safe_json_loads(row[5]),
            stability=row[6],
            last_updated=self._safe_datetime_parse(row[7])
        )
