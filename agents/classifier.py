from utils.llm_utils import get_llm_response
from utils.prompts import CLASSIFIER_PROMPT

class ClassifierAgent:
    """Агент для классификации запросов."""
    
    async def classify_async(self, text: str) -> dict:
        """
        Асинхронно классифицирует запрос пользователя.
        """
        prompt = CLASSIFIER_PROMPT.format(text=text)
        
        # Вызываем LLM и ожидаем JSON-ответ
        classification_data = await get_llm_response(prompt, is_json=True)
        
        # Возвращаем результат или значение по умолчанию
        return classification_data or {
            "category": "general",
            "priority": "medium",
            "requires_tools": False,
            "confidence": 0.5
        }
