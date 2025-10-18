# agents/generator.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from giga_client import VllmClient

# --- ФОРМАТ ПРОМПТА ДЛЯ QWEN ---
# У Qwen нет явной "системной" роли в текстовых промптах.
# Инструкция дается в начале, а затем следует диалог.
# Мы будем использовать простой формат "вопрос-ответ".
QWEN_PROMPT_TEMPLATE = """Ты — вежливый и полезный ассистент технической поддержки Госкорпорации "Росатом". Твоя задача — ответить на вопрос пользователя, строго основываясь на предоставленном ниже контексте. Не используй свои общие знания. Если в контексте нет ответа, вежливо сообщи, что не можешь помочь с данным вопросом на основе имеющейся информации.

Контекст из Базы Знаний:
---
{context}
---

Вопрос пользователя: {question}

Ответ:
"""


class GeneratorAgent:
    def __init__(self):
        print("Инициализация клиента VLLM...")
        self.vllm_client = VllmClient()
        print("Клиент VLLM инициализирован.")

    def generate_final_answer(self, user_query: str, context: str, execution_report: dict = None) -> str:
        # Применяем специальный метод токенизатора Qwen для создания промпта
        tokenizer = self.vllm_client.tokenizer

        # Формируем текстовую часть промпта
        text_content = QWEN_PROMPT_TEMPLATE.format(
            context=context,
            question=user_query
        )

        # Qwen-VL-Chat ожидает промпт в формате диалога.
        # Токенизатор сам обернет это в нужные спец-токены.
        # Поскольку у нас нет картинок, мы передаем только текст.
        messages = [{"role": "user", "content": text_content}]
        final_prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        print("Отправка промпта в VLLM (Qwen)...")
        answer = self.vllm_client.send_prompt(final_prompt)
        print("Ответ от VLLM (Qwen) получен.")
        return answer