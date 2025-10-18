import chromadb
from sentence_transformers import SentenceTransformer
import os
import logging
import asyncio
from typing import List, Dict, Any

# --- Настройка ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем модель один раз при инициализации
# paraphrase-multilingual-mpnet-base-v2 - хорошая многоязычная модель
try:
    logger.info("Загрузка embedding-модели... Это может занять некоторое время.")
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
    logger.info("Embedding-модель успешно загружена.")
except Exception as e:
    logger.error(f"Не удалось загрузить embedding-модель: {e}")
    model = None

# Путь к базе данных и коллекции
DB_PATH = "data/chroma_db"
COLLECTION_NAME = "knowledge_base"

# Инициализация клиента ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Класс для работы с векторным хранилищем
class VectorStore:
    """Класс для работы с векторным хранилищем на базе ChromaDB."""
    
    def __init__(self):
        self.client = client
        self.collection = collection
        self.model = model
    
    async def search_async(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Асинхронно выполняет семантический поиск в базе знаний.
        
        Args:
            query: Текст запроса
            limit: Количество возвращаемых результатов
            
        Returns:
            Список документов с метаданными
        """
        # Используем функцию поиска из модуля, но оборачиваем в асинхронный контекст
        result = await asyncio.to_thread(search_in_kb, query, limit)
        
        # Преобразуем результат в формат, ожидаемый RetrieverAgent
        documents = []
        if result and not result.startswith("Ошибка"):
            # Разделяем результат на отдельные документы
            docs = result.split("\n---\n")
            for i, doc_content in enumerate(docs):
                documents.append(type('Document', (), {
                    'page_content': doc_content,
                    'metadata': {'source': f'doc_{i+1}'},
                    'score': 1.0 - (0.1 * i)  # Имитация score
                }))
        
        return documents

def initialize_knowledge_base(kb_path="data/kb"):
    """
    Индексирует текстовые файлы из папки в векторную базу данных.
    """
    if not model:
        logger.error("Embedding-модель не загружена. Инициализация базы знаний невозможна.")
        return

    logger.info(f"Чтение документов из {kb_path}...")
    doc_files = [f for f in os.listdir(kb_path) if f.endswith(".txt")]

    if not doc_files:
        logger.warning("ВНИМАНИЕ: База знаний пуста. Положите .txt файлы в папку data/kb.")
        return

    documents = []
    metadatas = []
    ids = []
    doc_id = 1

    for doc_file in doc_files:
        with open(os.path.join(kb_path, doc_file), 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            metadatas.append({"source": doc_file})
            ids.append(str(doc_id))
            doc_id += 1
    
    if documents:
        logger.info(f"Индексация {len(documents)} документов...")
        embeddings = model.encode(documents, show_progress_bar=True)
        collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info("Индексация завершена.")

def search_in_kb(query_text: str, n_results: int = 3) -> str:
    """
    Выполняет семантический поиск в базе знаний.

    :param query_text: Текст запроса.
    :param n_results: Количество возвращаемых результатов.
    :return: Строка, содержащая объединенный контекст из найденных документов.
    """
    if not model:
        logger.error("Embedding-модель не загружена. Поиск невозможен.")
        return "Ошибка: embedding-модель не инициализирована."

    try:
        query_embedding = model.encode([query_text])
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        
        context = "\n---\n".join(results['documents'][0])
        return context
    except Exception as e:
        logger.error(f"Ошибка при поиске в ChromaDB: {e}")
        return "Ошибка при поиске в базе знаний."

# Выполняем инициализацию при запуске модуля
if __name__ == '__main__':
    # Создаем папки, если их нет
    os.makedirs("data/kb", exist_ok=True)
    # Пример: создадим тестовый файл в базе знаний
    with open("data/kb/test_doc.txt", "w", encoding="utf-8") as f:
        f.write("Сброс пароля в системе 'Альфа'. Для сброса пароля необходимо перейти на страницу входа и нажать кнопку 'Забыли пароль?'.")
    
    initialize_knowledge_base()
    
    """test_query = "Как мне поменять пароль в альфе?"
    search_result = search_in_kb(test_query)
    
    print(f"Запрос: {test_query}")
    print("\nНайденный контекст:")
    print(search_result)"""
else:
    # Инициализация при импорте в основное приложение
    os.makedirs("data/kb", exist_ok=True)
    initialize_knowledge_base()
