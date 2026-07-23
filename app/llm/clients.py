from app.config.settings import MODEL_NAME,MAX_TOKENS,TEMPERATURE,GROQ_API_KEY
from groq import AsyncGroq

class LLMClient:

    def __init__(self):
        self.client = AsyncGroq(api_key=GROQ_API_KEY)

    async def generate(self,prompt:str) -> str:

        response = await self.client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            messages=[
                {
                    'role' :'user',
                    'content' : prompt
                }
            ]
        )

        return response.choices[0].message.content