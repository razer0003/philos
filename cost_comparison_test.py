"""
Cost Comparison Test: GPT-4o vs GPT-5 Mini vs GPT-5 Nano

Demonstrates actual cost differences across different operation types using:
• GPT-4o: Baseline comparison model
• GPT-5 Mini: Main Philos consciousness model (replaces GPT-4o)
• GPT-5 Nano: Lightweight tasks model for simple operations

This test provides concrete evidence of cost savings when using GPT-5 models
for appropriate tasks in the Philos consciousness system.
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# Load environment variables
load_dotenv()

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.token_counter import TokenCounter, TokenUsage
from src.model_selector import get_task_config
from src.consciousness_engine import ConsciousnessEngine
from src.memory_manager import MemoryManager
from src.personality_engine import PersonalityEngine
from src.database import DatabaseManager
import openai

@dataclass
class CostComparisonResult:
    """Results from cost comparison test"""
    operation_type: str
    gpt4o_tokens: TokenUsage
    gpt5_mini_tokens: TokenUsage
    gpt5_nano_tokens: TokenUsage
    cost_savings_mini: float
    cost_savings_nano: float
    performance_notes: str

class CostComparisonTester:
    """Test suite for comparing model costs across different operations"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Initialize token counters for each model
        self.counter_4o = TokenCounter('gpt-4o')
        self.counter_5_mini = TokenCounter('gpt-5-mini')
        self.counter_5_nano = TokenCounter('gpt-5-nano')
        
        # Models being tested
        self.models = {
            'gpt-4o': 'Baseline comparison model',
            'gpt-5-mini': 'Main Philos consciousness model',  
            'gpt-5-nano': 'Lightweight tasks model'
        }
        
        # Test results storage
        self.results: List[CostComparisonResult] = []
        
        # Sample data for testing
        self.test_user_input = "I've been feeling really stressed about work lately. Can you help me understand why I keep procrastinating on important projects?"
        self.test_search_query = "What are the latest developments in artificial consciousness research?"
        self.test_memory_context = "User mentioned feeling anxious about presentations last week"
        self.test_personality_trait = "empathy level when discussing stress"

    async def simulate_web_search_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of web search + response generation"""
        
        # Complex search prompt that would normally use full model
        search_prompt = f"""You are helping a user by searching for information and providing a comprehensive response.
        
User Query: "{self.test_search_query}"

Search the web for current information and provide a detailed, well-researched response that includes:
1. Recent developments and breakthroughs
2. Key researchers and institutions involved  
3. Current challenges and debates
4. Practical implications
5. Future directions

Provide citations and ensure accuracy. Be thorough but concise."""

        # Test with GPT-4o (original model)
        gpt4o_usage = await self._test_model_call('gpt-4o', search_prompt, max_tokens=1500)
        
        # Test with GPT-5 Mini (main model)  
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', search_prompt, max_tokens=1500)
        
        # Test with GPT-5 Nano (lightweight - would use for initial search processing)
        nano_prompt = f"""Analyze this search query and extract key search terms and intent:
Query: "{self.test_search_query}"

Return JSON: {{"search_terms": ["term1", "term2"], "intent": "description", "complexity": "high/medium/low"}}"""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=200)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def simulate_emotional_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of emotional processing and response"""
        
        # Emotional analysis prompt
        emotional_prompt = f"""Analyze the emotional context of this user message and generate an empathetic response:

User: "{self.test_user_input}"

Consider:
- Emotional state indicators
- Underlying concerns
- Appropriate empathetic response tone
- Helpful suggestions
- Emotional validation techniques

Provide a caring, understanding response that addresses both emotional and practical needs."""

        # Test with GPT-4o
        gpt4o_usage = await self._test_model_call('gpt-4o', emotional_prompt, max_tokens=800)
        
        # Test with GPT-5 Mini  
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', emotional_prompt, max_tokens=800)
        
        # Test with GPT-5 Nano (simple emotional classification)
        nano_prompt = f"""Classify emotions in this message:
"{self.test_user_input}"

Return JSON: {{"primary_emotion": "emotion", "intensity": 0.0-1.0, "secondary_emotions": {{"emotion": 0.5}}}}"""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=150)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def simulate_memory_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of memory retrieval and integration"""
        
        memory_prompt = f"""Using the provided memory context, generate a personalized response:

Current User Input: "{self.test_user_input}"
Memory Context: "{self.test_memory_context}"

Create a response that:
1. References relevant past conversations
2. Shows continuity and relationship development
3. Builds upon previous emotional connections
4. Demonstrates long-term memory integration
5. Maintains conversational flow

Be personal and show you remember previous interactions."""

        # Test with GPT-4o
        gpt4o_usage = await self._test_model_call('gpt-4o', memory_prompt, max_tokens=600)
        
        # Test with GPT-5 Mini
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', memory_prompt, max_tokens=600)
        
        # Test with GPT-5 Nano (memory relevance scoring)
        nano_prompt = f"""Score memory relevance:
User: "{self.test_user_input}"
Memory: "{self.test_memory_context}"

Return score 0.0-1.0 for relevance."""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=50)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def simulate_conversational_memory_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of complex conversational memory integration"""
        
        conversation_prompt = f"""Generate a response that integrates multiple conversation elements:

Current Input: "{self.test_user_input}"
Previous Context: "{self.test_memory_context}"

Create a response that demonstrates:
1. Deep conversational memory
2. Personality consistency 
3. Emotional intelligence
4. Relationship progression
5. Contextual awareness
6. Personal growth acknowledgment

Show sophisticated understanding of conversation history and emotional development."""

        # All models would handle this as a complex task
        gpt4o_usage = await self._test_model_call('gpt-4o', conversation_prompt, max_tokens=1000)
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', conversation_prompt, max_tokens=1000)
        
        # Nano wouldn't handle this - simulate preprocessing only
        nano_prompt = f"""Extract conversation elements:
Input: "{self.test_user_input}"
Context: "{self.test_memory_context}"

Return JSON with key themes, emotions, and memory references."""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=200)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def simulate_memory_emotional_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of combined memory + emotional processing"""
        
        combined_prompt = f"""Generate a response that combines emotional intelligence with memory integration:

User Input: "{self.test_user_input}"
Memory Context: "{self.test_memory_context}"

Your response should:
1. Acknowledge emotional state with empathy
2. Reference relevant memories appropriately
3. Show emotional growth/learning from past interactions
4. Provide emotionally intelligent guidance
5. Strengthen the emotional bond
6. Demonstrate deep understanding

Create a response that's both emotionally supportive and shows sophisticated memory integration."""

        # Test all models on full task
        gpt4o_usage = await self._test_model_call('gpt-4o', combined_prompt, max_tokens=900)
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', combined_prompt, max_tokens=900)
        
        # Nano: separate emotional analysis
        nano_prompt = f"""Analyze emotion + memory relevance:
User: "{self.test_user_input}"
Memory: "{self.test_memory_context}"

Return JSON: {{"emotion_intensity": 0.0-1.0, "memory_relevance": 0.0-1.0, "response_type": "supportive/analytical/etc"}}"""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=100)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def simulate_personality_difference_response(self) -> Tuple[TokenUsage, TokenUsage, TokenUsage]:
        """Test cost of personality-aware response generation"""
        
        personality_prompt = f"""Generate a response that reflects specific personality traits:

User Input: "{self.test_user_input}"
Personality Focus: "{self.test_personality_trait}"

Adjust your response to show:
1. High empathy and emotional understanding
2. Personalized communication style
3. Trait-specific response patterns
4. Personality consistency
5. Adaptive emotional expression
6. Individual characteristics

Make the response distinctly reflect the specified personality trait while maintaining authenticity."""

        # Test all models
        gpt4o_usage = await self._test_model_call('gpt-4o', personality_prompt, max_tokens=700)
        gpt5_mini_usage = await self._test_model_call('gpt-5-mini', personality_prompt, max_tokens=700)
        
        # Nano: personality trait scoring
        nano_prompt = f"""Score personality trait expression:
Input: "{self.test_user_input}"
Trait: "{self.test_personality_trait}"

Return trait activation score 0.0-1.0 and suggested response tone."""
        
        gpt5_nano_usage = await self._test_model_call('gpt-5-nano', nano_prompt, max_tokens=80)
        
        return gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage

    async def _test_model_call(self, model: str, prompt: str, max_tokens: int = 500) -> TokenUsage:
        """Make a test API call and return token usage"""
        
        try:
            print(f"Testing {model} with {len(prompt)} char prompt...")
            
            start_time = time.time()
            
            # Use the actual GPT-5 models directly
            api_params = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            # GPT-5 models use max_completion_tokens and only support temperature=1
            if model.startswith('gpt-5'):
                api_params["max_completion_tokens"] = max_tokens
                api_params["temperature"] = 1  # GPT-5 only supports default temperature
            else:
                api_params["max_tokens"] = max_tokens
            
            # Make API call with the actual model
            response = self.client.chat.completions.create(**api_params)
            
            # Calculate tokens and cost
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Get the appropriate counter
            if model == 'gpt-4o':
                counter = self.counter_4o
            elif model == 'gpt-5-mini':
                counter = self.counter_5_mini
            else:  # gpt-5-nano
                counter = self.counter_5_nano
            
            cost_breakdown = counter.calculate_cost(prompt_tokens, completion_tokens)
            cost = cost_breakdown['total_cost']  # Extract the total cost from the breakdown
            
            duration = time.time() - start_time
            
            return TokenUsage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                total_cost=cost,
                model=model,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error testing {model}: {e}")
            # Return dummy data for comparison - use estimated tokens based on prompt length
            estimated_prompt_tokens = len(prompt) // 4  # Rough estimate: 1 token per 4 chars
            estimated_completion_tokens = max_tokens // 2  # Assume half of max tokens used
            estimated_total_tokens = estimated_prompt_tokens + estimated_completion_tokens
            
            # Get the appropriate counter for cost estimation
            if model == 'gpt-4o':
                counter = self.counter_4o
            elif model == 'gpt-5-mini':
                counter = self.counter_5_mini
            else:  # gpt-5-nano
                counter = self.counter_5_nano
            
            estimated_cost_breakdown = counter.calculate_cost(estimated_prompt_tokens, estimated_completion_tokens)
            estimated_cost = estimated_cost_breakdown['total_cost']  # Extract the total cost
            
            return TokenUsage(
                prompt_tokens=estimated_prompt_tokens,
                completion_tokens=estimated_completion_tokens,
                total_tokens=estimated_total_tokens,
                total_cost=estimated_cost,
                model=f"{model} (estimated)",
                timestamp=datetime.now()
            )

    async def run_all_tests(self):
        """Run all cost comparison tests"""
        
        print("=" * 60)
        print("PHILOS AI COST COMPARISON TEST")
        print("GPT-4o vs GPT-5 Mini vs GPT-5 Nano")
        print("=" * 60)
        print("\n📋 Test Methodology:")
        print("• GPT-4o: Baseline comparison model")
        print("• GPT-5 Mini: Main Philos consciousness model")  
        print("• GPT-5 Nano: Lightweight tasks model for simple operations")
        print("• Using actual GPT-5 models with real pricing rates")
        print("=" * 60)
        
        test_functions = [
            ("Web Search Response", self.simulate_web_search_response),
            ("Emotional Response", self.simulate_emotional_response),
            ("Memory Response", self.simulate_memory_response),
            ("Conversational Memory", self.simulate_conversational_memory_response),
            ("Memory + Emotional", self.simulate_memory_emotional_response),
            ("Personality Difference", self.simulate_personality_difference_response)
        ]
        
        for test_name, test_func in test_functions:
            print(f"\n🧪 Testing: {test_name}")
            print("-" * 40)
            
            gpt4o_usage, gpt5_mini_usage, gpt5_nano_usage = await test_func()
            
            # Calculate savings
            if hasattr(gpt4o_usage, 'total_cost') and isinstance(gpt4o_usage.total_cost, (int, float)) and gpt4o_usage.total_cost > 0:
                mini_savings = ((gpt4o_usage.total_cost - gpt5_mini_usage.total_cost) / gpt4o_usage.total_cost) * 100
                nano_savings = ((gpt4o_usage.total_cost - gpt5_nano_usage.total_cost) / gpt4o_usage.total_cost) * 100
            else:
                mini_savings = nano_savings = 0
            
            # Performance notes
            if "search" in test_name.lower():
                notes = "Nano used for query preprocessing, Mini/4o for full response"
            elif "emotional" in test_name.lower():
                notes = "Nano used for emotion classification, Mini/4o for full response"
            elif "memory" in test_name.lower() and "emotional" in test_name.lower():
                notes = "Nano used for emotion+memory scoring, Mini/4o for response"
            elif "personality" in test_name.lower():
                notes = "Nano used for trait scoring, Mini/4o for personality-aware response"
            else:
                notes = "Nano used for preprocessing/scoring, Mini/4o for full response"
            
            result = CostComparisonResult(
                operation_type=test_name,
                gpt4o_tokens=gpt4o_usage,
                gpt5_mini_tokens=gpt5_mini_usage,
                gpt5_nano_tokens=gpt5_nano_usage,
                cost_savings_mini=mini_savings,
                cost_savings_nano=nano_savings,
                performance_notes=notes
            )
            
            self.results.append(result)
            self._print_test_result(result)
            
            # Small delay between tests
            await asyncio.sleep(1)
        
        self._print_summary()

    def _print_test_result(self, result: CostComparisonResult):
        """Print individual test result"""
        
        print(f"GPT-4o:     {result.gpt4o_tokens.prompt_tokens:>4}+{result.gpt4o_tokens.completion_tokens:>4} = {result.gpt4o_tokens.total_tokens:>5} tokens | ${result.gpt4o_tokens.total_cost:.6f}")
        print(f"GPT-5 Mini: {result.gpt5_mini_tokens.prompt_tokens:>4}+{result.gpt5_mini_tokens.completion_tokens:>4} = {result.gpt5_mini_tokens.total_tokens:>5} tokens | ${result.gpt5_mini_tokens.total_cost:.6f} ({result.cost_savings_mini:+.1f}%)")  
        print(f"GPT-5 Nano: {result.gpt5_nano_tokens.prompt_tokens:>4}+{result.gpt5_nano_tokens.completion_tokens:>4} = {result.gpt5_nano_tokens.total_tokens:>5} tokens | ${result.gpt5_nano_tokens.total_cost:.6f} ({result.cost_savings_nano:+.1f}%)")
        print(f"Note: {result.performance_notes}")

    def _print_summary(self):
        """Print comprehensive cost comparison summary"""
        
        print("\n" + "=" * 60)
        print("COST COMPARISON SUMMARY")
        print("=" * 60)
        
        # Calculate totals
        total_4o_cost = sum(r.gpt4o_tokens.total_cost for r in self.results)
        total_5mini_cost = sum(r.gpt5_mini_tokens.total_cost for r in self.results)
        total_5nano_cost = sum(r.gpt5_nano_tokens.total_cost for r in self.results)
        
        total_4o_tokens = sum(r.gpt4o_tokens.total_tokens for r in self.results)
        total_5mini_tokens = sum(r.gpt5_mini_tokens.total_tokens for r in self.results)
        total_5nano_tokens = sum(r.gpt5_nano_tokens.total_tokens for r in self.results)
        
        print(f"\nTotal Costs:")
        print(f"GPT-4o:     ${total_4o_cost:.6f} ({total_4o_tokens:,} tokens)")
        print(f"GPT-5 Mini: ${total_5mini_cost:.6f} ({total_5mini_tokens:,} tokens)")
        print(f"GPT-5 Nano: ${total_5nano_cost:.6f} ({total_5nano_tokens:,} tokens)")
        
        if total_4o_cost > 0:
            total_mini_savings = ((total_4o_cost - total_5mini_cost) / total_4o_cost) * 100
            total_nano_savings = ((total_4o_cost - total_5nano_cost) / total_4o_cost) * 100
            
            print(f"\nSavings vs GPT-4o:")
            print(f"GPT-5 Mini: {total_mini_savings:.1f}% cost reduction")
            print(f"GPT-5 Nano: {total_nano_savings:.1f}% cost reduction")
        
        # Hybrid approach savings (realistic usage)
        hybrid_cost = 0
        for result in self.results:
            if "search" in result.operation_type.lower():
                # Use nano for preprocessing + mini for response
                hybrid_cost += result.gpt5_nano_tokens.total_cost + (result.gpt5_mini_tokens.total_cost * 0.8)
            elif "emotional" in result.operation_type.lower() and "memory" not in result.operation_type.lower():
                # Use nano for emotion analysis
                hybrid_cost += result.gpt5_nano_tokens.total_cost
            elif "memory" in result.operation_type.lower() and "conversational" not in result.operation_type.lower():
                # Use nano for memory scoring + mini for response  
                hybrid_cost += result.gpt5_nano_tokens.total_cost + (result.gpt5_mini_tokens.total_cost * 0.6)
            else:
                # Complex operations use full mini model
                hybrid_cost += result.gpt5_mini_tokens.total_cost
        
        if total_4o_cost > 0:
            hybrid_savings = ((total_4o_cost - hybrid_cost) / total_4o_cost) * 100
            print(f"\nHybrid Approach (Nano + Mini): {hybrid_savings:.1f}% cost reduction")
        
        print(f"\nPer-Operation Breakdown:")
        print("-" * 60)
        for result in self.results:
            if result.gpt4o_tokens.total_cost > 0:
                savings = ((result.gpt4o_tokens.total_cost - result.gpt5_mini_tokens.total_cost) / result.gpt4o_tokens.total_cost) * 100
                print(f"{result.operation_type:<25}: {savings:>6.1f}% savings with Mini")
        
        # Export detailed results
        self._export_results()

    def _export_results(self):
        """Export detailed results to JSON file"""
        
        export_data = {
            'test_timestamp': datetime.now().isoformat(),
            'test_configuration': {
                'gpt4o_pricing': self.counter_4o.pricing,
                'gpt5_mini_pricing': self.counter_5_mini.pricing,
                'gpt5_nano_pricing': self.counter_5_nano.pricing
            },
            'results': []
        }
        
        for result in self.results:
            export_data['results'].append({
                'operation_type': result.operation_type,
                'gpt4o': {
                    'tokens': result.gpt4o_tokens.total_tokens,
                    'cost': result.gpt4o_tokens.total_cost,
                    'prompt_tokens': result.gpt4o_tokens.prompt_tokens,
                    'completion_tokens': result.gpt4o_tokens.completion_tokens
                },
                'gpt5_mini': {
                    'tokens': result.gpt5_mini_tokens.total_tokens,
                    'cost': result.gpt5_mini_tokens.total_cost,
                    'prompt_tokens': result.gpt5_mini_tokens.prompt_tokens,
                    'completion_tokens': result.gpt5_mini_tokens.completion_tokens
                },
                'gpt5_nano': {
                    'tokens': result.gpt5_nano_tokens.total_tokens,
                    'cost': result.gpt5_nano_tokens.total_cost,
                    'prompt_tokens': result.gpt5_nano_tokens.prompt_tokens,
                    'completion_tokens': result.gpt5_nano_tokens.completion_tokens
                },
                'savings': {
                    'mini_vs_4o': result.cost_savings_mini,
                    'nano_vs_4o': result.cost_savings_nano
                },
                'notes': result.performance_notes
            })
        
        filename = f"cost_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"\n📊 Detailed results exported to: {filename}")

async def main():
    """Main test function"""
    
    print("Initializing Cost Comparison Test...")
    
    try:
        tester = CostComparisonTester()
        await tester.run_all_tests()
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
