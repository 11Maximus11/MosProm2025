import json
from utils.llm_utils import get_llm_response
from utils.prompts import PERSONALIZER_PROMPT

class PersonalizerAgent:
    """Агент для персонализации ответов."""
    
    def personalize(self, answer: str, user_profile: dict) -> str:
        """
        Персонализирует ответ на основе данных пользователя.
        """
        # Если нет данных пользователя, возвращаем ответ без изменений
        if not user_profile:
            return answer
            
        # Преобразуем данные пользователя в строку для промпта
        user_data_str = json.dumps(user_profile, ensure_ascii=False)
        
        # Формирование промпта для персонализации
        prompt = PERSONALIZER_PROMPT.format(
            answer=answer,
            user_data=user_data_str
        )
        
        # Вызов LLM для персонализации ответа
        personalized_answer = get_llm_response(prompt, is_json=False)
        
        # Возвращаем персонализированный ответ или исходный, если персонализация не удалась
        return personalized_answer or answer