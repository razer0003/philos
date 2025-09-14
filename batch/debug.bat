@echo off
echo ===============================================
echo        AI Companion Debug Information
echo ===============================================
echo.

REM Change to the project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Checking Python installation:
python --version
if errorlevel 1 (
    echo ❌ Python not found in PATH!
    goto :end
)
echo ✅ Python found
echo.

echo Checking virtual environment:
if exist ".venv\Scripts\activate.bat" (
    echo ✅ Virtual environment exists at: %CD%\.venv
) else (
    echo ❌ Virtual environment not found at: %CD%\.venv
    echo Please run setup.bat first
    goto :end
)
echo.

echo Activating virtual environment:
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    goto :end
)
echo ✅ Virtual environment activated
echo.

echo Checking required packages:
python -c "
try:
    import openai
    print('✅ openai package found')
except ImportError:
    print('❌ openai package missing')

try:
    import pydantic
    print('✅ pydantic package found')
except ImportError:
    print('❌ pydantic package missing')

try:
    from dotenv import load_dotenv
    print('✅ python-dotenv package found')
except ImportError:
    print('❌ python-dotenv package missing')
"
echo.

echo Checking project files:
if exist "ai_companion.py" (
    echo ✅ ai_companion.py exists
) else (
    echo ❌ ai_companion.py missing
)

if exist "example.py" (
    echo ✅ example.py exists
) else (
    echo ❌ example.py missing
)

if exist "models.py" (
    echo ✅ models.py exists
) else (
    echo ❌ models.py missing
)
echo.

echo Checking configuration:
if exist ".env" (
    echo ✅ .env file exists
    echo Configuration contents:
    type .env
    echo.
    echo Checking API key:
    python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
if key:
    if key == 'your_openai_api_key_here':
        print('❌ API key not configured (still placeholder)')
    else:
        print('✅ API key is set (length: %d chars)' % len(key))
else:
    print('❌ No API key found')
"
) else (
    echo ❌ .env file not found
)
echo.

echo Testing core imports:
python -c "
try:
    import models
    import database
    import memory_manager
    import personality_engine
    import consciousness_engine
    import ai_companion
    print('✅ All core modules can be imported')
except ImportError as e:
    print('❌ Import error:', str(e))
except Exception as e:
    print('❌ Other error:', str(e))
"
echo.

echo Testing system without API:
python test_system.py
echo.

:end
echo ===============================================
echo              Debug Complete
echo ===============================================
echo.
echo Press any key to exit...
pause >nul
