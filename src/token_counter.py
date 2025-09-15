"""
Token counter and cost calculator for OpenAI API usage.

This module provides utilities to track token usage and calculate costs
for different OpenAI models.
"""

import tiktoken
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class TokenUsage:
    """Token usage statistics for a single interaction"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    
    # Breakdown by component
    base_prompt_tokens: int = 0
    memory_context_tokens: int = 0
    personality_context_tokens: int = 0
    conversation_history_tokens: int = 0
    internal_monologue_tokens: int = 0
    response_tokens: int = 0
    
    # Cost calculation
    prompt_cost: float = 0.0
    completion_cost: float = 0.0
    total_cost: float = 0.0
    
    # Metadata
    model: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SessionTokens:
    """Cumulative token usage for a session"""
    total_interactions: int = 0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    interactions: List[TokenUsage] = field(default_factory=list)
    
    def add_interaction(self, token_usage: TokenUsage):
        """Add a new interaction's token usage"""
        self.interactions.append(token_usage)
        self.total_interactions += 1
        self.total_prompt_tokens += token_usage.prompt_tokens
        self.total_completion_tokens += token_usage.completion_tokens
        self.total_tokens += token_usage.total_tokens
        self.total_cost += token_usage.total_cost

class TokenCounter:
    """Token counter with cost calculation for OpenAI models"""
    
    # OpenAI pricing per 1K tokens (as of 2025)
    PRICING = {
        'gpt-4': {
            'prompt': 0.03,      # $0.03 per 1K prompt tokens
            'completion': 0.06   # $0.06 per 1K completion tokens
        },
        'gpt-4-turbo': {
            'prompt': 0.01,      # $0.01 per 1K prompt tokens
            'completion': 0.03   # $0.03 per 1K completion tokens
        },
        'gpt-4o': {
            'prompt': 0.005,     # $0.005 per 1K prompt tokens
            'completion': 0.015  # $0.015 per 1K completion tokens
        },
        'gpt-5-mini': {
            'prompt': 0.003,     # $0.003 per 1K prompt tokens (estimated)
            'completion': 0.012  # $0.012 per 1K completion tokens (estimated)
        },
        'gpt-5-nano': {
            'prompt': 0.001,     # $0.001 per 1K prompt tokens (estimated)
            'completion': 0.004  # $0.004 per 1K completion tokens (estimated)
        },
        'gpt-3.5-turbo': {
            'prompt': 0.0015,    # $0.0015 per 1K prompt tokens
            'completion': 0.002  # $0.002 per 1K completion tokens
        }
    }
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.session_tokens = SessionTokens()
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string"""
        if not text:
            return 0
        return len(self.tokenizer.encode(str(text)))
    
    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of chat messages"""
        if not messages:
            return 0
        
        total_tokens = 0
        for message in messages:
            # Count tokens for each message
            total_tokens += self.count_tokens(message.get('content', ''))
            total_tokens += 4  # Overhead for message formatting
        
        total_tokens += 2  # Overhead for assistant response
        return total_tokens
    
    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> Dict[str, float]:
        """Calculate cost for token usage"""
        pricing = self.PRICING.get(self.model, self.PRICING['gpt-4'])  # Default to GPT-4 pricing
        
        prompt_cost = (prompt_tokens / 1000) * pricing['prompt']
        completion_cost = (completion_tokens / 1000) * pricing['completion']
        total_cost = prompt_cost + completion_cost
        
        return {
            'prompt_cost': prompt_cost,
            'completion_cost': completion_cost,
            'total_cost': total_cost
        }
    
    def analyze_interaction_tokens(self, 
                                  base_prompt: str,
                                  memory_context: str = "",
                                  personality_context: str = "",
                                  conversation_history: str = "",
                                  internal_monologue: str = "",
                                  user_input: str = "",
                                  ai_response: str = "",
                                  full_prompt_tokens: int = 0,
                                  response_tokens: int = 0) -> TokenUsage:
        """Analyze token usage for a complete interaction"""
        
        # Count individual components
        base_prompt_tokens = self.count_tokens(base_prompt)
        memory_context_tokens = self.count_tokens(memory_context)
        personality_context_tokens = self.count_tokens(personality_context)
        conversation_history_tokens = self.count_tokens(conversation_history)
        internal_monologue_tokens = self.count_tokens(internal_monologue)
        user_input_tokens = self.count_tokens(user_input)
        response_tokens_counted = self.count_tokens(ai_response)
        
        # Use provided token counts if available, otherwise calculate
        prompt_tokens = full_prompt_tokens if full_prompt_tokens > 0 else (
            base_prompt_tokens + memory_context_tokens + personality_context_tokens + 
            conversation_history_tokens + user_input_tokens
        )
        
        completion_tokens = response_tokens if response_tokens > 0 else (
            response_tokens_counted + internal_monologue_tokens
        )
        
        total_tokens = prompt_tokens + completion_tokens
        
        # Calculate costs
        costs = self.calculate_cost(prompt_tokens, completion_tokens)
        
        # Create token usage record
        token_usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            base_prompt_tokens=base_prompt_tokens,
            memory_context_tokens=memory_context_tokens,
            personality_context_tokens=personality_context_tokens,
            conversation_history_tokens=conversation_history_tokens,
            internal_monologue_tokens=internal_monologue_tokens,
            response_tokens=response_tokens_counted,
            prompt_cost=costs['prompt_cost'],
            completion_cost=costs['completion_cost'],
            total_cost=costs['total_cost'],
            model=self.model
        )
        
        # Add to session tracking
        self.session_tokens.add_interaction(token_usage)
        
        return token_usage
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get session token usage summary"""
        avg_tokens_per_interaction = (
            self.session_tokens.total_tokens / max(self.session_tokens.total_interactions, 1)
        )
        
        avg_cost_per_interaction = (
            self.session_tokens.total_cost / max(self.session_tokens.total_interactions, 1)
        )
        
        return {
            'total_interactions': self.session_tokens.total_interactions,
            'total_tokens': self.session_tokens.total_tokens,
            'total_prompt_tokens': self.session_tokens.total_prompt_tokens,
            'total_completion_tokens': self.session_tokens.total_completion_tokens,
            'total_cost': self.session_tokens.total_cost,
            'average_tokens_per_interaction': avg_tokens_per_interaction,
            'average_cost_per_interaction': avg_cost_per_interaction,
            'model': self.model
        }
    
    def format_token_report(self, token_usage: TokenUsage, show_breakdown: bool = True) -> str:
        """Format a detailed token usage report"""
        lines = []
        lines.append("📊 TOKEN USAGE REPORT")
        lines.append("═" * 50)
        
        # Main statistics
        lines.append(f"Model: {token_usage.model}")
        lines.append(f"Total Tokens: {token_usage.total_tokens:,}")
        lines.append(f"  Prompt Tokens: {token_usage.prompt_tokens:,}")
        lines.append(f"  Completion Tokens: {token_usage.completion_tokens:,}")
        
        # Cost breakdown
        lines.append(f"Cost Breakdown:")
        lines.append(f"  Prompt Cost: ${token_usage.prompt_cost:.6f}")
        lines.append(f"  Completion Cost: ${token_usage.completion_cost:.6f}")
        lines.append(f"  Total Cost: ${token_usage.total_cost:.6f}")
        
        if show_breakdown:
            lines.append("")
            lines.append("Component Breakdown:")
            lines.append(f"  Base Prompt: {token_usage.base_prompt_tokens:,} tokens")
            lines.append(f"  Memory Context: {token_usage.memory_context_tokens:,} tokens")
            lines.append(f"  Personality Context: {token_usage.personality_context_tokens:,} tokens")
            lines.append(f"  Conversation History: {token_usage.conversation_history_tokens:,} tokens")
            lines.append(f"  Internal Monologue: {token_usage.internal_monologue_tokens:,} tokens")
            lines.append(f"  AI Response: {token_usage.response_tokens:,} tokens")
        
        return "\n".join(lines)
    
    def format_session_summary(self) -> str:
        """Format session summary report"""
        summary = self.get_session_summary()
        
        lines = []
        lines.append("📈 SESSION SUMMARY")
        lines.append("═" * 50)
        lines.append(f"Total Interactions: {summary['total_interactions']}")
        lines.append(f"Total Tokens Used: {summary['total_tokens']:,}")
        lines.append(f"Total Session Cost: ${summary['total_cost']:.6f}")
        lines.append(f"Average Tokens/Interaction: {summary['average_tokens_per_interaction']:.1f}")
        lines.append(f"Average Cost/Interaction: ${summary['average_cost_per_interaction']:.6f}")
        lines.append(f"Model: {summary['model']}")
        
        return "\n".join(lines)
    
    def get_cost_estimate(self, prompt_text: str, estimated_response_length: int = 100) -> Dict[str, float]:
        """Get cost estimate for a potential interaction"""
        prompt_tokens = self.count_tokens(prompt_text)
        estimated_completion_tokens = estimated_response_length
        
        return self.calculate_cost(prompt_tokens, estimated_completion_tokens)
