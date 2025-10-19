import json
import asyncio
import logging
from giga_client import VllmClient

# Инициализация клиента Qwen
vllm_client = VllmClient()
logger = logging.getLogger(__name__)

# Вспомогательная функция для извлечения JSON из произвольного текста
def _extract_json_text(response: str) -> str | None:
    # Попытка извлечь из fenced-блока ```json ... ```
    if "```json" in response:
        start = response.find("```json") + len("```json")
        end = response.find("```", start)
        if end != -1:
            return response[start:end].strip()
    
    # Попытка извлечь из обычного fenced-блока ``` ... ```
    if "```" in response:
        start = response.find("```") + len("```")
        end = response.find("```", start)
        if end != -1:
            candidate = response[start:end].strip()
            # Обрезаем всё до первого JSON-литерала
            brace_index = candidate.find('{')
            bracket_index = candidate.find('[')
            indices = [i for i in [brace_index, bracket_index] if i != -1]
            if indices:
                candidate = candidate[min(indices):]
            return candidate
    
    # Сканирование с балансировкой скобок для объекта {...}
    start = response.find('{')
    if start != -1:
        depth = 0
        for i, ch in enumerate(response[start:], start=start):
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return response[start:i+1]
    
    # Сканирование для массива [...]
    start = response.find('[')
    if start != -1:
        depth = 0
        for i, ch in enumerate(response[start:], start=start):
            if ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    return response[start:i+1]
    
    return None

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
            # Робастное извлечение JSON из ответа
            json_text = _extract_json_text(response)
            if not json_text:
                raise ValueError("Не удалось извлечь JSON из ответа")
            return json.loads(json_text)
        
        return response

    except Exception as e:
        logger.error(f"Ошибка при вызове LLM: {e}")
        # В случае ошибки возвращаем "безопасное" значение
        return {} if is_json else "Извините, произошла ошибка при обработке вашего запроса."

if __name__ == '__main__':
    # Пример использования
    async def main():
        test_prompt = "Привет! Как дела?"
        result = await get_llm_response(test_prompt)
        print(f"Обычный ответ: {result}")

        json_prompt = "Верни JSON с полями 'name' и 'age'. Например: {'name': 'John', 'age': 30}"
        json_result = await get_llm_response(json_prompt, is_json=True)
        print(f"JSON ответ: {json_result}")

    asyncio.run(main())
