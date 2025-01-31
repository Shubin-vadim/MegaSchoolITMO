import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import asyncio
import logging

class NewsService:
    def __init__(self):
        self.news_url = "https://news.itmo.ru/ru/news/"
        self.rss_url = "https://news.itmo.ru/ru/news/rss/"
        self.cache = {}
        self.cache_ttl = 3600
        self.last_update = 0

    async def get_latest_news(self) -> List[Dict]:
        """Получение последних новостей ИТМО"""
        try:
            if self._should_update_cache():
                async with aiohttp.ClientSession() as session:
                    try:
                        news = await self._fetch_rss(session)
                    except Exception:
                        news = await self._fetch_html(session)
                    
                    self.cache['news'] = news
                    self.last_update = asyncio.get_event_loop().time()
            
            return self.cache['news'][:3]
        
        except Exception as e:
            logging.error(f"Error fetching news: {str(e)}")
            return []

    async def _fetch_rss(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Получение новостей через RSS"""
        async with session.get(self.rss_url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'xml')
                items = soup.find_all('item')
                
                return [
                    {
                        'title': item.title.text,
                        'link': item.link.text,
                        'description': item.description.text,
                        'date': item.pubDate.text
                    }
                    for item in items[:10]
                ]
            raise Exception("Failed to fetch RSS")

    async def _fetch_html(self, session: aiohttp.ClientSession) -> List[Dict]:
        """Парсинг новостей с HTML страницы"""
        async with session.get(self.news_url) as response:
            if response.status == 200:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                news_items = soup.find_all('div', class_='news_item')
                
                return [
                    {
                        'title': item.find('h3').text.strip(),
                        'link': f"https://news.itmo.ru{item.find('a')['href']}",
                        'description': item.find('p').text.strip(),
                        'date': item.find('div', class_='date').text.strip()
                    }
                    for item in news_items[:5]
                ]
            raise Exception("Failed to fetch HTML")

    def _should_update_cache(self) -> bool:
        """Проверка необходимости обновления кэша"""
        current_time = asyncio.get_event_loop().time()
        return (
            'news' not in self.cache or 
            current_time - self.last_update > self.cache_ttl
        )
