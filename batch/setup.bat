@echo off
echo ===============================================
echo        AI Companion System Setup
echo ===============================================
echo.

REM Change to the project directory
cd /d "%~dp0"

echo 🔧 Setting up AI Companion development environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo.
    echo 📦 Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo.
echo 📦 Installing required packages...
pip install openai>=1.0.0 pydantic>=2.0.0 python-dotenv>=1.0.0

if errorlevel 1 (
    echo ❌ Failed to install packages!
    pause
    exit /b 1
)

echo.
echo ✅ Packages installed successfully!

REM Run system tests
echo.
echo 🧪 Running system tests...
python test_system.py

if errorlevel 1 (
    echo ❌ System tests failed!
    pause
    exit /b 1
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo 📝 Creating configuration file...
    python -c "
import os
env_content = '''# AI Companion Environment Variables
OPENAI_API_KEY=your_openai_api_key_here
GPT_MODEL=gpt-5-mini
MAX_TOKENS=2048
TEMPERATURE=0.7

# Database Configuration
DB_PATH=./data/ai_companion.db
CONVERSATIONS_PATH=./data/conversations
MEMORY_PATH=./data/memory

# Memory Configuration
STM_DECAY_DAYS=7
LTM_IMPORTANCE_THRESHOLD=0.7
MAX_CONVERSATION_CONTEXT=10

# Personality Configuration
PERSONALITY_UPDATE_FREQUENCY=0.1
CONSCIOUSNESS_INTENSITY=0.8'''
with open('.env', 'w') as f:
    f.write(env_content)
print('✅ .env file created')
"
)

echo.
echo ===============================================
echo            Setup Complete! 🎉
echo ===============================================
echo.
echo Next steps:
echo 1. Edit .env and add your OpenAI API key
echo 2. Run run_ai_companion.bat to start the AI
echo.
echo Opening .env file for editing...
notepad .env
echo.
echo After adding your API key, you can run:
echo - run_ai_companion.bat (main application)
echo - test_system.bat (run tests)
echo.
pause
