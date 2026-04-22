# type: ignore
import boto3

import json
from typing import List, Dict, Any

class BedrockChatbot:
    def __init__(self) -> None:
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id: str = "us.amazon.nova-lite-v1:0"
        self.conversation_history: List[Dict[str, Any]] = []

    def chat(self, user_message: str) -> str:
        """Send a message to the AI and get a response"""
        self.conversation_history.append({
            "role": "user",
            "content": [{"text": user_message}]
        })

        try:
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=self.conversation_history,
                inferenceConfig={
                    "maxTokens": 500,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            )
            
            ai_response: str = response['output']['message']['content'][0]['text']
            
            self.conversation_history.append({
                "role": "assistant",
                "content": [{"text": ai_response}]
            })
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self) -> str:
        """Start a fresh conversation"""
        self.conversation_history = []
        return "Conversation history cleared!"

if __name__ == "__main__":
    bot = BedrockChatbot()
    
    print("🤖 AWS Bedrock Chatbot")
    print("=" * 40)
    print("Type 'quit' to exit")
    print("Type 'clear' to reset conversation")
    print("=" * 40)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye! 👋")
            break
        elif user_input.lower() == 'clear':
            print(bot.clear_history())
            continue
        elif not user_input:
            continue
            
        print("Bot: ", end="", flush=True)
        response = bot.chat(user_input)
        print(response)
        import time
from datetime import datetime

class BedrockChatbot:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = "us.amazon.nova-lite-v1:0"
        self.conversation_history = []
        
        # Cost tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        
        # Pricing per 1M tokens (as of April 2026)
        self.pricing = {
            "us.amazon.nova-lite-v1:0": {
                "input": 0.06,   # $0.06 per 1M input tokens
                "output": 0.24   # $0.24 per 1M output tokens
            }
        }
    
    def calculate_cost(self, input_tokens, output_tokens):
        """Calculate cost for this API call"""
        prices = self.pricing.get(self.model_id, {"input": 0.06, "output": 0.24})
        cost = (input_tokens * prices["input"] / 1_000_000) + \
               (output_tokens * prices["output"] / 1_000_000)
        return cost
    
    def show_cost(self):
        """Display total cost so far"""
        print(f"\n💰 Total cost this session: ${self.total_cost:.6f} USD")
        print(f"   (About ₹{self.total_cost * 85:.4f} INR)")
        print(f"   Input tokens: {self.total_input_tokens}")
        print(f"   Output tokens: {self.total_output_tokens}")
    
    def chat(self, user_message):
        """Send a message with cost tracking"""
        self.conversation_history.append({
            "role": "user",
            "content": [{"text": user_message}]
        })

        try:
            response = self.bedrock.converse(
                modelId=self.model_id,
                messages=self.conversation_history,
                inferenceConfig={"maxTokens": 500, "temperature": 0.7}
            )
            
            # Get token usage from response
            usage = response.get('usage', {})
            input_tokens = usage.get('inputTokens', 0)
            output_tokens = usage.get('outputTokens', 0)
            
            # Update totals
            self.total_input_tokens += input_tokens
            self.total_output_tokens += output_tokens
            call_cost = self.calculate_cost(input_tokens, output_tokens)
            self.total_cost += call_cost
            
            ai_response = response['output']['message']['content'][0]['text']
            
            self.conversation_history.append({
                "role": "assistant",
                "content": [{"text": ai_response}]
            })
            
            # Show cost per message
            print(f"\n[⚡ Cost: ${call_cost:.8f} | Total: ${self.total_cost:.6f}]")
            
            return ai_response
            
        except Exception as e:
            return f"Error: {str(e)}"
        