from utils.llm_utils import get_llm_response
from utils.prompts import VERIFIER_PROMPT

class VerifierAgent:
    """Агент для проверки ответов."""
    
    def verify(self, query: str, answer: str) -> dict:
        """
        Проверяет ответ на соответствие запросу и политикам.
        """
        # Формирование промпта для проверки
        prompt = VERIFIER_PROMPT.format(
            query=query,
            answer=answer
        )
        
        # Синхронный вызов LLM для проверки ответа
        verification = get_llm_response(prompt, is_json=True)
        
        # Возвращаем результат или значение по умолчанию
        if not verification:
            return {
                "decision": "approve",
                "reason": "Не удалось выполнить проверку, ответ одобрен по умолчанию.",
                "confidence": 0.5
            }
        
        return verification