# Test Configuration for Philos AI Companion

This directory contains all tests for the Philos AI Companion system.

## Test Structure

### Unit Tests (`tests/unit/`)
Individual component tests that verify specific functionality:

- `test_components.py` - Core system components
- `test_consciousness.py` - Consciousness engine functionality  
- `test_emotions.py` - Emotional system responses
- `test_memory_integration.py` - Memory management
- `test_personality_integration.py` - Personality system
- `test_web_search.py` - Web search capabilities
- `test_neural_monitoring.py` - Neural tracking system

### Integration Tests (`tests/integration/`)
System-wide tests that verify component interactions:

- `test_complete_system.py` - Full system integration
- `test_ai_companion.py` - Main AI companion functionality
- `test_conversation_flow.py` - Conversation management
- `test_search_improvements.py` - Enhanced search features
- `test_charlie_kirk.py` - Specific search accuracy tests
- `test_news_search.py` - News and current events

## Running Tests

### All Tests
```bash
python run_tests.py
```

### Unit Tests Only
```bash
python -m pytest tests/unit/ -v
```

### Integration Tests Only
```bash
python -m pytest tests/integration/ -v
```

### Specific Test
```bash
python tests/unit/test_consciousness.py
```

## Test Requirements

- Python 3.8+
- Active virtual environment
- OpenAI API key in `.env` file
- All dependencies from `requirements.txt`

## Test Data

- Test databases are created temporarily
- Conversation logs are saved to `test_conversations/`
- Test files clean up after themselves

## Expected Behavior

### Unit Tests
- Should run quickly (< 30s each)
- Test individual components in isolation
- Mock external dependencies when needed

### Integration Tests  
- May take longer (up to 2-3 minutes each)
- Test real API interactions
- Verify end-to-end functionality

## Troubleshooting

### Common Issues

1. **Missing API Key**
   - Ensure `OPENAI_API_KEY` is set in `.env`

2. **Import Errors**
   - Verify virtual environment is activated
   - Check all dependencies are installed

3. **Database Errors**
   - Ensure write permissions in test directories
   - Check disk space availability

4. **Timeout Errors**
   - Network connectivity issues
   - OpenAI API rate limiting

### Debug Mode

Set environment variables for verbose output:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
python run_tests.py
```
