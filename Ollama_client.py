from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import httpx

class OllamaClient:
    def __init__(self, model):
        # Initialize the Ollama model
        self.model = OllamaLLM(model=model)

    def generate_text(self, prompt):
        try:
            # Try invoking the model to generate a response
            result = self.model.invoke(prompt)
            return result
        except httpx.RequestError as e:
            # Handle errors related to HTTP request
            return f"HTTP error occurred: {str(e)}"
        except httpx.TimeoutException as e:
            # Handle timeout errors
            return f"Request timed out: {str(e)}"
        except Exception as e:
            # Catch all other errors
            return f"Error generating response: {str(e)}"
