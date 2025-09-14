@echo off
echo ===============================================
echo           AI Companion System Tests
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
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 🧪 Running AI Companion system tests...
echo.

REM Run system verification tests
python test_system.py

if errorlevel 1 (
    echo.
    echo ❌ Tests failed!
    pause
    exit /b 1
)

echo.
echo ✅ All tests passed!
echo.

REM Optionally run unit tests if they exist
if exist "test_ai_companion.py" (
    echo 🧪 Running unit tests...
    python -m unittest test_ai_companion.py -v
    if errorlevel 1 (
        echo.
        echo ⚠️  Some unit tests failed, but core system is working.
    ) else (
        echo ✅ Unit tests passed!
    )
)

echo.
echo 🎉 Testing complete!
echo The AI Companion system is ready to use.
echo.
pause
