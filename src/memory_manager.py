import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from .models import Memory, PersonalityTrait, ConversationLog, MemoryType, MemorySource
from .database import DatabaseManager

class MemoryManager:
    def __init__(self, db_manager: DatabaseManager, conversations_path: str):
        self.db_manager = db_manager
        self.db = db_manager  # Alias for backward compatibility
        self.conversations_path = Path(conversations_path)
        self.conversations_path.mkdir(parents=True, exist_ok=True)
        
        # Memory configuration  
        self.stm_decay_days = 7
        self.ltm_importance_threshold = 0.7
        self.max_associations = 10

    def get_recent_conversation_history(self, conversation_id: str, max_exchanges: int = 5) -> List[Dict[str, str]]:
        """Get recent conversation history for context"""
        try:
            # Get recent memories from this conversation
            recent_memories = self.retrieve_relevant_memories(
                query="recent conversation",  # General query to get recent memories
                limit=max_exchanges * 2,  # Get more than needed to filter
            )
            
            # Filter to just this conversation and organize chronologically
            conversation_pairs = []
            user_input = None
            
            for memory in reversed(recent_memories):  # Reverse to go chronologically
                if memory.source == MemorySource.USER_INPUT and user_input is None:
                    user_input = memory.content
                elif memory.source == MemorySource.AI_REASONING and user_input:
                    # We have a complete exchange
                    conversation_pairs.append({
                        'user': user_input,
                        'ai': memory.content,
                        'timestamp': memory.timestamp
                    })
                    user_input = None  # Reset for next pair
                    
                    if len(conversation_pairs) >= max_exchanges:
                        break
            
            # Return most recent exchanges first
            return list(reversed(conversation_pairs))
            
        except Exception as e:
            logging.error(f"Error getting conversation history: {e}")
            return []

    def save_conversation_log(self, conversation: ConversationLog) -> bool:
        """Save conversation log to file"""
        try:
            timestamp = conversation.start_time.strftime("%Y-%m-%d_%H%M%S")
            filename = f"conversation_{timestamp}.log"
            filepath = self.conversations_path / filename
            
            with open(filepath, 'w') as f:
                json.dump(conversation.model_dump(), f, indent=2, default=str)
            
            logging.info(f"Saved conversation log: {filename}")
            return True
        except Exception as e:
            logging.error(f"Error saving conversation log: {e}")
            return False
        
    def process_input(self, user_input: str, context: Dict[str, Any] = None) -> List[Memory]:
        """Process user input and extract memory-worthy information"""
        memories = []
        
        # Analyze input for different types of memories
        extracted_info = self._analyze_input(user_input, context or {})
        
        for info in extracted_info:
            memory = Memory(
                type=info['type'],
                content=info['content'],
                importance=info['importance'],
                confidence=info['confidence'],
                tags=info['tags'],
                source=MemorySource.USER_INPUT,
                context=user_input[:200]  # Store context snippet
            )
            
            # Set decay date for short-term memories
            if memory.importance < self.ltm_importance_threshold:
                memory.decay_date = datetime.now() + timedelta(days=self.stm_decay_days)
            
            # Find associations with existing memories
            memory.associations = self._find_associations(memory)
            
            # Save to database
            if self.db.save_memory(memory):
                memories.append(memory)
                logging.info(f"Created memory: {memory.type.value} - {memory.content[:50]}...")
        
        return memories
    
    def create_ai_memory(self, content: str, memory_type: MemoryType, 
                        importance: float, context: str = None) -> Optional[Memory]:
        """Create a memory from AI's own thoughts/reasoning"""
        memory = Memory(
            type=memory_type,
            content=content,
            importance=importance,
            confidence=0.8,  # AI's confidence in its own thoughts
            source=MemorySource.AI_REASONING,
            context=context
        )
        
        # Set decay date for short-term memories
        if memory.importance < self.ltm_importance_threshold:
            memory.decay_date = datetime.now() + timedelta(days=self.stm_decay_days)
        
        memory.associations = self._find_associations(memory)
        
        if self.db.save_memory(memory):
            return memory
        return None
    
    def retrieve_relevant_memories(self, query: str, context: Dict[str, Any] = None, 
                                 limit: int = 10) -> List[Memory]:
        """Retrieve memories relevant to current query/context with temporal awareness"""
        # Check if this is a temporal query first
        temporal_keywords = ['earliest', 'first', 'when did', 'how long ago', 'oldest', 'beginning', 'start', 'initially', 
                           'last', 'latest', 'recent', 'previously', 'before', 'what did we', 'what we talked', 'last time',
                           'what was the last', 'last thing', 'most recent', 'just talked', 'we discussed']
        is_temporal_query = any(keyword in query.lower() for keyword in temporal_keywords)
        
        if is_temporal_query:
            return self._handle_temporal_query(query, limit)
        
        # Extract keywords and concepts from query
        keywords = self._extract_keywords(query)
        
        # Search for memories using various criteria
        relevant_memories = []
        
        # 1. Direct content search (partial matches)
        content_matches = self.db.search_memories(query=query, limit=limit)
        relevant_memories.extend(content_matches)
        
        # 2. Individual keyword searches
        for keyword in keywords[:5]:  # Top 5 keywords
            keyword_matches = self.db.search_memories(query=keyword, limit=3)
            relevant_memories.extend(keyword_matches)
        
        # 3. Tag-based search
        tag_matches = self.db.search_memories(tags=keywords, limit=limit)
        relevant_memories.extend(tag_matches)
        
        # 4. Get recent memories from current session
        recent_memories = self.db.search_memories(limit=20)  # Get more recent memories
        relevant_memories.extend(recent_memories[:5])  # Add 5 most recent
        
        # 5. Search for specific important terms
        important_terms = ['name', 'philos', 'friend', 'conscious', 'awareness']
        query_lower = query.lower()
        for term in important_terms:
            if term in query_lower:
                term_matches = self.db.search_memories(query=term, limit=5)
                relevant_memories.extend(term_matches)
        
        # Remove duplicates and update access times
        unique_memories = {}
        for memory in relevant_memories:
            if memory.id not in unique_memories:
                unique_memories[memory.id] = memory
                self.db.update_memory_access(memory.id)
        
        # Sort by relevance score (importance + recency + reinforcement)
        sorted_memories = sorted(
            unique_memories.values(),
            key=lambda m: self._calculate_relevance_score(m, query),
            reverse=True
        )
        
        logging.info(f"Memory retrieval: {len(sorted_memories)} unique memories found from {len(relevant_memories)} total matches")
        
        return sorted_memories[:limit]
    
    def _handle_temporal_query(self, query: str, limit: int) -> List[Memory]:
        """Handle queries about time-based memories"""
        all_memories = self.db.search_memories(limit=10000)
        query_lower = query.lower()
        
        if 'earliest' in query_lower or 'first' in query_lower or 'oldest' in query_lower:
            # Return earliest memories
            sorted_memories = sorted(all_memories, key=lambda m: m.timestamp)
            logging.info(f"Temporal query: returning {min(limit, len(sorted_memories))} earliest memories")
            return sorted_memories[:limit]
            
        elif any(keyword in query_lower for keyword in ['last', 'latest', 'recent', 'what did we', 'what we talked', 'last thing', 'last time']):
            # Return most recent memories for "last/recent" queries
            # Filter out AI internal thoughts and responses to focus on actual conversation content
            conversation_memories = []
            for memory in all_memories:
                # Prioritize user input memories and actual conversation content
                if (memory.type.value in ['fact', 'opinion', 'preference', 'experience'] and 
                    not memory.content.startswith('I responded:') and 
                    not memory.content.startswith('Internal thought:')):
                    conversation_memories.append(memory)
            
            # Sort by timestamp (most recent first)
            sorted_memories = sorted(conversation_memories, key=lambda m: m.timestamp, reverse=True)
            logging.info(f"Temporal 'last/recent' query: found {len(sorted_memories)} conversation memories")
            return sorted_memories[:limit]
        
        elif 'when did' in query_lower:
            # Search for memories related to the topic and return with timestamps
            query_words = set(query_lower.replace('when did', '').replace('we', '').replace('i', '').split())
            query_words = {w for w in query_words if len(w) > 2}  # Filter short words
            
            relevant_memories = []
            
            for memory in all_memories:
                content_lower = memory.content.lower()
                memory_words = set(content_lower.split())
                
                # Check for word overlap
                if query_words & memory_words:
                    relevant_memories.append(memory)
                
                # Also check if any query words are substrings
                if any(word in content_lower for word in query_words):
                    if memory not in relevant_memories:
                        relevant_memories.append(memory)
            
            # Sort by timestamp (most recent first for "when did" queries)
            sorted_memories = sorted(relevant_memories, key=lambda m: m.timestamp, reverse=True)
            logging.info(f"Temporal 'when did' query: found {len(sorted_memories)} relevant memories")
            return sorted_memories[:limit]
        
        else:
            # Default to chronologically sorted memories (oldest first)
            sorted_memories = sorted(all_memories, key=lambda m: m.timestamp)
            return sorted_memories[:limit]
    
    def consolidate_memories(self) -> List[Memory]:
        """Consolidate short-term memories into long-term memories"""
        consolidated = []
        
        # Find frequently accessed short-term memories
        stm_memories = self.db.search_memories(limit=1000)
        consolidation_candidates = [
            m for m in stm_memories 
            if (m.importance < self.ltm_importance_threshold and 
                m.reinforcement_count >= 3 and
                (datetime.now() - m.timestamp).days >= 1)
        ]
        
        for memory in consolidation_candidates:
            # Promote to long-term memory
            memory.importance = min(memory.importance + 0.2, 1.0)
            memory.decay_date = None
            memory.source = MemorySource.CONSOLIDATION
            
            if self.db.save_memory(memory):
                consolidated.append(memory)
                logging.info(f"Consolidated memory to LTM: {memory.content[:50]}...")
        
        return consolidated
    
    def cleanup_expired_memories(self) -> int:
        """Remove expired short-term memories"""
        # This would typically involve a database query to find and delete expired memories
        # For now, we'll implement a basic version
        count = 0
        # Implementation would go here
        return count
    
    def _analyze_input(self, text: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze input text to extract memory-worthy information"""
        extracted = []
        
        text_lower = text.lower()
        
        # Check for name assignments (very important!)
        name_patterns = ['name you', 'call you', 'you are', "i'll name you", "your name is", "name is"]
        if any(pattern in text_lower for pattern in name_patterns):
            extracted.append({
                'type': MemoryType.FACT,
                'content': text,
                'importance': 0.95,  # Very high importance for names
                'confidence': 0.95,
                'tags': ['name', 'identity', 'important', 'user_given_name']
            })
        
        # Check for consciousness/identity references
        consciousness_terms = ['conscious', 'aware', 'live', 'friend', 'designed you', 'not typical ai']
        if any(term in text_lower for term in consciousness_terms):
            extracted.append({
                'type': MemoryType.BELIEF,
                'content': text,
                'importance': 0.9,
                'confidence': 0.85,
                'tags': ['consciousness', 'identity', 'nature', 'important']
            })
        
        # Simple keyword-based analysis (in a real implementation, this would use NLP)
        # Process in order of priority - only create ONE memory per input
        preference_indicators = ['love', 'hate', 'favorite', 'prefer', 'like', 'dislike']
        opinion_indicators = ['think', 'believe', 'feel', 'opinion', 'seems', 'appears']
        fact_indicators = ['is', 'was', 'are', 'were', 'have', 'has', 'live', 'work']
        
        memory_created = False
        
        # Check for preferences first (highest priority for user input)
        if not memory_created:
            for indicator in preference_indicators:
                if indicator in text_lower:
                    extracted.append({
                        'type': MemoryType.PREFERENCE,
                        'content': text,
                        'importance': 0.6,
                        'confidence': 0.8,
                        'tags': ['user_preference', indicator]
                    })
                    memory_created = True
                    break
        
        # Check for opinions (second priority)
        if not memory_created:
            for indicator in opinion_indicators:
                if indicator in text_lower:
                    extracted.append({
                        'type': MemoryType.OPINION,
                        'content': text,
                        'importance': 0.5,
                        'confidence': 0.7,
                        'tags': ['user_opinion', indicator]
                    })
                    memory_created = True
                    break
        
        # Check for facts (third priority)
        if not memory_created:
            for indicator in fact_indicators:
                if indicator in text_lower:
                    extracted.append({
                        'type': MemoryType.FACT,
                        'content': text,
                        'importance': 0.7,
                        'confidence': 0.9,
                        'tags': ['user_fact', indicator]
                    })
                    memory_created = True
                    break
        
        # If no specific type detected, create a general experience memory
        if not memory_created and not extracted:
            extracted.append({
                'type': MemoryType.EXPERIENCE,
                'content': text,
                'importance': 0.4,
                'confidence': 0.6,
                'tags': ['general', 'experience']
            })
        
        return extracted
    
    def _find_associations(self, memory: Memory) -> List[str]:
        """Find memories associated with the given memory"""
        # Search for memories with similar tags or content
        similar_memories = []
        
        # Tag-based associations
        if memory.tags:
            tag_matches = self.db.search_memories(tags=memory.tags, limit=self.max_associations)
            similar_memories.extend(tag_matches)
        
        # Content-based associations (simple keyword matching)
        keywords = self._extract_keywords(memory.content)
        for keyword in keywords[:3]:  # Limit to top 3 keywords
            content_matches = self.db.search_memories(query=keyword, limit=3)
            similar_memories.extend(content_matches)
        
        # Remove duplicates and self-references
        associations = []
        for mem in similar_memories:
            if mem.id != memory.id and mem.id not in associations:
                associations.append(mem.id)
                if len(associations) >= self.max_associations:
                    break
        
        return associations
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text (simplified implementation)"""
        # Simple keyword extraction (in practice, would use NLP libraries)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'cannot', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these', 'those'}
        
        words = text.lower().split()
        keywords = [word.strip('.,!?;:"()[]') for word in words if word not in stop_words and len(word) > 2]
        
        # Return most frequent keywords (simplified)
        return list(set(keywords))[:10]
    
    def _calculate_relevance_score(self, memory: Memory, query: str) -> float:
        """Calculate relevance score for a memory given a query"""
        score = 0.0
        
        # Base importance score
        score += memory.importance * 0.4
        
        # Reinforcement score (how often it's been accessed)
        score += min(memory.reinforcement_count / 10.0, 0.3)
        
        # Recency score (more recent = higher score)
        days_old = (datetime.now() - memory.timestamp).days
        recency_score = max(0, 1 - (days_old / 30.0)) * 0.2
        score += recency_score
        
        # Content relevance (simple keyword matching)
        query_keywords = set(self._extract_keywords(query))
        memory_keywords = set(self._extract_keywords(memory.content))
        content_overlap = len(query_keywords.intersection(memory_keywords))
        if query_keywords:
            content_score = (content_overlap / len(query_keywords)) * 0.1
            score += content_score
        
        return score
    
    def save_conversation_log(self, conversation: ConversationLog) -> bool:
        """Save conversation log to file"""
        try:
            timestamp = conversation.start_time.strftime("%Y-%m-%d_%H%M%S")
            filename = f"conversation_{timestamp}.log"
            filepath = self.conversations_path / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(conversation.model_dump(), f, indent=2, default=str)
            
            logging.info(f"Saved conversation log: {filename}")
            return True
        except Exception as e:
            logging.error(f"Error saving conversation log: {e}")
            return False

    def get_recent_conversation_history(self, conversation_id: str = None, max_exchanges: int = 5) -> List[Dict[str, str]]:
        """Get recent conversation history for context"""
        try:
            # Get recent memories from this conversation
            recent_memories = self.db.search_memories(
                limit=max_exchanges * 10  # Get more recent memories to filter from
            )
            
            # Organize into conversation pairs chronologically
            conversation_pairs = []
            temp_exchanges = []
            
            # Sort by timestamp to process chronologically
            for memory in sorted(recent_memories, key=lambda m: m.timestamp):
                if memory.source == MemorySource.USER_INPUT:
                    # Start a new exchange
                    temp_exchanges.append({'user': memory.content, 'timestamp': memory.timestamp})
                elif memory.source == MemorySource.AI_REASONING and temp_exchanges:
                    # Complete the exchange
                    last_exchange = temp_exchanges[-1]
                    last_exchange['ai'] = memory.content
                    conversation_pairs.append(last_exchange)
                    
                    if len(conversation_pairs) >= max_exchanges:
                        break
            
            # Return most recent exchanges (reverse to show recent first)
            return list(reversed(conversation_pairs))
            
        except Exception as e:
            logging.error(f"Error getting conversation history: {e}")
            return []
    
    def load_conversation_log(self, conversation_id: str) -> Optional[ConversationLog]:
        """Load conversation log by ID"""
        try:
            # Search through conversation files
            for log_file in self.conversations_path.glob("conversation_*.log"):
                with open(log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('conversation_id') == conversation_id:
                        return ConversationLog(**data)
            return None
        except Exception as e:
            logging.error(f"Error loading conversation log: {e}")
            return None
