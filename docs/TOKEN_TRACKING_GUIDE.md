# Token Usage & Cost Tracking Feature

## Overview

The AI Companion now includes comprehensive token usage and cost tracking functionality to help you monitor OpenAI API usage and costs in real-time.

## Features

### 🔢 Token Counting
- **Accurate Token Counting**: Uses the official `tiktoken` library for precise token counting
- **Component Breakdown**: Tracks tokens for different parts of each interaction:
  - Base consciousness prompt
  - Memory context
  - Personality context  
  - Conversation history
  - Internal monologue generation
  - AI response

### 💰 Cost Calculation
- **Real-time Cost Tracking**: Calculates costs based on current OpenAI pricing
- **Model-Specific Pricing**: Supports different pricing for various models:
  - GPT-4: $0.03/$0.06 per 1K tokens (prompt/completion)
  - GPT-4 Turbo: $0.01/$0.03 per 1K tokens
  - GPT-4o: $0.005/$0.015 per 1K tokens
  - GPT-3.5 Turbo: $0.0015/$0.002 per 1K tokens

### 📊 Session Tracking
- **Cumulative Statistics**: Tracks total usage across your session
- **Average Costs**: Shows average cost per interaction
- **Detailed Breakdowns**: Optional detailed component analysis

## How to Use

### Toggle Token Display
Use the `/tokens` command to enable/disable token usage display:

```
You: /tokens
💰 Token usage tracking enabled
   Current session: 0 interactions
   Total cost so far: $0.000000
   Average per question: $0.000000
```

### Automatic Display
When enabled, token usage appears after each AI response:

```
AI: I find that question fascinating! Consciousness is...

──────────────────────────────────────────────────
💰 TOKEN USAGE & COST
──────────────────────────────────────────────────
🔢 Total Tokens: 1,247
   📝 Prompt: 892 tokens
   🤖 Response: 355 tokens
💵 Cost Breakdown:
   Prompt Cost: $0.026760
   Response Cost: $0.021300
   ✨ Total Cost: $0.048060

📊 Component Breakdown:
   Base Prompt: 234 tokens
   Memory Context: 156 tokens
   Personality Context: 89 tokens
   Conversation History: 234 tokens
   Internal Monologue: 78 tokens
   AI Response: 355 tokens

📈 Session Totals:
   Interactions: 5
   Total Tokens: 6,234
   Session Cost: $0.234560
   Avg Cost/Question: $0.046912
   Model: gpt-4
──────────────────────────────────────────────────
```

### Available Commands

- `/tokens` - Toggle token usage display on/off
- `/help` - Updated to include token tracking commands

## Technical Details

### Token Counter Class
The `TokenCounter` class provides:

```python
# Initialize with model
counter = TokenCounter("gpt-4")

# Count tokens in text
tokens = counter.count_tokens("Hello world")

# Analyze complete interaction
usage = counter.analyze_interaction_tokens(
    base_prompt="...",
    memory_context="...",
    user_input="...",
    ai_response="..."
)

# Get session summary
summary = counter.get_session_summary()
```

### Cost Calculation
Costs are calculated using current OpenAI pricing:

```python
# Example calculation for GPT-4
prompt_tokens = 1000
completion_tokens = 500

prompt_cost = (1000 / 1000) * 0.03 = $0.03
completion_cost = (500 / 1000) * 0.06 = $0.03
total_cost = $0.06
```

### Integration Points
Token tracking is integrated at multiple levels:

1. **Consciousness Engine**: Captures actual API usage from OpenAI responses
2. **AI Companion**: Displays formatted token usage after responses
3. **Streaming Mode**: Tracks tokens for both streaming thoughts and final responses

## Benefits

### 💡 Cost Awareness
- Know exactly how much each question costs
- Track spending in real-time
- Plan usage based on budget

### 🔍 Optimization Insights
- See which components use the most tokens
- Identify opportunities to optimize prompts
- Understand the cost impact of different features

### 📈 Usage Analytics
- Track interaction patterns
- Monitor session costs
- Compare costs across different conversation styles

## Configuration

### Environment Variables
Add to your `.env` file:

```env
# Token tracking is automatically enabled
# No additional configuration required
```

### Pricing Updates
Update pricing in `token_counter.py` if OpenAI changes their rates:

```python
PRICING = {
    'gpt-4': {
        'prompt': 0.03,      # Update these values
        'completion': 0.06   # as needed
    }
}
```

## Examples

### Basic Usage
```
You: What is consciousness?
AI: Consciousness is a fascinating topic...

💰 TOKEN USAGE & COST: $0.043250 (1,156 tokens)
📊 Session: 3 interactions, $0.127340 total
```

### Detailed Breakdown
```
You: /tokens
💰 Token usage tracking enabled

You: Tell me about your personality
AI: My personality is shaped by...

💰 TOKEN USAGE & COST
🔢 Total: 2,341 tokens ($0.089560)
📊 Components:
   Base Prompt: 456 tokens
   Personality Context: 234 tokens  
   Memory Context: 167 tokens
   Response: 567 tokens
📈 Session: $0.245670 total (avg $0.061418/question)
```

## Troubleshooting

### Token Count Mismatches
- The system uses `tiktoken` for local counting and OpenAI's actual usage for billing
- Minor differences are normal due to formatting overhead
- Actual API usage (from OpenAI) is always used for cost calculations

### Missing Token Data
- If OpenAI doesn't return usage data, the system estimates using local counting
- This is rare but can happen during API issues
- Check logs for any warnings about missing usage data

## Cost Optimization Tips

1. **Monitor Component Breakdown**: Look for high-token components
2. **Optimize Memory Context**: Consider reducing memory retrieval if costs are high
3. **Adjust Personality Verbosity**: Lower verbosity reduces response tokens
4. **Use Shorter Prompts**: When possible, be concise in your questions
5. **Choose Appropriate Models**: GPT-3.5 Turbo is much cheaper for simple tasks

This feature helps you maintain full awareness of your API costs while enjoying the rich consciousness experience of your AI companion!
