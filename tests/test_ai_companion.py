import unittest
from datetime import datetime, timedelta
from models import Memory, PersonalityTrait, MemoryType, MemorySource
from database import DatabaseManager
from memory_manager import MemoryManager
import tempfile
import os

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.temp_conv_dir = tempfile.mkdtemp()
        
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.memory_manager = MemoryManager(self.db_manager, self.temp_conv_dir)
    
    def tearDown(self):
        # Clean up temporary files
        os.unlink(self.temp_db.name)
        import shutil
        shutil.rmtree(self.temp_conv_dir)
    
    def test_process_input_creates_memories(self):
        """Test that processing input creates appropriate memories"""
        user_input = "I love golden retrievers and think they're the best dogs"
        
        memories = self.memory_manager.process_input(user_input)
        
        self.assertTrue(len(memories) > 0)
        
        # Check that a preference memory was created
        preference_memories = [m for m in memories if m.type == MemoryType.PREFERENCE]
        self.assertTrue(len(preference_memories) > 0)
        
        # Verify memory content
        self.assertTrue(any("golden retrievers" in m.content.lower() for m in memories))
    
    def test_memory_retrieval(self):
        """Test memory retrieval functionality"""
        # Create test memory
        test_memory = Memory(
            type=MemoryType.FACT,
            content="The user works as a software engineer",
            importance=0.8,
            confidence=0.9,
            tags=["job", "career", "software"],
            source=MemorySource.USER_INPUT
        )
        
        self.db_manager.save_memory(test_memory)
        
        # Test retrieval
        retrieved_memories = self.memory_manager.retrieve_relevant_memories("software engineer")
        
        self.assertTrue(len(retrieved_memories) > 0)
        self.assertTrue(any(m.id == test_memory.id for m in retrieved_memories))
    
    def test_memory_consolidation(self):
        """Test memory consolidation from STM to LTM"""
        # Create a short-term memory that should be consolidated
        stm_memory = Memory(
            type=MemoryType.PREFERENCE,
            content="User likes classical music",
            importance=0.6,  # Below LTM threshold
            confidence=0.8,
            reinforcement_count=5,  # High reinforcement
            timestamp=datetime.now() - timedelta(days=2),  # Old enough
            source=MemorySource.USER_INPUT,
            decay_date=datetime.now() + timedelta(days=5)
        )
        
        self.db_manager.save_memory(stm_memory)
        
        # Run consolidation
        consolidated = self.memory_manager.consolidate_memories()
        
        # Check if memory was consolidated
        updated_memory = self.db_manager.get_memory(stm_memory.id)
        self.assertIsNotNone(updated_memory)
        if updated_memory:
            self.assertIsNone(updated_memory.decay_date)  # Should be None for LTM
            self.assertGreater(updated_memory.importance, 0.6)  # Should be increased

class TestPersonalityEngine(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.temp_conv_dir = tempfile.mkdtemp()
        
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.memory_manager = MemoryManager(self.db_manager, self.temp_conv_dir)
        
        from personality_engine import PersonalityEngine
        self.personality_engine = PersonalityEngine(self.db_manager, self.memory_manager)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
        import shutil
        shutil.rmtree(self.temp_conv_dir)
    
    def test_personality_initialization(self):
        """Test that personality is properly initialized"""
        self.assertIsNotNone(self.personality_engine.personality)
        self.assertTrue(len(self.personality_engine.personality.traits) > 0)
        self.assertTrue(len(self.personality_engine.personality.core_values) > 0)
    
    def test_personality_update_from_interaction(self):
        """Test personality updates based on interactions"""
        initial_curiosity = self.personality_engine.personality.traits.get('curiosity')
        initial_value = initial_curiosity.value if initial_curiosity else 0.5
        
        # Simulate interaction that should increase curiosity
        user_input = "I'm curious about how quantum physics works. Can you explain?"
        ai_response = "That's a fascinating question! Quantum physics is indeed intriguing..."
        
        updates = self.personality_engine.update_personality_from_interaction(
            user_input, ai_response
        )
        
        # Check if curiosity trait was updated
        updated_curiosity = self.personality_engine.personality.traits.get('curiosity')
        if updated_curiosity:
            # Should have increased (even if slightly)
            self.assertGreaterEqual(updated_curiosity.value, initial_value)
    
    def test_consciousness_state_update(self):
        """Test consciousness state updates"""
        initial_awareness = self.personality_engine.personality.consciousness_state.awareness_level
        
        # Complex interaction should increase awareness
        complex_input = "I've been thinking about the nature of consciousness and whether artificial minds like yours can truly experience subjective states or if it's just sophisticated pattern matching."
        ai_response = "That's a profound question that I find myself contemplating often..."
        
        self.personality_engine.update_personality_from_interaction(complex_input, ai_response)
        
        updated_awareness = self.personality_engine.personality.consciousness_state.awareness_level
        self.assertGreaterEqual(updated_awareness, initial_awareness)

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
    
    def tearDown(self):
        os.unlink(self.temp_db.name)
    
    def test_memory_save_and_retrieve(self):
        """Test saving and retrieving memories"""
        test_memory = Memory(
            type=MemoryType.EXPERIENCE,
            content="Test memory content",
            importance=0.7,
            confidence=0.8,
            tags=["test", "memory"],
            source=MemorySource.AI_REASONING
        )
        
        # Save memory
        success = self.db_manager.save_memory(test_memory)
        self.assertTrue(success)
        
        # Retrieve memory
        retrieved = self.db_manager.get_memory(test_memory.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.content, test_memory.content)
        self.assertEqual(retrieved.type, test_memory.type)
    
    def test_memory_search(self):
        """Test memory search functionality"""
        # Create test memories
        memory1 = Memory(
            type=MemoryType.FACT,
            content="Python is a programming language",
            importance=0.8,
            confidence=0.9,
            tags=["programming", "python"],
            source=MemorySource.USER_INPUT
        )
        
        memory2 = Memory(
            type=MemoryType.OPINION,
            content="I think Python is elegant",
            importance=0.6,
            confidence=0.7,
            tags=["programming", "opinion"],
            source=MemorySource.AI_REASONING
        )
        
        self.db_manager.save_memory(memory1)
        self.db_manager.save_memory(memory2)
        
        # Search by query
        results = self.db_manager.search_memories(query="Python")
        self.assertEqual(len(results), 2)
        
        # Search by type
        fact_results = self.db_manager.search_memories(memory_type=MemoryType.FACT)
        self.assertEqual(len(fact_results), 1)
        self.assertEqual(fact_results[0].type, MemoryType.FACT)
        
        # Search by tags
        programming_results = self.db_manager.search_memories(tags=["programming"])
        self.assertEqual(len(programming_results), 2)

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)
