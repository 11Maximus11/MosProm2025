# В будущем здесь будут функции типа reset_password()
def get_available_tools():
    return "No tools available in MVP."

# Список доступных инструментов для планировщика
AVAILABLE_TOOLS = {
    "search_knowledge_base": {
        "description": "Поиск информации в базе знаний",
        "parameters": {
            "query": "Текст запроса для поиска"
        }
    }
}