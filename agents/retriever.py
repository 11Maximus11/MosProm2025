from utils.vector_store import VectorStore

class RetrieverAgent:
    """Агент для поиска релевантных документов."""
    
    def __init__(self):
        self.vector_store = VectorStore()
    
    async def retrieve_documents_async(self, query: str) -> list:
        """
        Асинхронно ищет релевантные документы по запросу.
        """
        # Получаем релевантные документы из векторного хранилища
        documents = await self.vector_store.search_async(query, limit=5)
        
        # Форматируем результаты для дальнейшего использования
        context = []
        for doc in documents:
            context.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": doc.score if hasattr(doc, 'score') else 0.0
            })
            
        return context
