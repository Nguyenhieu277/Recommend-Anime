import openai
import os
from dotenv import load_dotenv

load_dotenv()
class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    
    def generate_text(self, messages):
        chat_completion = self.client.chat.completions.create(
            model = 'gpt-4o',
            messages=messages
        )
        return chat_completion.choices[0].message.content
    