import os
from dotenv import load_dotenv
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import logging

# Настраиваем логирование, чтобы видеть, что происходит
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения. Нам они больше не нужны для пути,
# но могут пригодиться для других настроек в будущем.
load_dotenv()

class GigaChatClient:
    def __init__(self):
        # --- Параметры модели ---
        # Репозиторий на Hugging Face
        repo_id = "ai-sage/GigaChat-20B-A3B-instruct-GGUF"
        # Имя файла модели для скачивания
        filename = "ggml-model-q4_k_m.gguf"
        # Локальная папка для хранения моделей
        models_dir = "models"
        
        # Полный путь к файлу модели
        model_path = os.path.join(models_dir, filename)

        # --- Логика проверки и скачивания модели ---
        if not os.path.exists(model_path):
            logging.warning(f"Файл модели не найден по пути: {model_path}")
            logging.info(f"Начинается скачивание модели '{filename}' из репозитория '{repo_id}'.")
            logging.info("Это может занять много времени в зависимости от скорости вашего интернета...")
            
            # Создаем папку для моделей, если ее нет
            os.makedirs(models_dir, exist_ok=True)
            
            try:
                # Используем huggingface_hub для скачивания файла с прогресс-баром
                hf_hub_download(
                    repo_id=repo_id,
                    filename=filename,
                    local_dir=models_dir,
                    local_dir_use_symlinks=False # Скачиваем файл напрямую, а не через кеш
                )
                logging.info(f"Модель успешно скачана в папку '{models_dir}'.")
            except Exception as e:
                logging.error(f"Не удалось скачать модель: {e}")
                raise
        else:
            logging.info(f"Файл модели найден: {model_path}")

        # --- Инициализация модели из локального файла ---
        logging.info("Инициализация модели LlamaCPP... Это может занять несколько минут.")
        try:
            self.model = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_gpu_layers=-1, # -1 для максимального использования GPU
                n_threads=8,     # Количество потоков CPU
                verbose=False    # Убираем лишние логи от llama-cpp
            )
            logging.info("Модель LlamaCPP успешно инициализирована.")
        except Exception as e:
            logging.error(f"Ошибка при загрузке модели LlamaCPP: {e}")
            logging.error("Возможные причины: несовместимая версия llama-cpp-python, нехватка RAM/VRAM, поврежденный файл модели.")
            raise

    def send_prompt(self, user_content: str) -> str:
        """
        Отправляет промпт в локально запущенную модель GigaChat.
        """
        try:
            output = self.model.create_chat_completion(
                messages=[
                    {
                        "role": "system",
                        "content": "Ты — вежливый и полезный ассистент технической поддержки Госкорпорации Росатом. Твоя задача — ответить на вопрос пользователя, строго основываясь на предоставленном ниже контексте. Не используй свои общие знания. Если в контексте нет ответа, вежливо сообщи, что не можешь помочь с данным вопросом на основе имеющейся информации."
                    },
                    {
                        "role": "user",
                        "content": user_content
                    }
                ],
                max_tokens=1024,
                stop=["<|im_end|>"],
                temperature=0.7,
            )
            answer = output['choices'][0]['message']['content']
            return answer.strip()
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа моделью: {e}")
            return "К сожалению, произошла ошибка при обработке вашего запроса моделью."