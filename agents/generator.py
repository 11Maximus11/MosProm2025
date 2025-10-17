# agents/generator.py

import sys
import os
# Этот хак нужен, чтобы найти giga_client.py в корневой папке
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from giga_client import GigaChatClient

# Копируем промпт прямо сюда, чтобы избавиться от импорта из utils
GENERATOR_PROMPT_TEMPLATE = """<|im_start|>system
Ты — вежливый и полезный ассистент технической поддержки Госкорпорации "Росатом". Твоя задача — ответить на вопрос пользователя, строго основываясь на предоставленном ниже контексте. Не используй свои общие знания. Если в контексте нет ответа, вежливо сообщи, что не можешь помочь с данным вопросом на основе имеющейся информации.<|im_end|>
<|im_start|>user
Контекст из Базы Знаний:
---
{context}
---

Вопрос пользователя: {question}<|im_end|>
<|im_start|>assistant
"""


class GeneratorAgent:
    def __init__(self):
        print("Инициализация клиента GigaChat...")
        self.giga_client = GigaChatClient()
        print("Клиент GigaChat инициализирован.")

    def generate_final_answer(self, user_query: str, context: str, execution_report: dict = None) -> str:
        # Теперь мы используем локальную переменную GENERATOR_PROMPT_TEMPLATE,
        # а не импортированную. Но ее нет в user_content, мы должны ее передать
        # в giga_client. Это ошибка в предыдущем коде. Давайте исправим.
        
        # Формируем полный промпт здесь
        final_prompt = GENERATOR_PROMPT_TEMPLATE.format(
            context=context,
            question=user_query
        )
        
        print("Отправка промпта в GigaChat...")
        # giga_client должен принимать полный промпт
        answer = self.giga_client.send_prompt(final_prompt)
        print("Ответ от GigaChat получен.")
        return answer