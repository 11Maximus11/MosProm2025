import json
import asyncio
import logging
from giga_client import VllmClient

# Инициализация клиента Qwen
vllm_client = VllmClient()
logger = logging.getLogger(__name__)

async def get_llm_response(prompt: str, is_json: bool = False) -> str | dict:
    """
    Асинхронно получает ответ от локальной модели Qwen.

    :param prompt: Промпт для модели.
    :param is_json: Указывает, нужно ли парсить ответ как JSON.
    :return: Строку с ответом или словарь, если is_json=True.
    """
    try:
        # Используем локальную модель Qwen через vLLM
        response = vllm_client.send_prompt(prompt)
        
        if not response:
            raise ValueError("Получен пустой ответ от модели")

        if is_json:
            # Попытка найти и извлечь JSON из ответа
            json_part = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_part)
        
        return response

    except Exception as e:
        logger.error(f"Ошибка при вызове LLM: {e}")
        # В случае ошибки возвращаем "безопасное" значение
        return {} if is_json else "Извините, произошла ошибка при обработке вашего запроса."

if __name__ == '__main__':
    # Пример использования
    """async def main():
        test_prompt = "Привет! Как дела?"
        result = await get_llm_response(test_prompt)
        print(f"Обычный ответ: {result}")

        json_prompt = "Верни JSON с полями 'name' и 'age'. Например: {'name': 'John', 'age': 30}"
        json_result = await get_llm_response(json_prompt, is_json=True)
        print(f"JSON ответ: {json_result}")"""

    asyncio.run(main())
