import sys
from main import process_ticket_logic

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print("--- Отправка запроса ---")
        print(f"Вопрос: {query}")
        print("\n--- Ответ системы ---")
        response = process_ticket_logic(query)
        print(response)
    else:
        print("Использование: python cli.py 'ваш вопрос'")