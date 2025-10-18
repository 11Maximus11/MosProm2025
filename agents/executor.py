from tools.system_tools import get_available_tools
import asyncio

class ExecutorAgent:
    """Агент для выполнения действий."""
    
    def __init__(self):
        self.tools = get_available_tools()
    
    async def execute_plan_async(self, plan: dict) -> dict:
        """
        Асинхронно выполняет план действий.
        """
        results = []
        summary = ""
        
        # Проверяем, есть ли действия в плане
        if not plan or 'actions' not in plan or not plan['actions']:
            return {
                "success": False,
                "results": [],
                "summary": "План не содержит действий для выполнения."
            }
        
        # Выполняем каждое действие из плана
        for action in plan['actions']:
            tool_name = action.get('tool', '')
            params = action.get('params', {})
            
            # Проверяем, существует ли инструмент
            if tool_name in self.tools:
                try:
                    # Выполняем инструмент с переданными параметрами
                    tool_function = self.tools[tool_name]
                    
                    # Проверяем, является ли функция асинхронной
                    if asyncio.iscoroutinefunction(tool_function):
                        tool_result = await tool_function(**params)
                    else:
                        tool_result = tool_function(**params)
                        
                    results.append({
                        "action": action,
                        "success": True,
                        "result": tool_result
                    })
                    summary += f"Успешно выполнено: {tool_name}\n"
                except Exception as e:
                    results.append({
                        "action": action,
                        "success": False,
                        "error": str(e)
                    })
                    summary += f"Ошибка при выполнении {tool_name}: {str(e)}\n"
            else:
                results.append({
                    "action": action,
                    "success": False,
                    "error": f"Инструмент '{tool_name}' не найден"
                })
                summary += f"Инструмент '{tool_name}' не найден\n"
        
        # Формируем итоговый отчет
        return {
            "success": any(r["success"] for r in results) if results else False,
            "results": results,
            "summary": summary
        }
