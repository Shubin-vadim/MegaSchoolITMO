from typing import Dict, List
import json
import logging
from openai import AsyncOpenAI
from config import settings

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, base_url="https://api.proxyapi.ru/openai/v1")
        self.model = settings.MODEL_NAME
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE

    async def generate_response(
        self, 
        query: str, 
        news_context: List[Dict], 
        search_results: List[str]
    ) -> Dict:
        try:
            news_text = "\n".join([
                f"- {news['title']}: {news['description']}"
                for news in news_context
            ])

            prompt = self._create_prompt(query, news_text, search_results)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are ITMO University's AI assistant. Your task is to answer questions about the university using the provided context and return responses in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                response_format={ "type": "json_object" }
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"GPT error: {str(e)}")
            return self._create_error_response(query)

    def _create_prompt(self, query: str, news_text: str, search_results: List[str]) -> str:
        return f"""Use the following context to answer questions about ITMO University.

<Instructions>
1. You must answer only in Russian. This is very important
2. The answer field contains a number from 1 to 10 or null if question has no options.
3. The reasoning field contains a clear explanation.
4. The sources field contains maximum 3 sources.
5. All sources are valid URLs.
</Instructions>

<Recent ITMO News>
{news_text}
</Recent ITMO News>

<Found Information>
{' '.join(search_results)}
</Found Information>

<Question>
Question: {query}
</Question>


<Response Format>
Respond in JSON format with the following structure:
{{
    "answer": <correct answer number (1-10) or null if question has no options>,
    "reasoning": <explanation of the answer>,
    "sources": <list of used sources, maximum 3>
}}
</Response Format>

<Final checks>
1. The answer field contains a number from 1 to 10 or null
2. The reasoning field contains a clear explanation
3. The sources field contains maximum 3 sources
4. All sources are valid URLs
</Final checks>"""

    def _create_error_response(self, query: str) -> Dict:
        """Создание ответа при ошибке"""
        return {
            "answer": None,
            "reasoning": "Извините, произошла ошибка при обработке запроса.",
            "sources": []
        }
