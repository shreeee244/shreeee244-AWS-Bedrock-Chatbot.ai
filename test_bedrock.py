
# type: ignore
import boto3


bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# This works with ANY model automatically!
response = bedrock.converse(
    modelId='us.amazon.nova-lite-v1:0',  # or 'anthropic.claude-3-sonnet-20240229-v1:0'
    messages=[
        {
            "role": "user",
            "content": [{"text": "Say 'Hello from AWS Bedrock!'"}]
        }
    ],
    inferenceConfig={
        "maxTokens": 100,
        "temperature": 0.7
    }
)

print(response['output']['message']['content'][0]['text'])
class BedrockChatbot:
    def __init__(self, max_budget_usd=0.50):  # Stop at 50 cents
        # ... existing code ...
        self.max_budget_usd = max_budget_usd
        self.total_cost = 0.0
    
    def chat(self, user_message):
        # Check budget before making call
        if self.total_cost >= self.max_budget_usd:
            return f"❌ Budget limit of ${self.max_budget_usd} reached. Please start a new session."
        
        # ... rest of chat code ...
        class BedrockChatbot:
    def __init__(self, max_cost_usd=0.10):  # Stop at 10 cents
        self.max_cost_usd = max_cost_usd
        self.total_cost = 0.0
        # ... rest of your existing code ...
    
    def chat(self, user_message):
        # Check budget BEFORE making any API call
        if self.total_cost >= self.max_cost_usd:
            return f"⚠️ Budget limit of ${self.max_cost_usd} reached. Session stopped."
        # ... rest of your existing chat code ...