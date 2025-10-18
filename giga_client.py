# giga_client.py

import os
from vllm import LLM, SamplingParams
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

class VllmClient:
    def __init__(self):
        # ID модели GigaChat в формате, подходящем для vLLM
        # ВНИМАНИЕ: GigaChat-29B требует ОЧЕНЬ много VRAM (>60GB).
        # Для тестов на обычном железе лучше взять модель поменьше, например Mistral 7B.
        # Я оставлю GigaChat, но с комментарием.
        model_id = "ai-forever/GigaChat-Plus-29B"
        # model_id = "mistralai/Mistral-7B-Instruct-v0.2" # <--- Хорошая альтернатива для тестов

        logging.info(f"Инициализация модели VLLM: {model_id}...")
        try:
            # Инициализация модели vLLM.
            self.llm = LLM(
                model=model_id,
                quantization=None,  # GigaChat-29B не поддерживает AWQ "из коробки"
                dtype="bfloat16",   # Используем bfloat16, если поддерживается GPU (Ampere+)
                gpu_memory_utilization=0.95, # Используем 95% VRAM
                trust_remote_code=True,
            )
            # Настройки для генерации
            self.sampling_params = SamplingParams(temperature=0.7, max_tokens=1024, stop=["<|im_end|>"])
            self.tokenizer = self.llm.get_tokenizer()
            logging.info("Модель VLLM успешно инициализирована.")
        except Exception as e:
            logging.error(f"ОШИБКА: Не удалось инициализировать модель VLLM. {e}", exc_info=True)
            raise

    def send_prompt(self, full_prompt: str) -> str:
        """
        Отправляет готовый промпт в vLLM и возвращает ответ.
        """
        try:
            # vLLM принимает список промптов, даже если он один
            outputs = self.llm.generate([full_prompt], self.sampling_params)
            
            # Извлекаем текст из первого результата
            answer = outputs[0].outputs[0].text
            return answer.strip()
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа моделью vLLM: {e}")
            return "К сожалению, произошла ошибка при обработке вашего запроса моделью."
