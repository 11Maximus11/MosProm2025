import asyncio
from agents.retriever import RetrieverAgent
from agents.generator import GeneratorAgent
from agents.analyzer import AnalyzerAgent
from agents.classifier import ClassifierAgent
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent
from agents.personalizer import PersonalizerAgent
import logging

class OrchestratorAgent:
    """
    Главный агент, который управляет всем процессом обработки запроса.
    Он вызывает других агентов асинхронно, где это возможно, чтобы ускорить ответ.
    """
    def __init__(self):
        # Инициализируем всех дочерних агентов один раз
        try:
            self.retriever = RetrieverAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.generator = GeneratorAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.analyzer = AnalyzerAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.classifier = ClassifierAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.planner = PlannerAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.executor = ExecutorAgent()
        except Exception: logging.ERROR(Exception)
        try:
            self.verifier = VerifierAgent() 
        except Exception: logging.ERROR(Exception)
        try:
            self.personalizer = PersonalizerAgent()
        except Exception: logging.ERROR(Exception)

    async def process_query(self, user_query: str) -> str:
        """
        Обрабатывает запрос пользователя, координируя работу других агентов.
        """
        # Шаг 1: Параллельный запуск анализа и классификации
        # Эти агенты не зависят друг от друга и могут работать одновременно
        analysis_task = asyncio.create_task(self.analyzer.analyze_async(user_query))
        classification_task = asyncio.create_task(self.classifier.classify_async(user_query))
        
        analysis, classification = await asyncio.gather(analysis_task, classification_task)

        # Шаг 2: Поиск релевантной информации (зависит от анализа)
        context = await self.retriever.retrieve_documents_async(analysis['full_text'])

        # Шаг 3: Планирование и выполнение (зависят от предыдущих шагов)
        plan = await self.planner.plan_actions_async(analysis['full_text'], context)
        execution_report = await self.executor.execute_plan_async(plan)

        # Шаг 4: Генерация ответа (зависит от всех предыдущих данных)
        draft_answer = await self.generator.generate_final_answer_async(user_query, context, execution_report)

        # Шаг 5: Проверка и персонализация
        # Эти шаги также можно было бы сделать асинхронными, если бы они делали I/O вызовы
        verification = self.verifier.verify(user_query, draft_answer)
        if verification['decision'] != 'approve':
            return "Ответ системы не прошел внутреннюю проверку. Обращение передано оператору."

        final_answer = self.personalizer.personalize(draft_answer, {})
        return final_answer
