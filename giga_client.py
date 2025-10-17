# giga_client.py

import os
from dotenv import load_dotenv
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

class GigaChatClient:
    def __init__(self):
        repo_id = "ai-sage/GigaChat-20B-A3B-instruct-GGUF"
        filename = "ggml-model-q4_k_m.gguf"
        models_dir = "models"
        model_path = os.path.join(models_dir, filename)

        if not os.path.exists(model_path):
            logging.warning(f"Файл модели не найден: {model_path}")
            logging.info(f"Начинается скачивание модели '{filename}'...")
            os.makedirs(models_dir, exist_ok=True)
            try:
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=models_dir,
                    local_dir_use_symlinks=False
                )
                logging.info(f"Модель успешно скачана в '{models_dir}'.")
            except Exception as e:
                logging.error(f"Не удалось скачать модель: {e}")
                raise
        else:
            logging.info(f"Файл модели найден: {model_path}")

        logging.info("Инициализация модели LlamaCPP...")
        try:
            self.model = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_gpu_layers=-1,
                n_threads=8,
                verbose=False
            )
            logging.info("Модель LlamaCPP успешно инициализирована.")
        except Exception as e:
            logging.error(f"Ошибка при загрузке модели LlamaCPP: {e}")
            raise

    def send_prompt(self, full_prompt: str) -> str:
        """
        Принимает ПОЛНЫЙ, уже отформатированный промпт и отправляет в модель.
        """
        try:
            # Используем create_completion, так как передаем уже готовый к употреблению промпт
            output = self.model(
                prompt=full_prompt,
                max_tokens=1024,
                stop=["<|im_end|>"],
                temperature=0.7,
                echo=False # Не повторять промпт в ответе
            )
            answer = output['choices'][0]['text']
            return answer.strip()
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа моделью: {e}")
            return "К сожалению, произошла ошибка при обработке вашего запроса моделью."