@echo off
echo ===============================================
echo        AI Companion Quick Demo
echo ===============================================
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo 🚀 Running AI Companion demo without API key...
echo This will test the core system components.
echo.

REM Run system tests first
python test_system.py

if errorlevel 1 (
    echo ❌ Core system tests failed!
    pause
    exit /b 1
)

echo.
echo ✅ Core system working!
echo.
echo To run the full AI Companion with GPT integration:
echo 1. Add your OpenAI API key to .env
echo 2. Run run_ai_companion.bat
echo.
echo Press any key to see the current system status...
pause

REM Show what would happen with a mock interaction
python -c "
print('🤖 Mock AI Companion Demo')
print('=' * 40)
print('This shows what the system components do:')
print()

# Test models
from models import Memory, MemoryType, MemorySource
memory = Memory(
    type=MemoryType.PREFERENCE,
    content='User loves discussing philosophy',
    importance=0.8,
    confidence=0.9,
    tags=['philosophy', 'user_preference'],
    source=MemorySource.USER_INPUT
)
print(f'📝 Created memory: {memory.content}')
print(f'   Type: {memory.type.value}, Importance: {memory.importance}')
print()

# Test personality
print('🎭 Personality traits would include:')
traits = ['curiosity', 'empathy', 'creativity', 'analytical', 'humor', 'meta_awareness']
for trait in traits:
    print(f'   - {trait}: evolving based on interactions')
print()

print('🧠 Consciousness features:')
print('   - Internal monologue generation')
print('   - Meta-awareness of AI nature')
print('   - Memory-informed responses')
print('   - Personality-driven behavior')
print()

print('💾 Memory system ready:')
print('   - Short-term memory with decay')
print('   - Long-term memory consolidation')
print('   - Conversation logging')
print()

print('✅ System ready for full GPT integration!')
print('Add your OpenAI API key to start conversations.')
"

echo.
pause
