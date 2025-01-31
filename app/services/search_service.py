import aiohttp
from typing import List
import os
import logging
from urllib.parse import quote

class SearchService:
    def __init__(self):
        self.google_key = os.getenv("GOOGLE_SEARCH_KEY")
        self.google_cx = os.getenv("GOOGLE_SEARCH_CX")
        self.search_url = "https://www.googleapis.com/customsearch/v1"

    async def search(self, query: str) -> List[str]:
        """Поиск информации через Google Custom Search API"""
        try:
            search_query = quote(f"ИТМО {query}")
            
            params = {
                'key': self.google_key,
                'cx': self.google_cx,
                'q': search_query,
                'num': 3,
                'lr': 'lang_ru'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.search_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            item['link']
                            for item in data.get('items', [])
                            if 'itmo.ru' in item['link']
                        ][:5]
                    else:
                        logging.error(f"Search API error: {response.status}")
                        return []
                        
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            return []
