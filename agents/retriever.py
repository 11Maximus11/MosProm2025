import os
import glob
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RetrieverAgent:
    def __init__(self, kb_path: str = "data/kb", model_name: str = 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2'):
        self.kb_path = kb_path
        self.documents = []
        self.index = None
        print("Загрузка embedding-модели... Это может занять некоторое время.")
        self.model = SentenceTransformer(model_name)
        self._load_and_index()

    def _load_and_index(self):
        print(f"Чтение документов из {self.kb_path}...")
        for file_path in glob.glob(os.path.join(self.kb_path, "*.txt")):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.documents.append(f.read())
        
        if not self.documents:
            print("ВНИМАНИЕ: База знаний пуста. Положите .txt файлы в папку data/kb.")
            return

        print(f"Найдено документов: {len(self.documents)}. Создание векторов...")
        embeddings = self.model.encode(self.documents, show_progress_bar=True)
        
        embedding_dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(embeddings.astype('float32'))
        print("Индексация завершена.")

    def retrieve_documents(self, query: str, top_k: int = 2) -> str:
        if not self.index or not self.documents:
            return "База знаний пуста или не проиндексирована."

        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        context = "\n---\n".join([self.documents[i] for i in indices[0]])
        return context