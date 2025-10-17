from giga_client import GigaChatClient
from utils.prompts import GENERATOR_PROMPT_TEMPLATE

class GeneratorAgent:
    def __init__(self):
        print("Инициализация клиента GigaChat...")
        self.giga_client = GigaChatClient()
        print("Клиент GigaChat инициализирован.")

    def generate_final_answer(self, user_query: str, context: str, execution_report: dict = None) -> str:
        user_content = f"""Контекст из Базы Знаний:
---
{context}
---

Вопрос пользователя: {user_query}"""
        
        print("Отправка промпта в GigaChat...")
        answer = self.giga_client.send_prompt(user_content)
        print("Ответ от GigaChat получен.")
        return answer