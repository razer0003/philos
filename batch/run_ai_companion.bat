@echo off
echo ===============================================
echo           AI Companion Launcher
echo ===============================================
echo.

REM Change to the project directory
cd /d "%~dp0"
echo 📁 Current directory: %CD%

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Looking for: %CD%\.venv\Scripts\activate.bat
    echo Please run setup.bat first to create the virtual environment.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    echo Please try running setup.bat again.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo ✅ Virtual environment activated

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Configuration file (.env) not found!
    echo Expected location: %CD%\.env
    echo Running example.py to create it...
    echo.
    python example.py
    if errorlevel 1 (
        echo ❌ Failed to create .env file!
        echo Please check if Python is working correctly.
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo.
    echo Please edit .env with your OpenAI API key and run this script again.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo ✅ Configuration file found

REM Check if OpenAI API key is set
echo 🔍 Checking configuration...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('OPENAI_API_KEY'); print('API key found:', 'Yes' if key and key != 'your_openai_api_key_here' else 'No'); exit(0 if key and key != 'your_openai_api_key_here' else 1)" 2>nul
if errorlevel 1 (
    echo ❌ OpenAI API key not configured!
    echo Please edit .env and add your OpenAI API key.
    echo Current .env location: %CD%\.env
    echo.
    echo Opening .env file for editing...
    if exist "notepad.exe" (
        start notepad .env
    ) else (
        echo Please manually edit .env file
    )
    echo.
    echo After adding your API key, run this script again.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo ✅ Configuration looks good!
echo.

REM Run the AI Companion
echo 🚀 Starting AI Companion...
echo.
python example.py
if errorlevel 1 (
    echo.
    echo ❌ AI Companion encountered an error!
    echo Check the error messages above for details.
    echo.
    echo Common issues:
    echo - Invalid OpenAI API key
    echo - Missing packages (run setup.bat)
    echo - Network connection issues
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

echo.
echo 👋 AI Companion session ended normally.
echo.
echo Press any key to exit...
pause >nul
