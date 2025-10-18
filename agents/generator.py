# agents/generator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- ИЗМЕНЕНИЕ ---
# Меняем GigaChatClient на VllmClient
from giga_client import VllmClient

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
        print("Инициализация клиента VLLM...")
        # --- ИЗМЕНЕНИЕ ---
        self.vllm_client = VllmClient()
        print("Клиент VLLM инициализирован.")

    def generate_final_answer(self, user_query: str, context: str, execution_report: dict = None) -> str:
        # Формируем полный промпт
        final_prompt = GENERATOR_PROMPT_TEMPLATE.format(
            context=context,
            question=user_query
        )
        
        print("Отправка промпта в VLLM...")
        # --- ИЗМЕНЕНИЕ ---
        answer = self.vllm_client.send_prompt(final_prompt)
        print("Ответ от VLLM получен.")
        return answer