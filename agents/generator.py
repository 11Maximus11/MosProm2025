from utils.llm_utils import get_llm_response
from utils.prompts import GENERATOR_PROMPT_TEMPLATE

class GeneratorAgent:
    """Агент для генерации ответов."""
    
    async def generate_final_answer_async(self, question: str, context: list, execution_report: dict = None) -> str:
        """
        Асинхронно генерирует финальный ответ на основе контекста и результатов выполнения.
        """
        # Подготовка контекста для промпта
        context_text = ""
        for doc in context:
            context_text += f"Документ: {doc['content']}\n"
            if 'metadata' in doc and doc['metadata']:
                context_text += f"Метаданные: {doc['metadata']}\n"
            context_text += "---\n"
        
        # Добавление результатов выполнения, если они есть
        if execution_report:
            context_text += f"\nРезультаты выполнения действий:\n{execution_report['summary']}\n---\n"
        
        # Формирование промпта
        prompt = GENERATOR_PROMPT_TEMPLATE.format(
            context=context_text,
            question=question
        )
        
        # Вызов LLM для генерации ответа
        answer = await get_llm_response(prompt, is_json=False)
        
        return answer or "Извините, я не смог сформировать ответ на основе имеющейся информации."
