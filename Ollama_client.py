from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate

class OllamaClient:
    def __init__(self, model="text-davinci-003"):
        # Initialize OpenAI model
        self.model = OpenAI(model=model)

    def generate_text(self, prompt):
        # Create a chat prompt template
        self.prompt = ChatPromptTemplate.from_template(prompt)

        # Combine the prompt with the model
        self.chain = self.model | self.prompt

        # Run the chain and get the result
        result = self.chain.invoke(prompt)
        return result
