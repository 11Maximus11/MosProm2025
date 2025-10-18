import json
from utils.llm_utils import get_llm_response
from utils.prompts import PLANNER_PROMPT
from tools.system_tools import AVAILABLE_TOOLS

class PlannerAgent:
    """Агент для планирования действий."""
    
    async def plan_actions_async(self, query: str, context: list) -> dict:
        """
        Асинхронно планирует действия на основе запроса и контекста.
        """
        # Подготовка контекста для промпта
        context_text = ""
        for doc in context:
            context_text += f"{doc['content']}\n---\n"
            
        # Преобразуем AVAILABLE_TOOLS в JSON-строку для промпта
        tools_json = json.dumps([{
            "tool": name,
            "description": details["description"],
            "params": details["params"]
        } for name, details in AVAILABLE_TOOLS.items()], ensure_ascii=False, indent=2)

        prompt = PLANNER_PROMPT.format(
            user_query=query,
            context=context_text,
            tools_json=tools_json
        )
        
        # Вызов LLM для генерации плана
        plan_data = await get_llm_response(prompt, is_json=True)
        
        # Возвращаем результат или значение по умолчанию
        return plan_data or {
            "actions": [],
            "reasoning": "Не удалось сформировать план действий.",
            "requires_tools": False
        }
