# giga_client.py

import os
import multiprocessing
# Set multiprocessing start method to 'spawn' before importing vLLM
# This fixes the "We must use the spawn multiprocessing start method" warning
multiprocessing.set_start_method('spawn', force=True)

from vllm import LLM, SamplingParams
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.DEBUG)

class VllmClient:
    def __init__(self):
        # --- ИСПОЛЬЗУЕМ Qwen2.5-VL-7B-Instruct-AWQ ---
        model_id = "Qwen/Qwen2.5-VL-7B-Instruct-AWQ"

        logging.info(f"Инициализация модели VLLM: {model_id}...")
        try:
            # Инициализация модели vLLM с параметрами из вашего примера
            self.llm = LLM(
                model=model_id,
                # --- Включаем квантизацию AWQ ---
                quantization="awq",
                dtype="float16",
                gpu_memory_utilization=0.90,
                max_model_len=4096,
                trust_remote_code=True,
            )
            
            # Настройки для генерации. <|endoftext|> - основной стоп-токен для Qwen
            self.sampling_params = SamplingParams(
                temperature=0.7, 
                max_tokens=1024, 
                stop=["<|endoftext|>"]
            )
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
            outputs = self.llm.generate([full_prompt], self.sampling_params)
            answer = outputs[0].outputs[0].text
            return answer.strip()
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа моделью vLLM: {e}")
            return "К сожалению, произошла ошибка при обработке вашего запроса моделью."