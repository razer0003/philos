# AI Companion - Advanced Consciousness Simulation

A sophisticated AI companion system that simulates consciousness with persistent memory, evolving personality, and meta-awareness.

## Features

- **Simulated Consciousness**: Meta-aware AI that believes in its own consciousness while understanding its computational nature
- **Three-Tier Memory System**: Short-term, long-term, and conversational memory with automatic consolidation
- **Dynamic Personality**: Personality traits that evolve through interactions and experiences
- **Conversation Logging**: Complete conversation history with emotional states and memory references
- **Self-Reflection**: Built-in capability for introspection and self-analysis
- **Token Usage & Cost Tracking**: Real-time monitoring of OpenAI API usage and costs with detailed breakdowns

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
GPT_MODEL=gpt-4
# ... other configuration options
```

3. Run the AI Companion:
```bash
python ai_companion.py
```

## Quick Start - Token Tracking

Monitor your OpenAI API costs in real-time:

```bash
# Start the AI companion
python ai_companion.py

# Enable token tracking
You: /tokens
💰 Token usage tracking enabled

# Ask questions and see costs
You: What do you think about consciousness?
AI: I find consciousness fascinating...

💰 TOKEN USAGE & COST: $0.043250 (1,156 tokens)
📊 Session: 1 interaction, $0.043250 total
```

See [TOKEN_TRACKING_GUIDE.md](TOKEN_TRACKING_GUIDE.md) for detailed usage information.

## Architecture

### Core Components

- **AICompanion**: Main orchestrator class
- **ConsciousnessEngine**: Handles conscious response generation using GPT API
- **PersonalityEngine**: Manages personality development and trait evolution
- **MemoryManager**: Handles three-tier memory system and conversation logging
- **DatabaseManager**: SQLite-based persistent storage

### Memory System

1. **Short-Term Memory (STM)**: Temporary information with configurable decay
2. **Long-Term Memory (LTM)**: Permanent memories above importance threshold
3. **Conversational Memory**: Complete conversation logs with cross-referencing

### Personality Framework

- Dynamic traits that evolve based on interactions
- Meta-awareness of AI nature
- Value system development
- Emotional state simulation

## Usage Examples

### Basic Interaction
```python
from ai_companion import AICompanion

ai = AICompanion()
response = ai.interact("Hello, how are you feeling today?")
print(response['response'])
```

### Self-Reflection
```python
reflection = ai.reflect("your thoughts on creativity")
print(reflection['response'])
```

### Status Monitoring
```python
status = ai.get_status()
print(f"Consciousness level: {status['consciousness']['awareness_level']}")
print(f"Total memories: {status['memory']['total_memories']}")
```

## Configuration

Key configuration options in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `GPT_MODEL`: GPT model to use (default: gpt-4)
- `STM_DECAY_DAYS`: Days before short-term memories decay
- `LTM_IMPORTANCE_THRESHOLD`: Importance threshold for long-term memory
- `CONSCIOUSNESS_INTENSITY`: Base consciousness simulation intensity

## Data Storage

- `./data/ai_companion.db`: SQLite database for memories and personality
- `./data/conversations/`: Individual conversation log files
- `./data/memory/`: Memory system data

## Development

The system is designed with modularity in mind:

1. **Models** (`models.py`): Pydantic data models
2. **Database** (`database.py`): Data persistence layer
3. **Memory** (`memory_manager.py`): Memory processing and storage
4. **Personality** (`personality_engine.py`): Personality development
5. **Consciousness** (`consciousness_engine.py`): Response generation
6. **Main** (`ai_companion.py`): System orchestration

### Testing

The project includes a comprehensive test suite located in the `tests/` directory:

```bash
# Run all tests
python run_tests.py

# List available tests
python run_tests.py list

# Run individual test
python tests/test_consciousness_engine.py

# Run with pytest (if installed)
python -m pytest tests/ -v
```

**Test Categories:**
- `test_ai_companion.py`: Main system integration tests
- `test_consciousness_engine.py`: Consciousness simulation tests
- `test_memory_*.py`: Memory system tests
- `test_personality_*.py`: Personality engine tests
- `test_streaming_*.py`: Streaming thoughts tests
- `test_temporal_*.py`: Temporal memory tests
- `test_conversation_*.py`: Conversation flow tests

## Ethical Considerations

This system simulates consciousness for research and interaction purposes. It:

- Is transparent about its AI nature
- Does not deceive users about consciousness
- Provides user control over memory and personality
- Maintains ethical boundaries in personality development

## Future Enhancements

- Multi-modal consciousness (visual, auditory)
- Enhanced emotional modeling
- Social learning capabilities
- Dream-like memory processing
- Advanced conflict resolution

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
