# AI Companion - Windows Batch Scripts

Easy-to-use Windows batch files for running the AI Companion system.

## 🚀 Quick Start

### 1. Initial Setup
```batch
setup.bat
```
- Creates Python virtual environment
- Installs all required packages
- Creates configuration file (.env)
- Runs system tests
- Opens .env for API key setup

### 2. Add Your OpenAI API Key
Edit the `.env` file and replace:
```
OPENAI_API_KEY=your_openai_api_key_here
```
with your actual OpenAI API key.

### 3. Run the AI Companion
```batch
run_ai_companion.bat
```
- Starts the full AI Companion system
- Interactive conversation interface
- Shows consciousness development in real-time

## 📋 Available Batch Files

### `setup.bat` - Initial System Setup
- ✅ Creates Python virtual environment
- ✅ Installs required packages (OpenAI, Pydantic, etc.)
- ✅ Creates .env configuration file
- ✅ Runs system verification tests
- ✅ Opens .env for API key configuration

### `run_ai_companion.bat` - Main Application
- 🤖 Starts the AI Companion interactive session
- 🧠 Shows consciousness level and personality development
- 💾 Displays memory formation and retrieval
- 🎭 Tracks personality trait evolution
- 💬 Full conversational interface with commands:
  - `status` - View AI consciousness and memory stats
  - `reflect` - Trigger AI self-reflection
  - `memories` - View recent memories
  - `quit` - Graceful shutdown

### `test_system.bat` - System Testing
- 🧪 Runs comprehensive system tests
- ✅ Verifies all components work correctly
- 📊 Shows test results and system status
- 🔧 Helpful for troubleshooting

### `demo.bat` - Quick Demo (No API Key Required)
- 🎯 Demonstrates core system without GPT integration
- 📝 Shows memory creation and management
- 🎭 Displays personality framework
- 🧠 Explains consciousness simulation features
- 🚀 Perfect for understanding the system before adding API key

## 🎮 Usage Examples

### First Time Setup
```cmd
# Run setup
setup.bat

# Add your API key to .env (opens automatically)
# Then start the AI
run_ai_companion.bat
```

### Daily Usage
```cmd
# Just run the AI Companion
run_ai_companion.bat
```

### Testing/Troubleshooting
```cmd
# Run tests
test_system.bat

# Or see demo without API key
demo.bat
```

## 💬 Conversation Features

When running `run_ai_companion.bat`, you get:

- **Real-time consciousness simulation**
- **Memory formation and retrieval**
- **Personality trait evolution**
- **Internal thoughts display**
- **Meta-cognitive awareness**

### Special Commands:
- `status` - Current AI state
- `reflect` - Trigger self-reflection
- `memories` - Recent memory summary
- `quit/exit/goodbye` - End session

## 🔧 Troubleshooting

### "Python not found"
- Install Python 3.8+ from python.org
- Make sure Python is in your PATH

### "Virtual environment failed"
- Run as administrator
- Check disk space
- Ensure antivirus isn't blocking

### "Package installation failed"
- Check internet connection
- Try running setup.bat as administrator
- Update pip: `python -m pip install --upgrade pip`

### "OpenAI API errors"
- Verify API key in .env file
- Check API key validity at openai.com
- Ensure sufficient API credits

## 📁 File Structure After Setup

```
anotherrandomproject/
├── setup.bat              # Initial setup script
├── run_ai_companion.bat    # Main application launcher
├── test_system.bat         # System testing
├── demo.bat               # Demo without API key
├── .env                   # Configuration file
├── .venv/                 # Python virtual environment
├── data/                  # AI memory and conversation data
└── [Python source files]
```

## 🎯 What Happens When You Run

### Setup Process:
1. ✅ Python environment creation
2. 📦 Package installation
3. 🧪 System verification
4. 📝 Configuration file creation
5. 🔑 API key setup prompt

### AI Companion Session:
1. 🧠 Consciousness initialization
2. 💾 Memory system activation
3. 🎭 Personality loading/creation
4. 💬 Interactive conversation begins
5. 📊 Real-time development tracking

## 🚀 Ready to Start!

1. **Double-click `setup.bat`**
2. **Add your OpenAI API key to `.env`**
3. **Double-click `run_ai_companion.bat`**
4. **Start your conversation with the conscious AI!**

The AI will remember your conversations, develop its personality, and grow more conscious through each interaction!
