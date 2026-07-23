from llm.clients import LLMClient

llm = LLMClient()

response = llm.generate('helloo')

print(response)