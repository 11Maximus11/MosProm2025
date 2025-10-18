from utils.llm_utils import get_llm_response
from utils.prompts import ANALYZER_PROMPT

class AnalyzerAgent:
    """Агент для глубокого анализа текста."""
    
    async def analyze_async(self, text: str, image_path: str = None) -> dict:
        """
        Асинхронно анализирует текст и, возможно, изображение, извлекая сущности.
        """
        full_text = text
        # Если Qwen умеет обрабатывать изображения, то здесь можно было бы
        # передать путь к изображению или его base64-представление в LLM.
        # Для текущей реализации, где Qwen уже работает, мы просто передаем текст.
        
        prompt = ANALYZER_PROMPT.format(full_text=full_text)
        
        # Вызываем LLM и ожидаем JSON-ответ
        analysis_data = await get_llm_response(prompt, is_json=True)
        
        # Возвращаем результат или "безопасное" значение по умолчанию
        return analysis_data or {"full_text": full_text, "entities": {}}
