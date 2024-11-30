from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

class OllamaClient:
    def __init__(self, model):
        
        self.model = OllamaLLM(model=model)

    def generate_text(self, prompt):
        
        # Create a chat prompt template
        prompt_template = ChatPromptTemplate.from_template("{user_input}")
        result = self.model.invoke(prompt_template.format(user_input=prompt))
        return result

