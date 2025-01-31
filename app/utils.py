from typing import Dict
class JsonValidator:
    @staticmethod
    def validate_response(response: Dict) -> Dict:
        """Валидация JSON ответа"""
        required_fields = {"answer", "reasoning", "sources"}
        
        if not all(field in response for field in required_fields):
            raise ValueError("Missing required fields in response")
        
        if not isinstance(response["reasoning"], str):
            raise ValueError("reasoning must be string")
            
        if not isinstance(response["sources"], list):
            raise ValueError("sources must be list")
            
        if response["answer"] is not None and not isinstance(response["answer"], int):
            raise ValueError("answer must be integer or null")
            
        if isinstance(response["answer"], int) and not (1 <= response["answer"] <= 10):
            raise ValueError("answer must be between 1 and 10")
            
        if not all(isinstance(s, str) for s in response["sources"]):
            raise ValueError("all sources must be strings")
            
        response["sources"] = response["sources"][:3]
        
        return response
