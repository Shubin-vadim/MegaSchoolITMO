from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import logging
import asyncio
from datetime import datetime

from services.llm_service import LLMService
from services.news_service import NewsService
from services.search_service import SearchService
from utils import JsonValidator
from config import settings
from shemes import Query, Response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="ITMO AI Agent")

llm_service = LLMService()
news_service = NewsService()
search_service = SearchService()
json_validator = JsonValidator()

@app.post("/api/request", response_model=Response)
async def process_request(query: Query):
    start_time = datetime.now()
    
    try:
        news_context, search_results = await asyncio.gather(
            news_service.get_latest_news(),
            search_service.search(query.query)
        )
        
        response = await llm_service.generate_response(
            query=query.query,
            news_context=news_context,
            search_results=search_results
        )
        
        response['id'] = query.id
        
        validated_response = json_validator.validate_response(response)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Request processed in {execution_time:.2f} seconds")
        
        return validated_response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
